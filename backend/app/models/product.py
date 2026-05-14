from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    normalized_name = Column(String(255), index=True, nullable=False)
    category = Column(String(128), index=True, nullable=True)
    unit = Column(String(64), nullable=True)
    amount = Column(Float, nullable=True)
    barcode = Column(String(64), index=True, nullable=True)
    image_url = Column(String(512), nullable=True)

    offers = relationship("Offer", back_populates="product")
    nutrition = relationship("NutritionEstimate", back_populates="product", uselist=False)
