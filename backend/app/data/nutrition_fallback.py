"""Fallback voedingswaarden per 100 g/ml voor veelvoorkomende ingredienten.

Bron: gemiddelden uit NEVO/Open Food Facts. Dit is bewust een eenvoudige
lookup; de echte nutrition.py probeert eerst Open Food Facts.
"""

NUTRITION_FALLBACK: dict[str, dict[str, float]] = {
    # eiwitbronnen
    "kipfilet": {"kcal": 110, "protein": 23, "carbs": 0, "sugar": 0, "fat": 1.5, "satfat": 0.4, "fiber": 0, "salt": 0.2},
    "kipgehakt": {"kcal": 150, "protein": 21, "carbs": 0, "sugar": 0, "fat": 7, "satfat": 2.1, "fiber": 0, "salt": 0.2},
    "rundergehakt": {"kcal": 220, "protein": 19, "carbs": 0, "sugar": 0, "fat": 16, "satfat": 6.5, "fiber": 0, "salt": 0.2},
    "runderlapjes": {"kcal": 180, "protein": 24, "carbs": 0, "sugar": 0, "fat": 9, "satfat": 3.5, "fiber": 0, "salt": 0.2},
    "varkenshaas": {"kcal": 120, "protein": 22, "carbs": 0, "sugar": 0, "fat": 3, "satfat": 1.0, "fiber": 0, "salt": 0.2},
    "zalmfilet": {"kcal": 200, "protein": 20, "carbs": 0, "sugar": 0, "fat": 13, "satfat": 2.6, "fiber": 0, "salt": 0.1},
    "zalmmoot": {"kcal": 200, "protein": 20, "carbs": 0, "sugar": 0, "fat": 13, "satfat": 2.6, "fiber": 0, "salt": 0.1},
    "tonijn": {"kcal": 120, "protein": 26, "carbs": 0, "sugar": 0, "fat": 1, "satfat": 0.3, "fiber": 0, "salt": 0.6},
    "tofu": {"kcal": 130, "protein": 13, "carbs": 1, "sugar": 0.5, "fat": 8, "satfat": 1.2, "fiber": 1, "salt": 0.05},
    "eieren": {"kcal": 143, "protein": 13, "carbs": 1, "sugar": 1, "fat": 10, "satfat": 3.1, "fiber": 0, "salt": 0.3},
    "kikkererwten": {"kcal": 120, "protein": 7, "carbs": 18, "sugar": 1, "fat": 2, "satfat": 0.2, "fiber": 7, "salt": 0.4},
    "linzen": {"kcal": 110, "protein": 9, "carbs": 18, "sugar": 1, "fat": 0.5, "satfat": 0.1, "fiber": 8, "salt": 0.01},

    # zuivel
    "yoghurt": {"kcal": 55, "protein": 4.5, "carbs": 4.5, "sugar": 4.5, "fat": 1.5, "satfat": 1.0, "fiber": 0, "salt": 0.1},
    "magere yoghurt": {"kcal": 40, "protein": 4.5, "carbs": 5.5, "sugar": 5.5, "fat": 0.1, "satfat": 0.1, "fiber": 0, "salt": 0.1},
    "melk": {"kcal": 47, "protein": 3.5, "carbs": 4.7, "sugar": 4.7, "fat": 1.5, "satfat": 1.0, "fiber": 0, "salt": 0.1},
    "kaas": {"kcal": 360, "protein": 25, "carbs": 0.5, "sugar": 0.5, "fat": 28, "satfat": 18, "fiber": 0, "salt": 1.6},
    "mozzarella": {"kcal": 250, "protein": 18, "carbs": 1, "sugar": 1, "fat": 19, "satfat": 12, "fiber": 0, "salt": 1.0},
    "sojadrink": {"kcal": 45, "protein": 3.5, "carbs": 2, "sugar": 2, "fat": 2, "satfat": 0.3, "fiber": 0.5, "salt": 0.1},

    # granen / koolhydraten
    "pasta": {"kcal": 350, "protein": 12, "carbs": 70, "sugar": 3, "fat": 2, "satfat": 0.3, "fiber": 3, "salt": 0.01},
    "volkoren pasta": {"kcal": 330, "protein": 13, "carbs": 60, "sugar": 3, "fat": 3, "satfat": 0.5, "fiber": 8, "salt": 0.01},
    "spaghetti": {"kcal": 350, "protein": 12, "carbs": 70, "sugar": 3, "fat": 2, "satfat": 0.3, "fiber": 3, "salt": 0.01},
    "tagliatelle": {"kcal": 350, "protein": 12, "carbs": 70, "sugar": 3, "fat": 2, "satfat": 0.3, "fiber": 3, "salt": 0.01},
    "basmati rijst": {"kcal": 350, "protein": 7, "carbs": 78, "sugar": 0.5, "fat": 0.5, "satfat": 0.1, "fiber": 1.5, "salt": 0.01},
    "rijst": {"kcal": 350, "protein": 7, "carbs": 78, "sugar": 0.5, "fat": 0.5, "satfat": 0.1, "fiber": 1.5, "salt": 0.01},
    "aardappel": {"kcal": 75, "protein": 2, "carbs": 17, "sugar": 0.5, "fat": 0.1, "satfat": 0.0, "fiber": 2, "salt": 0.01},
    "aardappelen": {"kcal": 75, "protein": 2, "carbs": 17, "sugar": 0.5, "fat": 0.1, "satfat": 0.0, "fiber": 2, "salt": 0.01},
    "wraps": {"kcal": 280, "protein": 9, "carbs": 50, "sugar": 2, "fat": 5, "satfat": 1.5, "fiber": 4, "salt": 1.2},
    "brood": {"kcal": 230, "protein": 9, "carbs": 42, "sugar": 3, "fat": 2.5, "satfat": 0.5, "fiber": 6, "salt": 1.2},
    "haver": {"kcal": 370, "protein": 13, "carbs": 60, "sugar": 1, "fat": 7, "satfat": 1.2, "fiber": 10, "salt": 0.02},

    # groente
    "broccoli": {"kcal": 35, "protein": 3, "carbs": 4, "sugar": 2, "fat": 0.4, "satfat": 0.1, "fiber": 3, "salt": 0.02},
    "spinazie": {"kcal": 23, "protein": 3, "carbs": 1.5, "sugar": 0.5, "fat": 0.4, "satfat": 0.1, "fiber": 2.5, "salt": 0.08},
    "paprika": {"kcal": 30, "protein": 1, "carbs": 5, "sugar": 4, "fat": 0.3, "satfat": 0.1, "fiber": 2, "salt": 0.01},
    "champignons": {"kcal": 22, "protein": 3, "carbs": 1, "sugar": 1, "fat": 0.3, "satfat": 0.1, "fiber": 2, "salt": 0.01},
    "cherrytomaten": {"kcal": 20, "protein": 1, "carbs": 3, "sugar": 3, "fat": 0.2, "satfat": 0.0, "fiber": 1.5, "salt": 0.01},
    "tomaten": {"kcal": 20, "protein": 1, "carbs": 3, "sugar": 3, "fat": 0.2, "satfat": 0.0, "fiber": 1.5, "salt": 0.01},
    "courgette": {"kcal": 17, "protein": 1.2, "carbs": 2, "sugar": 2, "fat": 0.3, "satfat": 0.1, "fiber": 1, "salt": 0.01},
    "wortelen": {"kcal": 35, "protein": 0.8, "carbs": 7, "sugar": 5, "fat": 0.2, "satfat": 0.0, "fiber": 3, "salt": 0.07},
    "ui": {"kcal": 35, "protein": 1, "carbs": 7, "sugar": 4, "fat": 0.2, "satfat": 0.0, "fiber": 1.7, "salt": 0.01},
    "knoflook": {"kcal": 149, "protein": 6, "carbs": 33, "sugar": 1, "fat": 0.5, "satfat": 0.1, "fiber": 2, "salt": 0.04},
    "komkommer": {"kcal": 15, "protein": 0.7, "carbs": 2, "sugar": 1.5, "fat": 0.1, "satfat": 0.0, "fiber": 0.5, "salt": 0.01},
    "ijsbergsla": {"kcal": 14, "protein": 0.9, "carbs": 2, "sugar": 2, "fat": 0.1, "satfat": 0.0, "fiber": 1.2, "salt": 0.01},
    "bloemkool": {"kcal": 25, "protein": 2, "carbs": 3, "sugar": 2, "fat": 0.3, "satfat": 0.1, "fiber": 2, "salt": 0.03},
    "roergebakgroente": {"kcal": 35, "protein": 2, "carbs": 5, "sugar": 3, "fat": 0.5, "satfat": 0.1, "fiber": 2.5, "salt": 0.02},

    # fruit
    "bananen": {"kcal": 89, "protein": 1.1, "carbs": 20, "sugar": 12, "fat": 0.3, "satfat": 0.1, "fiber": 2.6, "salt": 0.01},
    "aardbeien": {"kcal": 32, "protein": 0.7, "carbs": 6, "sugar": 5, "fat": 0.3, "satfat": 0.0, "fiber": 2, "salt": 0.01},
    "avocado": {"kcal": 160, "protein": 2, "carbs": 2, "sugar": 0.7, "fat": 15, "satfat": 2.1, "fiber": 7, "salt": 0.01},

    # toevoegingen
    "olijfolie": {"kcal": 884, "protein": 0, "carbs": 0, "sugar": 0, "fat": 100, "satfat": 14, "fiber": 0, "salt": 0.0},
    "hummus": {"kcal": 220, "protein": 8, "carbs": 14, "sugar": 0.5, "fat": 14, "satfat": 2, "fiber": 6, "salt": 1.2},
}


