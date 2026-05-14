from app.services.scrapers import get_all_scrapers, get_scraper
from app.services.scrapers.base import SUPERMARKETS


def test_all_required_supermarkets_present():
    slugs = {sm.slug for sm in SUPERMARKETS}
    expected = {
        "jumbo", "ah", "lidl", "hoogvliet", "aldi",
        "ekoplaza", "plus", "dirk", "vomar", "coop",
    }
    assert expected.issubset(slugs)


def test_each_scraper_produces_mock_offers():
    for scraper in get_all_scrapers():
        offers = scraper.mock_offers()
        assert len(offers) > 0, f"{scraper.slug} produces 0 mock offers"
        for o in offers:
            assert o.product_name
            assert o.sale_price > 0
            if o.original_price:
                assert o.original_price >= o.sale_price


def test_get_scraper_by_slug():
    scraper = get_scraper("jumbo")
    assert scraper is not None
    assert scraper.slug == "jumbo"
    assert get_scraper("bestaat-niet") is None


def test_scrape_returns_offers():
    scraper = get_scraper("ah")
    assert scraper is not None
    offers = scraper.scrape()
    assert len(offers) > 0
