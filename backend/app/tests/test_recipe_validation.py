import pytest
from pydantic import ValidationError

from app.schemas.recipe import (
    LLMRecipe,
    LLMRecipeList,
    RecipeGenerateRequest,
)


def test_request_defaults():
    req = RecipeGenerateRequest()
    assert req.servings == 2
    assert req.count == 3
    assert req.diets == []
    assert req.use_llm is False


def test_invalid_servings_rejected():
    with pytest.raises(ValidationError):
        RecipeGenerateRequest(servings=0)


def test_invalid_diet_rejected():
    with pytest.raises(ValidationError):
        RecipeGenerateRequest(diets=["onzin"])


def test_llm_recipe_requires_ingredient_names():
    with pytest.raises(ValidationError):
        LLMRecipe(
            title="Test",
            description="x",
            instructions=["stap"],
            prep_time_minutes=10,
            servings=2,
            ingredients=[{"name": "", "quantity": 100, "unit": "g"}],
            missing_pantry_items=[],
            diet_tags=[],
        )


def test_llm_recipe_list_parses():
    raw = {
        "recipes": [
            {
                "title": "Pasta",
                "description": "Snel",
                "instructions": ["kook"],
                "prep_time_minutes": 15,
                "servings": 2,
                "ingredients": [
                    {"name": "Pasta", "quantity": 200, "unit": "g", "is_pantry": False, "offer_product_name": "Volkoren pasta"}
                ],
                "missing_pantry_items": [],
                "diet_tags": ["vegetarisch"],
            }
        ]
    }
    parsed = LLMRecipeList.model_validate(raw)
    assert len(parsed.recipes) == 1
    assert parsed.recipes[0].ingredients[0].name == "Pasta"
