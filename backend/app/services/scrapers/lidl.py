from __future__ import annotations

import logging

import httpx

from app.schemas.offer import ScrapedOffer
from app.services.scrapers.base import BaseScraper
from app.services.scrapers.mock_data import generate_mock_offers

logger = logging.getLogger(__name__)


class LidlScraper(BaseScraper):
    """Lidl publiceert aanbiedingen in een dynamisch geladen folder.
    Een stabiel publiek JSON-endpoint is niet beschikbaar; we proberen
    de offer-leaflet HTML en vallen anders terug op mock.
    """
    slug = "lidl"
    name = "Lidl"
    base_url = "https://www.lidl.nl"

    async def fetch_live(self, client: httpx.AsyncClient) -> list[ScrapedOffer]:
        try:
            r = await client.get(f"{self.base_url}/c/aanbiedingen/s10020128")
            r.raise_for_status()
            # Lidl rendert offers grotendeels client-side; zonder JS
            # geen bruikbare data. We laten dit bewust falen zodat de
            # uitgebreide mockdata wordt gebruikt.
        except Exception as exc:  # noqa: BLE001
            logger.debug("Lidl live faalde: %s", exc)
        raise RuntimeError("Lidl live niet ondersteund — gebruik mock")

    def mock_offers(self) -> list[ScrapedOffer]:
        return generate_mock_offers(self.slug)
