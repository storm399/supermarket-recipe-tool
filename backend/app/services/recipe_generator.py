"""Rule-based receptgenerator met strikte supermarktfiltering en variatie.

Belangrijkste features:
- Respecteert `selected_supermarkets`: gebruikt uitsluitend aanbiedingen
  van die supermarkten als de lijst niet leeg is.
- Per recept toont welke supermarkt(en) gebruikt zijn.
- Heeft een variatie-algoritme zodat dezelfde aanbieding niet in elk recept
  als hoofdingrediënt terugkomt.
- Mag desgewenst combinaties uit meerdere supermarkten maken; standaard niet.
- Genereert minimaal `count` (default 12) gevarieerde recepten als er
  voldoende aanbiedingen zijn.
"""
from __future__ import annotations

import logging
from collections import defaultdict
from datetime import datetime
from typing import Iterable

from app.data.pantry import is_pantry
from app.data.recipe_images import photo_url_for
from app.data.recipe_templates import RECIPE_TEMPLATES, RecipeTemplate
from app.models.offer import Offer
from app.schemas.recipe import (
    HealthInfo,
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
from app.services.offer_matcher import match_offers, normalize

logger = logging.getLogger(__name__)


VEG_FRUIT_CATEGORIES = {"groente", "fruit"}


def _cost_for_offer(offer: Offer, grams_needed: float) -> float:
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


def _template_meal_type_match(template: RecipeTemplate, meal_types: list[str]) -> bool:
    if not meal_types:
        return True
    return template.get("meal_type", "diner") in meal_types


def _allowed_offers_for_supermarkets(
    offers: Iterable[Offer], allowed_slugs: set[str]
) -> list[Offer]:
    if not allowed_slugs:
        return list(offers)
    result = []
    for o in offers:
        sm = getattr(o, "supermarket", None)
        if sm is not None and getattr(sm, "slug", None) in allowed_slugs:
            result.append(o)
    return result


def _select_offer_for_ingredient(
    keywords: list[str],
    offers: list[Offer],
    *,
    exclude_names: list[str],
    favorite_supermarkets: list[str],
    used_offer_counts: dict[int, int],
    forced_supermarket: str | None = None,
) -> Offer | None:
    matches = match_offers(
        keywords,
        offers,
        exclude_names=exclude_names,
        favorite_supermarkets=favorite_supermarkets,
    )
    if not matches:
        return None
    # Forceer supermarkt indien gevraagd (strikte single-supermarket mode).
    if forced_supermarket:
        matches = [m for m in matches if m.offer.supermarket and m.offer.supermarket.slug == forced_supermarket]
        if not matches:
            return None
    # Re-rank: minder gebruikte aanbiedingen krijgen voorrang voor variatie.
    matches.sort(
        key=lambda m: (used_offer_counts.get(m.offer.id, 0), -m.score)
    )
    return matches[0].offer


def _build_recipe_from_template(
    template: RecipeTemplate,
    request: RecipeGenerateRequest,
    allowed_offers: list[Offer],
    used_offer_counts: dict[int, int],
    forced_supermarket: str | None = None,
) -> RecipeOut | None:
    if not _template_diet_match(template, request.diets):
        return None
    if not _template_meal_type_match(template, request.meal_types):
        return None
    if request.max_prep_minutes:
        total_time = template.get("prep_time_minutes", 0) + template.get("cook_time_minutes", 0)
        if total_time > request.max_prep_minutes:
            return None

    servings = request.servings
    ingredients_out: list[RecipeIngredientOut] = []
    nutrition_items: list[tuple[str, str | None, float]] = []
    missing_pantry: list[str] = []
    total_cost = 0.0
    used_offer_ids: set[int] = set()
    veg_fruit_grams = 0.0
    weighted_categories: list[tuple[str | None, float]] = []
    supermarket_counts: dict[str, dict] = {}
    shopping_items: list[str] = []
    pantry_items_used: list[str] = []

    matched_real_offers = 0

    for ing in template["ingredients"]:
        name = ing["name"]
        if any(normalize(ex) in normalize(name) for ex in request.exclude_ingredients):
            return None

        keywords = ing.get("keywords", [name])
        grams_per_serving = float(ing.get("grams_per_serving", 0))
        grams_total = grams_per_serving * servings

        offer = _select_offer_for_ingredient(
            keywords,
            allowed_offers,
            exclude_names=list(request.exclude_ingredients),
            favorite_supermarkets=list(request.selected_supermarkets),
            used_offer_counts=used_offer_counts,
            forced_supermarket=forced_supermarket,
        )

        is_pantry_item = ing.get("is_pantry", False) or is_pantry(name)
        cost: float | None = None
        offer_id: int | None = None
        note: str | None = None
        category = None
        supermarket_slug: str | None = None
        supermarket_name: str | None = None
        offer_product_name: str | None = None

        if offer:
            offer_id = offer.id
            used_offer_ids.add(offer.id)
            used_offer_counts[offer.id] = used_offer_counts.get(offer.id, 0) + 1
            cost = _cost_for_offer(offer, grams_total)
            category = offer.category
            offer_product_name = offer.product_name
            if offer.supermarket:
                supermarket_slug = offer.supermarket.slug
                supermarket_name = offer.supermarket.name
                note = f"Uit aanbieding bij {offer.supermarket.name}"
                bucket = supermarket_counts.setdefault(
                    supermarket_slug, {"name": supermarket_name, "count": 0}
                )
                bucket["count"] += 1
            matched_real_offers += 1
            shopping_items.append(f"{offer.product_name} (€{offer.sale_price:.2f}) bij {supermarket_name or '?'}")
        elif is_pantry_item:
            note = "Standaardproduct (verwacht voorhanden)"
            pantry_items_used.append(name)
        else:
            missing_pantry.append(name)
            note = "Geen aanbieding gevonden — los aanschaffen"
            shopping_items.append(f"{name} (geen aanbieding)")

        ingredients_out.append(
            RecipeIngredientOut(
                name=name,
                quantity=round(grams_total, 1) if grams_total else None,
                unit=ing.get("unit"),
                is_pantry=is_pantry_item,
                estimated_cost=cost,
                offer_id=offer_id,
                note=note,
                supermarket_slug=supermarket_slug,
                supermarket_name=supermarket_name,
                offer_product_name=offer_product_name,
            )
        )
        if cost:
            total_cost += cost

        nutrition_items.append((name, category, grams_total))
        weighted_categories.append((category, grams_total))
        if category and category.lower() in VEG_FRUIT_CATEGORIES:
            veg_fruit_grams += grams_per_serving

    # Minimaal de helft van de niet-pantry ingredienten moet uit een
    # aanbieding komen, anders is het recept niet zinvol bij deze selectie.
    non_pantry_count = sum(1 for i in template["ingredients"] if not i.get("is_pantry"))
    if matched_real_offers < max(2, non_pantry_count // 2):
        return None

    # Single-supermarket regel: als allow_multi_supermarket=False en er
    # zijn meerdere supermarkten gebruikt, recept verwerpen.
    if not request.allow_multi_supermarket and len(supermarket_counts) > 1:
        return None

    totals_per_serving, confidence = aggregate_recipe_nutrition(
        nutrition_items, servings, try_remote=False
    )

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

    if request.min_health_score and health.score < request.min_health_score:
        return None

    diet_tags = list(template.get("diet_tags", []))
    if cost_per_serving is not None and cost_per_serving < 3.0:
        health.labels.append("budgetvriendelijk")
    for tag in diet_tags:
        if tag in {"vegetarisch", "vegan"} and tag not in health.labels:
            health.labels.append(tag)

    supermarkets_used = [
        RecipeSupermarketUse(slug=slug, name=info["name"], offer_count=info["count"])
        for slug, info in supermarket_counts.items()
    ]

    prep_t = template.get("prep_time_minutes", 0) or 0
    cook_t = template.get("cook_time_minutes", 0) or 0

    image_key = template.get("image_key", "default")
    photo_url = photo_url_for(image_key, title=template["title"])

    return RecipeOut(
        title=template["title"],
        description=template.get("description"),
        meal_type=template.get("meal_type", "diner"),
        difficulty=template.get("difficulty", "makkelijk"),
        instructions=list(template["instructions"]),
        servings=servings,
        prep_time_minutes=prep_t,
        cook_time_minutes=cook_t,
        total_time_minutes=prep_t + cook_t,
        total_cost=round(total_cost, 2),
        cost_per_serving=cost_per_serving,
        diet_tags=diet_tags,
        missing_pantry_items=missing_pantry,
        allergens=list(template.get("allergens", [])),
        serving_tips=list(template.get("serving_tips", [])),
        storage_tips=list(template.get("storage_tips", [])),
        variations=list(template.get("variations", [])),
        ingredients=ingredients_out,
        supermarkets_used=supermarkets_used,
        why_smart=template.get("why_smart"),
        shopping_items=shopping_items,
        pantry_items=pantry_items_used,
        image_url=photo_url,
        image_key=image_key,
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
    """Genereer recepten met de rule-based engine."""
    allowed_slugs = {s.lower() for s in request.selected_supermarkets if s}
    allowed_offers = _allowed_offers_for_supermarkets(offers, allowed_slugs)

    logger.info(
        "recept-generatie: %d offers, %d na supermarktfiltering (selectie=%s, multi=%s)",
        len(offers), len(allowed_offers), allowed_slugs or "alle", request.allow_multi_supermarket,
    )

    if not allowed_offers:
        return []

    # Voor variatie: doorloop templates meerdere keren met verschillende
    # 'forced_supermarket' rotatie. Eerste pass alle templates, daarna
    # met de wisselende rotatie om diversiteit te boosten.
    used_offer_counts: dict[int, int] = defaultdict(int)
    results: list[RecipeOut] = []
    seen_titles: set[str] = set()

    # Bepaal de forced-supermarket modus.
    # Single-supermarket mode = elke selected supermarket krijgt een
    # subset van recepten.
    if not request.allow_multi_supermarket:
        # Als 1 supermarkt geselecteerd: forceer die. Anders: per recept
        # forceren door eerste matched supermarket.
        if len(allowed_slugs) == 1:
            forced_list = [next(iter(allowed_slugs))]
        elif allowed_slugs:
            # Roteer per recept door geselecteerde slugs zodat elke
            # supermarkt aan bod komt.
            forced_list = list(allowed_slugs)
        else:
            # Geen selectie -> probeer per recept te forceren naar 1
            # supermarkt zodat je niet hoeft te shoppen op 5 plekken.
            forced_list = sorted({o.supermarket.slug for o in allowed_offers if o.supermarket})
    else:
        forced_list = [None]  # type: ignore[list-item]

    # We hebben max 24 templates * len(forced_list) potentiele recepten.
    rotation_idx = 0
    passes = 0
    max_passes = 4

    while len(results) < request.count and passes < max_passes:
        for template in RECIPE_TEMPLATES:
            if template["title"] in seen_titles:
                continue
            forced = forced_list[rotation_idx % len(forced_list)]
            recipe = _build_recipe_from_template(
                template, request, allowed_offers, used_offer_counts, forced_supermarket=forced
            )
            if recipe:
                results.append(recipe)
                seen_titles.add(template["title"])
                rotation_idx += 1
                if len(results) >= request.count:
                    break
        passes += 1
        # Bij vervolg-passes proberen we het minder strikt met andere
        # rotatie zodat we wel genoeg recepten halen.
        if len(results) < request.count and passes < max_passes:
            # In volgende pass mogen al gebruikte templates op andere
            # supermarkt forceringen opnieuw aan bod komen.
            seen_titles.clear()
            rotation_idx += 1

    sort_mode = getattr(request, "sort", "smart")
    if sort_mode == "health-desc":
        results.sort(key=lambda r: r.health.score, reverse=True)
    elif sort_mode == "price-asc":
        results.sort(key=lambda r: r.cost_per_serving or 999)
    elif sort_mode == "time-asc":
        results.sort(key=lambda r: r.total_time_minutes or 999)
    else:
        def sort_key(r: RecipeOut) -> float:
            cost = r.cost_per_serving or 5.0
            return -(r.health.score - cost * 3)
        results.sort(key=sort_key)

    logger.info("recept-generatie klaar: %d recepten", len(results))
    return results[: request.count]
