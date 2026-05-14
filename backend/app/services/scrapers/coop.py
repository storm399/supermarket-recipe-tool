from app.schemas.offer import ScrapedOffer
from app.services.scrapers.base import BaseScraper, make_offer


class CoopScraper(BaseScraper):
    slug = "coop"
    name = "Coop"
    base_url = "https://www.coop.nl"

    def fetch_live(self) -> list[ScrapedOffer]:
        raise NotImplementedError("Live Coop scraper nog niet geimplementeerd")

    def mock_offers(self) -> list[ScrapedOffer]:
        return [
            make_offer(
                product_name="Zalmmoot",
                category="vis",
                unit="g",
                amount=250,
                original_price=6.49,
                sale_price=4.49,
                source_url=f"{self.base_url}/aanbiedingen/zalmmoot",
            ),
            make_offer(
                product_name="Aardbeien",
                category="fruit",
                unit="g",
                amount=400,
                original_price=3.99,
                sale_price=2.49,
                source_url=f"{self.base_url}/aanbiedingen/aardbeien",
            ),
            make_offer(
                product_name="Ui",
                category="groente",
                unit="kg",
                amount=1.0,
                original_price=1.29,
                sale_price=0.79,
                source_url=f"{self.base_url}/aanbiedingen/ui",
            ),
            make_offer(
                product_name="Knoflook",
                category="groente",
                unit="stuk",
                amount=3,
                original_price=1.49,
                sale_price=0.99,
                source_url=f"{self.base_url}/aanbiedingen/knoflook",
            ),
        ]
