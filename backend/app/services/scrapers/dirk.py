from app.schemas.offer import ScrapedOffer
from app.services.scrapers.base import BaseScraper, make_offer


class DirkScraper(BaseScraper):
    slug = "dirk"
    name = "Dirk"
    base_url = "https://www.dirk.nl"

    def fetch_live(self) -> list[ScrapedOffer]:
        raise NotImplementedError("Live Dirk scraper nog niet geimplementeerd")

    def mock_offers(self) -> list[ScrapedOffer]:
        return [
            make_offer(
                product_name="Varkenshaas",
                category="vlees",
                unit="g",
                amount=500,
                original_price=7.99,
                sale_price=4.99,
                source_url=f"{self.base_url}/aanbiedingen/varkenshaas",
            ),
            make_offer(
                product_name="IJsbergsla",
                category="groente",
                unit="stuk",
                amount=1,
                original_price=1.49,
                sale_price=0.79,
                source_url=f"{self.base_url}/aanbiedingen/ijsbergsla",
            ),
            make_offer(
                product_name="Volle yoghurt",
                category="zuivel",
                unit="l",
                amount=1.0,
                original_price=1.59,
                sale_price=0.99,
                source_url=f"{self.base_url}/aanbiedingen/yoghurt",
            ),
            make_offer(
                product_name="Spaghetti",
                category="pasta",
                unit="g",
                amount=500,
                original_price=1.29,
                sale_price=0.79,
                source_url=f"{self.base_url}/aanbiedingen/spaghetti",
            ),
        ]
