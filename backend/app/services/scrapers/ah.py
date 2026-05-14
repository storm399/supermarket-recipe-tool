from app.schemas.offer import ScrapedOffer
from app.services.scrapers.base import BaseScraper
from app.services.scrapers.mock_data import generate_mock_offers


class AlbertHeijnScraper(BaseScraper):
    slug = "ah"
    name = "Albert Heijn"
    base_url = "https://www.ah.nl"

    def fetch_live(self) -> list[ScrapedOffer]:
        raise NotImplementedError("Live AH scraper nog niet geimplementeerd")

    def mock_offers(self) -> list[ScrapedOffer]:
        return generate_mock_offers(self.slug)
