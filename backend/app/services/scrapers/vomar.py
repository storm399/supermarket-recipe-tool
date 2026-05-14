from app.schemas.offer import ScrapedOffer
from app.services.scrapers.base import BaseScraper, make_offer


class VomarScraper(BaseScraper):
    slug = "vomar"
    name = "Vomar"
    base_url = "https://www.vomar.nl"

    def fetch_live(self) -> list[ScrapedOffer]:
        raise NotImplementedError("Live Vomar scraper nog niet geimplementeerd")

    def mock_offers(self) -> list[ScrapedOffer]:
        return [
            make_offer(
                product_name="Runderlapjes",
                category="vlees",
                unit="g",
                amount=500,
                original_price=6.99,
                sale_price=4.49,
                source_url=f"{self.base_url}/aanbiedingen/runderlapjes",
            ),
            make_offer(
                product_name="Courgette",
                category="groente",
                unit="stuk",
                amount=1,
                original_price=1.29,
                sale_price=0.79,
                source_url=f"{self.base_url}/aanbiedingen/courgette",
            ),
            make_offer(
                product_name="Mozzarella",
                category="zuivel",
                unit="g",
                amount=125,
                original_price=1.49,
                sale_price=0.99,
                source_url=f"{self.base_url}/aanbiedingen/mozzarella",
            ),
            make_offer(
                product_name="Linzen rood",
                category="peulvrucht",
                unit="g",
                amount=500,
                original_price=2.49,
                sale_price=1.69,
                source_url=f"{self.base_url}/aanbiedingen/linzen",
            ),
        ]
