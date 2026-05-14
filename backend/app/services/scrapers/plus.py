from app.schemas.offer import ScrapedOffer
from app.services.scrapers.base import BaseScraper, make_offer


class PlusScraper(BaseScraper):
    slug = "plus"
    name = "Plus"
    base_url = "https://www.plus.nl"

    def fetch_live(self) -> list[ScrapedOffer]:
        raise NotImplementedError("Live Plus scraper nog niet geimplementeerd")

    def mock_offers(self) -> list[ScrapedOffer]:
        return [
            make_offer(
                product_name="Kipgehakt",
                category="vlees",
                unit="g",
                amount=500,
                original_price=4.99,
                sale_price=3.49,
                source_url=f"{self.base_url}/aanbiedingen/kipgehakt",
            ),
            make_offer(
                product_name="Wortelen",
                category="groente",
                unit="kg",
                amount=1.0,
                original_price=1.69,
                sale_price=0.99,
                source_url=f"{self.base_url}/aanbiedingen/wortelen",
            ),
            make_offer(
                product_name="Volkoren brood",
                category="brood",
                unit="stuk",
                amount=1,
                original_price=2.49,
                sale_price=1.79,
                source_url=f"{self.base_url}/aanbiedingen/volkoren-brood",
            ),
            make_offer(
                product_name="Hummus",
                category="spread",
                unit="g",
                amount=200,
                original_price=2.29,
                sale_price=1.49,
                source_url=f"{self.base_url}/aanbiedingen/hummus",
            ),
        ]
