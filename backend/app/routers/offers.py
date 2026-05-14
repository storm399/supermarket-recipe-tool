from __future__ import annotations

import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.offer import Offer
from app.models.supermarket import Supermarket
from app.schemas.offer import OfferListResponse, OfferOut
from app.schemas.supermarket import SupermarketOut
from app.services.offer_service import refresh_all_offers, refresh_supermarket

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["offers"])


@router.get("/supermarkets", response_model=list[SupermarketOut])
def list_supermarkets(db: Session = Depends(get_db)) -> list[Supermarket]:
    return db.query(Supermarket).order_by(Supermarket.name).all()


@router.get("/offers", response_model=OfferListResponse)
def list_offers(
    supermarket: str | None = Query(None, description="Slug van supermarkt"),
    category: str | None = Query(None),
    q: str | None = Query(None, description="Zoekterm in productnaam"),
    max_price: float | None = Query(None, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
) -> OfferListResponse:
    query = db.query(Offer).options(joinedload(Offer.supermarket))
    if supermarket:
        query = query.join(Supermarket).filter(Supermarket.slug == supermarket)
    if category:
        query = query.filter(Offer.category == category)
    if q:
        query = query.filter(Offer.product_name.ilike(f"%{q}%"))
    if max_price is not None:
        query = query.filter(Offer.sale_price <= max_price)
    total = query.count()
    rows = (
        query.order_by(Offer.sale_price.asc()).offset(offset).limit(limit).all()
    )
    return OfferListResponse(total=total, offers=[OfferOut.model_validate(o) for o in rows])


@router.get("/offers/categories", response_model=list[str])
def list_categories(db: Session = Depends(get_db)) -> list[str]:
    rows = db.query(Offer.category).distinct().all()
    return sorted({r[0] for r in rows if r[0]})


@router.post("/offers/refresh", response_model=dict)
def trigger_refresh(
    supermarket: str | None = Query(None, description="Specifieke supermarkt-slug (optioneel)"),
    db: Session = Depends(get_db),
) -> dict:
    try:
        if supermarket:
            count = refresh_supermarket(db, supermarket)
            return {"ok": True, "supermarket": supermarket, "count": count}
        results = refresh_all_offers(db)
        return {"ok": True, "results": results, "total": sum(results.values())}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        logger.exception("Refresh mislukt: %s", exc)
        raise HTTPException(status_code=500, detail="Refresh mislukt") from exc
