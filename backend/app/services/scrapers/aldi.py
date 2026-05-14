from app.schemas.offer import ScrapedOffer
from app.services.scrapers.base import BaseScraper, make_offer


class AldiScraper(BaseScraper):
    slug = "aldi"
    name = "Aldi"
    base_url = "https://www.aldi.nl"

    def fetch_live(self) -> list[ScrapedOffer]:
        raise NotImplementedError("Live Aldi scraper nog niet geimplementeerd")

    def mock_offers(self) -> list[ScrapedOffer]:
        return [
            make_offer(
                product_name="Bananen",
                category="fruit",
                unit="kg",
                amount=1.0,
                original_price=1.79,
                sale_price=1.19,
                source_url=f"{self.base_url}/aanbiedingen/bananen",
            ),
            make_offer(
                product_name="Eieren scharrel",
                category="ei",
                unit="stuk",
                amount=10,
                original_price=2.59,
                sale_price=1.79,
                source_url=f"{self.base_url}/aanbiedingen/eieren",
            ),
            make_offer(
                product_name="Tonijn in olijfolie",
                category="vis",
                unit="g",
                amount=160,
                original_price=1.69,
                sale_price=1.19,
                source_url=f"{self.base_url}/aanbiedingen/tonijn",
            ),
            make_offer(
                product_name="Komkommer",
                category="groente",
                unit="stuk",
                amount=1,
                original_price=0.99,
                sale_price=0.69,
                source_url=f"{self.base_url}/aanbiedingen/komkommer",
            ),
        ]
