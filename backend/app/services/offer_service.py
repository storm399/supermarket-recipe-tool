"""Service voor het ophalen, normaliseren en opslaan van aanbiedingen."""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Iterable

from sqlalchemy.orm import Session

from app.models.offer import Offer
from app.models.supermarket import Supermarket
from app.schemas.offer import ScrapeResult, ScrapedOffer
from app.services.scrapers import SUPERMARKETS, get_all_scrapers, get_scraper
from app.services.scrapers.base import BaseScraper, ScrapeStats

logger = logging.getLogger(__name__)


def ensure_supermarkets(db: Session) -> None:
    existing = {sm.slug for sm in db.query(Supermarket).all()}
    for sm in SUPERMARKETS:
        if sm.slug in existing:
            continue
        db.add(Supermarket(slug=sm.slug, name=sm.name, base_url=sm.base_url, active=True))
    db.commit()


def _save_offers_for_supermarket(
    db: Session, supermarket: Supermarket, scraped: Iterable[ScrapedOffer]
) -> int:
    db.query(Offer).filter(Offer.supermarket_id == supermarket.id).delete()
    db.flush()

    count = 0
    now = datetime.utcnow()
    for s in scraped:
        offer = Offer(
            supermarket_id=supermarket.id,
            product_name=s.product_name,
            category=s.category,
            unit=s.unit,
            amount=s.amount,
            original_price=s.original_price,
            sale_price=s.sale_price,
            discount_percent=s.discount_percent,
            discount_text=s.discount_text,
            valid_from=s.valid_from,
            valid_until=s.valid_until,
            image_url=s.image_url,
            source_url=s.source_url,
            description=s.description,
            source=s.source,
            fetched_at=now,
        )
        db.add(offer)
        count += 1
    db.commit()
    return count


async def _run_scraper(scraper: BaseScraper) -> ScrapeStats:
    try:
        return await scraper.fetch_offers()
    except Exception as exc:  # noqa: BLE001
        logger.exception("[%s] onverwachte scraper-fout: %s", scraper.slug, exc)
        stats = ScrapeStats()
        stats.ok = False
        stats.error = str(exc)
        return stats


def _stats_to_result(scraper: BaseScraper, stats: ScrapeStats, saved: int) -> ScrapeResult:
    return ScrapeResult(
        supermarket=scraper.slug,
        source=stats.source,
        fetched=stats.fetched,
        saved=saved,
        duplicates_skipped=stats.duplicates_skipped,
        ok=stats.ok and saved >= 0,
        error=stats.error,
        duration_ms=stats.duration_ms,
    )


async def refresh_all_offers_async(db: Session) -> list[ScrapeResult]:
    """Async variant: alle scrapers parallel."""
    ensure_supermarkets(db)
    supermarkets = {sm.slug: sm for sm in db.query(Supermarket).all()}
    scrapers = get_all_scrapers()

    stats_list = await asyncio.gather(*[_run_scraper(s) for s in scrapers])

    out: list[ScrapeResult] = []
    for scraper, stats in zip(scrapers, stats_list):
        sm = supermarkets.get(scraper.slug)
        if not sm:
            out.append(_stats_to_result(scraper, stats, 0))
            continue
        try:
            saved = _save_offers_for_supermarket(db, sm, stats.raw_offers)
        except Exception as exc:  # noqa: BLE001
            logger.exception("[%s] opslag mislukt: %s", scraper.slug, exc)
            stats.ok = False
            stats.error = (stats.error or "") + f"; opslag: {exc}"
            saved = 0
        out.append(_stats_to_result(scraper, stats, saved))
        logger.info(
            "[%s] klaar: bron=%s fetched=%d saved=%d dups=%d ok=%s",
            scraper.slug, stats.source, stats.fetched, saved,
            stats.duplicates_skipped, stats.ok,
        )
    return out


async def refresh_supermarket_async(db: Session, slug: str) -> ScrapeResult:
    ensure_supermarkets(db)
    sm = db.query(Supermarket).filter(Supermarket.slug == slug).one_or_none()
    if not sm:
        raise ValueError(f"Onbekende supermarkt: {slug}")
    scraper = get_scraper(slug)
    if not scraper:
        raise ValueError(f"Geen scraper voor: {slug}")

    stats = await _run_scraper(scraper)
    try:
        saved = _save_offers_for_supermarket(db, sm, stats.raw_offers)
    except Exception as exc:  # noqa: BLE001
        stats.ok = False
        stats.error = (stats.error or "") + f"; opslag: {exc}"
        saved = 0
    return _stats_to_result(scraper, stats, saved)


def _run_async(coro):
    """Run een coroutine vanuit synchrone context, óók als er al een
    event loop draait (FastAPI/uvloop) — dan draait de coroutine in een
    aparte thread met eigen loop."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = None
    if loop and loop.is_running():
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as pool:
            return pool.submit(lambda: asyncio.run(coro)).result()
    return asyncio.run(coro)


def refresh_all_offers(db: Session) -> list[ScrapeResult]:
    """Sync wrapper voor gebruik vanuit scripts en sync endpoints."""
    return _run_async(refresh_all_offers_async(db))


def refresh_supermarket(db: Session, slug: str) -> ScrapeResult:
    return _run_async(refresh_supermarket_async(db, slug))
