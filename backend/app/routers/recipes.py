from __future__ import annotations

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.offer import Offer
from app.models.supermarket import Supermarket
from app.schemas.recipe import RecipeGenerateRequest, RecipeOut
from app.services.ai_service import generate_recipes_llm, llm_available
from app.services.recipe_generator import generate_recipes_rule_based

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["recipes"])


def _load_offers(db: Session) -> list[Offer]:
    return (
        db.query(Offer)
        .options(joinedload(Offer.supermarket))
        .all()
    )


def _validate_selected_supermarkets(db: Session, slugs: list[str]) -> None:
    if not slugs:
        return
    existing = {
        s.slug for s in db.query(Supermarket).filter(Supermarket.slug.in_(slugs)).all()
    }
    unknown = [s for s in slugs if s not in existing]
    if unknown:
        raise HTTPException(
            status_code=400,
            detail=f"Onbekende supermarkt-slug(s): {', '.join(unknown)}",
        )


def _enforce_strict_supermarket_filter(
    recipes: list[RecipeOut], allowed: set[str], allow_multi: bool
) -> list[RecipeOut]:
    if not allowed and allow_multi:
        return recipes
    safe: list[RecipeOut] = []
    for r in recipes:
        used = {sm.slug for sm in r.supermarkets_used}
        if allowed and not used.issubset(allowed):
            logger.warning(
                "recept '%s' bevat supermarkt(en) buiten selectie %s: %s",
                r.title, allowed, used,
            )
            continue
        if not allow_multi and len(used) > 1:
            logger.warning(
                "recept '%s' gebruikt meerdere supermarkten terwijl allow_multi=False",
                r.title,
            )
            continue
        safe.append(r)
    return safe


@router.post("/recipes/generate", response_model=list[RecipeOut])
def generate_recipes(
    request: RecipeGenerateRequest,
    db: Session = Depends(get_db),
) -> list[RecipeOut]:
    _validate_selected_supermarkets(db, request.selected_supermarkets)
    offers = _load_offers(db)
    if not offers:
        raise HTTPException(
            status_code=400,
            detail="Geen aanbiedingen beschikbaar. Refresh eerst de aanbiedingen.",
        )

    allowed = {s.lower() for s in request.selected_supermarkets if s}
    if allowed:
        relevant = [o for o in offers if o.supermarket and o.supermarket.slug in allowed]
        if len(relevant) < 4:
            raise HTTPException(
                status_code=422,
                detail=(
                    "Er zijn te weinig passende aanbiedingen bij deze supermarkt. "
                    "Probeer een extra supermarkt of ruimere filters."
                ),
            )

    recipes: list[RecipeOut] = []
    if request.use_llm and llm_available():
        try:
            recipes = generate_recipes_llm(request, offers)
        except Exception as exc:  # noqa: BLE001
            logger.warning("LLM-generatie faalde, fallback: %s", exc)
            recipes = []

    if not recipes:
        recipes = generate_recipes_rule_based(request, offers)

    safe = _enforce_strict_supermarket_filter(recipes, allowed, request.allow_multi_supermarket)
    if not safe:
        raise HTTPException(
            status_code=422,
            detail=(
                "Er zijn te weinig passende aanbiedingen bij deze supermarkt. "
                "Probeer een extra supermarkt of ruimere filters."
            ),
        )
    return safe[: request.count]


@router.get("/recipes/health", response_model=dict)
def recipes_health() -> dict:
    return {
        "llm_available": llm_available(),
    }
