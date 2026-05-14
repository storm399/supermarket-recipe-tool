"""Service voor het ophalen, normaliseren en opslaan van aanbiedingen."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Iterable

from sqlalchemy.orm import Session

from app.models.offer import Offer
from app.models.supermarket import Supermarket
from app.schemas.offer import ScrapedOffer
from app.services.scrapers import SUPERMARKETS, get_all_scrapers

logger = logging.getLogger(__name__)


def ensure_supermarkets(db: Session) -> None:
    """Zorg dat alle supermarkten als rij in de DB bestaan."""
    existing = {sm.slug for sm in db.query(Supermarket).all()}
    for sm in SUPERMARKETS:
        if sm.slug in existing:
            continue
        db.add(Supermarket(slug=sm.slug, name=sm.name, base_url=sm.base_url, active=True))
    db.commit()


def _save_offers_for_supermarket(
    db: Session, supermarket: Supermarket, scraped: Iterable[ScrapedOffer]
) -> int:
    # Eenvoudige strategie voor MVP: gooi oude aanbiedingen van deze
    # supermarkt weg en voeg de verse set toe.
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
            fetched_at=now,
        )
        db.add(offer)
        count += 1
    db.commit()
    return count


def refresh_all_offers(db: Session) -> dict[str, int]:
    """Run alle scrapers en sla de resultaten op."""
    ensure_supermarkets(db)
    supermarkets = {sm.slug: sm for sm in db.query(Supermarket).all()}
    results: dict[str, int] = {}
    for scraper in get_all_scrapers():
        sm = supermarkets.get(scraper.slug)
        if not sm:
            logger.warning("Geen DB-rij voor %s, sla over", scraper.slug)
            continue
        try:
            scraped = scraper.scrape()
            n = _save_offers_for_supermarket(db, sm, scraped)
            results[scraper.slug] = n
        except Exception as exc:  # noqa: BLE001
            logger.exception("Refresh voor %s gefaald: %s", scraper.slug, exc)
            results[scraper.slug] = 0
    return results


def refresh_supermarket(db: Session, slug: str) -> int:
    ensure_supermarkets(db)
    sm = db.query(Supermarket).filter(Supermarket.slug == slug).one_or_none()
    if not sm:
        raise ValueError(f"Onbekende supermarkt: {slug}")
    from app.services.scrapers import get_scraper

    scraper = get_scraper(slug)
    if not scraper:
        raise ValueError(f"Geen scraper voor: {slug}")
    scraped = scraper.scrape()
    return _save_offers_for_supermarket(db, sm, scraped)
