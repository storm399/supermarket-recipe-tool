from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class NutritionEstimate(Base):
    __tablename__ = "nutrition_estimates"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)

    kcal_per_100 = Column(Float, nullable=True)
    protein_per_100 = Column(Float, nullable=True)
    carbs_per_100 = Column(Float, nullable=True)
    sugar_per_100 = Column(Float, nullable=True)
    fat_per_100 = Column(Float, nullable=True)
    saturated_fat_per_100 = Column(Float, nullable=True)
    fiber_per_100 = Column(Float, nullable=True)
    salt_per_100 = Column(Float, nullable=True)

    source = Column(String(64), nullable=False, default="fallback")
    confidence = Column(String(32), nullable=False, default="estimated")
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    product = relationship("Product", back_populates="nutrition")
