"""Optionele LLM-receptgenerator.

De LLM krijgt uitsluitend de geselecteerde aanbiedingen en moet
JSON teruggeven volgens een strikt Pydantic-schema. Hallucinaties
worden opgevangen door validatie en fallback naar de rule-based engine.
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
    RecipeSupermarketUse,
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
    "Je bent een Nederlandse receptgenerator voor een supermarkt-aanbiedingen-app. "
    "Je krijgt een lijst met huidige aanbiedingen en gebruikersvoorkeuren.\n\n"
    "STRIKTE REGELS:\n"
    "1. Gebruik UITSLUITEND ingredienten die letterlijk in de aanbiedingenlijst voorkomen, "
    "of die typische pantry-items zijn (zout, peper, olijfolie, kruiden, water).\n"
    "2. Verzin NOOIT prijzen. Het systeem rekent zelf de kosten uit.\n"
    "3. Geef per ingredient `offer_product_name` dat exact gelijk is aan een productnaam uit de lijst.\n"
    "4. Markeer ingredienten die niet in de aanbiedingen zitten en geen pantry zijn, als `missing_pantry_items`.\n"
    "5. Recepten moeten DIVERS zijn: gemengde maaltijdtypes (ontbijt/lunch/diner/snack/meal-prep), gemengde hoofdingredienten, gemengde keukens.\n"
    "6. Elk recept moet minimaal 6 concrete, gedetailleerde kookstappen hebben (snijden, verhitten, timing, temperatuur).\n"
    "7. Antwoord ALLEEN in geldig JSON dat voldoet aan het meegegeven schema. Geen extra tekst.\n"
)


def _build_user_prompt(offers: Sequence[Offer], request: RecipeGenerateRequest) -> str:
    offer_lines = []
    for o in offers[:80]:
        sm = o.supermarket.name if o.supermarket else "?"
        offer_lines.append(
            f"- {o.product_name} ({sm}) | {o.category or 'overig'} | "
            f"{o.amount or '?'} {o.unit or ''} | €{o.sale_price:.2f}"
        )
    diets = ", ".join(request.diets) or "geen"
    meal_types = ", ".join(request.meal_types) or "alle"
    excludes = ", ".join(request.exclude_ingredients) or "geen"
    favs = ", ".join(request.selected_supermarkets) or "alle"
    multi = "ja" if request.allow_multi_supermarket else "nee (recepten uit één supermarkt)"
    constraints = []
    if request.max_prep_minutes:
        constraints.append(f"maximaal {request.max_prep_minutes} minuten totaal")
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
        '      "meal_type": "ontbijt|lunch|diner|snack|meal-prep",\n'
        '      "difficulty": "makkelijk|gemiddeld|uitdagend",\n'
        '      "prep_time_minutes": 10,\n'
        '      "cook_time_minutes": 20,\n'
        '      "servings": 2,\n'
        '      "instructions": ["stap 1", "stap 2", "stap 3", "stap 4", "stap 5", "stap 6"],\n'
        '      "ingredients": [\n'
        '        {"name": "Kipfilet", "quantity": 300, "unit": "g", "is_pantry": false, "offer_product_name": "Kipfilet naturel"}\n'
        "      ],\n"
        '      "missing_pantry_items": [],\n'
        '      "diet_tags": ["halal"],\n'
        '      "allergens": ["gluten"],\n'
        '      "serving_tips": ["..."],\n'
        '      "storage_tips": ["..."],\n'
        '      "variations": ["..."]\n'
        "    }\n"
        "  ]\n"
        "}"
    )

    return (
        f"Aantal personen: {request.servings}\n"
        f"Aantal recepten: {request.count}\n"
        f"Dieetwensen: {diets}\n"
        f"Maaltijdtypes: {meal_types}\n"
        f"Uitsluiten: {excludes}\n"
        f"Geselecteerde supermarkten: {favs}\n"
        f"Combineren toegestaan: {multi}\n"
        f"Overige eisen: {constraints_txt}\n\n"
        f"Aanbiedingen:\n" + "\n".join(offer_lines) + "\n\n"
        f"Antwoord in dit JSON-schema (recepten DIVERS, elk ≥6 kookstappen):\n{schema_hint}\n"
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
    supermarket_counts: dict[str, dict] = {}
    shopping_items: list[str] = []

    for ing in llm_recipe.ingredients:
        offer = _match_offer_by_name(ing.offer_product_name or ing.name, offers)
        grams = (ing.quantity or 0) * (1 if (ing.unit or "g").lower() in {"g", "ml"} else 100)
        category = offer.category if offer else None

        cost: float | None = None
        note: str | None = None
        offer_id: int | None = None
        supermarket_slug: str | None = None
        supermarket_name: str | None = None

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
            if offer.supermarket:
                supermarket_slug = offer.supermarket.slug
                supermarket_name = offer.supermarket.name
                note = f"Uit aanbieding bij {offer.supermarket.name}"
                bucket = supermarket_counts.setdefault(
                    supermarket_slug, {"name": supermarket_name, "count": 0}
                )
                bucket["count"] += 1
            shopping_items.append(f"{offer.product_name} (€{offer.sale_price:.2f}) bij {supermarket_name or '?'}")
            if cost:
                total_cost += cost
        else:
            if not ing.is_pantry and ing.name not in missing_pantry:
                missing_pantry.append(ing.name)
            note = "Niet in aanbiedingen — los aanschaffen" if not ing.is_pantry else "Standaardproduct"

        ingredients_out.append(
            RecipeIngredientOut(
                name=ing.name,
                quantity=ing.quantity,
                unit=ing.unit,
                is_pantry=ing.is_pantry,
                estimated_cost=cost,
                offer_id=offer_id,
                note=note,
                supermarket_slug=supermarket_slug,
                supermarket_name=supermarket_name,
                offer_product_name=ing.offer_product_name,
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

    prep_t = llm_recipe.prep_time_minutes or 0
    cook_t = llm_recipe.cook_time_minutes or 0

    image_key = (llm_recipe.meal_type or "diner").replace("-", "")

    return RecipeOut(
        title=llm_recipe.title,
        description=llm_recipe.description,
        meal_type=(llm_recipe.meal_type or "diner"),  # type: ignore[arg-type]
        difficulty=(llm_recipe.difficulty or "makkelijk"),  # type: ignore[arg-type]
        instructions=llm_recipe.instructions,
        servings=llm_recipe.servings or request.servings,
        prep_time_minutes=prep_t,
        cook_time_minutes=cook_t,
        total_time_minutes=prep_t + cook_t,
        total_cost=round(total_cost, 2),
        cost_per_serving=cost_per_serving,
        diet_tags=list(llm_recipe.diet_tags),
        missing_pantry_items=missing_pantry,
        allergens=list(llm_recipe.allergens),
        serving_tips=list(llm_recipe.serving_tips),
        storage_tips=list(llm_recipe.storage_tips),
        variations=list(llm_recipe.variations),
        ingredients=ingredients_out,
        supermarkets_used=[
            RecipeSupermarketUse(slug=slug, name=info["name"], offer_count=info["count"])
            for slug, info in supermarket_counts.items()
        ],
        why_smart=None,
        shopping_items=shopping_items,
        image_url=f"/recipe-images/{image_key}.svg",
        image_key=image_key,
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
    if not llm_available():
        raise RuntimeError("LLM_API_KEY niet geconfigureerd")
    try:
        from openai import OpenAI
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"OpenAI SDK niet beschikbaar: {exc}") from exc

    # Filter aanbiedingen voor de prompt naar geselecteerde supermarkten.
    allowed = {s.lower() for s in request.selected_supermarkets if s}
    if allowed:
        relevant = [o for o in offers if o.supermarket and o.supermarket.slug in allowed]
    else:
        relevant = list(offers)

    client = OpenAI(api_key=settings.LLM_API_KEY)
    user_prompt = _build_user_prompt(relevant, request)
    try:
        completion = client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.6,
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

    recipes = [_llm_response_to_recipe(r, relevant, request) for r in parsed.recipes]
    return recipes[: request.count]
