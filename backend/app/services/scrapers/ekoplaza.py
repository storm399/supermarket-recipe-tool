from app.schemas.offer import ScrapedOffer
from app.services.scrapers.base import BaseScraper
from app.services.scrapers.mock_data import generate_mock_offers


class EkoplazaScraper(BaseScraper):
    slug = "ekoplaza"
    name = "Ekoplaza"
    base_url = "https://www.ekoplaza.nl"

    def fetch_live(self) -> list[ScrapedOffer]:
        raise NotImplementedError("Live Ekoplaza scraper nog niet geimplementeerd")

    def mock_offers(self) -> list[ScrapedOffer]:
        return generate_mock_offers(self.slug)
