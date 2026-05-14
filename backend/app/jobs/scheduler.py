"""In-process scheduler voor lokaal ontwikkelen.

Op productie (Render) gebruiken we een aparte Cron Job; op de lokale
machine is het handig dat de FastAPI-app zelf periodiek refresht.
"""
from __future__ import annotations

import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.config import settings
from app.database import SessionLocal
from app.services.offer_service import refresh_all_offers

logger = logging.getLogger(__name__)

_scheduler: BackgroundScheduler | None = None


def _job() -> None:
    db = SessionLocal()
    try:
        results = refresh_all_offers(db)
        logger.info("Periodieke refresh klaar: %s", results)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Periodieke refresh mislukt: %s", exc)
    finally:
        db.close()


def start_scheduler() -> None:
    global _scheduler
    if _scheduler is not None:
        return
    _scheduler = BackgroundScheduler(daemon=True)
    _scheduler.add_job(
        _job,
        IntervalTrigger(hours=settings.SCRAPER_INTERVAL_HOURS),
        id="refresh_offers",
        replace_existing=True,
    )
    _scheduler.start()
    logger.info("Scheduler gestart (elke %s uur)", settings.SCRAPER_INTERVAL_HOURS)


def stop_scheduler() -> None:
    global _scheduler
    if _scheduler:
        _scheduler.shutdown(wait=False)
        _scheduler = None
