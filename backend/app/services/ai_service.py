"""Optionele LLM-receptgenerator.

De LLM ontvangt uitsluitend de aanbiedingen die we hebben opgehaald en
moet daarop antwoorden in een strikt JSON-schema. Pydantic valideert de
output zodat hallucinaties opgevangen worden.

Wanneer geen LLM_API_KEY beschikbaar is, of wanneer de LLM faalt, valt
de aanroeper terug op de rule-based generator.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Sequence

from pydantic import ValidationError

from app.config import settings
from app.models.offer import Offer
from app.schemas.recipe import (
    HealthInfo,
    LLMRecipeList,
    NutritionInfo,
    RecipeGenerateRequest,
    RecipeIngredientOut,
    RecipeOut,
)
from app.services.health_score import (
    HealthScoreInput,
    compute_health_score,
    estimate_ultra_processed_ratio,
)
from app.services.nutrition import aggregate_recipe_nutrition
from app.services.offer_matcher import normalize

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = (
    "Je bent een Nederlandse receptgenerator. Je krijgt een lijst met huidige "
    "supermarktaanbiedingen en gebruikersvoorkeuren. Bedenk recepten die "
    "praktisch en gezond zijn.\n\n"
    "Strikte regels:\n"
    "1. Gebruik UITSLUITEND ingredienten waarvan de naam letterlijk in de lijst "
    "met aanbiedingen voorkomt, OF die typische pantry-items zijn (zout, peper, "
    "olijfolie, kruiden, water).\n"
    "2. Verzin nooit prijzen. Reken zelf geen kosten uit; dat doet het systeem.\n"
    "3. Geef per ingredient aan of het uit een aanbieding komt door 'offer_product_name' "
    "exact gelijk te maken aan de productnaam uit de lijst.\n"
    "4. Markeer ingredienten die niet in de aanbiedingen zitten en geen pantry zijn, "
    "als 'missing_pantry_items'.\n"
    "5. Antwoord ALLEEN in geldig JSON dat voldoet aan het meegegeven schema. Geen extra tekst.\n"
)


def _build_user_prompt(offers: Sequence[Offer], request: RecipeGenerateRequest) -> str:
    offer_lines = []
    for o in offers[:60]:  # cap om prompt klein te houden
        sm = o.supermarket.name if o.supermarket else "?"
        offer_lines.append(
            f"- {o.product_name} ({sm}) | {o.category or 'overig'} | "
            f"{o.amount or '?'} {o.unit or ''} | €{o.sale_price:.2f}"
        )
    diets = ", ".join(request.diets) or "geen"
    excludes = ", ".join(request.exclude_ingredients) or "geen"
    favs = ", ".join(request.favorite_supermarkets) or "alle"
    constraints = []
    if request.max_prep_minutes:
        constraints.append(f"maximaal {request.max_prep_minutes} minuten bereiding")
    if request.min_protein_g:
        constraints.append(f"minstens {request.min_protein_g} g eiwit per portie")
    if request.max_kcal_per_serving:
        constraints.append(f"maximaal {request.max_kcal_per_serving} kcal per portie")
    if request.max_budget_per_serving:
        constraints.append(f"maximaal €{request.max_budget_per_serving:.2f} per portie")
    constraints_txt = "; ".join(constraints) or "geen"

    schema_hint = (
        "{\n"
        '  "recipes": [\n'
        "    {\n"
        '      "title": "string",\n'
        '      "description": "string",\n'
        '      "instructions": ["stap 1", "stap 2"],\n'
        '      "prep_time_minutes": 25,\n'
        '      "servings": 2,\n'
        '      "ingredients": [\n'
        '        {"name": "Kipfilet", "quantity": 300, "unit": "g", "is_pantry": false, "offer_product_name": "Kipfilet naturel"}\n'
        "      ],\n"
        '      "missing_pantry_items": ["citroen"],\n'
        '      "diet_tags": ["halal"]\n'
        "    }\n"
        "  ]\n"
        "}"
    )

    return (
        f"Aantal personen: {request.servings}\n"
        f"Aantal recepten: {request.count}\n"
        f"Dieetwensen: {diets}\n"
        f"Uitsluiten: {excludes}\n"
        f"Favoriete supermarkten: {favs}\n"
        f"Overige eisen: {constraints_txt}\n\n"
        f"Aanbiedingen:\n" + "\n".join(offer_lines) + "\n\n"
        f"Antwoord in dit JSON-schema:\n{schema_hint}\n"
    )


def _match_offer_by_name(name: str, offers: Sequence[Offer]) -> Offer | None:
    target = normalize(name)
    if not target:
        return None
    for o in offers:
        if normalize(o.product_name) == target:
            return o
    for o in offers:
        if target in normalize(o.product_name) or normalize(o.product_name) in target:
            return o
    return None


def _llm_response_to_recipe(
    llm_recipe,
    offers: Sequence[Offer],
    request: RecipeGenerateRequest,
) -> RecipeOut:
    ingredients_out: list[RecipeIngredientOut] = []
    nutrition_items: list[tuple[str, str | None, float]] = []
    weighted_categories: list[tuple[str | None, float]] = []
    missing_pantry = list(llm_recipe.missing_pantry_items)
    total_cost = 0.0
    veg_fruit_grams = 0.0

    for ing in llm_recipe.ingredients:
        offer = _match_offer_by_name(ing.offer_product_name or ing.name, offers)
        # belangrijk: als LLM een offer_product_name verzint die niet bestaat,
        # accepteren we het niet als 'echt' ingredient maar markeren als ontbrekend.
        grams = (ing.quantity or 0) * (1 if (ing.unit or "g").lower() in {"g", "ml"} else 100)
        category = offer.category if offer else None

        cost: float | None = None
        note: str | None = None
        offer_id: int | None = None
        if offer:
            offer_id = offer.id
            amount = offer.amount or 0
            unit = (offer.unit or "").lower()
            if amount and unit in {"g", "ml"}:
                cost = round((offer.sale_price / amount) * grams, 2)
            elif amount and unit in {"kg", "l"}:
                cost = round((offer.sale_price / (amount * 1000)) * grams, 2)
            else:
                cost = round(offer.sale_price, 2)
            note = f"Uit aanbieding bij {offer.supermarket.name}" if offer.supermarket else None
            if cost:
                total_cost += cost
        else:
            if not ing.is_pantry and ing.name not in missing_pantry:
                missing_pantry.append(ing.name)
            note = "Niet in aanbiedingen – los aanschaffen" if not ing.is_pantry else "Standaardproduct"

        ingredients_out.append(
            RecipeIngredientOut(
                name=ing.name,
                quantity=ing.quantity,
                unit=ing.unit,
                is_pantry=ing.is_pantry,
                estimated_cost=cost,
                offer_id=offer_id,
                note=note,
            )
        )
        nutrition_items.append((ing.name, category, grams))
        weighted_categories.append((category, grams))
        if category and category.lower() in {"groente", "fruit"}:
            veg_fruit_grams += grams / max(1, request.servings)

    totals, confidence = aggregate_recipe_nutrition(
        nutrition_items, request.servings, try_remote=False
    )

    health = compute_health_score(
        HealthScoreInput(
            kcal_per_serving=totals.kcal,
            protein_g=totals.protein,
            fiber_g=totals.fiber,
            saturated_fat_g=totals.satfat,
            salt_g=totals.salt,
            sugar_g=totals.sugar,
            veg_fruit_grams_per_serving=veg_fruit_grams,
            ultra_processed_ratio=estimate_ultra_processed_ratio(weighted_categories),
        )
    )

    cost_per_serving = round(total_cost / request.servings, 2) if request.servings else None
    if cost_per_serving is not None and cost_per_serving < 3.0:
        health.labels.append("budgetvriendelijk")

    return RecipeOut(
        title=llm_recipe.title,
        description=llm_recipe.description,
        instructions=llm_recipe.instructions,
        servings=llm_recipe.servings or request.servings,
        prep_time_minutes=llm_recipe.prep_time_minutes,
        total_cost=round(total_cost, 2),
        cost_per_serving=cost_per_serving,
        diet_tags=list(llm_recipe.diet_tags),
        missing_pantry_items=missing_pantry,
        ingredients=ingredients_out,
        nutrition=NutritionInfo(
            kcal=totals.kcal,
            protein_g=totals.protein,
            carbs_g=totals.carbs,
            sugar_g=totals.sugar,
            fat_g=totals.fat,
            saturated_fat_g=totals.satfat,
            fiber_g=totals.fiber,
            salt_g=totals.salt,
            source=confidence,
        ),
        health=HealthInfo(score=health.score, explanation=health.explanation, labels=health.labels),
        generated_by="llm",
        generated_at=datetime.utcnow(),
    )


def llm_available() -> bool:
    return bool(settings.LLM_API_KEY)


def generate_recipes_llm(
    request: RecipeGenerateRequest,
    offers: Sequence[Offer],
) -> list[RecipeOut]:
    """Probeer recepten te genereren via een LLM. Werpt bij falen."""
    if not llm_available():
        raise RuntimeError("LLM_API_KEY niet geconfigureerd")
    try:
        from openai import OpenAI  # lazy import zodat dependency optioneel is
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"OpenAI SDK niet beschikbaar: {exc}") from exc

    client = OpenAI(api_key=settings.LLM_API_KEY)
    user_prompt = _build_user_prompt(offers, request)
    try:
        completion = client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.4,
        )
        raw = completion.choices[0].message.content or "{}"
    except Exception as exc:  # noqa: BLE001
        logger.warning("LLM-aanroep faalde: %s", exc)
        raise

    try:
        data = json.loads(raw)
        parsed = LLMRecipeList.model_validate(data)
    except (json.JSONDecodeError, ValidationError) as exc:
        logger.warning("LLM gaf ongeldige JSON: %s", exc)
        raise

    recipes = [_llm_response_to_recipe(r, offers, request) for r in parsed.recipes]
    return recipes[: request.count]
