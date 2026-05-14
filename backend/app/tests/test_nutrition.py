from app.services.nutrition import (
    aggregate_recipe_nutrition,
    get_nutrition_per_100,
    lookup_fallback,
)


def test_fallback_finds_known_product():
    n = lookup_fallback("kipfilet")
    assert n is not None
    assert n.protein > 15
    assert n.source == "fallback-table"


def test_fallback_uses_category_when_unknown():
    n = lookup_fallback("xyz-onbekend", category="groente")
    assert n is not None
    assert n.source == "category-fallback"


def test_default_when_completely_unknown():
    n = get_nutrition_per_100("absurd-onbekend-product", category=None, try_remote=False)
    assert n.source in {"default", "fallback-table", "category-fallback"}


def test_aggregate_scales_correctly():
    totals, confidence = aggregate_recipe_nutrition(
        [("kipfilet", "vlees", 300.0), ("broccoli", "groente", 300.0)],
        servings=2,
        try_remote=False,
    )
    # 300 g kip * 23 g eiwit/100 + 300 g broccoli * 3 g eiwit / 100 = 69 + 9 = 78 / 2 = 39
    assert 30 < totals.protein < 50
    assert totals.kcal > 0
    assert confidence in {"estimated", "partial", "exact"}
