from app.schemas.offer import ScrapedOffer
from app.services.scrapers.base import BaseScraper
from app.services.scrapers.mock_data import generate_mock_offers


class CoopScraper(BaseScraper):
    slug = "coop"
    name = "Coop"
    base_url = "https://www.coop.nl"

    def fetch_live(self) -> list[ScrapedOffer]:
        raise NotImplementedError("Live Coop scraper nog niet geimplementeerd")

    def mock_offers(self) -> list[ScrapedOffer]:
        return generate_mock_offers(self.slug)
