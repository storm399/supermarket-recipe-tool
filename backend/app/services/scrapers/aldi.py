from __future__ import annotations

import logging
import httpx

from app.schemas.offer import ScrapedOffer
from app.services.scrapers.base import BaseScraper
from app.services.scrapers.mock_data import generate_mock_offers

logger = logging.getLogger(__name__)


class AldiScraper(BaseScraper):
    slug = "aldi"
    name = "Aldi"
    base_url = "https://www.aldi.nl"

    async def fetch_live(self, client: httpx.AsyncClient) -> list[ScrapedOffer]:
        try:
            r = await client.get(f"{self.base_url}/aanbiedingen.html")
            r.raise_for_status()
        except Exception as exc:  # noqa: BLE001
            logger.debug("Aldi live faalde: %s", exc)
        raise RuntimeError("Aldi live niet ondersteund — gebruik mock")

    def mock_offers(self) -> list[ScrapedOffer]:
        return generate_mock_offers(self.slug)
