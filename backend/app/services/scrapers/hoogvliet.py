from app.schemas.offer import ScrapedOffer
from app.services.scrapers.base import BaseScraper
from app.services.scrapers.mock_data import generate_mock_offers


class HoogvlietScraper(BaseScraper):
    slug = "hoogvliet"
    name = "Hoogvliet"
    base_url = "https://www.hoogvliet.com"

    def fetch_live(self) -> list[ScrapedOffer]:
        raise NotImplementedError("Live Hoogvliet scraper nog niet geimplementeerd")

    def mock_offers(self) -> list[ScrapedOffer]:
        return generate_mock_offers(self.slug)
