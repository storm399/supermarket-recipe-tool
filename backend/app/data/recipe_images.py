"""Recipe foto-database.

Twee lagen:
1. TITLE_PHOTO_URLS — specifieke foto per recept (op normalised titel).
   Hiermee krijgt elk recept een eigen unieke food-foto.
2. CATEGORY_PHOTO_URLS — fallback op image_key wanneer geen titel match.

URLs zijn stabiele Unsplash CDN-links (geen API-key nodig). De frontend
valt automatisch terug op de lokale SVG-illustraties als de externe URL
faalt of niet laadt.
"""
from __future__ import annotations


# Specifieke foto per receptsjabloon. Sleutel is een sub-string van de
# genormaliseerde titel (lowercase). De langste match wint.
TITLE_PHOTO_URLS: dict[str, str] = {
    "pasta met kipfilet": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=800&q=70",
    "tofu-roerbak": "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=800&q=70",
    "zalmfilet uit de oven": "https://images.unsplash.com/photo-1485921325833-c519f76c4927?auto=format&fit=crop&w=800&q=70",
    "marokkaanse linzensoep": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=800&q=70",
    "volkoren wraps met hummus": "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?auto=format&fit=crop&w=800&q=70",
    "kikkererwten-curry": "https://images.unsplash.com/photo-1631292784640-2b24be784d5d?auto=format&fit=crop&w=800&q=70",
    "spaghetti bolognese": "https://images.unsplash.com/photo-1572441713132-51c75654db73?auto=format&fit=crop&w=800&q=70",
    "omelet met champignons": "https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=800&q=70",
    "overnight oats": "https://images.unsplash.com/photo-1568689573208-30fb3edd0386?auto=format&fit=crop&w=800&q=70",
    "roerei op volkoren toast": "https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=800&q=70",
    "griekse salade": "https://images.unsplash.com/photo-1505253758473-96b7015fcd40?auto=format&fit=crop&w=800&q=70",
    "couscous-salade": "https://images.unsplash.com/photo-1543339308-43e59d6b73a6?auto=format&fit=crop&w=800&q=70",
    "tonijnsalade": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?auto=format&fit=crop&w=800&q=70",
    "aardappel-ovenschotel": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=70",
    "stamppot met spek": "https://images.unsplash.com/photo-1543352634-99a5d50ae78e?auto=format&fit=crop&w=800&q=70",
    "frittata": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?auto=format&fit=crop&w=800&q=70",
    "snelle kip-currie": "https://images.unsplash.com/photo-1455619452474-d2be8b1e70cd?auto=format&fit=crop&w=800&q=70",
    "smoothie bowl": "https://images.unsplash.com/photo-1502741338009-cac2772e18bc?auto=format&fit=crop&w=800&q=70",
    "gehaktballetjes": "https://images.unsplash.com/photo-1529042410759-befb1204b468?auto=format&fit=crop&w=800&q=70",
    "falafel bowl": "https://images.unsplash.com/photo-1547592166-23ac45744acd?auto=format&fit=crop&w=800&q=70",
    "quinoa-bowl": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=70",
    "pasta pesto": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=800&q=70",
    "pasta met garnalen": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=800&q=70",
    "hüttenkäse-salade": "https://images.unsplash.com/photo-1505253758473-96b7015fcd40?auto=format&fit=crop&w=800&q=70",
    "pita met gemarineerde kipgyros": "https://images.unsplash.com/photo-1565299543923-37dd37887442?auto=format&fit=crop&w=800&q=70",
    "warme havermoutpap": "https://images.unsplash.com/photo-1517673400267-0251440c45dc?auto=format&fit=crop&w=800&q=70",
    "snelle groente-ramen": "https://images.unsplash.com/photo-1591814468924-caf88d1232e1?auto=format&fit=crop&w=800&q=70",
    "risotto met champignons": "https://images.unsplash.com/photo-1476124369491-e7addf5db371?auto=format&fit=crop&w=800&q=70",
    "klassieke lasagne": "https://images.unsplash.com/photo-1619895092538-128341789043?auto=format&fit=crop&w=800&q=70",
    "pannenkoeken met appel": "https://images.unsplash.com/photo-1565299543923-37dd37887442?auto=format&fit=crop&w=800&q=70",
    "kip-taco": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?auto=format&fit=crop&w=800&q=70",
    "yoghurt bowl": "https://images.unsplash.com/photo-1488477181946-6428a0291777?auto=format&fit=crop&w=800&q=70",
    "gevulde paprika": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?auto=format&fit=crop&w=800&q=70",
    "pesto-aardappels": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=70",
    "kabeljauw uit de oven": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?auto=format&fit=crop&w=800&q=70",
    "macaronischotel": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?auto=format&fit=crop&w=800&q=70",
    "pita met falafel": "https://images.unsplash.com/photo-1547592166-23ac45744acd?auto=format&fit=crop&w=800&q=70",
    "wrap-pizza": "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=800&q=70",
    "snelle erwtensoep": "https://images.unsplash.com/photo-1547308283-b941a1c8b3d2?auto=format&fit=crop&w=800&q=70",
    "bulgur-salade": "https://images.unsplash.com/photo-1505253758473-96b7015fcd40?auto=format&fit=crop&w=800&q=70",
    "hollands stoofvlees": "https://images.unsplash.com/photo-1605908502724-9093a79a1b39?auto=format&fit=crop&w=800&q=70",
    "ovenfrietjes": "https://images.unsplash.com/photo-1576107232684-1279f390859f?auto=format&fit=crop&w=800&q=70",
    # nieuwe templates (toegevoegd in deze iteratie)
    "indiase dal": "https://images.unsplash.com/photo-1631292784640-2b24be784d5d?auto=format&fit=crop&w=800&q=70",
    "shakshuka": "https://images.unsplash.com/photo-1590412200988-a436970781fa?auto=format&fit=crop&w=800&q=70",
    "buddha bowl": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=800&q=70",
    "tomatensoep": "https://images.unsplash.com/photo-1547308283-b941a1c8b3d2?auto=format&fit=crop&w=800&q=70",
    "kipsoep": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=800&q=70",
    "broodjes tonijn": "https://images.unsplash.com/photo-1539252554935-80c8cb09c1d3?auto=format&fit=crop&w=800&q=70",
    "vegan chili": "https://images.unsplash.com/photo-1455619452474-d2be8b1e70cd?auto=format&fit=crop&w=800&q=70",
    "chia pudding": "https://images.unsplash.com/photo-1502741338009-cac2772e18bc?auto=format&fit=crop&w=800&q=70",
    "groentespiesjes": "https://images.unsplash.com/photo-1529042410759-befb1204b468?auto=format&fit=crop&w=800&q=70",
    "vissticks met rijst": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?auto=format&fit=crop&w=800&q=70",
    "kapsalon": "https://images.unsplash.com/photo-1576107232684-1279f390859f?auto=format&fit=crop&w=800&q=70",
    "pad thai": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=800&q=70",
    "italiaanse tomatensalade": "https://images.unsplash.com/photo-1505253758473-96b7015fcd40?auto=format&fit=crop&w=800&q=70",
    "ovenkip met groente": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?auto=format&fit=crop&w=800&q=70",
    "broccoli-ovenschotel": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=70",
    "courgettelinguine": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=800&q=70",
    "snelle nasi": "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=800&q=70",
    "hartige muffins": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?auto=format&fit=crop&w=800&q=70",
    "tortellini in roomsaus": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=800&q=70",
    "groenten lasagne": "https://images.unsplash.com/photo-1619895092538-128341789043?auto=format&fit=crop&w=800&q=70",
}

