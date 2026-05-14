from __future__ import annotations

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.schemas.supermarket import SupermarketOut


class ScrapedOffer(BaseModel):
    """Resultaat van een scraper, voordat het in de DB komt."""
    product_name: str
    category: Optional[str] = None
    unit: Optional[str] = None
    amount: Optional[float] = None
    original_price: Optional[float] = None
    sale_price: float
    discount_percent: Optional[float] = None
    discount_text: Optional[str] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    image_url: Optional[str] = None
    source_url: Optional[str] = None
    description: Optional[str] = None


class OfferCreate(ScrapedOffer):
    supermarket_slug: str


class OfferOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_name: str
    category: Optional[str] = None
    unit: Optional[str] = None
    amount: Optional[float] = None
    original_price: Optional[float] = None
    sale_price: float
    discount_percent: Optional[float] = None
    discount_text: Optional[str] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    image_url: Optional[str] = None
    source_url: Optional[str] = None
    fetched_at: datetime
    supermarket: SupermarketOut


class OfferListResponse(BaseModel):
    total: int
    offers: list[OfferOut]
