"""Centrale productenpool en generator voor mock-aanbiedingen.

Doel: zorg dat elke supermarkt 30+ realistische, gevarieerde
aanbiedingen heeft uit alle relevante categorieen (groente, fruit,
vlees, vis, zuivel, brood, ontbijt, pasta/rijst, peulvruchten, snacks,
dranken, biologisch). Elke supermarkt krijgt zijn eigen prijsbias zodat
prijsverschillen ontstaan en filters zichtbaar effect hebben.
"""
from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass

from app.schemas.offer import ScrapedOffer
from app.services.scrapers.base import make_offer


@dataclass(frozen=True)
class Product:
    name: str
    category: str
    unit: str
    amount: float
    base_price: float
    image_keyword: str  # gebruikt voor placeholder image lookup
    tags: tuple[str, ...] = ()


# ~80 producten verdeeld over 12 categorieen
PRODUCT_POOL: list[Product] = [
    # --- groente ---
    Product("Broccoli", "groente", "stuk", 1, 1.49, "broccoli"),
    Product("Bloemkool", "groente", "stuk", 1, 2.49, "bloemkool"),
    Product("Spinazie vers", "groente", "g", 300, 2.49, "spinazie"),
    Product("Cherrytomaten", "groente", "g", 250, 2.29, "tomaat"),
    Product("Roma tomaten", "groente", "kg", 1.0, 2.99, "tomaat"),
    Product("Paprika mix", "groente", "g", 500, 2.79, "paprika"),
    Product("Rode paprika", "groente", "stuk", 1, 1.19, "paprika"),
    Product("Komkommer", "groente", "stuk", 1, 0.99, "komkommer"),
    Product("IJsbergsla", "groente", "stuk", 1, 1.49, "sla"),
    Product("Veldsla", "groente", "g", 150, 1.99, "sla"),
    Product("Champignons", "groente", "g", 250, 1.59, "champignons"),
    Product("Courgette", "groente", "stuk", 1, 1.29, "courgette"),
    Product("Wortelen", "groente", "kg", 1.0, 1.69, "wortel"),
    Product("Ui", "groente", "kg", 1.0, 1.29, "ui"),
    Product("Rode ui", "groente", "kg", 1.0, 1.79, "ui"),
    Product("Knoflook", "groente", "stuk", 3, 1.49, "knoflook"),
    Product("Aubergine", "groente", "stuk", 1, 1.69, "aubergine"),
    Product("Prei", "groente", "stuk", 2, 1.79, "prei"),
    Product("Roergebakgroente", "groente", "g", 400, 2.29, "roerbak"),
    Product("Spruitjes", "groente", "g", 500, 2.49, "spruit"),
    # --- fruit ---
    Product("Bananen", "fruit", "kg", 1.0, 1.79, "banaan"),
    Product("Appels Jonagold", "fruit", "kg", 1.0, 1.99, "appel"),
    Product("Appels Elstar", "fruit", "kg", 1.0, 1.99, "appel"),
    Product("Aardbeien", "fruit", "g", 400, 3.99, "aardbei"),
    Product("Blauwe bessen", "fruit", "g", 125, 2.49, "bes"),
    Product("Avocado", "fruit", "stuk", 2, 2.99, "avocado"),
    Product("Mandarijnen", "fruit", "kg", 1.0, 2.49, "mandarijn"),
    Product("Sinaasappels", "fruit", "kg", 1.0, 2.29, "sinaasappel"),
    Product("Mango", "fruit", "stuk", 1, 1.99, "mango"),
    Product("Druiven", "fruit", "g", 500, 3.49, "druif"),
    # --- vlees ---
    Product("Kipfilet naturel", "vlees", "kg", 1.0, 10.49, "kip"),
    Product("Kipgehakt", "vlees", "g", 500, 4.99, "kip"),
    Product("Rundergehakt", "vlees", "g", 500, 4.49, "gehakt"),
    Product("Runderlapjes", "vlees", "g", 500, 6.99, "rundvlees"),
    Product("Varkenshaas", "vlees", "g", 500, 7.99, "varken"),
    Product("Speklapjes", "vlees", "g", 500, 4.99, "spek"),
    Product("Kipgyros", "vlees", "g", 400, 4.79, "kip"),
    Product("Slavink", "vlees", "stuk", 4, 4.99, "vlees"),
    # --- vis ---
    Product("Zalmfilet", "vis", "g", 200, 5.99, "zalm"),
    Product("Zalmmoot", "vis", "g", 250, 6.49, "zalm"),
    Product("Tonijn in olijfolie", "vis", "g", 160, 1.69, "tonijn"),
    Product("Pangasiusfilet", "vis", "g", 400, 5.49, "vis"),
    Product("Garnalen", "vis", "g", 200, 4.99, "garnaal"),
    # --- vleesvervanger ---
    Product("Biologische tofu", "vleesvervanger", "g", 375, 3.49, "tofu"),
    Product("Tempeh", "vleesvervanger", "g", 200, 2.79, "tempeh", ("biologisch",)),
    Product("Vegetarische schnitzel", "vleesvervanger", "stuk", 2, 2.99, "vegaschnitzel"),
    Product("Falafel", "vleesvervanger", "g", 220, 2.49, "falafel"),
    # --- zuivel ---
    Product("Halfvolle melk", "zuivel", "l", 1.0, 1.19, "melk"),
    Product("Magere yoghurt", "zuivel", "l", 1.0, 1.79, "yoghurt"),
    Product("Griekse yoghurt", "zuivel", "g", 500, 2.49, "yoghurt"),
    Product("Volle yoghurt", "zuivel", "l", 1.0, 1.59, "yoghurt"),
    Product("Hüttenkäse", "zuivel", "g", 200, 1.79, "huttenkase"),
    Product("Kaas belegen", "zuivel", "g", 400, 4.99, "kaas"),
    Product("Mozzarella", "zuivel", "g", 125, 1.49, "mozzarella"),
    Product("Roomboter", "zuivel", "g", 250, 2.49, "boter"),
    # --- ei ---
    Product("Eieren scharrel", "ei", "stuk", 10, 2.59, "ei"),
    Product("Eieren vrije uitloop", "ei", "stuk", 6, 2.29, "ei"),
    # --- granen / koolhydraten ---
    Product("Volkoren pasta", "pasta", "g", 500, 1.79, "pasta"),
    Product("Spaghetti", "pasta", "g", 500, 1.29, "pasta"),
    Product("Tagliatelle", "pasta", "g", 500, 1.69, "pasta"),
    Product("Penne", "pasta", "g", 500, 1.49, "pasta"),
    Product("Basmati rijst", "rijst", "g", 1000, 2.99, "rijst"),
    Product("Volkoren rijst", "rijst", "g", 500, 2.49, "rijst"),
    Product("Couscous", "graan", "g", 500, 1.99, "couscous"),
    Product("Quinoa", "graan", "g", 400, 3.49, "quinoa"),
    Product("Bulgur", "graan", "g", 500, 2.29, "bulgur"),
    Product("Aardappelen kruimig", "aardappel", "kg", 2.0, 2.79, "aardappel"),
    Product("Aardappelen vastkokend", "aardappel", "kg", 2.0, 2.79, "aardappel"),
    # --- peulvruchten / blik ---
    Product("Kikkererwten in blik", "peulvrucht", "g", 400, 1.19, "kikkererwt"),
    Product("Bruine bonen in blik", "peulvrucht", "g", 400, 1.09, "bonen"),
    Product("Linzen rood", "peulvrucht", "g", 500, 2.49, "linzen"),
    Product("Witte bonen in tomatensaus", "peulvrucht", "g", 400, 1.29, "bonen"),
    Product("Gepelde tomaten", "blik", "g", 400, 0.89, "tomaat"),
    # --- brood / wraps ---
    Product("Volkoren brood", "brood", "stuk", 1, 2.49, "brood"),
    Product("Bruin brood", "brood", "stuk", 1, 1.99, "brood"),
    Product("Pistolets", "brood", "stuk", 6, 1.49, "brood"),
    Product("Volkoren wraps", "brood", "stuk", 8, 2.29, "wrap"),
    Product("Pitabroodjes", "brood", "stuk", 6, 1.69, "brood"),
    # --- ontbijt ---
    Product("Havermout", "ontbijt", "g", 500, 1.49, "havermout"),
    Product("Muesli", "ontbijt", "g", 500, 2.79, "muesli"),
    Product("Cruesli noten", "ontbijt", "g", 450, 3.49, "muesli"),
    # --- snacks / extra ---
    Product("Hummus", "spread", "g", 200, 1.99, "hummus"),
    Product("Olijven", "spread", "g", 250, 2.49, "olijf"),
    Product("Pesto groen", "spread", "g", 190, 2.19, "pesto"),
    Product("Pindakaas", "spread", "g", 350, 2.79, "pindakaas"),
    # --- dranken ---
    Product("Sinaasappelsap", "drank", "l", 1.0, 1.99, "sap"),
    Product("Appelsap", "drank", "l", 1.0, 1.79, "sap"),
    # --- biologisch / overig ---
    Product("Biologische haver", "ontbijt", "g", 500, 2.79, "havermout", ("biologisch",)),
    Product("Biologische bloemkool", "groente", "stuk", 1, 2.99, "bloemkool", ("biologisch",)),
    Product("Biologische sojadrink", "zuivelvervanger", "l", 1.0, 2.29, "soja", ("biologisch",)),
    Product("Biologische appels", "fruit", "kg", 1.0, 2.99, "appel", ("biologisch",)),
    Product("Olijfolie extra vergine", "olie", "ml", 500, 6.99, "olijfolie"),
]


