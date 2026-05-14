"""Jumbo scraper.

Jumbo heeft een (publieke) search API met promo-filter. We querieen
meerdere afdelingen om een breed assortiment te krijgen.
"""
from __future__ import annotations

import asyncio
import logging
from typing import Any

import httpx

from app.schemas.offer import ScrapedOffer
from app.services.scrapers.base import BaseScraper
from app.services.scrapers.mock_data import generate_mock_offers

logger = logging.getLogger(__name__)


JUMBO_CATEGORIES = [
    ("aardappelen-groenten-fruit", "groente"),
    ("vlees-vis-vegetarisch", "vlees"),
    ("zuivel-eieren-koffie-thee", "zuivel"),
    ("kaas-vleeswaren-tapas", "kaas"),
    ("brood-bakkerij", "brood"),
    ("ontbijt-broodbeleg", "ontbijt"),
    ("pasta-rijst-saus-olie", "pasta"),
    ("diepvries", "diepvries"),
    ("frisdrank-sap-water-koffie-thee", "drank"),
]


def _parse_size(raw: str | None) -> tuple[float | None, str | None]:
    if not raw:
        return None, None
    s = str(raw).lower().replace(",", ".").strip()
    for u in ("kg", "g", "ml", "l", "stuks", "stuk"):
        if s.endswith(u):
            try:
                return float(s[: -len(u)].strip()), u.replace("stuks", "stuk")
            except ValueError:
                return None, u
    return None, None


def _map_jumbo(item: dict[str, Any], category: str) -> ScrapedOffer | None:
    try:
        name = item.get("title")
        prices = item.get("prices") or {}
        price = prices.get("price")
        promo = item.get("promotion") or {}
        promo_price = (promo.get("offerPrice") or {}).get("amount")
        if isinstance(price, dict):
            price = price.get("amount")
        if not name or price is None:
            return None
        # Alleen items met geldige promo houden we.
        if not promo_price and not promo:
            return None
        amount, unit = _parse_size(item.get("quantity") or item.get("size"))
        image_url = None
        imgs = item.get("imageInfo") or item.get("image")
        if isinstance(imgs, dict):
            image_url = imgs.get("primaryView", [{}])[0].get("url") if "primaryView" in imgs else imgs.get("url")
        product_url = item.get("link") or f"https://www.jumbo.com/aanbieding/{item.get('id', '')}"
        sale = float(promo_price if promo_price is not None else price)
        original = float(price) if promo_price is not None else None
        return ScrapedOffer(
            product_name=name,
            category=category,
            unit=unit,
            amount=amount,
            original_price=original,
            sale_price=sale,
            discount_text=(promo.get("tags") or [None])[0] if isinstance(promo.get("tags"), list) else None,
            image_url=image_url,
            source_url=product_url,
            source="live_scraper",
        )
    except Exception as exc:  # noqa: BLE001
        logger.debug("Jumbo map failed: %s", exc)
        return None


class JumboScraper(BaseScraper):
    slug = "jumbo"
    name = "Jumbo"
    base_url = "https://www.jumbo.com"

    async def fetch_live(self, client: httpx.AsyncClient) -> list[ScrapedOffer]:
        offers: list[ScrapedOffer] = []
        seen: set[str] = set()
        for cat_slug, cat_name in JUMBO_CATEGORIES:
            try:
                url = f"{self.base_url}/api/v17/search"
                params = {
                    "facets": f"category:{cat_slug}",
                    "filters": "promotion:Aanbiedingen",
                    "offSet": 0,
                    "pageSize": 36,
                }
                r = await client.get(url, params=params)
                r.raise_for_status()
                data = r.json()
                products = (
                    data.get("products", {}).get("data", [])
                    if isinstance(data, dict) else []
                )
                for p in products:
                    offer = _map_jumbo(p, cat_name)
                    if offer and offer.product_name not in seen:
                        offers.append(offer)
                        seen.add(offer.product_name)
                await asyncio.sleep(0.4)
            except Exception as exc:  # noqa: BLE001
                logger.debug("Jumbo cat %s faalde: %s", cat_slug, exc)
                continue
        if not offers:
            raise RuntimeError("Jumbo live: 0 bruikbare aanbiedingen")
        return offers

    def mock_offers(self) -> list[ScrapedOffer]:
        return generate_mock_offers(self.slug)
