import asyncio

from app.services.scrapers import get_all_scrapers, get_scraper
from app.services.scrapers.base import SUPERMARKETS


def test_all_required_supermarkets_present():
    slugs = {sm.slug for sm in SUPERMARKETS}
    expected = {
        "jumbo", "ah", "lidl", "hoogvliet", "aldi",
        "ekoplaza", "plus", "dirk", "vomar", "coop",
    }
    assert expected.issubset(slugs)


def test_each_scraper_produces_50plus_mock_offers():
    for scraper in get_all_scrapers():
        offers = scraper.mock_offers()
        assert len(offers) >= 50, f"{scraper.slug} levert maar {len(offers)} mocks"
        for o in offers:
            assert o.product_name
            assert o.sale_price > 0
            assert o.source == "fallback_mock"
            if o.original_price:
                assert o.original_price >= o.sale_price


def test_get_scraper_by_slug():
    scraper = get_scraper("jumbo")
    assert scraper is not None
    assert scraper.slug == "jumbo"
    assert get_scraper("bestaat-niet") is None


def test_fetch_offers_returns_stats_with_source():
    scraper = get_scraper("ah")
    assert scraper is not None
    stats = asyncio.run(scraper.fetch_offers())
    assert stats.ok
    assert stats.source in {"fallback_mock", "live_scraper", "public_api"}
    assert stats.fetched > 0
    assert len(stats.raw_offers) > 0
    for o in stats.raw_offers:
        assert o.source == stats.source
