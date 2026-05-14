"""Voedingsinformatie ophalen of schatten.

Strategie:
1. Probeer eerst de fallback-tabel (snel en offline).
2. Probeer daarna Open Food Facts als product onbekend is.
3. Val tot slot terug op een categorie-gemiddelde.

Markeert per recept of de waarden 'exact', 'estimated' of 'partial' zijn.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass

import httpx

from app.config import settings
from app.data.nutrition_fallback import CATEGORY_FALLBACK, NUTRITION_FALLBACK
from app.services.offer_matcher import normalize

logger = logging.getLogger(__name__)


@dataclass
class NutritionPer100:
    kcal: float = 0
    protein: float = 0
    carbs: float = 0
    sugar: float = 0
    fat: float = 0
    satfat: float = 0
    fiber: float = 0
    salt: float = 0
    source: str = "fallback"
    confidence: str = "estimated"

    def scale(self, grams: float) -> "NutritionTotals":
        factor = grams / 100.0
        return NutritionTotals(
            kcal=self.kcal * factor,
            protein=self.protein * factor,
            carbs=self.carbs * factor,
            sugar=self.sugar * factor,
            fat=self.fat * factor,
            satfat=self.satfat * factor,
            fiber=self.fiber * factor,
            salt=self.salt * factor,
        )


@dataclass
class NutritionTotals:
    kcal: float = 0
    protein: float = 0
    carbs: float = 0
    sugar: float = 0
    fat: float = 0
    satfat: float = 0
    fiber: float = 0
    salt: float = 0

    def add(self, other: "NutritionTotals") -> None:
        self.kcal += other.kcal
        self.protein += other.protein
        self.carbs += other.carbs
        self.sugar += other.sugar
        self.fat += other.fat
        self.satfat += other.satfat
        self.fiber += other.fiber
        self.salt += other.salt

    def per_serving(self, servings: int) -> "NutritionTotals":
        if servings <= 0:
            return self
        return NutritionTotals(
            kcal=round(self.kcal / servings, 1),
            protein=round(self.protein / servings, 1),
            carbs=round(self.carbs / servings, 1),
            sugar=round(self.sugar / servings, 1),
            fat=round(self.fat / servings, 1),
            satfat=round(self.satfat / servings, 1),
            fiber=round(self.fiber / servings, 1),
            salt=round(self.salt / servings, 2),
        )


def _from_dict(d: dict[str, float], source: str, confidence: str) -> NutritionPer100:
    return NutritionPer100(
        kcal=d.get("kcal", 0),
        protein=d.get("protein", 0),
        carbs=d.get("carbs", 0),
        sugar=d.get("sugar", 0),
        fat=d.get("fat", 0),
        satfat=d.get("satfat", 0),
        fiber=d.get("fiber", 0),
        salt=d.get("salt", 0),
        source=source,
        confidence=confidence,
    )


def lookup_fallback(product_name: str, category: str | None = None) -> NutritionPer100 | None:
    norm = normalize(product_name)
    # exacte match
    if norm in NUTRITION_FALLBACK:
        return _from_dict(NUTRITION_FALLBACK[norm], source="fallback-table", confidence="estimated")
    # substring match
    for key, data in NUTRITION_FALLBACK.items():
        if key in norm or norm in key:
            return _from_dict(data, source="fallback-table", confidence="estimated")
    # categorie
    if category and category.lower() in CATEGORY_FALLBACK:
        return _from_dict(
            CATEGORY_FALLBACK[category.lower()],
            source="category-fallback",
            confidence="partial",
        )
    return None


def lookup_openfoodfacts(product_name: str) -> NutritionPer100 | None:
    """Zoek naar product op Open Food Facts. Best-effort, faalt stil."""
    try:
        headers = {"User-Agent": settings.OPENFOODFACTS_USER_AGENT}
        url = f"{settings.OPENFOODFACTS_BASE_URL}/cgi/search.pl"
        params = {
            "search_terms": product_name,
            "search_simple": 1,
            "action": "process",
            "json": 1,
            "page_size": 1,
            "fields": "product_name,nutriments",
        }
        with httpx.Client(timeout=8.0, headers=headers) as client:
            r = client.get(url, params=params)
            r.raise_for_status()
            data = r.json()
        products = data.get("products") or []
        if not products:
            return None
        n = products[0].get("nutriments") or {}

        def pick(*keys: str) -> float:
            for k in keys:
                v = n.get(k)
                if isinstance(v, (int, float)):
                    return float(v)
            return 0.0

        return NutritionPer100(
            kcal=pick("energy-kcal_100g", "energy-kcal"),
            protein=pick("proteins_100g", "proteins"),
            carbs=pick("carbohydrates_100g", "carbohydrates"),
            sugar=pick("sugars_100g", "sugars"),
            fat=pick("fat_100g", "fat"),
            satfat=pick("saturated-fat_100g", "saturated-fat"),
            fiber=pick("fiber_100g", "fiber"),
            salt=pick("salt_100g", "salt"),
            source="openfoodfacts",
            confidence="exact",
        )
    except Exception as exc:  # noqa: BLE001
        logger.debug("OpenFoodFacts lookup mislukt voor '%s': %s", product_name, exc)
        return None


def get_nutrition_per_100(
    product_name: str,
    category: str | None = None,
    *,
    try_remote: bool = False,
) -> NutritionPer100:
    """Haal voedingswaarden op met fallback-cascade.

    `try_remote=False` is de default zodat de app snel werkt en geen
    afhankelijkheid heeft tijdens tests; de aanbieding-fetch job kan
    de remote variant gebruiken om de DB te verrijken.
    """
    if try_remote:
        result = lookup_openfoodfacts(product_name)
        if result:
            return result
    fb = lookup_fallback(product_name, category)
    if fb:
        return fb
    # laatste redmiddel: zeer ruwe defaults
    return NutritionPer100(
        kcal=100, protein=3, carbs=15, sugar=2, fat=2, satfat=0.5, fiber=1, salt=0.1,
        source="default",
        confidence="partial",
    )


def aggregate_recipe_nutrition(
    items: list[tuple[str, str | None, float]],
    servings: int,
    *,
    try_remote: bool = False,
) -> tuple[NutritionTotals, str]:
    """Reken voedingswaarden uit voor een lijst (naam, categorie, gram).

    Geeft totalen per portie terug en de algehele confidence.
    """
    totals = NutritionTotals()
    confidences: list[str] = []
    sources: list[str] = []
    for name, category, grams in items:
        per100 = get_nutrition_per_100(name, category, try_remote=try_remote)
        confidences.append(per100.confidence)
        sources.append(per100.source)
        totals.add(per100.scale(grams))

    if all(c == "exact" for c in confidences):
        overall = "exact"
    elif any(c == "partial" for c in confidences) or "default" in sources:
        overall = "partial"
    else:
        overall = "estimated"

    return totals.per_serving(servings), overall
