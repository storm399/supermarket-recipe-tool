from __future__ import annotations

from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


DietTag = Literal["vegetarisch", "vegan", "halal", "lactosevrij", "glutenvrij"]
MealType = Literal["ontbijt", "lunch", "diner", "snack", "meal-prep"]
Difficulty = Literal["makkelijk", "gemiddeld", "uitdagend"]


class RecipeGenerateRequest(BaseModel):
    servings: int = Field(default=2, ge=1, le=12)
    diets: List[DietTag] = Field(default_factory=list)
    meal_types: List[MealType] = Field(default_factory=list)
    max_prep_minutes: Optional[int] = Field(default=None, ge=5, le=240)
    min_protein_g: Optional[float] = Field(default=None, ge=0)
    max_kcal_per_serving: Optional[float] = Field(default=None, ge=0)
    max_budget_per_serving: Optional[float] = Field(default=None, ge=0)
    min_health_score: Optional[int] = Field(default=None, ge=0, le=100)
    # Strikte supermarktselectie. Lege lijst = alle supermarkten.
    selected_supermarkets: List[str] = Field(default_factory=list)
    # Mag de generator aanbiedingen uit meerdere supermarkten combineren?
    allow_multi_supermarket: bool = False
    exclude_ingredients: List[str] = Field(default_factory=list)
    count: int = Field(default=12, ge=1, le=24)
    sort: Literal["smart", "health-desc", "price-asc", "time-asc"] = "smart"
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
    supermarket_slug: Optional[str] = None
    supermarket_name: Optional[str] = None
    offer_product_name: Optional[str] = None


class RecipeSupermarketUse(BaseModel):
    slug: str
    name: str
    offer_count: int


class RecipeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    meal_type: MealType = "diner"
    difficulty: Difficulty = "makkelijk"
    instructions: List[str]
    servings: int
    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    total_time_minutes: Optional[int] = None
    total_cost: Optional[float] = None
    cost_per_serving: Optional[float] = None
    diet_tags: List[str] = Field(default_factory=list)
    missing_pantry_items: List[str] = Field(default_factory=list)
    allergens: List[str] = Field(default_factory=list)
    serving_tips: List[str] = Field(default_factory=list)
    storage_tips: List[str] = Field(default_factory=list)
    variations: List[str] = Field(default_factory=list)
    ingredients: List[RecipeIngredientOut] = Field(default_factory=list)
    supermarkets_used: List[RecipeSupermarketUse] = Field(default_factory=list)
    why_smart: Optional[str] = None
    shopping_items: List[str] = Field(default_factory=list)
    pantry_items: List[str] = Field(default_factory=list)
    image_url: Optional[str] = None
    image_key: Optional[str] = None
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
    meal_type: Optional[str] = "diner"
    difficulty: Optional[str] = "makkelijk"
    instructions: List[str]
    prep_time_minutes: int
    cook_time_minutes: Optional[int] = None
    servings: int
    ingredients: List[LLMRecipeIngredient]
    missing_pantry_items: List[str] = Field(default_factory=list)
    diet_tags: List[str] = Field(default_factory=list)
    allergens: List[str] = Field(default_factory=list)
    serving_tips: List[str] = Field(default_factory=list)
    storage_tips: List[str] = Field(default_factory=list)
    variations: List[str] = Field(default_factory=list)

    @field_validator("instructions")
    @classmethod
    def at_least_six_steps(cls, v: List[str]) -> List[str]:
        cleaned = [s.strip() for s in v if s and s.strip()]
        if len(cleaned) < 6:
            raise ValueError("recept moet minimaal 6 kookstappen hebben")
        return cleaned


class LLMRecipeList(BaseModel):
    recipes: List[LLMRecipe]


class OfferStats(BaseModel):
    total: int
    by_supermarket: dict[str, int]
    by_category: dict[str, int]
    average_discount_percent: Optional[float] = None
    source: str = "mock"
