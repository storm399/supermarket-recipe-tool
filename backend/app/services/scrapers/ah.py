from app.schemas.offer import ScrapedOffer
from app.services.scrapers.base import BaseScraper, make_offer


class AlbertHeijnScraper(BaseScraper):
    slug = "ah"
    name = "Albert Heijn"
    base_url = "https://www.ah.nl"

    def fetch_live(self) -> list[ScrapedOffer]:
        # Albert Heijn heeft een (niet-officiele) bonus API endpoint.
        # Voor productie: gebruik httpx, parse JSON en map naar ScrapedOffer.
        raise NotImplementedError("Live AH scraper nog niet geimplementeerd")

    def mock_offers(self) -> list[ScrapedOffer]:
        return [
            make_offer(
                product_name="Magere yoghurt",
                category="zuivel",
                unit="l",
                amount=1.0,
                original_price=1.79,
                sale_price=1.29,
                source_url=f"{self.base_url}/bonus/magere-yoghurt",
            ),
            make_offer(
                product_name="Zalmfilet",
                category="vis",
                unit="g",
                amount=200,
                original_price=5.99,
                sale_price=3.99,
                discount_text="35% korting",
                source_url=f"{self.base_url}/bonus/zalmfilet",
            ),
            make_offer(
                product_name="Spinazie vers",
                category="groente",
                unit="g",
                amount=300,
                original_price=2.49,
                sale_price=1.49,
                source_url=f"{self.base_url}/bonus/spinazie",
            ),
            make_offer(
                product_name="Kikkererwten in blik",
                category="peulvrucht",
                unit="g",
                amount=400,
                original_price=1.19,
                sale_price=0.79,
                source_url=f"{self.base_url}/bonus/kikkererwten",
            ),
            make_offer(
                product_name="Volkoren wraps",
                category="brood",
                unit="stuk",
                amount=8,
                original_price=2.29,
                sale_price=1.49,
                source_url=f"{self.base_url}/bonus/wraps",
            ),
            make_offer(
                product_name="Avocado",
                category="fruit",
                unit="stuk",
                amount=2,
                original_price=2.99,
                sale_price=1.99,
                source_url=f"{self.base_url}/bonus/avocado",
            ),
        ]
