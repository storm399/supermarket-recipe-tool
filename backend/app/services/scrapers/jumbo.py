from app.schemas.offer import ScrapedOffer
from app.services.scrapers.base import BaseScraper, make_offer


class JumboScraper(BaseScraper):
    slug = "jumbo"
    name = "Jumbo"
    base_url = "https://www.jumbo.com"

    def fetch_live(self) -> list[ScrapedOffer]:
        # Plaats hier de echte implementatie. Een Jumbo Promotions API of
        # de publieke folderpagina kan als bron dienen. Houd rekening met
        # robots.txt en gebruik httpx met self.user_agent en self.timeout.
        raise NotImplementedError("Live Jumbo scraper nog niet geimplementeerd")

    def mock_offers(self) -> list[ScrapedOffer]:
        return [
            make_offer(
                product_name="Kipfilet naturel",
                category="vlees",
                unit="kg",
                amount=1.0,
                original_price=10.49,
                sale_price=6.99,
                discount_text="1+1 gratis",
                source_url=f"{self.base_url}/aanbiedingen/kipfilet",
            ),
            make_offer(
                product_name="Broccoli",
                category="groente",
                unit="stuk",
                amount=1.0,
                original_price=1.49,
                sale_price=0.99,
                source_url=f"{self.base_url}/aanbiedingen/broccoli",
            ),
            make_offer(
                product_name="Volkoren pasta",
                category="pasta",
                unit="g",
                amount=500,
                original_price=1.79,
                sale_price=1.19,
                source_url=f"{self.base_url}/aanbiedingen/volkoren-pasta",
            ),
            make_offer(
                product_name="Cherrytomaten",
                category="groente",
                unit="g",
                amount=250,
                original_price=2.29,
                sale_price=1.49,
                source_url=f"{self.base_url}/aanbiedingen/cherrytomaten",
            ),
            make_offer(
                product_name="Olijfolie extra vergine",
                category="olie",
                unit="ml",
                amount=500,
                original_price=6.99,
                sale_price=4.99,
                source_url=f"{self.base_url}/aanbiedingen/olijfolie",
            ),
        ]
