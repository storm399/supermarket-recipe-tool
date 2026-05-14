from __future__ import annotations

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.offer import Offer
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


@router.post("/recipes/generate", response_model=list[RecipeOut])
def generate_recipes(
    request: RecipeGenerateRequest,
    db: Session = Depends(get_db),
) -> list[RecipeOut]:
    offers = _load_offers(db)
    if not offers:
        raise HTTPException(
            status_code=400,
            detail="Geen aanbiedingen beschikbaar. Refresh eerst de aanbiedingen.",
        )

    if request.use_llm and llm_available():
        try:
            recipes = generate_recipes_llm(request, offers)
            if recipes:
                return recipes
            logger.info("LLM gaf 0 recepten terug, val terug op rule-based")
        except Exception as exc:  # noqa: BLE001
            logger.warning("LLM-generatie faalde, fallback: %s", exc)

    return generate_recipes_rule_based(request, offers)


@router.get("/recipes/health", response_model=dict)
def recipes_health() -> dict:
    return {
        "llm_available": llm_available(),
    }
