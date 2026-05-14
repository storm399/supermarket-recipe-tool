from app.schemas.offer import ScrapedOffer
from app.services.scrapers.base import BaseScraper
from app.services.scrapers.mock_data import generate_mock_offers


class JumboScraper(BaseScraper):
    slug = "jumbo"
    name = "Jumbo"
    base_url = "https://www.jumbo.com"

    def fetch_live(self) -> list[ScrapedOffer]:
        # TODO: gebruik Jumbo Promotions API of folderpagina.
        raise NotImplementedError("Live Jumbo scraper nog niet geimplementeerd")

    def mock_offers(self) -> list[ScrapedOffer]:
        return generate_mock_offers(self.slug)
