"""Cron-job script om dagelijks aanbiedingen op te halen.

Gebruik op Render als Cron Job:
    cd backend && python -m app.jobs.fetch_offers
"""
from __future__ import annotations

import logging
import sys

from app.database import SessionLocal, init_db
from app.services.offer_service import refresh_all_offers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("fetch_offers")


def main() -> int:
    init_db()
    db = SessionLocal()
    try:
        results = refresh_all_offers(db)
        total = sum(r.saved for r in results)
        logger.info(
            "Klaar. %d aanbiedingen opgeslagen. Per supermarkt: %s",
            total,
            {r.supermarket: f"{r.saved}({r.source})" for r in results},
        )
        for r in results:
            if not r.ok:
                logger.warning("FAIL %s: %s", r.supermarket, r.error)
        return 0
    except Exception:  # noqa: BLE001
        logger.exception("Fetch job mislukt")
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
