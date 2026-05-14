from __future__ import annotations

from app.services.scrapers.base import BaseScraper
from app.services.scrapers.jumbo import JumboScraper
from app.services.scrapers.ah import AlbertHeijnScraper
from app.services.scrapers.lidl import LidlScraper
from app.services.scrapers.hoogvliet import HoogvlietScraper
from app.services.scrapers.aldi import AldiScraper
from app.services.scrapers.ekoplaza import EkoplazaScraper
from app.services.scrapers.plus import PlusScraper
from app.services.scrapers.dirk import DirkScraper
from app.services.scrapers.vomar import VomarScraper
from app.services.scrapers.coop import CoopScraper


_SCRAPER_CLASSES: list[type[BaseScraper]] = [
    JumboScraper,
    AlbertHeijnScraper,
    LidlScraper,
    HoogvlietScraper,
    AldiScraper,
    EkoplazaScraper,
    PlusScraper,
    DirkScraper,
    VomarScraper,
    CoopScraper,
]


def get_all_scrapers() -> list[BaseScraper]:
    return [cls() for cls in _SCRAPER_CLASSES]


def get_scraper(slug: str) -> BaseScraper | None:
    for cls in _SCRAPER_CLASSES:
        if cls.slug == slug:
            return cls()
    return None
