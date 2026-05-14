from app.schemas.offer import ScrapedOffer
from app.services.scrapers.base import BaseScraper, make_offer


class HoogvlietScraper(BaseScraper):
    slug = "hoogvliet"
    name = "Hoogvliet"
    base_url = "https://www.hoogvliet.com"

    def fetch_live(self) -> list[ScrapedOffer]:
        raise NotImplementedError("Live Hoogvliet scraper nog niet geimplementeerd")

    def mock_offers(self) -> list[ScrapedOffer]:
        return [
            make_offer(
                product_name="Halfvolle melk",
                category="zuivel",
                unit="l",
                amount=1.0,
                original_price=1.19,
                sale_price=0.89,
                source_url=f"{self.base_url}/aanbiedingen/melk",
            ),
            make_offer(
                product_name="Aardappelen kruimig",
                category="aardappel",
                unit="kg",
                amount=2.0,
                original_price=2.79,
                sale_price=1.99,
                source_url=f"{self.base_url}/aanbiedingen/aardappelen",
            ),
            make_offer(
                product_name="Roergebakgroente",
                category="groente",
                unit="g",
                amount=400,
                original_price=2.29,
                sale_price=1.49,
                source_url=f"{self.base_url}/aanbiedingen/roerbak",
            ),
            make_offer(
                product_name="Tagliatelle",
                category="pasta",
                unit="g",
                amount=500,
                original_price=1.69,
                sale_price=0.99,
                source_url=f"{self.base_url}/aanbiedingen/tagliatelle",
            ),
        ]