# Generieke categorie-fallback wanneer een product niet in de lookup zit
CATEGORY_FALLBACK: dict[str, dict[str, float]] = {
    "groente": {"kcal": 30, "protein": 2, "carbs": 5, "sugar": 3, "fat": 0.3, "satfat": 0.1, "fiber": 2, "salt": 0.02},
    "fruit": {"kcal": 60, "protein": 1, "carbs": 14, "sugar": 12, "fat": 0.3, "satfat": 0.0, "fiber": 2, "salt": 0.01},
    "vlees": {"kcal": 200, "protein": 22, "carbs": 0, "sugar": 0, "fat": 12, "satfat": 5, "fiber": 0, "salt": 0.3},
    "vis": {"kcal": 150, "protein": 22, "carbs": 0, "sugar": 0, "fat": 7, "satfat": 1.5, "fiber": 0, "salt": 0.3},
    "ei": {"kcal": 143, "protein": 13, "carbs": 1, "sugar": 1, "fat": 10, "satfat": 3, "fiber": 0, "salt": 0.3},
    "zuivel": {"kcal": 80, "protein": 5, "carbs": 5, "sugar": 5, "fat": 4, "satfat": 2.5, "fiber": 0, "salt": 0.2},
    "zuivelvervanger": {"kcal": 45, "protein": 3, "carbs": 3, "sugar": 2, "fat": 2, "satfat": 0.3, "fiber": 0.5, "salt": 0.1},
    "pasta": {"kcal": 350, "protein": 12, "carbs": 70, "sugar": 3, "fat": 2, "satfat": 0.3, "fiber": 4, "salt": 0.01},
    "rijst": {"kcal": 350, "protein": 7, "carbs": 78, "sugar": 0.5, "fat": 0.5, "satfat": 0.1, "fiber": 1.5, "salt": 0.01},
    "aardappel": {"kcal": 75, "protein": 2, "carbs": 17, "sugar": 0.5, "fat": 0.1, "satfat": 0.0, "fiber": 2, "salt": 0.01},
    "brood": {"kcal": 250, "protein": 9, "carbs": 45, "sugar": 3, "fat": 3, "satfat": 0.5, "fiber": 6, "salt": 1.2},
    "olie": {"kcal": 884, "protein": 0, "carbs": 0, "sugar": 0, "fat": 100, "satfat": 14, "fiber": 0, "salt": 0.0},
    "peulvrucht": {"kcal": 115, "protein": 8, "carbs": 18, "sugar": 1, "fat": 1, "satfat": 0.2, "fiber": 7, "salt": 0.1},
    "vleesvervanger": {"kcal": 130, "protein": 13, "carbs": 3, "sugar": 1, "fat": 7, "satfat": 1, "fiber": 2, "salt": 0.5},
    "spread": {"kcal": 220, "protein": 8, "carbs": 14, "sugar": 1, "fat": 14, "satfat": 2, "fiber": 6, "salt": 1.0},
    "ontbijt": {"kcal": 370, "protein": 12, "carbs": 65, "sugar": 5, "fat": 6, "satfat": 1, "fiber": 8, "salt": 0.3},
}
