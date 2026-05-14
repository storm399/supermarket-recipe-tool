from __future__ import annotations

import logging
import httpx

from app.schemas.offer import ScrapedOffer
from app.services.scrapers.base import BaseScraper
from app.services.scrapers.mock_data import generate_mock_offers

logger = logging.getLogger(__name__)


class VomarScraper(BaseScraper):
    slug = "vomar"
    name = "Vomar"
    base_url = "https://www.vomar.nl"

    async def fetch_live(self, client: httpx.AsyncClient) -> list[ScrapedOffer]:
        try:
            r = await client.get(f"{self.base_url}/aanbiedingen")
            r.raise_for_status()
        except Exception as exc:  # noqa: BLE001
            logger.debug("Vomar live faalde: %s", exc)
        raise RuntimeError("Vomar live niet ondersteund — gebruik mock")

    def mock_offers(self) -> list[ScrapedOffer]:
        return generate_mock_offers(self.slug)
