from app.schemas.offer import ScrapedOffer
from app.services.scrapers.base import BaseScraper
from app.services.scrapers.mock_data import generate_mock_offers


class LidlScraper(BaseScraper):
    slug = "lidl"
    name = "Lidl"
    base_url = "https://www.lidl.nl"

    def fetch_live(self) -> list[ScrapedOffer]:
        raise NotImplementedError("Live Lidl scraper nog niet geimplementeerd")

    def mock_offers(self) -> list[ScrapedOffer]:
        return generate_mock_offers(self.slug)