# Categorie-fallback (image_key) wanneer er geen titel-match is.
CATEGORY_PHOTO_URLS: dict[str, str] = {
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
    "pizza": "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=800&q=70",
    "risotto": "https://images.unsplash.com/photo-1476124369491-e7addf5db371?auto=format&fit=crop&w=800&q=70",
    "lasagne": "https://images.unsplash.com/photo-1619895092538-128341789043?auto=format&fit=crop&w=800&q=70",
    "default": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=800&q=70",
}


def _normalize(s: str) -> str:
    return s.lower().strip()


def photo_url_for_title(title: str) -> str | None:
    """Best-match foto op basis van de genormaliseerde titel (langste sleutel wint)."""
    if not title:
        return None
    norm = _normalize(title)
    for key in sorted(TITLE_PHOTO_URLS.keys(), key=len, reverse=True):
        if key in norm:
            return TITLE_PHOTO_URLS[key]
    return None


def photo_url_for(image_key: str | None, title: str | None = None) -> str | None:
    """Beste foto-URL: titel-specifiek > categorie > default."""
    if title:
        url = photo_url_for_title(title)
        if url:
            return url
    if not image_key:
        return CATEGORY_PHOTO_URLS.get("default")
    return CATEGORY_PHOTO_URLS.get(image_key) or CATEGORY_PHOTO_URLS.get("default")
