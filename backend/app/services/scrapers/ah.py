"""Albert Heijn scraper.

AH publiceert via `https://www.ah.nl/zoeken/api/products/search` een
gestructureerde JSON-feed van producten met bonus-info. We loopen over
meerdere taxonomy-ids (afdelingen) zodat we niet beperkt zijn tot 1
categorie. Bij falen vallen we terug op gegenereerde mock-data.
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


# AH afdelings-taxonomy ids — een breed assortiment.
AH_TAXONOMIES = [
    ("aardappel-groente-fruit", 6401),
    ("vlees-vis-vega", 19258),
    ("zuivel-eieren", 6404),
    ("kaas", 19259),
    ("brood-banket", 6402),
    ("ontbijt-broodbeleg", 6478),
    ("pasta-rijst-internationaal", 6446),
    ("diepvries", 6477),
    ("snoep-koek-chips", 6444),
    ("frisdrank-sappen", 6442),
]


def _parse_unit(unit_size: str | None) -> tuple[float | None, str | None]:
    if not unit_size:
        return None, None
    s = unit_size.strip().lower().replace(",", ".")
    for u in ("kg", "g", "ml", "l", "stuks", "stuk"):
        if s.endswith(u):
            num = s[: -len(u)].strip()
            try:
                return float(num), u.replace("stuks", "stuk")
            except ValueError:
                return None, u
    return None, None


def _map_ah_product(item: dict[str, Any], category: str) -> ScrapedOffer | None:
    try:
        name = item.get("title")
        if not name:
            return None
        price = item.get("price") or {}
        now = price.get("now")
        was = price.get("was")
        if now is None and price.get("amount") is not None:
            now = price.get("amount")
        if now is None:
            return None
        # Filter producten zonder echte bonus uit.
        discount_label = (item.get("shield") or {}).get("text") or item.get("priceLabel")
        is_bonus = bool(was and was > now) or bool(discount_label and "bonus" in str(discount_label).lower())
        if not is_bonus and not was:
            return None
        amount, unit = _parse_unit(item.get("unitSize") or item.get("salesUnitSize"))
        webshop_id = item.get("webshopId") or item.get("hqId") or ""
        source_url = f"https://www.ah.nl/producten/product/wi{webshop_id}" if webshop_id else "https://www.ah.nl/bonus"
        image_url = None
        images = item.get("images") or []
        if images and isinstance(images, list):
            image_url = images[0].get("url") if isinstance(images[0], dict) else None
        return ScrapedOffer(
            product_name=name,
            category=category,
            unit=unit,
            amount=amount,
            original_price=float(was) if was else None,
            sale_price=float(now),
            discount_text=str(discount_label) if discount_label else None,
            image_url=image_url,
            source_url=source_url,
            source="live_scraper",
        )
    except Exception as exc:  # noqa: BLE001
        logger.debug("AH map failed: %s", exc)
        return None


def _normalize_category(label: str) -> str:
    label = label.lower()
    if "groente" in label or "fruit" in label or "aardappel" in label:
        return "groente" if "groente" in label else "fruit"
    if "vlees" in label:
        return "vlees"
    if "vis" in label:
        return "vis"
    if "vega" in label:
        return "vleesvervanger"
    if "zuivel" in label or "eieren" in label:
        return "zuivel"
    if "kaas" in label:
        return "kaas"
    if "brood" in label or "banket" in label:
        return "brood"
    if "ontbijt" in label or "beleg" in label:
        return "ontbijt"
    if "pasta" in label or "rijst" in label:
        return "pasta"
    if "diepvries" in label:
        return "diepvries"
    if "snoep" in label or "chips" in label or "koek" in label:
        return "snack"
    if "frisdrank" in label or "sap" in label:
        return "drank"
    return "overig"


class AlbertHeijnScraper(BaseScraper):
    slug = "ah"
    name = "Albert Heijn"
    base_url = "https://www.ah.nl"

    async def fetch_live(self, client: httpx.AsyncClient) -> list[ScrapedOffer]:
        offers: list[ScrapedOffer] = []
        seen: set[str] = set()

        for taxonomy_label, taxonomy_id in AH_TAXONOMIES:
            try:
                url = f"{self.base_url}/zoeken/api/products/search"
                params = {
                    "taxonomySlug": taxonomy_label,
                    "taxonomyId": str(taxonomy_id),
                    "sortOn": "PRICELOW",
                    "page": 0,
                    "size": 36,
                    "properties": "bonus",
                }
                r = await client.get(url, params=params)
                r.raise_for_status()
                data = r.json()
                cards = (data.get("cards") or []) if isinstance(data, dict) else []
                cat = _normalize_category(taxonomy_label)
                for card in cards:
                    products = card.get("products") or []
                    for p in products:
                        offer = _map_ah_product(p, cat)
                        if offer and offer.product_name not in seen:
                            offers.append(offer)
                            seen.add(offer.product_name)
                # vriendelijke vertraging tussen calls
                await asyncio.sleep(0.4)
            except Exception as exc:  # noqa: BLE001
                logger.debug("AH categorie %s faalde: %s", taxonomy_label, exc)
                continue

        if not offers:
            raise RuntimeError("AH live: 0 bruikbare aanbiedingen")
        return offers

    def mock_offers(self) -> list[ScrapedOffer]:
        return generate_mock_offers(self.slug)
