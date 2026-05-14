from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Boolean, JSON
from sqlalchemy.orm import relationship

from app.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    instructions = Column(JSON, nullable=False, default=list)
    servings = Column(Integer, nullable=False, default=2)
    prep_time_minutes = Column(Integer, nullable=True)

    total_cost = Column(Float, nullable=True)
    cost_per_serving = Column(Float, nullable=True)

    diet_tags = Column(JSON, nullable=False, default=list)
    missing_pantry_items = Column(JSON, nullable=False, default=list)

    kcal_per_serving = Column(Float, nullable=True)
    protein_g = Column(Float, nullable=True)
    carbs_g = Column(Float, nullable=True)
    sugar_g = Column(Float, nullable=True)
    fat_g = Column(Float, nullable=True)
    saturated_fat_g = Column(Float, nullable=True)
    fiber_g = Column(Float, nullable=True)
    salt_g = Column(Float, nullable=True)
    nutrition_source = Column(String(64), nullable=True)

    health_score = Column(Integer, nullable=True)
    health_explanation = Column(Text, nullable=True)
    health_labels = Column(JSON, nullable=False, default=list)

    generated_by = Column(String(32), nullable=False, default="rule")
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False, index=True)
    offer_id = Column(Integer, ForeignKey("offers.id", ondelete="SET NULL"), nullable=True, index=True)

    name = Column(String(255), nullable=False)
    quantity = Column(Float, nullable=True)
    unit = Column(String(64), nullable=True)
    is_pantry = Column(Boolean, default=False, nullable=False)
    estimated_cost = Column(Float, nullable=True)
    note = Column(String(255), nullable=True)

    recipe = relationship("Recipe", back_populates="ingredients")
    offer = relationship("Offer")
