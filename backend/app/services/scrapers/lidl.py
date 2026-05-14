from app.schemas.offer import ScrapedOffer
from app.services.scrapers.base import BaseScraper, make_offer


class LidlScraper(BaseScraper):
    slug = "lidl"
    name = "Lidl"
    base_url = "https://www.lidl.nl"

    def fetch_live(self) -> list[ScrapedOffer]:
        raise NotImplementedError("Live Lidl scraper nog niet geimplementeerd")

    def mock_offers(self) -> list[ScrapedOffer]:
        return [
            make_offer(
                product_name="Rundergehakt",
                category="vlees",
                unit="g",
                amount=500,
                original_price=4.49,
                sale_price=2.99,
                source_url=f"{self.base_url}/aanbiedingen/rundergehakt",
            ),
            make_offer(
                product_name="Paprika mix",
                category="groente",
                unit="g",
                amount=500,
                original_price=2.49,
                sale_price=1.79,
                source_url=f"{self.base_url}/aanbiedingen/paprika",
            ),
            make_offer(
                product_name="Basmati rijst",
                category="rijst",
                unit="g",
                amount=1000,
                original_price=2.99,
                sale_price=1.99,
                source_url=f"{self.base_url}/aanbiedingen/basmati",
            ),
            make_offer(
                product_name="Champignons",
                category="groente",
                unit="g",
                amount=250,
                original_price=1.59,
                sale_price=0.99,
                source_url=f"{self.base_url}/aanbiedingen/champignons",
            ),
            make_offer(
                product_name="Kaas belegen",
                category="zuivel",
                unit="g",
                amount=400,
                original_price=4.99,
                sale_price=3.49,
                source_url=f"{self.base_url}/aanbiedingen/kaas",
            ),
        ]
