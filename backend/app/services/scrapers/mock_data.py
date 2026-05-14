"""Uitgebreide mock-aanbiedingen pool.

~140 unieke producten verdeeld over alle hoofdcategorieen. Per supermarkt
worden 50 items gekozen met realistische prijsbias (Lidl/Aldi budget,
Ekoplaza bio, AH premium, etc). Output is deterministisch per slug zodat
de mock-data stabiel is tussen runs.
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
    image_keyword: str
    tags: tuple[str, ...] = ()


# Grote productenpool — tenminste 12 categorieen
PRODUCT_POOL: list[Product] = [
    # ---- groente (~22) ----
    Product("Broccoli", "groente", "stuk", 1, 1.49, "broccoli"),
    Product("Bloemkool", "groente", "stuk", 1, 2.49, "bloemkool"),
    Product("Spinazie vers", "groente", "g", 300, 2.49, "spinazie"),
    Product("Cherrytomaten", "groente", "g", 250, 2.29, "tomaat"),
    Product("Roma tomaten", "groente", "kg", 1.0, 2.99, "tomaat"),
    Product("Trostomaten", "groente", "kg", 1.0, 2.49, "tomaat"),
    Product("Paprika mix", "groente", "g", 500, 2.79, "paprika"),
    Product("Rode paprika", "groente", "stuk", 1, 1.19, "paprika"),
    Product("Komkommer", "groente", "stuk", 1, 0.99, "komkommer"),
    Product("IJsbergsla", "groente", "stuk", 1, 1.49, "sla"),
    Product("Veldsla", "groente", "g", 150, 1.99, "sla"),
    Product("Rucola", "groente", "g", 100, 1.79, "sla"),
    Product("Champignons", "groente", "g", 250, 1.59, "champignons"),
    Product("Kastanjechampignons", "groente", "g", 250, 1.99, "champignons"),
    Product("Courgette", "groente", "stuk", 1, 1.29, "courgette"),
    Product("Wortelen", "groente", "kg", 1.0, 1.69, "wortel"),
    Product("Ui", "groente", "kg", 1.0, 1.29, "ui"),
    Product("Rode ui", "groente", "kg", 1.0, 1.79, "ui"),
    Product("Knoflook", "groente", "stuk", 3, 1.49, "knoflook"),
    Product("Aubergine", "groente", "stuk", 1, 1.69, "aubergine"),
    Product("Prei", "groente", "stuk", 2, 1.79, "prei"),
    Product("Roergebakgroente", "groente", "g", 400, 2.29, "roerbak"),
    Product("Spruitjes", "groente", "g", 500, 2.49, "spruit"),
    Product("Andijvie", "groente", "g", 400, 1.79, "andijvie"),
    Product("Boerenkool", "groente", "g", 400, 1.99, "boerenkool"),
    Product("Bospeen", "groente", "bos", 1, 1.49, "wortel"),
    Product("Snijbonen", "groente", "g", 300, 2.49, "boon"),
    Product("Sperziebonen", "groente", "g", 400, 2.79, "boon"),
    # ---- fruit (~16) ----
    Product("Bananen", "fruit", "kg", 1.0, 1.79, "banaan"),
    Product("Appels Jonagold", "fruit", "kg", 1.0, 1.99, "appel"),
    Product("Appels Elstar", "fruit", "kg", 1.0, 1.99, "appel"),
    Product("Peren Conference", "fruit", "kg", 1.0, 2.29, "peer"),
    Product("Aardbeien", "fruit", "g", 400, 3.99, "aardbei"),
    Product("Frambozen", "fruit", "g", 125, 2.49, "framboos"),
    Product("Blauwe bessen", "fruit", "g", 125, 2.49, "bes"),
    Product("Avocado", "fruit", "stuk", 2, 2.99, "avocado"),
    Product("Mandarijnen", "fruit", "kg", 1.0, 2.49, "mandarijn"),
    Product("Sinaasappels", "fruit", "kg", 1.0, 2.29, "sinaasappel"),
    Product("Mango", "fruit", "stuk", 1, 1.99, "mango"),
    Product("Druiven", "fruit", "g", 500, 3.49, "druif"),
    Product("Kiwi's", "fruit", "stuk", 4, 1.99, "kiwi"),
    Product("Ananas", "fruit", "stuk", 1, 2.49, "ananas"),
    Product("Watermeloen", "fruit", "stuk", 1, 4.99, "meloen"),
    Product("Citroenen", "fruit", "stuk", 4, 1.79, "citroen"),
    # ---- aardappel (~3) ----
    Product("Aardappelen kruimig", "aardappel", "kg", 2.0, 2.79, "aardappel"),
    Product("Aardappelen vastkokend", "aardappel", "kg", 2.0, 2.79, "aardappel"),
    Product("Zoete aardappel", "aardappel", "kg", 1.0, 2.99, "aardappel"),
    # ---- vlees (~11) ----
    Product("Kipfilet naturel", "vlees", "kg", 1.0, 10.49, "kip"),
    Product("Kipfilet gemarineerd", "vlees", "g", 500, 5.99, "kip"),
    Product("Kipgehakt", "vlees", "g", 500, 4.99, "kip"),
    Product("Rundergehakt", "vlees", "g", 500, 4.49, "gehakt"),
    Product("Half-om-half gehakt", "vlees", "g", 500, 3.99, "gehakt"),
    Product("Runderlapjes", "vlees", "g", 500, 6.99, "rundvlees"),
    Product("Riblappen", "vlees", "g", 500, 7.49, "rundvlees"),
    Product("Varkenshaas", "vlees", "g", 500, 7.99, "varken"),
    Product("Speklapjes", "vlees", "g", 500, 4.99, "spek"),
    Product("Kipgyros", "vlees", "g", 400, 4.79, "kip"),
    Product("Slavink", "vlees", "stuk", 4, 4.99, "vlees"),
    Product("Rookworst", "vlees", "stuk", 1, 2.99, "worst"),
    # ---- vis (~7) ----
    Product("Zalmfilet", "vis", "g", 200, 5.99, "zalm"),
    Product("Zalmmoot", "vis", "g", 250, 6.49, "zalm"),
    Product("Tonijn in olijfolie", "vis", "g", 160, 1.69, "tonijn"),
    Product("Pangasiusfilet", "vis", "g", 400, 5.49, "vis"),
    Product("Kabeljauwfilet", "vis", "g", 300, 6.99, "vis"),
    Product("Garnalen", "vis", "g", 200, 4.99, "garnaal"),
    Product("Vissticks", "diepvries", "stuk", 10, 2.49, "vis"),
    # ---- vleesvervanger (~6) ----
    Product("Biologische tofu", "vleesvervanger", "g", 375, 3.49, "tofu", ("biologisch",)),
    Product("Tempeh", "vleesvervanger", "g", 200, 2.79, "tempeh", ("biologisch",)),
    Product("Vegetarische schnitzel", "vleesvervanger", "stuk", 2, 2.99, "vegaschnitzel"),
    Product("Vegetarische gehakt", "vleesvervanger", "g", 350, 3.49, "vegagehakt"),
    Product("Falafel", "vleesvervanger", "g", 220, 2.49, "falafel"),
    Product("Quorn stukjes", "vleesvervanger", "g", 300, 3.79, "quorn"),
    # ---- zuivel (~10) ----
    Product("Halfvolle melk", "zuivel", "l", 1.0, 1.19, "melk"),
    Product("Volle melk", "zuivel", "l", 1.0, 1.29, "melk"),
    Product("Magere yoghurt", "zuivel", "l", 1.0, 1.79, "yoghurt"),
    Product("Griekse yoghurt", "zuivel", "g", 500, 2.49, "yoghurt"),
    Product("Volle yoghurt", "zuivel", "l", 1.0, 1.59, "yoghurt"),
    Product("Hüttenkäse", "zuivel", "g", 200, 1.79, "huttenkase"),
    Product("Kwark", "zuivel", "g", 500, 2.29, "kwark"),
    Product("Karnemelk", "zuivel", "l", 1.0, 1.19, "karnemelk"),
    Product("Slagroom", "zuivel", "ml", 250, 1.69, "slagroom"),
    Product("Roomboter", "zuivel", "g", 250, 2.49, "boter"),
    # ---- kaas (~6) ----
    Product("Kaas jong", "kaas", "g", 400, 4.49, "kaas"),
    Product("Kaas belegen", "kaas", "g", 400, 4.99, "kaas"),
    Product("Mozzarella", "kaas", "g", 125, 1.49, "mozzarella"),
    Product("Geitenkaas", "kaas", "g", 100, 2.79, "geitenkaas"),
    Product("Feta", "kaas", "g", 200, 1.99, "feta"),
    Product("Parmezaan", "kaas", "g", 100, 3.49, "parmezaan"),
    # ---- ei (~3) ----
    Product("Eieren scharrel", "ei", "stuk", 10, 2.59, "ei"),
    Product("Eieren vrije uitloop", "ei", "stuk", 6, 2.29, "ei"),
    Product("Eieren bio", "ei", "stuk", 6, 2.99, "ei", ("biologisch",)),
    # ---- pasta / rijst / graan (~12) ----
    Product("Volkoren pasta", "pasta", "g", 500, 1.79, "pasta"),
    Product("Spaghetti", "pasta", "g", 500, 1.29, "pasta"),
    Product("Tagliatelle", "pasta", "g", 500, 1.69, "pasta"),
    Product("Penne", "pasta", "g", 500, 1.49, "pasta"),
    Product("Macaroni", "pasta", "g", 500, 1.39, "pasta"),
    Product("Lasagnebladen", "pasta", "g", 250, 1.59, "pasta"),
    Product("Basmati rijst", "rijst", "g", 1000, 2.99, "rijst"),
    Product("Volkoren rijst", "rijst", "g", 500, 2.49, "rijst"),
    Product("Risottorijst", "rijst", "g", 500, 2.79, "rijst"),
    Product("Couscous", "graan", "g", 500, 1.99, "couscous"),
    Product("Quinoa", "graan", "g", 400, 3.49, "quinoa"),
    Product("Bulgur", "graan", "g", 500, 2.29, "bulgur"),
    # ---- peulvrucht / blik (~7) ----
    Product("Kikkererwten in blik", "peulvrucht", "g", 400, 1.19, "kikkererwt"),
    Product("Bruine bonen in blik", "peulvrucht", "g", 400, 1.09, "bonen"),
    Product("Linzen rood", "peulvrucht", "g", 500, 2.49, "linzen"),
    Product("Witte bonen in tomatensaus", "peulvrucht", "g", 400, 1.29, "bonen"),
    Product("Kidneybonen in blik", "peulvrucht", "g", 400, 1.19, "bonen"),
    Product("Gepelde tomaten", "blik", "g", 400, 0.89, "tomaat"),
    Product("Tomatenpassata", "blik", "ml", 500, 1.29, "tomaat"),
    # ---- brood / wraps (~6) ----
    Product("Volkoren brood", "brood", "stuk", 1, 2.49, "brood"),
    Product("Bruin brood", "brood", "stuk", 1, 1.99, "brood"),
    Product("Pistolets", "brood", "stuk", 6, 1.49, "brood"),
    Product("Volkoren wraps", "brood", "stuk", 8, 2.29, "wrap"),
    Product("Pitabroodjes", "brood", "stuk", 6, 1.69, "brood"),
    Product("Stokbrood", "brood", "stuk", 1, 1.29, "brood"),
    # ---- ontbijt (~5) ----
    Product("Havermout", "ontbijt", "g", 500, 1.49, "havermout"),
    Product("Muesli", "ontbijt", "g", 500, 2.79, "muesli"),
    Product("Cruesli noten", "ontbijt", "g", 450, 3.49, "muesli"),
    Product("Cornflakes", "ontbijt", "g", 500, 2.29, "cornflakes"),
    Product("Beschuit", "ontbijt", "stuk", 13, 1.49, "beschuit"),
    # ---- diepvries (~4) ----
    Product("Diepvries doperwten", "diepvries", "g", 750, 1.99, "doperwten"),
    Product("Diepvries spinazie", "diepvries", "g", 450, 1.89, "spinazie"),
    Product("Diepvries roerbak mix", "diepvries", "g", 750, 2.49, "roerbak"),
    Product("Diepvries broccoli", "diepvries", "g", 500, 1.99, "broccoli"),
    # ---- snacks / spread (~8) ----
    Product("Hummus", "spread", "g", 200, 1.99, "hummus"),
    Product("Olijven", "spread", "g", 250, 2.49, "olijf"),
    Product("Tapenade", "spread", "g", 150, 2.19, "tapenade"),
    Product("Pesto groen", "spread", "g", 190, 2.19, "pesto"),
    Product("Pesto rosso", "spread", "g", 190, 2.29, "pesto"),
    Product("Pindakaas", "spread", "g", 350, 2.79, "pindakaas"),
    Product("Honing", "spread", "g", 350, 3.49, "honing"),
    Product("Jam aardbeien", "spread", "g", 300, 1.99, "jam"),
    # ---- dranken (~5) ----
    Product("Sinaasappelsap", "drank", "l", 1.0, 1.99, "sap"),
    Product("Appelsap", "drank", "l", 1.0, 1.79, "sap"),
    Product("Mineraalwater", "drank", "l", 1.5, 0.59, "water"),
    Product("Bruisend mineraalwater", "drank", "l", 1.5, 0.59, "water"),
    Product("Koffiebonen", "drank", "g", 500, 6.49, "koffie"),
    # ---- olie ----
    Product("Olijfolie extra vergine", "olie", "ml", 500, 6.99, "olijfolie"),
    Product("Zonnebloemolie", "olie", "ml", 1000, 2.49, "olie"),
    # ---- biologisch (~5) ----
    Product("Biologische haver", "ontbijt", "g", 500, 2.79, "havermout", ("biologisch",)),
    Product("Biologische bloemkool", "groente", "stuk", 1, 2.99, "bloemkool", ("biologisch",)),
    Product("Biologische sojadrink", "zuivelvervanger", "l", 1.0, 2.29, "soja", ("biologisch",)),
    Product("Biologische appels", "fruit", "kg", 1.0, 2.99, "appel", ("biologisch",)),
    Product("Biologische amandeldrink", "zuivelvervanger", "l", 1.0, 2.49, "amandel", ("biologisch",)),
    Product("Biologische kipfilet", "vlees", "g", 300, 5.99, "kip", ("biologisch",)),
    # ---- huishouden / verzorging (~3) ----
    Product("Wasmiddel vloeibaar", "huishouden", "l", 1.5, 5.99, "huishouden"),
    Product("Toiletpapier", "huishouden", "stuk", 8, 4.49, "huishouden"),
    Product("Tandpasta", "verzorging", "ml", 75, 1.99, "verzorging"),
]


@dataclass(frozen=True)
class SupermarketProfile:
    price_multiplier: float
    discount_range: tuple[float, float]
    bio_bias: float = 0.0
    premium_bias: float = 0.0
    budget_bias: float = 0.0
    # Aantal aanbiedingen dat we mock'en per supermarkt.
    target_count: int = 52


PROFILES: dict[str, SupermarketProfile] = {
    "jumbo":     SupermarketProfile(1.00, (0.55, 0.80), target_count=58),
    "ah":        SupermarketProfile(1.05, (0.60, 0.85), premium_bias=0.2, target_count=62),
    "lidl":      SupermarketProfile(0.85, (0.50, 0.75), budget_bias=0.3, target_count=54),
    "aldi":      SupermarketProfile(0.85, (0.50, 0.75), budget_bias=0.3, target_count=52),
    "hoogvliet": SupermarketProfile(0.95, (0.55, 0.80), target_count=52),
    "ekoplaza":  SupermarketProfile(1.25, (0.65, 0.85), bio_bias=0.8, premium_bias=0.4, target_count=50),
    "plus":      SupermarketProfile(1.02, (0.55, 0.80), target_count=54),
    "dirk":      SupermarketProfile(0.88, (0.50, 0.75), budget_bias=0.2, target_count=52),
    "vomar":     SupermarketProfile(0.95, (0.55, 0.80), target_count=50),
    "coop":      SupermarketProfile(1.00, (0.55, 0.80), target_count=52),
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


def _seed(slug: str) -> int:
    h = hashlib.md5(slug.encode("utf-8")).digest()
    return int.from_bytes(h[:4], "big")


def _select_products(slug: str, profile: SupermarketProfile) -> list[Product]:
    rng = random.Random(_seed(slug))
    n = profile.target_count
    bio_pool = [p for p in PRODUCT_POOL if "biologisch" in p.tags]
    non_bio = [p for p in PRODUCT_POOL if "biologisch" not in p.tags]

    selected: list[Product] = []
    if profile.bio_bias > 0 and bio_pool:
        bio_count = max(3, int(n * profile.bio_bias * 0.3))
        selected.extend(rng.sample(bio_pool, min(bio_count, len(bio_pool))))

    # Stratificeer per categorie zodat we niet 50x groente krijgen.
    by_category: dict[str, list[Product]] = {}
    for p in non_bio:
        by_category.setdefault(p.category, []).append(p)

    # Eerst minstens 1 product per categorie als bredere dekking.
    for cat, items in by_category.items():
        if items:
            selected.append(rng.choice(items))

    # Vul aan met weighted random selection tot we de target hebben.
    weights = []
    for p in non_bio:
        w = 1.0
        if profile.premium_bias and p.base_price >= 3.0:
            w += profile.premium_bias
        if profile.budget_bias and p.base_price <= 2.5:
            w += profile.budget_bias
        weights.append(w)

    seen_names = {p.name for p in selected}
    attempts = 0
    while len(selected) < n and attempts < 5000:
        idx = rng.choices(range(len(non_bio)), weights=weights, k=1)[0]
        cand = non_bio[idx]
        if cand.name not in seen_names:
            selected.append(cand)
            seen_names.add(cand.name)
        attempts += 1

    return selected[:n]


def generate_mock_offers(slug: str) -> list[ScrapedOffer]:
    profile = PROFILES[slug]
    rng = random.Random(_seed(slug) ^ 0xDEADBEEF)
    base_url = SUPERMARKET_URLS[slug]
    products = _select_products(slug, profile)

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
        # Variatie in actie-types
        roll = rng.random()
        if roll < 0.07:
            sale = round(original / 2, 2)
            discount_text = "1+1 gratis"
        elif roll < 0.12:
            discount_text = "2e halve prijs"
            sale = round(original * 0.75, 2)
        elif roll < 0.16:
            discount_text = "3 voor €5"
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
                source="fallback_mock",
            )
        )
    return offers