@dataclass(frozen=True)
class SupermarketProfile:
    price_multiplier: float
    discount_range: tuple[float, float]  # min/max fractie van basisprijs als saleprice
    bio_bias: float = 0.0       # fractie van mock-offers die uit bio-pool komen
    premium_bias: float = 0.0   # bias richting duurdere (hoog basisprijs) producten
    budget_bias: float = 0.0    # bias richting goedkopere producten


PROFILES: dict[str, SupermarketProfile] = {
    "jumbo":      SupermarketProfile(1.00, (0.55, 0.80)),
    "ah":         SupermarketProfile(1.05, (0.60, 0.85), premium_bias=0.2),
    "lidl":       SupermarketProfile(0.85, (0.50, 0.75), budget_bias=0.3),
    "aldi":       SupermarketProfile(0.85, (0.50, 0.75), budget_bias=0.3),
    "hoogvliet":  SupermarketProfile(0.95, (0.55, 0.80)),
    "ekoplaza":   SupermarketProfile(1.25, (0.65, 0.85), bio_bias=0.8, premium_bias=0.4),
    "plus":       SupermarketProfile(1.02, (0.55, 0.80)),
    "dirk":       SupermarketProfile(0.88, (0.50, 0.75), budget_bias=0.2),
    "vomar":      SupermarketProfile(0.95, (0.55, 0.80)),
    "coop":       SupermarketProfile(1.00, (0.55, 0.80)),
}


