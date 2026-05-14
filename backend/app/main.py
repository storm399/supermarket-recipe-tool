from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import SessionLocal, init_db
from app.jobs.scheduler import start_scheduler, stop_scheduler
from app.routers import offers as offers_router
from app.routers import recipes as recipes_router
from app.services.offer_service import ensure_supermarkets, refresh_all_offers

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def _seed_if_empty() -> None:
    from app.models.offer import Offer

    db = SessionLocal()
    try:
        ensure_supermarkets(db)
        if db.query(Offer).count() == 0:
            logger.info("Geen aanbiedingen gevonden, seeden met mock-data...")
            results = refresh_all_offers(db)
            logger.info("Seed klaar: %s", results)
    finally:
        db.close()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    _seed_if_empty()
    if settings.APP_ENV != "test":
        start_scheduler()
    try:
        yield
    finally:
        stop_scheduler()


app = FastAPI(title=settings.APP_NAME, version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_origin_regex=settings.CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(offers_router.router)
app.include_router(recipes_router.router)


@app.get("/")
def root() -> dict:
    return {
        "app": settings.APP_NAME,
        "status": "ok",
        "docs": "/docs",
    }


@app.get("/healthz")
def healthz() -> dict:
    return {"ok": True}
