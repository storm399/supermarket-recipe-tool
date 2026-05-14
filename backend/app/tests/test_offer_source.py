import asyncio

from app.services.scrapers import get_all_scrapers


def test_mock_offers_default_source_is_fallback_mock():
    for scraper in get_all_scrapers():
        for o in scraper.mock_offers():
            assert o.source == "fallback_mock", (
                f"{scraper.slug} levert offer met onverwachte source {o.source}"
            )


def test_fetch_offers_marks_offers_with_correct_source():
    # In test-modus geldt USE_MOCK_SCRAPERS=true, dus we verwachten fallback_mock
    for scraper in get_all_scrapers():
        stats = asyncio.run(scraper.fetch_offers())
        assert stats.ok
        assert stats.source in {"fallback_mock", "live_scraper"}
        for o in stats.raw_offers:
            assert o.source == stats.source


def test_dedupe_keeps_unique_offers():
    from app.schemas.offer import ScrapedOffer
    from app.services.scrapers.base import BaseScraper

    raw = [
        ScrapedOffer(product_name="Kip", sale_price=4.99),
        ScrapedOffer(product_name="Kip", sale_price=4.99),  # duplicate
        ScrapedOffer(product_name="Kip", sale_price=5.99),  # andere prijs => uniek
        ScrapedOffer(product_name="Brood", sale_price=2.00),
    ]
    unique, dups = BaseScraper._dedupe(raw)
    assert len(unique) == 3
    assert dups == 1


def test_each_scraper_has_50plus_offers_in_stats():
    for scraper in get_all_scrapers():
        stats = asyncio.run(scraper.fetch_offers())
        assert stats.fetched >= 50, f"{scraper.slug} levert maar {stats.fetched}"
