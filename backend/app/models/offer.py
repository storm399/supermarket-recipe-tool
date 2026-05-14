from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    supermarket_id = Column(Integer, ForeignKey("supermarkets.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"), nullable=True, index=True)

    product_name = Column(String(255), index=True, nullable=False)
    category = Column(String(128), index=True, nullable=True)
    unit = Column(String(64), nullable=True)
    amount = Column(Float, nullable=True)

    original_price = Column(Float, nullable=True)
    sale_price = Column(Float, nullable=False)
    discount_percent = Column(Float, nullable=True)
    discount_text = Column(String(128), nullable=True)

    valid_from = Column(DateTime, nullable=True)
    valid_until = Column(DateTime, nullable=True)

    image_url = Column(String(512), nullable=True)
    source_url = Column(String(512), nullable=True)
    description = Column(Text, nullable=True)
    source = Column(String(32), nullable=False, default="fallback_mock", index=True)

    fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    supermarket = relationship("Supermarket", back_populates="offers")
    product = relationship("Product", back_populates="offers")
