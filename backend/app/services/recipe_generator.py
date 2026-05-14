"""Rule-based receptgenerator.

Combineert sjablonen uit `recipe_templates.py` met actuele aanbiedingen.
Het LLM is optioneel en kan via `ai_service.py` worden ingezet, maar
deze module garandeert een werkende output zonder LLM.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Iterable

from app.data.pantry import is_pantry
from app.data.recipe_templates import RECIPE_TEMPLATES, RecipeTemplate
from app.models.offer import Offer
from app.schemas.recipe import (
    HealthInfo,
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
from app.services.offer_matcher import best_offer_for, normalize

logger = logging.getLogger(__name__)


VEG_FRUIT_CATEGORIES = {"groente", "fruit"}


def _cost_for_offer(offer: Offer, grams_needed: float) -> float:
    """Schat hoeveel een ingredient kost op basis van de aanbieding."""
    amount = offer.amount or 0
    if amount <= 0 or offer.unit in (None, "stuk"):
        return round(offer.sale_price, 2)
    unit = (offer.unit or "").lower()
    if unit in {"g", "ml"}:
        per_unit = offer.sale_price / amount
        return round(per_unit * grams_needed, 2)
    if unit in {"kg", "l"}:
        per_g = offer.sale_price / (amount * 1000)
        return round(per_g * grams_needed, 2)
    return round(offer.sale_price, 2)


def _template_diet_match(template: RecipeTemplate, diets: list[str]) -> bool:
    if not diets:
        return True
    tags = set(template.get("diet_tags", []))
    return all(d in tags for d in diets)


def _build_recipe_from_template(
    template: RecipeTemplate,
    request: RecipeGenerateRequest,
    offers: Iterable[Offer],
) -> RecipeOut | None:
    if not _template_diet_match(template, request.diets):
        return None
    if request.max_prep_minutes and template["prep_time_minutes"] > request.max_prep_minutes:
        return None

    servings = request.servings
    ingredients_out: list[RecipeIngredientOut] = []
    nutrition_items: list[tuple[str, str | None, float]] = []
    missing_pantry: list[str] = []
    total_cost = 0.0
    used_offer_ids: set[int] = set()
    veg_fruit_grams = 0.0
    weighted_categories: list[tuple[str | None, float]] = []

    matched_real_offers = 0

    for ing in template["ingredients"]:
        name = ing["name"]
        if any(normalize(ex) in normalize(name) for ex in request.exclude_ingredients):
            # ingredient uitgesloten -> recept ongeschikt
            return None

        keywords = ing.get("keywords", [name])
        grams_per_serving = float(ing.get("grams_per_serving", 0))
        grams_total = grams_per_serving * servings

        offer = best_offer_for(
            keywords,
            offers,
            exclude_names=request.exclude_ingredients,
            favorite_supermarkets=request.favorite_supermarkets,
        )

        is_pantry_item = ing.get("is_pantry", False) or is_pantry(name)
        cost: float | None = None
        offer_id: int | None = None
        note: str | None = None
        category = None

        if offer:
            offer_id = offer.id
            used_offer_ids.add(offer.id)
            cost = _cost_for_offer(offer, grams_total)
            category = offer.category
            matched_real_offers += 1
            note = f"Uit aanbieding bij {offer.supermarket.name}" if offer.supermarket else None
        elif is_pantry_item:
            note = "Standaardproduct (verwacht voorhanden)"
        else:
            missing_pantry.append(name)
            note = "Geen aanbieding gevonden – los aanschaffen"

        ingredients_out.append(
            RecipeIngredientOut(
                name=name,
                quantity=round(grams_total, 1) if grams_total else None,
                unit=ing.get("unit"),
                is_pantry=is_pantry_item,
                estimated_cost=cost,
                offer_id=offer_id,
                note=note,
            )
        )
        if cost:
            total_cost += cost

        nutrition_items.append((name, category, grams_total))
        weighted_categories.append((category, grams_total))
        if category and category.lower() in VEG_FRUIT_CATEGORIES:
            veg_fruit_grams += grams_per_serving

    # Recept moet minstens een echt aanbiedings-ingredient bevatten,
    # anders matcht het niet zinvol bij de huidige aanbiedingen.
    if matched_real_offers == 0:
        return None

    totals_per_serving, confidence = aggregate_recipe_nutrition(
        nutrition_items, servings, try_remote=False
    )

    # Filters op kcal / eiwit toepassen
    if request.max_kcal_per_serving and totals_per_serving.kcal > request.max_kcal_per_serving:
        return None
    if request.min_protein_g and totals_per_serving.protein < request.min_protein_g:
        return None
    cost_per_serving = round(total_cost / servings, 2) if servings else None
    if request.max_budget_per_serving and cost_per_serving and cost_per_serving > request.max_budget_per_serving:
        return None

    upc = estimate_ultra_processed_ratio(weighted_categories)
    health = compute_health_score(
        HealthScoreInput(
            kcal_per_serving=totals_per_serving.kcal,
            protein_g=totals_per_serving.protein,
            fiber_g=totals_per_serving.fiber,
            saturated_fat_g=totals_per_serving.satfat,
            salt_g=totals_per_serving.salt,
            sugar_g=totals_per_serving.sugar,
            veg_fruit_grams_per_serving=veg_fruit_grams,
            ultra_processed_ratio=upc,
        )
    )

    diet_tags = list(template.get("diet_tags", []))
    if cost_per_serving is not None and cost_per_serving < 3.0:
        health.labels.append("budgetvriendelijk")
    for tag in diet_tags:
        if tag in {"vegetarisch", "vegan"} and tag not in health.labels:
            health.labels.append(tag)

    return RecipeOut(
        title=template["title"],
        description=template["description"],
        instructions=list(template["instructions"]),
        servings=servings,
        prep_time_minutes=template["prep_time_minutes"],
        total_cost=round(total_cost, 2),
        cost_per_serving=cost_per_serving,
        diet_tags=diet_tags,
        missing_pantry_items=missing_pantry,
        ingredients=ingredients_out,
        nutrition=NutritionInfo(
            kcal=totals_per_serving.kcal,
            protein_g=totals_per_serving.protein,
            carbs_g=totals_per_serving.carbs,
            sugar_g=totals_per_serving.sugar,
            fat_g=totals_per_serving.fat,
            saturated_fat_g=totals_per_serving.satfat,
            fiber_g=totals_per_serving.fiber,
            salt_g=totals_per_serving.salt,
            source=confidence,
        ),
        health=HealthInfo(
            score=health.score,
            explanation=health.explanation,
            labels=health.labels,
        ),
        generated_by="rule",
        generated_at=datetime.utcnow(),
    )


def generate_recipes_rule_based(
    request: RecipeGenerateRequest,
    offers: list[Offer],
) -> list[RecipeOut]:
    """Genereer recepten met de rule-based engine.

    Sorteert resultaten op een combinatie van gezondheidsscore en
    kosten per portie zodat 'meest passend' bovenaan staat.
    """
    results: list[RecipeOut] = []
    for template in RECIPE_TEMPLATES:
        recipe = _build_recipe_from_template(template, request, offers)
        if recipe:
            results.append(recipe)

    def sort_key(r: RecipeOut) -> float:
        cost = r.cost_per_serving or 5.0
        return -(r.health.score - cost * 3)

    results.sort(key=sort_key)
    return results[: request.count]
