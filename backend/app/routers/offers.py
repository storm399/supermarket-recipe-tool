from __future__ import annotations

import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.config import settings
from app.database import get_db
from app.models.offer import Offer
from app.models.supermarket import Supermarket
from app.schemas.offer import OfferListResponse, OfferOut, RefreshResponse
from app.schemas.recipe import OfferStats
from app.schemas.supermarket import SupermarketOut
from app.services.offer_service import (
    refresh_all_offers_async,
    refresh_supermarket_async,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["offers"])


def _apply_offer_filters(
    query, *,
    supermarkets, supermarket, category, q,
    max_price, min_discount, has_image, source,
):
    if supermarkets:
        slugs = [s.strip() for s in supermarkets.split(",") if s.strip()]
        query = query.join(Supermarket).filter(Supermarket.slug.in_(slugs))
    elif supermarket:
        query = query.join(Supermarket).filter(Supermarket.slug == supermarket)
    if category:
        query = query.filter(Offer.category == category)
    if q:
        query = query.filter(Offer.product_name.ilike(f"%{q}%"))
    if max_price is not None:
        query = query.filter(Offer.sale_price <= max_price)
    if min_discount is not None:
        query = query.filter(Offer.discount_percent >= min_discount)
    if has_image:
        query = query.filter(Offer.image_url.isnot(None))
    if source:
        query = query.filter(Offer.source == source)
    return query


@router.get("/supermarkets", response_model=list[SupermarketOut])
def list_supermarkets(db: Session = Depends(get_db)) -> list[Supermarket]:
    return db.query(Supermarket).order_by(Supermarket.name).all()


@router.get("/offers", response_model=OfferListResponse)
def list_offers(
    supermarket: str | None = Query(None),
    supermarkets: str | None = Query(None),
    category: str | None = Query(None),
    q: str | None = Query(None),
    max_price: float | None = Query(None, ge=0),
    min_discount: float | None = Query(None, ge=0, le=100),
    has_image: bool = Query(False),
    source: str | None = Query(None),
    sort: str = Query("price-asc", description="price-asc|price-desc|discount-desc|name-asc"),
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
) -> OfferListResponse:
    query = db.query(Offer).options(joinedload(Offer.supermarket))
    query = _apply_offer_filters(
        query,
        supermarkets=supermarkets, supermarket=supermarket, category=category, q=q,
        max_price=max_price, min_discount=min_discount, has_image=has_image, source=source,
    )
    total = query.count()
    if sort == "price-desc":
        query = query.order_by(Offer.sale_price.desc())
    elif sort == "discount-desc":
        query = query.order_by(Offer.discount_percent.desc().nullslast(), Offer.sale_price.asc())
    elif sort == "name-asc":
        query = query.order_by(Offer.product_name.asc())
    else:
        query = query.order_by(Offer.sale_price.asc())
    rows = query.offset(offset).limit(limit).all()
    return OfferListResponse(total=total, offers=[OfferOut.model_validate(o) for o in rows])


@router.get("/offers/stats", response_model=OfferStats)
def offer_stats(
    supermarket: str | None = Query(None),
    supermarkets: str | None = Query(None),
    category: str | None = Query(None),
    q: str | None = Query(None),
    max_price: float | None = Query(None, ge=0),
    min_discount: float | None = Query(None, ge=0, le=100),
    has_image: bool = Query(False),
    source: str | None = Query(None),
    db: Session = Depends(get_db),
) -> OfferStats:
    base = db.query(Offer)
    base = _apply_offer_filters(
        base,
        supermarkets=supermarkets, supermarket=supermarket, category=category, q=q,
        max_price=max_price, min_discount=min_discount, has_image=has_image, source=source,
    )
    total = base.count()

    by_sm_rows = (
        db.query(Supermarket.slug, func.count(Offer.id))
        .join(Offer, Offer.supermarket_id == Supermarket.id)
        .group_by(Supermarket.slug)
        .all()
    )
    by_supermarket = {slug: cnt for slug, cnt in by_sm_rows}

    by_cat_rows = (
        db.query(Offer.category, func.count(Offer.id))
        .group_by(Offer.category)
        .all()
    )
    by_category = {(cat or "overig"): cnt for cat, cnt in by_cat_rows}

    avg_discount = db.query(func.avg(Offer.discount_percent)).scalar()
    avg_discount = round(avg_discount, 1) if avg_discount is not None else None

    # Bepaal de dominante bron op basis van werkelijke data, niet alleen
    # de config-vlag.
    src_rows = db.query(Offer.source, func.count(Offer.id)).group_by(Offer.source).all()
    if src_rows:
        sources = sorted(src_rows, key=lambda r: r[1], reverse=True)
        if any(s == "live_scraper" for s, _ in src_rows):
            primary_source = "live"
        elif sources[0][0] == "public_api":
            primary_source = "live"
        else:
            primary_source = "mock"
    else:
        primary_source = "mock" if settings.USE_MOCK_SCRAPERS else "live"

    return OfferStats(
        total=total,
        by_supermarket=by_supermarket,
        by_category=by_category,
        average_discount_percent=avg_discount,
        source=primary_source,
    )


@router.get("/offers/categories", response_model=list[str])
def list_categories(db: Session = Depends(get_db)) -> list[str]:
    rows = db.query(Offer.category).distinct().all()
    return sorted({r[0] for r in rows if r[0]})


@router.post("/offers/refresh", response_model=RefreshResponse)
async def trigger_refresh(
    supermarket: str | None = Query(None, description="Specifieke supermarkt-slug (optioneel)"),
    db: Session = Depends(get_db),
) -> RefreshResponse:
    try:
        if supermarket:
            result = await refresh_supermarket_async(db, supermarket)
            return RefreshResponse(
                ok=result.ok,
                total=result.saved,
                results=[result],
            )
        results = await refresh_all_offers_async(db)
        total = sum(r.saved for r in results)
        return RefreshResponse(
            ok=any(r.ok for r in results),
            total=total,
            results=results,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        logger.exception("Refresh mislukt: %s", exc)
        raise HTTPException(status_code=500, detail="Refresh mislukt") from exc
