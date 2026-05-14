from __future__ import annotations

import asyncio
import logging
import random
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Iterable

import httpx
from tenacity import AsyncRetrying, RetryError, stop_after_attempt, wait_exponential

from app.config import settings
from app.schemas.offer import ScrapedOffer

logger = logging.getLogger(__name__)


# Categorieen die we centraal benoemen zodat alle scrapers dezelfde
# 'taxonomie' gebruiken. Een scraper mag zelf categorieen toevoegen,
# maar deze lijst dekt de standaard supermarkt-afdelingen.
STANDARD_CATEGORIES = [
    "groente",
    "fruit",
    "aardappel",
    "vlees",
    "vis",
    "vleesvervanger",
    "ei",
    "zuivel",
    "zuivelvervanger",
    "kaas",
    "brood",
    "ontbijt",
    "pasta",
    "rijst",
    "graan",
    "peulvrucht",
    "blik",
    "diepvries",
    "snack",
    "spread",
    "drank",
    "olie",
    "biologisch",
    "huishouden",
    "verzorging",
]


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


@dataclass
class ScrapeStats:
    fetched: int = 0
    saved: int = 0
    duplicates_skipped: int = 0
    duration_ms: int = 0
    source: str = "fallback_mock"
    ok: bool = False
    error: str | None = None
    raw_offers: list[ScrapedOffer] = field(default_factory=list)


class BaseScraper(ABC):
    """Async basisklasse voor supermarkt-scrapers.

    Subclasses overriden:
    - `fetch_live()`: probeer echte data op te halen via API/HTML.
    - `mock_offers()`: lever uitgebreide fallback-aanbiedingen.

    `fetch_offers()` is het publieke contract: probeert live, valt
    terug op mock, levert altijd een resultaat plus stats.
    """

    slug: str = ""
    name: str = ""
    base_url: str = ""

    def __init__(self, *, user_agent: str | None = None, timeout: int | None = None) -> None:
        self.user_agent = user_agent or settings.SCRAPER_USER_AGENT
        self.timeout = timeout or settings.SCRAPER_TIMEOUT

    # ---- abstracte / overrideable ----

    @abstractmethod
    async def fetch_live(self, client: httpx.AsyncClient) -> list[ScrapedOffer]:
        """Implementeer echte ophaal-logica. Werp bij gebrek aan data of fout."""

    @abstractmethod
    def mock_offers(self) -> list[ScrapedOffer]:
        """Realistische fallback-aanbiedingen, gebruikt als live faalt."""

    # ---- helpers ----

    def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            headers={
                "User-Agent": self.user_agent,
                "Accept": "application/json, text/html;q=0.9, */*;q=0.8",
                "Accept-Language": "nl-NL,nl;q=0.9,en;q=0.8",
            },
            timeout=self.timeout,
            follow_redirects=True,
        )

    @staticmethod
    def _dedupe(offers: Iterable[ScrapedOffer]) -> tuple[list[ScrapedOffer], int]:
        seen: set[tuple[str, float]] = set()
        result: list[ScrapedOffer] = []
        dups = 0
        for o in offers:
            key = (o.product_name.strip().lower(), round(o.sale_price, 2))
            if key in seen:
                dups += 1
                continue
            seen.add(key)
            result.append(o)
        return result, dups

    async def _try_live(self) -> list[ScrapedOffer]:
        async with self._client() as client:
            try:
                async for attempt in AsyncRetrying(
                    stop=stop_after_attempt(2),
                    wait=wait_exponential(min=1, max=4),
                    reraise=True,
                ):
                    with attempt:
                        offers = await self.fetch_live(client)
                        if not offers:
                            raise RuntimeError("0 offers from live source")
                        return offers
            except (RetryError, Exception) as exc:  # noqa: BLE001
                raise exc
        return []  # niet bereikbaar

    # ---- publieke entrypoint ----

    async def fetch_offers(self) -> ScrapeStats:
        start = time.time()
        stats = ScrapeStats()

        if not settings.USE_MOCK_SCRAPERS:
            try:
                live = await self._try_live()
                deduped, dups = self._dedupe(live)
                stats.raw_offers = deduped
                stats.fetched = len(live)
                stats.duplicates_skipped = dups
                stats.source = "live_scraper"
                stats.ok = True
                logger.info(
                    "[%s] live ok: %d items (%d dups)", self.slug, len(deduped), dups,
                )
            except Exception as exc:  # noqa: BLE001
                logger.warning("[%s] live faalde: %s -> val terug op mock", self.slug, exc)
                stats.error = str(exc)
                mock = self.mock_offers()
                deduped, dups = self._dedupe(mock)
                stats.raw_offers = deduped
                stats.fetched = len(mock)
                stats.duplicates_skipped = dups
                stats.source = "fallback_mock"
                stats.ok = True  # we hebben fallback dus succes
        else:
            mock = self.mock_offers()
            deduped, dups = self._dedupe(mock)
            stats.raw_offers = deduped
            stats.fetched = len(mock)
            stats.duplicates_skipped = dups
            stats.source = "fallback_mock"
            stats.ok = True
            logger.info("[%s] mock-modus: %d items (%d dups)", self.slug, len(deduped), dups)

        # zet source-veld op elke ScrapedOffer als die nog niet gezet is
        for o in stats.raw_offers:
            if o.source == "fallback_mock" and stats.source != "fallback_mock":
                o.source = stats.source

        stats.duration_ms = int((time.time() - start) * 1000)
        return stats


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
    source: str = "fallback_mock",
) -> ScrapedOffer:
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
        source=source,
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
