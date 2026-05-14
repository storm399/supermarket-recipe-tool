"""Receptsjablonen voor de rule-based generator.

Elk sjabloon definieert benodigde ingrediente n (met zoekwoorden om
aanbiedingen te matchen) en bereidingsstappen. De generator vult de
echte hoeveelheden, prijzen en aanbiedingen in op basis van de input.
"""

from typing import TypedDict


class TemplateIngredient(TypedDict, total=False):
    name: str
    keywords: list[str]
    grams_per_serving: float
    unit: str
    is_pantry: bool
    optional: bool


class RecipeTemplate(TypedDict):
    title: str
    description: str
    instructions: list[str]
    prep_time_minutes: int
    diet_tags: list[str]
    ingredients: list[TemplateIngredient]


RECIPE_TEMPLATES: list[RecipeTemplate] = [
    {
        "title": "Pasta met kipfilet en cherrytomaten",
        "description": "Snelle Italiaanse pasta met malse kip en gerooste tomaatjes.",
        "instructions": [
            "Kook de pasta volgens de aanwijzingen op de verpakking.",
            "Snijd de kipfilet in blokjes en bak goudbruin in olijfolie.",
            "Voeg de gehalveerde cherrytomaten en gesnipperde knoflook toe.",
            "Breng op smaak met Italiaanse kruiden, zout en peper.",
            "Meng de pasta erdoor en serveer met een scheutje olijfolie.",
        ],
        "prep_time_minutes": 25,
        "diet_tags": ["halal"],
        "ingredients": [
            {"name": "Kipfilet", "keywords": ["kipfilet", "kipgehakt"], "grams_per_serving": 150, "unit": "g"},
            {"name": "Pasta", "keywords": ["pasta", "spaghetti", "tagliatelle"], "grams_per_serving": 90, "unit": "g"},
            {"name": "Cherrytomaten", "keywords": ["cherrytomaten", "tomaten"], "grams_per_serving": 120, "unit": "g"},
            {"name": "Knoflook", "keywords": ["knoflook"], "grams_per_serving": 5, "unit": "g", "is_pantry": True},
            {"name": "Olijfolie", "keywords": ["olijfolie"], "grams_per_serving": 10, "unit": "ml", "is_pantry": True},
            {"name": "Italiaanse kruiden", "keywords": ["italiaanse kruiden"], "grams_per_serving": 2, "unit": "g", "is_pantry": True},
        ],
    },
    {
        "title": "Roerbak met tofu en broccoli",
        "description": "Plantaardige roerbak vol eiwit en vezels.",
        "instructions": [
            "Snijd tofu in blokjes, dep droog en bak krokant in een hete pan.",
            "Voeg broccoliroosjes en gesnipperde ui toe en roerbak 5 minuten.",
            "Blus af met sojasaus en een beetje water.",
            "Serveer met rijst.",
        ],
        "prep_time_minutes": 20,
        "diet_tags": ["vegetarisch", "vegan", "lactosevrij"],
        "ingredients": [
            {"name": "Tofu", "keywords": ["tofu"], "grams_per_serving": 150, "unit": "g"},
            {"name": "Broccoli", "keywords": ["broccoli", "bloemkool"], "grams_per_serving": 200, "unit": "g"},
            {"name": "Ui", "keywords": ["ui"], "grams_per_serving": 50, "unit": "g"},
            {"name": "Rijst", "keywords": ["basmati", "rijst"], "grams_per_serving": 80, "unit": "g"},
            {"name": "Sojasaus", "keywords": ["sojasaus"], "grams_per_serving": 10, "unit": "ml", "is_pantry": True},
        ],
    },
    {
        "title": "Zalmfilet uit de oven met spinazie",
        "description": "Omega-3 rijke maaltijd, klaar in een half uur.",
        "instructions": [
            "Verwarm de oven voor op 200°C.",
            "Leg de zalmfilet op bakpapier, besprenkel met olijfolie, zout en peper.",
            "Bak 12-15 minuten in de oven.",
            "Smoor ondertussen de spinazie met knoflook in een pan.",
            "Serveer samen met aardappelen of brood.",
        ],
        "prep_time_minutes": 25,
        "diet_tags": ["lactosevrij", "glutenvrij", "halal"],
        "ingredients": [
            {"name": "Zalmfilet", "keywords": ["zalm", "zalmmoot"], "grams_per_serving": 150, "unit": "g"},
            {"name": "Spinazie", "keywords": ["spinazie"], "grams_per_serving": 150, "unit": "g"},
            {"name": "Aardappelen", "keywords": ["aardappel"], "grams_per_serving": 200, "unit": "g"},
            {"name": "Knoflook", "keywords": ["knoflook"], "grams_per_serving": 5, "unit": "g"},
            {"name": "Olijfolie", "keywords": ["olijfolie"], "grams_per_serving": 10, "unit": "ml", "is_pantry": True},
        ],
    },
    {
        "title": "Linzensoep met wortel en ui",
        "description": "Voedzame plantaardige soep, ideaal voor een budget.",
        "instructions": [
            "Snipper de ui en snijd de wortelen in blokjes.",
            "Fruit ui en wortel in een pan met olijfolie.",
            "Voeg de afgespoelde linzen, een bouillonblokje en 1 liter water toe.",
            "Laat 25 minuten zachtjes koken tot de linzen gaar zijn.",
            "Pureer eventueel deels en breng op smaak met peper.",
        ],
        "prep_time_minutes": 35,
        "diet_tags": ["vegetarisch", "vegan", "lactosevrij", "halal"],
        "ingredients": [
            {"name": "Linzen", "keywords": ["linzen"], "grams_per_serving": 80, "unit": "g"},
            {"name": "Wortelen", "keywords": ["wortel"], "grams_per_serving": 150, "unit": "g"},
            {"name": "Ui", "keywords": ["ui"], "grams_per_serving": 80, "unit": "g"},
            {"name": "Bouillonblokje", "keywords": ["bouillonblokje"], "grams_per_serving": 2, "unit": "g", "is_pantry": True},
            {"name": "Olijfolie", "keywords": ["olijfolie"], "grams_per_serving": 5, "unit": "ml", "is_pantry": True},
        ],
    },
    {
        "title": "Volkoren wraps met hummus en groente",
        "description": "Snelle, vezelrijke lunch.",
        "instructions": [
            "Smeer elke wrap in met hummus.",
            "Verdeel reepjes paprika, komkommer en eventueel sla erover.",
            "Rol stevig op en snijd schuin doormidden.",
        ],
        "prep_time_minutes": 10,
        "diet_tags": ["vegetarisch", "vegan", "lactosevrij", "halal"],
        "ingredients": [
            {"name": "Volkoren wraps", "keywords": ["wraps", "wrap"], "grams_per_serving": 80, "unit": "g"},
            {"name": "Hummus", "keywords": ["hummus"], "grams_per_serving": 60, "unit": "g"},
            {"name": "Paprika", "keywords": ["paprika"], "grams_per_serving": 100, "unit": "g"},
            {"name": "Komkommer", "keywords": ["komkommer"], "grams_per_serving": 80, "unit": "g"},
        ],
    },
    {
        "title": "Kikkererwten curry met rijst",
        "description": "Geurige plantaardige curry met veel eiwit en vezels.",
        "instructions": [
            "Fruit gesnipperde ui en knoflook in olijfolie.",
            "Voeg kerriepoeder en kurkuma toe en bak kort mee.",
            "Doe de afgespoelde kikkererwten, tomaten en een scheut water erbij.",
            "Laat 15 minuten zachtjes koken.",
            "Serveer met gekookte basmati rijst.",
        ],
        "prep_time_minutes": 30,
        "diet_tags": ["vegetarisch", "vegan", "lactosevrij", "glutenvrij", "halal"],
        "ingredients": [
            {"name": "Kikkererwten", "keywords": ["kikkererwten"], "grams_per_serving": 150, "unit": "g"},
            {"name": "Tomaten", "keywords": ["tomaten", "cherrytomaten"], "grams_per_serving": 120, "unit": "g"},
            {"name": "Ui", "keywords": ["ui"], "grams_per_serving": 60, "unit": "g"},
            {"name": "Knoflook", "keywords": ["knoflook"], "grams_per_serving": 5, "unit": "g"},
            {"name": "Rijst", "keywords": ["basmati", "rijst"], "grams_per_serving": 80, "unit": "g"},
            {"name": "Kerriepoeder", "keywords": ["kerrie"], "grams_per_serving": 2, "unit": "g", "is_pantry": True},
        ],
    },
    {
        "title": "Pasta bolognese met rundergehakt",
        "description": "Klassieker met saus van tomaat en gehakt.",
        "instructions": [
            "Bak het rundergehakt rul in olijfolie.",
            "Voeg gesnipperde ui, knoflook en wortel toe.",
            "Voeg gepelde tomaten of verse tomaten en Italiaanse kruiden toe.",
            "Laat 20 minuten zachtjes pruttelen.",
            "Kook intussen de pasta en serveer met de saus.",
        ],
        "prep_time_minutes": 35,
        "diet_tags": ["halal"],
        "ingredients": [
            {"name": "Rundergehakt", "keywords": ["rundergehakt", "gehakt"], "grams_per_serving": 125, "unit": "g"},
            {"name": "Pasta", "keywords": ["pasta", "spaghetti", "tagliatelle"], "grams_per_serving": 90, "unit": "g"},
            {"name": "Tomaten", "keywords": ["tomaten", "cherrytomaten"], "grams_per_serving": 150, "unit": "g"},
            {"name": "Ui", "keywords": ["ui"], "grams_per_serving": 60, "unit": "g"},
            {"name": "Wortelen", "keywords": ["wortel"], "grams_per_serving": 60, "unit": "g"},
            {"name": "Knoflook", "keywords": ["knoflook"], "grams_per_serving": 5, "unit": "g"},
        ],
    },
    {
        "title": "Omelet met champignons en spinazie",
        "description": "Eiwitrijk en snel.",
        "instructions": [
            "Snijd de champignons in plakjes en bak in olijfolie.",
            "Voeg spinazie toe tot deze geslonken is.",
            "Klop de eieren los met peper en zout en giet in de pan.",
            "Bak op laag vuur tot de omelet gestold is.",
        ],
        "prep_time_minutes": 15,
        "diet_tags": ["vegetarisch", "glutenvrij", "halal"],
        "ingredients": [
            {"name": "Eieren", "keywords": ["eieren"], "grams_per_serving": 120, "unit": "g"},
            {"name": "Champignons", "keywords": ["champignons"], "grams_per_serving": 100, "unit": "g"},
            {"name": "Spinazie", "keywords": ["spinazie"], "grams_per_serving": 80, "unit": "g"},
            {"name": "Olijfolie", "keywords": ["olijfolie"], "grams_per_serving": 5, "unit": "ml", "is_pantry": True},
        ],
    },
]
