from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.schemas.recipe import RecipeGenerateRequest
from app.services.recipe_generator import generate_recipes_rule_based


@dataclass
class FakeSupermarket:
    slug: str
    name: str


@dataclass
class FakeOffer:
    id: int
    product_name: str
    sale_price: float
    category: str
    unit: str
    amount: float
    supermarket: FakeSupermarket
    original_price: float = 0.0
    discount_percent: float = 20.0
    fetched_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self) -> None:
        if not self.original_price:
            self.original_price = self.sale_price * 1.3


_ID_COUNTER = {"value": 1}


def _make_offer(name: str, price: float, category: str, unit: str, amount: float, supermarket_name: str = "Jumbo") -> FakeOffer:
    _ID_COUNTER["value"] += 1
    return FakeOffer(
        id=_ID_COUNTER["value"],
        product_name=name,
        sale_price=price,
        category=category,
        unit=unit,
        amount=amount,
        supermarket=FakeSupermarket(slug=supermarket_name.lower(), name=supermarket_name),
    )


def _broad_offer_set(supermarket: str = "Jumbo") -> list[FakeOffer]:
    """Aanbiedingenset met genoeg variatie voor ≥12 recepten."""
    return [
        _make_offer("Kipfilet naturel", 6.99, "vlees", "kg", 1.0, supermarket),
        _make_offer("Kipgyros", 4.79, "vlees", "g", 400, supermarket),
        _make_offer("Rundergehakt", 4.49, "vlees", "g", 500, supermarket),
        _make_offer("Speklapjes", 4.99, "vlees", "g", 500, supermarket),
        _make_offer("Zalmfilet", 5.99, "vis", "g", 200, supermarket),
        _make_offer("Tonijn in olijfolie", 1.69, "vis", "g", 160, supermarket),
        _make_offer("Garnalen", 4.99, "vis", "g", 200, supermarket),
        _make_offer("Tofu", 2.49, "vleesvervanger", "g", 375, supermarket),
        _make_offer("Falafel", 2.49, "vleesvervanger", "g", 220, supermarket),
        _make_offer("Volkoren pasta", 1.19, "pasta", "g", 500, supermarket),
        _make_offer("Spaghetti", 0.79, "pasta", "g", 500, supermarket),
        _make_offer("Cherrytomaten", 1.49, "groente", "g", 250, supermarket),
        _make_offer("Gepelde tomaten", 0.69, "blik", "g", 400, supermarket),
        _make_offer("Broccoli", 0.99, "groente", "stuk", 1, supermarket),
        _make_offer("Bloemkool", 1.49, "groente", "stuk", 1, supermarket),
        _make_offer("Champignons", 0.99, "groente", "g", 250, supermarket),
        _make_offer("Paprika", 1.79, "groente", "g", 500, supermarket),
        _make_offer("Courgette", 0.79, "groente", "stuk", 1, supermarket),
        _make_offer("Spinazie", 1.49, "groente", "g", 300, supermarket),
        _make_offer("Komkommer", 0.69, "groente", "stuk", 1, supermarket),
        _make_offer("IJsbergsla", 0.79, "groente", "stuk", 1, supermarket),
        _make_offer("Wortelen", 0.99, "groente", "kg", 1.0, supermarket),
        _make_offer("Ui", 0.79, "groente", "kg", 1.0, supermarket),
        _make_offer("Rode ui", 1.19, "groente", "kg", 1.0, supermarket),
        _make_offer("Knoflook", 0.99, "groente", "stuk", 3, supermarket),
        _make_offer("Basmati rijst", 1.99, "rijst", "g", 1000, supermarket),
        _make_offer("Couscous", 1.49, "graan", "g", 500, supermarket),
        _make_offer("Quinoa", 2.99, "graan", "g", 400, supermarket),
        _make_offer("Aardappelen", 1.99, "aardappel", "kg", 2.0, supermarket),
        _make_offer("Kikkererwten in blik", 0.79, "peulvrucht", "g", 400, supermarket),
        _make_offer("Witte bonen", 0.89, "peulvrucht", "g", 400, supermarket),
        _make_offer("Linzen rood", 1.69, "peulvrucht", "g", 500, supermarket),
        _make_offer("Volkoren wraps", 1.49, "brood", "stuk", 8, supermarket),
        _make_offer("Pitabroodjes", 1.19, "brood", "stuk", 6, supermarket),
        _make_offer("Volkoren brood", 1.79, "brood", "stuk", 1, supermarket),
        _make_offer("Eieren", 1.79, "ei", "stuk", 10, supermarket),
        _make_offer("Yoghurt", 0.99, "zuivel", "l", 1.0, supermarket),
        _make_offer("Griekse yoghurt", 1.99, "zuivel", "g", 500, supermarket),
        _make_offer("Hüttenkäse", 1.49, "zuivel", "g", 200, supermarket),
        _make_offer("Kaas", 3.49, "zuivel", "g", 400, supermarket),
        _make_offer("Mozzarella", 0.99, "zuivel", "g", 125, supermarket),
        _make_offer("Melk", 0.89, "zuivel", "l", 1.0, supermarket),
        _make_offer("Havermout", 0.99, "ontbijt", "g", 500, supermarket),
        _make_offer("Muesli", 2.19, "ontbijt", "g", 500, supermarket),
        _make_offer("Banaan", 1.19, "fruit", "kg", 1.0, supermarket),
        _make_offer("Aardbeien", 2.49, "fruit", "g", 400, supermarket),
        _make_offer("Blauwe bessen", 1.99, "fruit", "g", 125, supermarket),
        _make_offer("Avocado", 1.99, "fruit", "stuk", 2, supermarket),
        _make_offer("Appel", 1.49, "fruit", "kg", 1.0, supermarket),
        _make_offer("Hummus", 1.49, "spread", "g", 200, supermarket),
        _make_offer("Olijven", 1.79, "spread", "g", 250, supermarket),
        _make_offer("Pesto", 1.69, "spread", "g", 190, supermarket),
    ]


