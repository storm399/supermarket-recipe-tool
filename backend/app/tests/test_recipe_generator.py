from __future__ import annotations

from dataclasses import dataclass
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
    fetched_at: datetime = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.fetched_at is None:
            self.fetched_at = datetime.utcnow()
        if not self.original_price:
            self.original_price = self.sale_price * 1.3


def _make_offer(name: str, price: float, category: str, unit: str, amount: float, supermarket_name: str = "Jumbo") -> FakeOffer:
    return FakeOffer(
        id=abs(hash(name)) % 10_000,
        product_name=name,
        sale_price=price,
        category=category,
        unit=unit,
        amount=amount,
        supermarket=FakeSupermarket(slug=supermarket_name.lower(), name=supermarket_name),
    )


def test_generator_returns_recipes_with_offers():
    offers = [
        _make_offer("Kipfilet naturel", 6.99, "vlees", "kg", 1.0),
        _make_offer("Volkoren pasta", 1.19, "pasta", "g", 500),
        _make_offer("Cherrytomaten", 1.49, "groente", "g", 250),
        _make_offer("Tofu", 2.49, "vleesvervanger", "g", 375),
        _make_offer("Broccoli", 0.99, "groente", "stuk", 1),
        _make_offer("Basmati rijst", 1.99, "rijst", "g", 1000),
        _make_offer("Ui", 0.79, "groente", "kg", 1.0),
    ]

    req = RecipeGenerateRequest(servings=2, count=5)
    recipes = generate_recipes_rule_based(req, offers)  # type: ignore[arg-type]

    assert len(recipes) > 0
    for r in recipes:
        assert r.title
        assert r.instructions
        assert r.servings == 2
        assert r.nutrition.kcal is not None
        assert 0 <= r.health.score <= 100
        # ten minste 1 ingredient moet uit een aanbieding komen
        assert any(ing.offer_id is not None for ing in r.ingredients)


def test_vegan_filter_excludes_meat_recipes():
    offers = [
        _make_offer("Tofu", 2.49, "vleesvervanger", "g", 375),
        _make_offer("Broccoli", 0.99, "groente", "stuk", 1),
        _make_offer("Basmati rijst", 1.99, "rijst", "g", 1000),
        _make_offer("Ui", 0.79, "groente", "kg", 1.0),
    ]
    req = RecipeGenerateRequest(servings=2, diets=["vegan"])
    recipes = generate_recipes_rule_based(req, offers)  # type: ignore[arg-type]
    for r in recipes:
        assert "vegan" in r.diet_tags


def test_exclude_ingredients_works():
    offers = [
        _make_offer("Kipfilet naturel", 6.99, "vlees", "kg", 1.0),
        _make_offer("Tofu", 2.49, "vleesvervanger", "g", 375),
        _make_offer("Broccoli", 0.99, "groente", "stuk", 1),
        _make_offer("Basmati rijst", 1.99, "rijst", "g", 1000),
    ]
    req = RecipeGenerateRequest(servings=2, exclude_ingredients=["kip"])
    recipes = generate_recipes_rule_based(req, offers)  # type: ignore[arg-type]
    for r in recipes:
        for ing in r.ingredients:
            assert "kip" not in ing.name.lower()