SUPERMARKET_URLS: dict[str, str] = {
    "jumbo": "https://www.jumbo.com",
    "ah": "https://www.ah.nl",
    "lidl": "https://www.lidl.nl",
    "aldi": "https://www.aldi.nl",
    "hoogvliet": "https://www.hoogvliet.com",
    "ekoplaza": "https://www.ekoplaza.nl",
    "plus": "https://www.plus.nl",
    "dirk": "https://www.dirk.nl",
    "vomar": "https://www.vomar.nl",
    "coop": "https://www.coop.nl",
}


def _deterministic_seed(slug: str) -> int:
    h = hashlib.md5(slug.encode("utf-8")).digest()
    return int.from_bytes(h[:4], "big")


def _select_products(slug: str, profile: SupermarketProfile, n: int = 32) -> list[Product]:
    rng = random.Random(_deterministic_seed(slug))
    pool = list(PRODUCT_POOL)
    # bio-pool apart
    bio_pool = [p for p in pool if "biologisch" in p.tags]
    non_bio = [p for p in pool if "biologisch" not in p.tags]

    selected: list[Product] = []
    if profile.bio_bias > 0 and bio_pool:
        bio_count = max(2, int(n * profile.bio_bias))
        selected.extend(rng.sample(bio_pool * 4, min(bio_count, len(bio_pool) * 4)))

    # rest uit non-bio, met budget/premium bias
    weights = []
    for p in non_bio:
        w = 1.0
        if profile.premium_bias and p.base_price >= 3.0:
            w += profile.premium_bias
        if profile.budget_bias and p.base_price <= 2.5:
            w += profile.budget_bias
        weights.append(w)

    remaining = n - len(selected)
    while len(selected) < n:
        idx = rng.choices(range(len(non_bio)), weights=weights, k=1)[0]
        if non_bio[idx] not in selected:
            selected.append(non_bio[idx])
        if len(selected) >= len(non_bio) + len(bio_pool) - 1:
            break  # geen duplicaten meer mogelijk
    return selected[:n]


def generate_mock_offers(slug: str) -> list[ScrapedOffer]:
    profile = PROFILES[slug]
    rng = random.Random(_deterministic_seed(slug) ^ 0xDEADBEEF)
    base_url = SUPERMARKET_URLS[slug]

    products = _select_products(slug, profile, n=32)
    offers: list[ScrapedOffer] = []
    for p in products:
        original = round(p.base_price * profile.price_multiplier, 2)
        sale_fraction = rng.uniform(*profile.discount_range)
        sale = round(original * sale_fraction, 2)
        if sale <= 0.10:
            sale = 0.49
        if sale >= original:
            sale = round(original * 0.85, 2)
        discount_text = None
        # 1+1 gratis voor sommige slugs/producten
        if rng.random() < 0.08:
            sale = round(original / 2, 2)
            discount_text = "1+1 gratis"
        offers.append(
            make_offer(
                product_name=p.name,
                category=p.category,
                unit=p.unit,
                amount=p.amount,
                original_price=original,
                sale_price=sale,
                discount_text=discount_text,
                source_url=f"{base_url}/aanbiedingen/{p.image_keyword}",
                image_url=f"/recipe-images/{p.image_keyword}.svg",
            )
        )
    return offers