def test_generator_returns_at_least_12_recipes():
    offers = _broad_offer_set()
    req = RecipeGenerateRequest(servings=2, count=12)
    recipes = generate_recipes_rule_based(req, offers)  # type: ignore[arg-type]
    assert len(recipes) >= 12


def test_each_recipe_has_six_or_more_steps():
    offers = _broad_offer_set()
    req = RecipeGenerateRequest(servings=2, count=12)
    recipes = generate_recipes_rule_based(req, offers)  # type: ignore[arg-type]
    for r in recipes:
        assert len(r.instructions) >= 6, f"Recept '{r.title}' heeft maar {len(r.instructions)} stappen"


def test_supermarkets_used_is_populated_and_single_when_strict():
    offers = _broad_offer_set("Jumbo") + _broad_offer_set("AH")
    req = RecipeGenerateRequest(servings=2, count=12, allow_multi_supermarket=False)
    recipes = generate_recipes_rule_based(req, offers)  # type: ignore[arg-type]
    assert len(recipes) > 0
    for r in recipes:
        assert len(r.supermarkets_used) >= 1
        assert len(r.supermarkets_used) == 1, (
            f"recept '{r.title}' gebruikt {len(r.supermarkets_used)} supermarkten in strict mode"
        )


def test_selected_supermarket_is_respected_strictly():
    offers = _broad_offer_set("Jumbo") + _broad_offer_set("AH")
    req = RecipeGenerateRequest(
        servings=2, count=12,
        selected_supermarkets=["jumbo"],
        allow_multi_supermarket=False,
    )
    recipes = generate_recipes_rule_based(req, offers)  # type: ignore[arg-type]
    assert len(recipes) >= 6
    for r in recipes:
        used = {sm.slug for sm in r.supermarkets_used}
        assert used.issubset({"jumbo"}), (
            f"recept '{r.title}' bevat supermarkt buiten selectie: {used}"
        )


def test_meal_types_filter_applied():
    offers = _broad_offer_set()
    req = RecipeGenerateRequest(servings=2, count=6, meal_types=["ontbijt"])
    recipes = generate_recipes_rule_based(req, offers)  # type: ignore[arg-type]
    if recipes:
        assert all(r.meal_type == "ontbijt" for r in recipes)


def test_recipes_have_health_score_and_cost_per_serving():
    offers = _broad_offer_set()
    req = RecipeGenerateRequest(servings=2, count=12)
    recipes = generate_recipes_rule_based(req, offers)  # type: ignore[arg-type]
    for r in recipes:
        assert 0 <= r.health.score <= 100
        assert r.cost_per_serving is not None
        assert r.cost_per_serving > 0


def test_exclude_ingredients_works():
    offers = _broad_offer_set()
    req = RecipeGenerateRequest(servings=2, exclude_ingredients=["kip"], count=12)
    recipes = generate_recipes_rule_based(req, offers)  # type: ignore[arg-type]
    for r in recipes:
        for ing in r.ingredients:
            assert "kip" not in ing.name.lower()


def test_vegan_filter_excludes_meat_recipes():
    offers = _broad_offer_set()
    req = RecipeGenerateRequest(servings=2, diets=["vegan"], count=6)
    recipes = generate_recipes_rule_based(req, offers)  # type: ignore[arg-type]
    for r in recipes:
        assert "vegan" in r.diet_tags
