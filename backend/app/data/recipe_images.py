"""Mapping van image_key naar echte food-foto's."""
from __future__ import annotations


# We gebruiken Unsplash's officiele CDN met specifieke photo-id's. Deze
# URL's zijn stabiel en vereisen geen API-key. Elke template krijgt een
# passende foto die thematisch klopt. Als de URL faalt valt de frontend
# terug op de lokale SVG-illustraties uit /public/recipe-images/.

# Specifieke Unsplash foto-id's geselecteerd om bij het receptthema te passen.
# Een lege string betekent: gebruik direct de SVG fallback.
RECIPE_PHOTO_URLS: dict[str, str] = {
    "pasta": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?auto=format&fit=crop&w=800&q=70",
    "salade": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=800&q=70",
    "curry": "https://images.unsplash.com/photo-1455619452474-d2be8b1e70cd?auto=format&fit=crop&w=800&q=70",
    "zalm": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?auto=format&fit=crop&w=800&q=70",
    "soep": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=800&q=70",
    "wrap": "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?auto=format&fit=crop&w=800&q=70",
    "ei": "https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=800&q=70",
    "ontbijt": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?auto=format&fit=crop&w=800&q=70",
    "roerbak": "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=800&q=70",
    "bowl": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=70",
    "ovenschotel": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=70",
    "stamppot": "https://images.unsplash.com/photo-1543352634-99a5d50ae78e?auto=format&fit=crop&w=800&q=70",
    "smoothie": "https://images.unsplash.com/photo-1502741338009-cac2772e18bc?auto=format&fit=crop&w=800&q=70",
    "gehaktballetjes": "https://images.unsplash.com/photo-1529042410759-befb1204b468?auto=format&fit=crop&w=800&q=70",
    "pita": "https://images.unsplash.com/photo-1565299543923-37dd37887442?auto=format&fit=crop&w=800&q=70",
    "ramen": "https://images.unsplash.com/photo-1591814468924-caf88d1232e1?auto=format&fit=crop&w=800&q=70",
    "burger": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=70",
    "pizza": "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=800&q=70",
    "risotto": "https://images.unsplash.com/photo-1476124369491-e7addf5db371?auto=format&fit=crop&w=800&q=70",
    "lasagne": "https://images.unsplash.com/photo-1574894709920-11b28e7367e3?auto=format&fit=crop&w=800&q=70",
    "pannenkoek": "https://images.unsplash.com/photo-1565299543923-37dd37887442?auto=format&fit=crop&w=800&q=70",
    "yoghurt": "https://images.unsplash.com/photo-1488477181946-6428a0291777?auto=format&fit=crop&w=800&q=70",
    "taco": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?auto=format&fit=crop&w=800&q=70",
    "noodles": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=800&q=70",
    "default": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=800&q=70",
}


def photo_url_for(image_key: str | None) -> str | None:
    if not image_key:
        return RECIPE_PHOTO_URLS.get("default")
    return RECIPE_PHOTO_URLS.get(image_key) or RECIPE_PHOTO_URLS.get("default")
