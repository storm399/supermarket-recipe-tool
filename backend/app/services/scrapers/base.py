from __future__ import annotations

import logging
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterable

from app.config import settings
from app.schemas.offer import ScrapedOffer

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SupermarketDef:
    slug: str
    name: str
    base_url: str
    logo_url: str | None = None


SUPERMARKETS: list[SupermarketDef] = [
    SupermarketDef("jumbo", "Jumbo", "https://www.jumbo.com"),
    SupermarketDef("ah", "Albert Heijn", "https://www.ah.nl"),
    SupermarketDef("lidl", "Lidl", "https://www.lidl.nl"),
    SupermarketDef("hoogvliet", "Hoogvliet", "https://www.hoogvliet.com"),
    SupermarketDef("aldi", "Aldi", "https://www.aldi.nl"),
    SupermarketDef("ekoplaza", "Ekoplaza", "https://www.ekoplaza.nl"),
    SupermarketDef("plus", "Plus", "https://www.plus.nl"),
    SupermarketDef("dirk", "Dirk", "https://www.dirk.nl"),
    SupermarketDef("vomar", "Vomar", "https://www.vomar.nl"),
    SupermarketDef("coop", "Coop", "https://www.coop.nl"),
]


class BaseScraper(ABC):
    """Basisklasse voor supermarkt-scrapers.

    Elke supermarkt heeft een eigen subclass zodat ze afzonderlijk
    aangepast en getest kunnen worden zonder andere scrapers te raken.
    """

    slug: str = ""
    name: str = ""
    base_url: str = ""

    def __init__(self, *, user_agent: str | None = None, timeout: int | None = None) -> None:
        self.user_agent = user_agent or settings.SCRAPER_USER_AGENT
        self.timeout = timeout or settings.SCRAPER_TIMEOUT

    @abstractmethod
    def fetch_live(self) -> list[ScrapedOffer]:
        """Haal echte aanbiedingen op. Subclasses implementeren dit."""

    @abstractmethod
    def mock_offers(self) -> list[ScrapedOffer]:
        """Lever realistische mock-aanbiedingen voor MVP en tests."""

    def scrape(self) -> list[ScrapedOffer]:
        if settings.USE_MOCK_SCRAPERS:
            offers = self.mock_offers()
            logger.info("[%s] mock-modus: %d aanbiedingen", self.slug, len(offers))
            return offers
        try:
            offers = self.fetch_live()
            logger.info("[%s] live: %d aanbiedingen", self.slug, len(offers))
            return offers
        except Exception as exc:  # noqa: BLE001
            logger.exception("[%s] scrape mislukt, val terug op mock: %s", self.slug, exc)
            return self.mock_offers()


def make_offer(
    *,
    product_name: str,
    sale_price: float,
    original_price: float | None = None,
    category: str | None = None,
    unit: str | None = None,
    amount: float | None = None,
    image_url: str | None = None,
    source_url: str | None = None,
    description: str | None = None,
    valid_days: int = 7,
    discount_text: str | None = None,
) -> ScrapedOffer:
    """Helper voor het bouwen van een ScrapedOffer in mock-modus."""
    now = datetime.utcnow()
    valid_from = now - timedelta(days=random.randint(0, 1))
    valid_until = now + timedelta(days=valid_days)
    discount = None
    if original_price and original_price > sale_price:
        discount = round((1 - sale_price / original_price) * 100, 1)
    return ScrapedOffer(
        product_name=product_name,
        category=category,
        unit=unit,
        amount=amount,
        original_price=original_price,
        sale_price=sale_price,
        discount_percent=discount,
        discount_text=discount_text,
        valid_from=valid_from,
        valid_until=valid_until,
        image_url=image_url,
        source_url=source_url,
        description=description,
    )


def chunked(items: Iterable, size: int):
    chunk: list = []
    for item in items:
        chunk.append(item)
        if len(chunk) >= size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk
