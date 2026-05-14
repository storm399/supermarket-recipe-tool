"""Match aanbiedingen aan ingredient-keywords.

Houdt de matchlogica eenvoudig en transparant: normaliseer naam,
zoek case-insensitive op keywords. Geef bij meerdere matches de
goedkoopste (per eenheid) terug.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from app.models.offer import Offer


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


@dataclass
class MatchedOffer:
    offer: Offer
    score: float


def match_offers(
    keywords: Iterable[str],
    offers: Iterable[Offer],
    *,
    exclude_names: Iterable[str] = (),
    favorite_supermarkets: Iterable[str] = (),
) -> list[MatchedOffer]:
    """Vind aanbiedingen die op een van de keywords matchen.

    Score is hoger naarmate:
      - meer keywords matchen
      - de prijs lager is
      - de aanbieding van een favoriete supermarkt komt
    """
    norm_keywords = [normalize(k) for k in keywords if k]
    excludes = {normalize(e) for e in exclude_names if e}
    favorites = {f.lower() for f in favorite_supermarkets if f}

    matched: list[MatchedOffer] = []
    for offer in offers:
        norm_name = normalize(offer.product_name)
        if any(excl and excl in norm_name for excl in excludes):
            continue
        hits = sum(1 for kw in norm_keywords if kw and kw in norm_name)
        if hits == 0:
            continue
        score = hits * 10.0
        score += max(0.0, 5.0 - offer.sale_price)
        if offer.discount_percent:
            score += offer.discount_percent / 20.0
        if favorites and offer.supermarket and offer.supermarket.slug.lower() in favorites:
            score += 5.0
        matched.append(MatchedOffer(offer=offer, score=score))

    matched.sort(key=lambda m: m.score, reverse=True)
    return matched


def best_offer_for(
    keywords: Iterable[str],
    offers: Iterable[Offer],
    *,
    exclude_names: Iterable[str] = (),
    favorite_supermarkets: Iterable[str] = (),
) -> Offer | None:
    matches = match_offers(
        keywords,
        offers,
        exclude_names=exclude_names,
        favorite_supermarkets=favorite_supermarkets,
    )
    return matches[0].offer if matches else None
