from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Supermarket(Base):
    __tablename__ = "supermarkets"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(64), unique=True, index=True, nullable=False)
    name = Column(String(128), nullable=False)
    base_url = Column(String(255), nullable=True)
    logo_url = Column(String(255), nullable=True)
    active = Column(Boolean, default=True, nullable=False)

    offers = relationship("Offer", back_populates="supermarket", cascade="all, delete-orphan")
