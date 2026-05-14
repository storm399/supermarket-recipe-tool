from app.schemas.offer import ScrapedOffer
from app.services.scrapers.base import BaseScraper, make_offer


class EkoplazaScraper(BaseScraper):
    slug = "ekoplaza"
    name = "Ekoplaza"
    base_url = "https://www.ekoplaza.nl"

    def fetch_live(self) -> list[ScrapedOffer]:
        raise NotImplementedError("Live Ekoplaza scraper nog niet geimplementeerd")

    def mock_offers(self) -> list[ScrapedOffer]:
        return [
            make_offer(
                product_name="Biologische tofu",
                category="vleesvervanger",
                unit="g",
                amount=375,
                original_price=3.49,
                sale_price=2.49,
                source_url=f"{self.base_url}/aanbiedingen/tofu",
            ),
            make_offer(
                product_name="Biologische haver",
                category="ontbijt",
                unit="g",
                amount=500,
                original_price=2.79,
                sale_price=1.99,
                source_url=f"{self.base_url}/aanbiedingen/haver",
            ),
            make_offer(
                product_name="Biologische bloemkool",
                category="groente",
                unit="stuk",
                amount=1,
                original_price=2.99,
                sale_price=1.99,
                source_url=f"{self.base_url}/aanbiedingen/bloemkool",
            ),
            make_offer(
                product_name="Biologische sojadrink",
                category="zuivelvervanger",
                unit="l",
                amount=1.0,
                original_price=2.29,
                sale_price=1.69,
                source_url=f"{self.base_url}/aanbiedingen/sojadrink",
            ),
        ]
