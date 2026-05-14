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
    assert req.count == 12
    assert req.diets == []
    assert req.use_llm is False
    assert req.allow_multi_supermarket is False


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
            instructions=[
                "stap 1", "stap 2", "stap 3", "stap 4", "stap 5", "stap 6",
            ],
            prep_time_minutes=10,
            servings=2,
            ingredients=[{"name": "", "quantity": 100, "unit": "g"}],
            missing_pantry_items=[],
            diet_tags=[],
        )


def test_llm_recipe_requires_six_steps():
    with pytest.raises(ValidationError) as exc_info:
        LLMRecipe(
            title="Test",
            description="x",
            instructions=["kook", "serveer"],
            prep_time_minutes=10,
            servings=2,
            ingredients=[{"name": "Pasta", "quantity": 100, "unit": "g"}],
        )
    assert "minimaal 6 kookstappen" in str(exc_info.value)


def test_llm_recipe_list_parses():
    raw = {
        "recipes": [
            {
                "title": "Pasta",
                "description": "Snel",
                "instructions": [
                    "Breng water aan de kook.",
                    "Voeg pasta toe.",
                    "Kook 9 minuten.",
                    "Verhit een pan met olie.",
                    "Voeg knoflook toe en bak kort.",
                    "Meng met de pasta en serveer.",
                ],
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
    assert len(parsed.recipes[0].instructions) >= 6
