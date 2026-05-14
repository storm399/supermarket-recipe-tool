"""Standaardproducten die we aannemen dat thuis liggen.

Wanneer een recept deze nodig heeft maar er geen aanbieding is, wordt
het ingredient als 'pantry/ontbrekend' gemarkeerd zodat de gebruiker
weet wat hij/zij nog moet kopen.
"""

PANTRY_ITEMS: set[str] = {
    "zout",
    "peper",
    "olijfolie",
    "zonnebloemolie",
    "boter",
    "water",
    "azijn",
    "suiker",
    "bloem",
    "bakpoeder",
    "kaneel",
    "paprikapoeder",
    "kerriepoeder",
    "kurkuma",
    "komijn",
    "italiaanse kruiden",
    "oregano",
    "basilicum",
    "tijm",
    "bouillonblokje",
    "sojasaus",
    "tomatenpuree",
    "ketjap",
    "honing",
    "citroensap",
}


def is_pantry(name: str) -> bool:
    return name.lower().strip() in PANTRY_ITEMS
