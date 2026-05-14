from __future__ import annotations

from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


DietTag = Literal["vegetarisch", "vegan", "halal", "lactosevrij", "glutenvrij"]


class RecipeGenerateRequest(BaseModel):
    servings: int = Field(default=2, ge=1, le=12)
    diets: List[DietTag] = Field(default_factory=list)
    max_prep_minutes: Optional[int] = Field(default=None, ge=5, le=240)
    min_protein_g: Optional[float] = Field(default=None, ge=0)
    max_kcal_per_serving: Optional[float] = Field(default=None, ge=0)
    max_budget_per_serving: Optional[float] = Field(default=None, ge=0)
    favorite_supermarkets: List[str] = Field(default_factory=list)
    exclude_ingredients: List[str] = Field(default_factory=list)
    count: int = Field(default=3, ge=1, le=10)
    use_llm: bool = False


class NutritionInfo(BaseModel):
    kcal: Optional[float] = None
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = None
    sugar_g: Optional[float] = None
    fat_g: Optional[float] = None
    saturated_fat_g: Optional[float] = None
    fiber_g: Optional[float] = None
    salt_g: Optional[float] = None
    source: str = "estimated"


class HealthInfo(BaseModel):
    score: int = Field(ge=0, le=100)
    explanation: str
    labels: List[str] = Field(default_factory=list)


class RecipeIngredientOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None
    is_pantry: bool = False
    estimated_cost: Optional[float] = None
    offer_id: Optional[int] = None
    note: Optional[str] = None


class RecipeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    instructions: List[str]
    servings: int
    prep_time_minutes: Optional[int] = None
    total_cost: Optional[float] = None
    cost_per_serving: Optional[float] = None
    diet_tags: List[str] = Field(default_factory=list)
    missing_pantry_items: List[str] = Field(default_factory=list)
    ingredients: List[RecipeIngredientOut] = Field(default_factory=list)
    nutrition: NutritionInfo
    health: HealthInfo
    generated_by: str = "rule"
    generated_at: Optional[datetime] = None


class LLMRecipeIngredient(BaseModel):
    """Strikte validatie voor LLM-output zodat we hallucinaties opvangen."""
    name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None
    is_pantry: bool = False
    offer_product_name: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("ingredient name mag niet leeg zijn")
        return v.strip()


class LLMRecipe(BaseModel):
    title: str
    description: str
    instructions: List[str]
    prep_time_minutes: int
    servings: int
    ingredients: List[LLMRecipeIngredient]
    missing_pantry_items: List[str] = Field(default_factory=list)
    diet_tags: List[str] = Field(default_factory=list)


class LLMRecipeList(BaseModel):
    recipes: List[LLMRecipe]
