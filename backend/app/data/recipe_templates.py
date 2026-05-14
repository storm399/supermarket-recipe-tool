"""Receptsjablonen met uitgebreide bereidingsstappen.

Elk sjabloon heeft 6+ concrete kookstappen, type-info, allergenen,
serveer/bewaartips, variaties en een 'waarom slim met aanbiedingen'.
"""
from __future__ import annotations

from typing import TypedDict


class TemplateIngredient(TypedDict, total=False):
    name: str
    keywords: list[str]
    grams_per_serving: float
    unit: str
    is_pantry: bool


class RecipeTemplate(TypedDict, total=False):
    title: str
    description: str
    meal_type: str
    difficulty: str
    prep_time_minutes: int
    cook_time_minutes: int
    diet_tags: list[str]
    allergens: list[str]
    serving_tips: list[str]
    storage_tips: list[str]
    variations: list[str]
    why_smart: str
    image_key: str
    instructions: list[str]
    ingredients: list[TemplateIngredient]


def _kip_pasta() -> RecipeTemplate:
    return {
        "title": "Pasta met kipfilet en cherrytomaten",
        "description": "Snelle Italiaanse pasta met malse kip en geroosterde tomaatjes.",
        "meal_type": "diner",
        "difficulty": "makkelijk",
        "prep_time_minutes": 10,
        "cook_time_minutes": 15,
        "diet_tags": ["halal"],
        "allergens": ["gluten"],
        "image_key": "pasta",
        "why_smart": "Volkoren pasta en kipfilet zijn vaak in de bonus; cherrytomaten en knoflook maken er een complete maaltijd van.",
        "serving_tips": ["Strooi er geraspte Parmezaan over.", "Lekker met een groene salade ernaast."],
        "storage_tips": ["1-2 dagen houdbaar in de koelkast.", "Niet invriezen — pasta wordt papperig."],
        "variations": ["Vervang kip door garnalen.", "Gebruik volkoren penne voor extra vezels."],
        "instructions": [
            "Breng een ruime pan water aan de kook met een snuf zout.",
            "Snijd ondertussen de kipfilet in blokjes van ongeveer 2 cm.",
            "Verhit een eetlepel olijfolie in een koekenpan op middelhoog vuur en bak de kip in 6-8 minuten goudbruin en gaar.",
            "Halveer de cherrytomaten en snipper 2 teentjes knoflook fijn.",
            "Doe pasta in het kokende water en kook volgens de aanwijzingen op de verpakking (meestal 9-11 minuten).",
            "Voeg de tomaten en knoflook bij de kip, bak 3-4 minuten en breng op smaak met Italiaanse kruiden, peper en zout.",
            "Giet de pasta af en bewaar een klein kopje kookvocht.",
            "Schep de pasta door de kip-tomatensaus en voeg eventueel een scheutje kookvocht toe voor een romige saus. Serveer direct.",
        ],
        "ingredients": [
            {"name": "Kipfilet", "keywords": ["kipfilet", "kipgehakt"], "grams_per_serving": 150, "unit": "g"},
            {"name": "Pasta", "keywords": ["pasta", "spaghetti", "tagliatelle", "penne"], "grams_per_serving": 90, "unit": "g"},
            {"name": "Cherrytomaten", "keywords": ["cherrytomaten", "roma tomaten"], "grams_per_serving": 120, "unit": "g"},
            {"name": "Knoflook", "keywords": ["knoflook"], "grams_per_serving": 5, "unit": "g", "is_pantry": True},
            {"name": "Olijfolie", "keywords": ["olijfolie"], "grams_per_serving": 10, "unit": "ml", "is_pantry": True},
            {"name": "Italiaanse kruiden", "keywords": ["italiaanse kruiden"], "grams_per_serving": 2, "unit": "g", "is_pantry": True},
        ],
    }


def _tofu_roerbak() -> RecipeTemplate:
    return {
        "title": "Tofu-roerbak met broccoli en rijst",
        "description": "Plantaardige roerbak vol eiwit, vezels en umami.",
        "meal_type": "diner",
        "difficulty": "makkelijk",
        "prep_time_minutes": 10,
        "cook_time_minutes": 15,
        "diet_tags": ["vegetarisch", "vegan", "lactosevrij"],
        "allergens": ["soja"],
        "image_key": "roerbak",
        "why_smart": "Tofu en broccoli zijn vaak in de bonus; sojasaus en knoflook heb je meestal in huis.",
        "serving_tips": ["Lekker met een paar zaadjes sesamzaad.", "Voeg een halve limoen toe voor frisheid."],
        "storage_tips": ["2-3 dagen houdbaar in een goed afgesloten bakje.", "Roerbak warm je het beste op in de koekenpan."],
        "variations": ["Vervang tofu door tempeh.", "Voeg cashewnoten toe voor extra crunch.", "Gebruik volkoren rijst voor meer vezels."],
        "instructions": [
            "Dep de tofu droog met keukenpapier en snijd in blokjes van 2 cm.",
            "Spoel de rijst kort af onder koud water en kook 12 minuten met dubbele hoeveelheid water; laat 5 minuten wellen.",
            "Verhit 1 el olie in een wok op hoog vuur en bak de tofu rondom goudbruin (5-7 minuten).",
            "Snijd ondertussen de broccoli in kleine roosjes en snipper de ui en knoflook.",
            "Schep de tofu uit de pan en bak in dezelfde pan de ui en knoflook 2 minuten.",
            "Voeg de broccoli toe met een scheutje water, leg het deksel op de pan en stoom 4 minuten.",
            "Doe de tofu terug, voeg sojasaus en eventueel chili toe en roerbak nog 2 minuten.",
            "Serveer de roerbak op de rijst.",
        ],
        "ingredients": [
            {"name": "Tofu", "keywords": ["tofu", "tempeh"], "grams_per_serving": 150, "unit": "g"},
            {"name": "Broccoli", "keywords": ["broccoli", "bloemkool"], "grams_per_serving": 200, "unit": "g"},
            {"name": "Ui", "keywords": ["ui"], "grams_per_serving": 50, "unit": "g"},
            {"name": "Rijst", "keywords": ["basmati rijst", "rijst", "volkoren rijst"], "grams_per_serving": 80, "unit": "g"},
            {"name": "Knoflook", "keywords": ["knoflook"], "grams_per_serving": 5, "unit": "g", "is_pantry": True},
            {"name": "Sojasaus", "keywords": ["sojasaus"], "grams_per_serving": 15, "unit": "ml", "is_pantry": True},
        ],
    }


def _zalm_oven() -> RecipeTemplate:
    return {
        "title": "Zalmfilet uit de oven met spinazie en aardappel",
        "description": "Omega-3 rijke maaltijd met groene smaakmakers.",
        "meal_type": "diner",
        "difficulty": "makkelijk",
        "prep_time_minutes": 10,
        "cook_time_minutes": 20,
        "diet_tags": ["lactosevrij", "glutenvrij", "halal"],
        "allergens": ["vis"],
        "image_key": "zalm",
        "why_smart": "Zalmfilet is regelmatig in de aanbieding; spinazie en aardappels zijn budgetvriendelijke begeleiders.",
        "serving_tips": ["Knijp een schijfje citroen over de zalm voor het serveren.", "Lekker met een dot Griekse yoghurt."],
        "storage_tips": ["Resten 1 dag houdbaar in de koelkast.", "Zalm laat zich slecht opwarmen — gebruik koud in een salade."],
        "variations": ["Vervang zalm door pangasiusfilet.", "Strooi sesamzaad over de zalm voor een Aziatische twist.", "Voeg cherrytomaten toe in de ovenschaal."],
        "instructions": [
            "Verwarm de oven voor op 200°C boven- en onderwarmte.",
            "Schil en snijd de aardappels in partjes en kook 10 minuten in licht gezouten water.",
            "Bekleed een bakplaat met bakpapier en leg de zalmfilet erop.",
            "Besprenkel de zalm met 1 el olijfolie, peper, zout en eventueel een snufje paprikapoeder.",
            "Bak de zalm 12-15 minuten in de oven tot hij rosé van binnen is.",
            "Verhit ondertussen 1 el olijfolie in een pan, fruit 1 teentje knoflook 30 seconden en voeg de spinazie toe.",
            "Roer de spinazie tot deze geslonken is (2-3 minuten) en breng op smaak met peper en zout.",
            "Schep aardappel, spinazie en zalm op een bord en serveer direct.",
        ],
        "ingredients": [
            {"name": "Zalmfilet", "keywords": ["zalm", "zalmmoot", "zalmfilet"], "grams_per_serving": 150, "unit": "g"},
            {"name": "Spinazie", "keywords": ["spinazie"], "grams_per_serving": 150, "unit": "g"},
            {"name": "Aardappelen", "keywords": ["aardappel"], "grams_per_serving": 200, "unit": "g"},
            {"name": "Knoflook", "keywords": ["knoflook"], "grams_per_serving": 5, "unit": "g"},
            {"name": "Olijfolie", "keywords": ["olijfolie"], "grams_per_serving": 10, "unit": "ml", "is_pantry": True},
        ],
    }


def _linzensoep() -> RecipeTemplate:
    return {
        "title": "Marokkaanse linzensoep",
        "description": "Voedzame plantaardige soep met een vleugje komijn en kurkuma.",
        "meal_type": "lunch",
        "difficulty": "makkelijk",
        "prep_time_minutes": 10,
        "cook_time_minutes": 25,
        "diet_tags": ["vegetarisch", "vegan", "lactosevrij", "halal"],
        "allergens": [],
        "image_key": "soep",
        "why_smart": "Linzen, ui en wortel zijn budgetfavorieten en haast altijd in de aanbieding. Een ideale maaltijd voor weinig geld.",
        "serving_tips": ["Garneer met een eetlepel yoghurt en verse koriander.", "Eet de soep met een sneetje volkoren brood."],
        "storage_tips": ["3 dagen houdbaar in de koelkast.", "Goed te invriezen in porties tot 3 maanden."],
        "variations": ["Voeg een blik tomaten toe voor een vollere smaak.", "Gebruik rode peper voor wat extra pit.", "Vervang linzen door kikkererwten."],
        "instructions": [
            "Snipper de ui en snijd de wortelen in blokjes van 1 cm.",
            "Verhit 1 el olijfolie in een soeppan op middelhoog vuur en fruit de ui 4 minuten glazig.",
            "Voeg de wortel, een theelepel komijn en een theelepel kurkuma toe en bak 2 minuten mee.",
            "Spoel de linzen af onder koud water en doe ze samen met een bouillonblokje in de pan.",
            "Giet er 1 liter water bij, breng aan de kook en laat met deksel 20-25 minuten zachtjes pruttelen tot de linzen gaar zijn.",
            "Pureer eventueel een deel van de soep met een staafmixer voor een romige textuur.",
            "Breng op smaak met peper, zout en een scheutje citroensap.",
            "Schep in kommen en serveer met yoghurt, koriander en brood.",
        ],
        "ingredients": [
            {"name": "Linzen", "keywords": ["linzen"], "grams_per_serving": 80, "unit": "g"},
            {"name": "Wortelen", "keywords": ["wortel"], "grams_per_serving": 150, "unit": "g"},
            {"name": "Ui", "keywords": ["ui"], "grams_per_serving": 80, "unit": "g"},
            {"name": "Bouillonblokje", "keywords": ["bouillonblokje"], "grams_per_serving": 2, "unit": "g", "is_pantry": True},
            {"name": "Olijfolie", "keywords": ["olijfolie"], "grams_per_serving": 5, "unit": "ml", "is_pantry": True},
        ],
    }


def _wrap_hummus() -> RecipeTemplate:
    return {
        "title": "Volkoren wraps met hummus en knapperige groente",
        "description": "Snelle, vezelrijke lunchwrap die je in 10 minuten klaar hebt.",
        "meal_type": "lunch",
        "difficulty": "makkelijk",
        "prep_time_minutes": 10,
        "cook_time_minutes": 0,
        "diet_tags": ["vegetarisch", "vegan", "lactosevrij", "halal"],
        "allergens": ["gluten", "sesam"],
        "image_key": "wrap",
        "why_smart": "Wraps en hummus liggen vaak in de bonus en groente uit de aanbieding maakt de wrap voller.",
        "serving_tips": ["Snijd schuin doormidden voor een mooi presentatie.", "Wikkel in bakpapier voor onderweg."],
        "storage_tips": ["Eet binnen 1 dag op.", "Niet invriezen — wrap wordt slap."],
        "variations": ["Voeg geroosterde kip toe als je geen vegetarische versie wilt.", "Gebruik tzatziki in plaats van hummus.", "Strooi pijnboompitten erover."],
        "instructions": [
            "Snijd de paprika in dunne reepjes en de komkommer in plakjes.",
            "Was de sla en dep droog.",
            "Verwarm de wraps kort in een droge koekenpan (10 seconden per kant) zodat ze soepel worden.",
            "Smeer elke wrap in met een ruime eetlepel hummus.",
            "Leg sla, paprika en komkommer in het midden van de wrap.",
            "Strooi peper en eventueel een snuf paprikapoeder erover.",
            "Vouw de zijkanten in en rol de wrap strak op.",
            "Snijd schuin doormidden en serveer direct.",
        ],
        "ingredients": [
            {"name": "Volkoren wraps", "keywords": ["wraps", "wrap", "pitabroodjes"], "grams_per_serving": 80, "unit": "g"},
            {"name": "Hummus", "keywords": ["hummus"], "grams_per_serving": 60, "unit": "g"},
            {"name": "Paprika", "keywords": ["paprika"], "grams_per_serving": 100, "unit": "g"},
            {"name": "Komkommer", "keywords": ["komkommer"], "grams_per_serving": 80, "unit": "g"},
            {"name": "IJsbergsla", "keywords": ["sla", "ijsbergsla", "veldsla"], "grams_per_serving": 30, "unit": "g"},
        ],
    }


def _kikkererwten_curry() -> RecipeTemplate:
    return {
        "title": "Kikkererwten-curry met basmati rijst",
        "description": "Geurige plantaardige curry met veel eiwit en vezels.",
        "meal_type": "diner",
        "difficulty": "makkelijk",
        "prep_time_minutes": 10,
        "cook_time_minutes": 20,
        "diet_tags": ["vegetarisch", "vegan", "lactosevrij", "glutenvrij", "halal"],
        "allergens": [],
        "image_key": "curry",
        "why_smart": "Kikkererwten, tomaten en rijst zijn standaard budgetfavorieten in elke aanbiedingsfolder.",
        "serving_tips": ["Bestrooi met verse koriander.", "Lekker met een lepel yoghurt erop."],
        "storage_tips": ["3 dagen houdbaar.", "Smaak ontwikkelt zich verder op dag 2 — perfect voor meal prep."],
        "variations": ["Voeg een handje spinazie toe op het einde.", "Gebruik kokosmelk voor een romigere curry.", "Vervang rijst door couscous."],
        "instructions": [
            "Snipper de ui en snijd de knoflook fijn.",
            "Verhit 1 el olijfolie in een hapjespan op middelhoog vuur en fruit de ui 5 minuten.",
            "Voeg knoflook, 2 tl kerriepoeder en 1 tl kurkuma toe en bak 30 seconden mee voor de geur.",
            "Voeg de gepelde tomaten en een scheut water toe en breng aan de kook.",
            "Roer de afgespoelde kikkererwten erdoor en laat 15 minuten zachtjes pruttelen.",
            "Kook ondertussen de basmati rijst in dubbele hoeveelheid water in 12 minuten gaar.",
            "Breng de curry op smaak met peper, zout en een scheutje citroensap.",
            "Serveer de curry op de rijst.",
        ],
        "ingredients": [
            {"name": "Kikkererwten", "keywords": ["kikkererwten"], "grams_per_serving": 150, "unit": "g"},
            {"name": "Gepelde tomaten", "keywords": ["gepelde tomaten", "tomaten", "cherrytomaten"], "grams_per_serving": 150, "unit": "g"},
            {"name": "Ui", "keywords": ["ui"], "grams_per_serving": 60, "unit": "g"},
            {"name": "Knoflook", "keywords": ["knoflook"], "grams_per_serving": 5, "unit": "g"},
            {"name": "Basmati rijst", "keywords": ["basmati rijst", "rijst"], "grams_per_serving": 80, "unit": "g"},
            {"name": "Kerriepoeder", "keywords": ["kerrie"], "grams_per_serving": 2, "unit": "g", "is_pantry": True},
            {"name": "Olijfolie", "keywords": ["olijfolie"], "grams_per_serving": 5, "unit": "ml", "is_pantry": True},
        ],
    }


def _bolognese() -> RecipeTemplate:
    return {
        "title": "Spaghetti bolognese",
        "description": "Klassieker met traag gegaarde saus van tomaat en gehakt.",
        "meal_type": "diner",
        "difficulty": "gemiddeld",
        "prep_time_minutes": 10,
        "cook_time_minutes": 30,
        "diet_tags": ["halal"],
        "allergens": ["gluten"],
        "image_key": "pasta",
        "why_smart": "Rundergehakt en spaghetti zijn topfavorieten in folders; tomaten in de aanbieding maken een echte ragu.",
        "serving_tips": ["Bestrooi met geraspte Parmezaan en verse basilicum.", "Een glas tomatensap erbij verlengt de saus."],
        "storage_tips": ["Saus is 3 dagen houdbaar en wordt lekkerder op dag 2.", "Saus is goed te invriezen tot 3 maanden."],
        "variations": ["Voeg een wortel en stengel bleekselderij toe (soffrito).", "Gebruik tagliatelle voor een traditionele variant.", "Voeg een scheutje rode wijn toe."],
        "instructions": [
            "Snipper de ui en snijd de knoflook fijn.",
            "Verhit 1 el olijfolie in een hapjespan en bak het gehakt rul op middelhoog vuur (5-7 minuten).",
            "Voeg de ui en knoflook toe en bak 3 minuten mee tot de ui glazig is.",
            "Schep de tomaten erbij en voeg 1 tl Italiaanse kruiden, peper en zout toe.",
            "Laat de saus zonder deksel 20 minuten zachtjes pruttelen, roer af en toe.",
            "Breng intussen een grote pan water aan de kook en kook de spaghetti volgens de verpakking (meestal 9-11 minuten).",
            "Proef de saus en breng op smaak; voeg eventueel een snuf suiker toe als de tomaten wat zuur zijn.",
            "Giet de pasta af, schep de bolognese erop en serveer met Parmezaan.",
        ],
        "ingredients": [
            {"name": "Rundergehakt", "keywords": ["rundergehakt", "gehakt"], "grams_per_serving": 125, "unit": "g"},
            {"name": "Pasta", "keywords": ["pasta", "spaghetti", "tagliatelle"], "grams_per_serving": 90, "unit": "g"},
            {"name": "Tomaten", "keywords": ["gepelde tomaten", "tomaten", "cherrytomaten"], "grams_per_serving": 150, "unit": "g"},
            {"name": "Ui", "keywords": ["ui"], "grams_per_serving": 60, "unit": "g"},
            {"name": "Knoflook", "keywords": ["knoflook"], "grams_per_serving": 5, "unit": "g"},
            {"name": "Italiaanse kruiden", "keywords": ["italiaanse kruiden"], "grams_per_serving": 2, "unit": "g", "is_pantry": True},
            {"name": "Olijfolie", "keywords": ["olijfolie"], "grams_per_serving": 10, "unit": "ml", "is_pantry": True},
        ],
    }


def _omelet_champignons() -> RecipeTemplate:
    return {
        "title": "Omelet met champignons en spinazie",
        "description": "Eiwitrijke, snelle maaltijd voor lunch of avondeten.",
        "meal_type": "lunch",
        "difficulty": "makkelijk",
        "prep_time_minutes": 5,
        "cook_time_minutes": 10,
        "diet_tags": ["vegetarisch", "glutenvrij", "halal"],
        "allergens": ["ei"],
        "image_key": "ei",
        "why_smart": "Eieren zijn vaak in de bonus, en met aanbieding-champignons en spinazie maak je een complete lunch.",
        "serving_tips": ["Lekker met een sneetje volkoren brood.", "Strooi geraspte oude kaas erover."],
        "storage_tips": ["Het lekkerst direct uit de pan.", "Restjes 1 dag houdbaar, opwarmen op laag vuur."],
        "variations": ["Voeg cherrytomaten toe.", "Vervang spinazie door rucola.", "Maak er een open frittata van in de oven."],
        "instructions": [
            "Veeg de champignons schoon met een doekje en snijd in plakjes.",
            "Verhit 1 el olijfolie in een koekenpan op middelhoog vuur en bak de champignons 4-5 minuten goudbruin.",
            "Voeg de spinazie toe en roer tot deze geslonken is (2 minuten).",
            "Klop de eieren los in een kom met peper en zout.",
            "Verdeel de groente over de pan en giet de eieren erover.",
            "Laat 2 minuten op laag vuur stollen en til de randen op zodat het rauwe ei eronder kan lopen.",
            "Dek de pan af met een deksel en gaar nog 2-3 minuten.",
            "Vouw dubbel met een spatel en laat op een bord glijden.",
        ],
        "ingredients": [
            {"name": "Eieren", "keywords": ["eieren"], "grams_per_serving": 120, "unit": "g"},
            {"name": "Champignons", "keywords": ["champignons"], "grams_per_serving": 100, "unit": "g"},
            {"name": "Spinazie", "keywords": ["spinazie"], "grams_per_serving": 80, "unit": "g"},
            {"name": "Olijfolie", "keywords": ["olijfolie"], "grams_per_serving": 5, "unit": "ml", "is_pantry": True},
        ],
    }


def _overnight_oats() -> RecipeTemplate:
    return {
        "title": "Overnight oats met banaan en blauwe bessen",
        "description": "Vezelrijk ontbijt dat je avond van tevoren klaarzet.",
        "meal_type": "ontbijt",
        "difficulty": "makkelijk",
        "prep_time_minutes": 5,
        "cook_time_minutes": 0,
        "diet_tags": ["vegetarisch", "halal"],
        "allergens": ["gluten", "lactose"],
        "image_key": "ontbijt",
        "why_smart": "Havermout en zuivel zijn structurele basis-aanbiedingen; bessen en bananen variëren in de folder.",
        "serving_tips": ["Voeg een lepel honing toe voor wie het wat zoeter wil.", "Top met geroosterde noten voor crunch."],
        "storage_tips": ["Maximaal 2 dagen houdbaar in de koelkast.", "Niet invriezen."],
        "variations": ["Vervang melk door sojadrink voor de vegan versie.", "Gebruik appel en kaneel in plaats van banaan.", "Roer een lepel pindakaas erdoor."],
        "instructions": [
            "Pak een glazen pot of bakje met deksel.",
            "Doe de havermout erin en voeg de melk of yoghurt toe.",
            "Voeg een mespunt kaneel en eventueel 1 tl honing toe en roer goed.",
            "Pers een kwart banaan tot moes en roer door het mengsel; bewaar de rest voor de topping.",
            "Schep de blauwe bessen en de plakjes banaan erop.",
            "Sluit het bakje en zet minstens 4 uur (bij voorkeur 8) in de koelkast.",
            "Roer het geheel kort door voor het serveren.",
            "Lekker met een lepel pindakaas of geroosterde noten.",
        ],
        "ingredients": [
            {"name": "Havermout", "keywords": ["havermout", "haver"], "grams_per_serving": 50, "unit": "g"},
            {"name": "Yoghurt", "keywords": ["yoghurt", "magere yoghurt", "griekse yoghurt"], "grams_per_serving": 150, "unit": "g"},
            {"name": "Banaan", "keywords": ["bananen", "banaan"], "grams_per_serving": 100, "unit": "g"},
            {"name": "Blauwe bessen", "keywords": ["blauwe bessen", "bessen"], "grams_per_serving": 40, "unit": "g"},
        ],
    }


def _scrambled_eggs_toast() -> RecipeTemplate:
    return {
        "title": "Roerei op volkoren toast met avocado",
        "description": "Eiwitrijk ontbijt met goede vetten en vezels.",
        "meal_type": "ontbijt",
        "difficulty": "makkelijk",
        "prep_time_minutes": 5,
        "cook_time_minutes": 8,
        "diet_tags": ["vegetarisch", "halal"],
        "allergens": ["ei", "gluten"],
        "image_key": "ei",
        "why_smart": "Eieren en brood zijn vrijwel altijd in de bonus; avocado maakt er een feestje van.",
        "serving_tips": ["Strooi cayennepeper of chili-flakes erover voor wat pit.", "Verse bieslook geeft een mooie look."],
        "storage_tips": ["Het lekkerst direct, restjes maximaal 1 dag.", "Roerei niet invriezen."],
        "variations": ["Voeg gerookte zalm toe als je vlees/vis mag.", "Gebruik geroosterde paprika als topping."],
        "instructions": [
            "Rooster 2 sneetjes volkoren brood in een broodrooster of koekenpan.",
            "Halveer de avocado, verwijder de pit en schep het vruchtvlees uit de schil.",
            "Prak de avocado met een vork en breng op smaak met peper, zout en een paar druppels citroensap.",
            "Klop de eieren los in een kom met een snuf zout.",
            "Verhit 1 tl boter in een koekenpan op laag vuur en giet de eieren erin.",
            "Roer rustig met een spatel; haal van het vuur zodra het ei nog net iets nat is (overgaarte is voorkomen).",
            "Smeer de avocado op de toast en schep het roerei erop.",
            "Strooi peper en eventueel verse bieslook erover.",
        ],
        "ingredients": [
            {"name": "Eieren", "keywords": ["eieren"], "grams_per_serving": 100, "unit": "g"},
            {"name": "Brood", "keywords": ["volkoren brood", "bruin brood", "brood"], "grams_per_serving": 60, "unit": "g"},
            {"name": "Avocado", "keywords": ["avocado"], "grams_per_serving": 80, "unit": "g"},
            {"name": "Boter", "keywords": ["boter", "roomboter"], "grams_per_serving": 5, "unit": "g", "is_pantry": True},
        ],
    }


def _greek_salad() -> RecipeTemplate:
    return {
        "title": "Griekse salade met feta en olijven",
        "description": "Frisse Mediterrane salade vol smaak.",
        "meal_type": "lunch",
        "difficulty": "makkelijk",
        "prep_time_minutes": 10,
        "cook_time_minutes": 0,
        "diet_tags": ["vegetarisch", "glutenvrij", "halal"],
        "allergens": ["lactose"],
        "image_key": "salade",
        "why_smart": "Komkommer, tomaten en mozzarella/feta zijn vaak in de bonus; samen heb je een complete maaltijd.",
        "serving_tips": ["Lekker met pitabroodjes en hummus erbij.", "Strooi gedroogde oregano erover."],
        "storage_tips": ["Het lekkerst meteen na bereiding.", "Maximaal 1 dag houdbaar, dressing dan apart bewaren."],
        "variations": ["Vervang olijven door kappertjes.", "Voeg een handje rucola toe.", "Top met geroosterde pijnboompitten."],
        "instructions": [
            "Snijd de tomaten in partjes en de komkommer in halve maantjes.",
            "Snijd de rode ui (of gewone ui) in heel dunne ringen.",
            "Verbrokkel de mozzarella in grove stukken.",
            "Schep de groente en kaas in een kom en voeg olijven toe.",
            "Maak een dressing van 3 el olijfolie, 1 el rode wijnazijn, peper en zout.",
            "Schenk de dressing over de salade en hussel voorzichtig.",
            "Bestrooi met gedroogde oregano en kraak er versgemalen peper over.",
            "Laat 5 minuten staan zodat de smaken trekken en serveer.",
        ],
        "ingredients": [
            {"name": "Tomaten", "keywords": ["tomaten", "cherrytomaten", "roma tomaten"], "grams_per_serving": 150, "unit": "g"},
            {"name": "Komkommer", "keywords": ["komkommer"], "grams_per_serving": 100, "unit": "g"},
            {"name": "Mozzarella", "keywords": ["mozzarella", "kaas"], "grams_per_serving": 60, "unit": "g"},
            {"name": "Rode ui", "keywords": ["rode ui", "ui"], "grams_per_serving": 30, "unit": "g"},
            {"name": "Olijven", "keywords": ["olijven"], "grams_per_serving": 30, "unit": "g"},
            {"name": "Olijfolie", "keywords": ["olijfolie"], "grams_per_serving": 10, "unit": "ml", "is_pantry": True},
        ],
    }


def _couscous_groente() -> RecipeTemplate:
    return {
        "title": "Couscous-salade met geroosterde paprika en kikkererwten",
        "description": "Kleurrijke meal-prep salade voor lunch of bijgerecht.",
        "meal_type": "meal-prep",
        "difficulty": "makkelijk",
        "prep_time_minutes": 10,
        "cook_time_minutes": 20,
        "diet_tags": ["vegetarisch", "vegan", "lactosevrij", "halal"],
        "allergens": ["gluten"],
        "image_key": "salade",
        "why_smart": "Couscous, kikkererwten en paprika zijn structurele aanbiedingen — perfecte basis voor een grote schaal salade.",
        "serving_tips": ["Strooi munt of peterselie erover.", "Voeg feta toe voor extra zoutigheid."],
        "storage_tips": ["3 dagen houdbaar in een goed afgesloten bakje.", "Niet invriezen — couscous wordt korrelig."],
        "variations": ["Voeg geroosterde halloumi toe.", "Gebruik bulgur of quinoa in plaats van couscous.", "Top met granaatappelpitjes voor zoete bite."],
        "instructions": [
            "Verwarm de oven voor op 200°C.",
            "Snijd de paprika in repen en hussel met 1 el olijfolie, peper en zout.",
            "Verdeel de paprika over een met bakpapier beklede plaat en rooster 20 minuten in de oven.",
            "Breng 200 ml water aan de kook met een snuf zout, doe de couscous erbij, dek af en laat 5 minuten wellen.",
            "Spoel ondertussen de kikkererwten af onder koud water en laat uitlekken.",
            "Snijd de cherrytomaten doormidden.",
            "Schep de couscous los met een vork en meng met de kikkererwten, tomaten en geroosterde paprika.",
            "Werk af met een dressing van 2 el olijfolie, sap van een halve citroen, peper en zout.",
        ],
        "ingredients": [
            {"name": "Couscous", "keywords": ["couscous"], "grams_per_serving": 70, "unit": "g"},
            {"name": "Paprika", "keywords": ["paprika", "rode paprika"], "grams_per_serving": 150, "unit": "g"},
            {"name": "Kikkererwten", "keywords": ["kikkererwten"], "grams_per_serving": 100, "unit": "g"},
            {"name": "Cherrytomaten", "keywords": ["cherrytomaten", "tomaten"], "grams_per_serving": 80, "unit": "g"},
            {"name": "Olijfolie", "keywords": ["olijfolie"], "grams_per_serving": 15, "unit": "ml", "is_pantry": True},
            {"name": "Citroensap", "keywords": ["citroensap"], "grams_per_serving": 10, "unit": "ml", "is_pantry": True},
        ],
    }


def _tonijnsalade() -> RecipeTemplate:
    return {
        "title": "Tonijnsalade met witte bonen",
        "description": "Eiwitrijke salade die je in 10 minuten op tafel hebt.",
        "meal_type": "lunch",
        "difficulty": "makkelijk",
        "prep_time_minutes": 10,
        "cook_time_minutes": 0,
        "diet_tags": ["lactosevrij", "glutenvrij", "halal"],
        "allergens": ["vis"],
        "image_key": "salade",
        "why_smart": "Tonijn in blik en bonen zijn budgetvriendelijke houdbare aanbiedingen — ideaal voor snelle lunches.",
        "serving_tips": ["Lekker op een sneetje volkoren brood.", "Voeg gehakte peterselie toe."],
        "storage_tips": ["2 dagen houdbaar in de koelkast.", "Niet invriezen."],
        "variations": ["Vervang witte bonen door kikkererwten.", "Voeg gekookt ei toe.", "Gebruik kappertjes voor extra zout-zuur."],
        "instructions": [
            "Laat de tonijn goed uitlekken boven de gootsteen.",
            "Spoel de witte bonen af onder koud water en laat ook uitlekken.",
            "Snijd de rode ui zo fijn mogelijk.",
            "Halveer de cherrytomaten.",
            "Schep alles samen in een kom.",
            "Meng een dressing van 2 el olijfolie, sap van een halve citroen, peper en zout.",
            "Schep de dressing door de salade en proef of er nog peper of citroen bij moet.",
            "Laat 5 minuten staan en serveer.",
        ],
        "ingredients": [
            {"name": "Tonijn in blik", "keywords": ["tonijn"], "grams_per_serving": 80, "unit": "g"},
            {"name": "Witte bonen", "keywords": ["witte bonen", "bonen"], "grams_per_serving": 120, "unit": "g"},
            {"name": "Cherrytomaten", "keywords": ["cherrytomaten", "tomaten"], "grams_per_serving": 80, "unit": "g"},
            {"name": "Rode ui", "keywords": ["rode ui", "ui"], "grams_per_serving": 30, "unit": "g"},
            {"name": "Olijfolie", "keywords": ["olijfolie"], "grams_per_serving": 10, "unit": "ml", "is_pantry": True},
            {"name": "Citroensap", "keywords": ["citroensap"], "grams_per_serving": 10, "unit": "ml", "is_pantry": True},
        ],
    }


def _aardappel_ovenschotel() -> RecipeTemplate:
    return {
        "title": "Aardappel-ovenschotel met champignons en kaas",
        "description": "Comforting ovenschotel die genoeg is voor 2 dagen.",
        "meal_type": "diner",
        "difficulty": "gemiddeld",
        "prep_time_minutes": 15,
        "cook_time_minutes": 35,
        "diet_tags": ["vegetarisch", "halal"],
        "allergens": ["lactose"],
        "image_key": "ovenschotel",
        "why_smart": "Aardappel, champignons en kaas zijn vaak in de aanbieding; perfecte basis voor een goedkope ovenschotel.",
        "serving_tips": ["Serveer met een groene salade.", "Lekker met een lik mosterd."],
        "storage_tips": ["3 dagen houdbaar in de koelkast.", "Goed te invriezen, ontdooi 's ochtends voor het avondeten."],
        "variations": ["Voeg spinazie of broccoli toe tussen de aardappellaag.", "Vervang kaas door geitenkaas voor pittige smaak.", "Voeg gehakt toe voor een vleesversie."],
        "instructions": [
            "Verwarm de oven voor op 200°C.",
            "Schil de aardappels en snijd ze in plakjes van een halve cm dik.",
            "Kook de aardappelplakken 8 minuten in licht gezouten water, giet af en laat stomen.",
            "Veeg de champignons schoon en snijd in plakjes.",
            "Verhit 1 el olijfolie in een pan, fruit de gesnipperde ui 4 minuten en voeg champignons toe; bak 5 minuten.",
            "Vet een ovenschaal in en leg een laag aardappelplakken neer, dan champignonmengsel, dan weer aardappel.",
            "Bestrooi rijkelijk met geraspte kaas en peper.",
            "Bak 25-30 minuten in de oven tot de bovenkant goudbruin en knapperig is.",
        ],
        "ingredients": [
            {"name": "Aardappelen", "keywords": ["aardappel"], "grams_per_serving": 250, "unit": "g"},
            {"name": "Champignons", "keywords": ["champignons"], "grams_per_serving": 150, "unit": "g"},
            {"name": "Kaas", "keywords": ["kaas"], "grams_per_serving": 60, "unit": "g"},
            {"name": "Ui", "keywords": ["ui"], "grams_per_serving": 60, "unit": "g"},
            {"name": "Olijfolie", "keywords": ["olijfolie"], "grams_per_serving": 10, "unit": "ml", "is_pantry": True},
        ],
    }


def _stamppot_andijvie() -> RecipeTemplate:
    return {
        "title": "Stamppot met spek en boerenkool/andijvie",
        "description": "Hollandse stamppot, klaar in een half uur.",
        "meal_type": "diner",
        "difficulty": "makkelijk",
        "prep_time_minutes": 10,
        "cook_time_minutes": 20,
        "diet_tags": [],
        "allergens": ["lactose"],
        "image_key": "stamppot",
        "why_smart": "Aardappels en speklapjes zijn budgetfavorieten in de folder; ideaal voor een Hollandse maaltijd.",
        "serving_tips": ["Maak een kuiltje in de stamppot en schenk er jus in.", "Lekker met een augurk."],
        "storage_tips": ["2 dagen houdbaar.", "Opwarmen het beste in de pan met een scheutje melk."],
        "variations": ["Vervang spek door rookworst.", "Maak een vegetarische versie met gebakken champignons in plaats van spek.", "Roer een lepel mosterd door de stamppot."],
        "instructions": [
            "Schil de aardappels en snijd in stukken van 3 cm.",
            "Kook de aardappels 15 minuten in licht gezouten water tot zacht.",
            "Bak intussen de speklapjes in een droge koekenpan tot ze knapperig zijn (5-7 minuten).",
            "Haal de spek uit de pan en laat uitlekken op keukenpapier; snijd in stukjes.",
            "Was de andijvie of boerenkool en snijd grof.",
            "Giet de aardappels af, bewaar een scheutje kookvocht, en stamp tot een grove puree.",
            "Roer de andijvie/boerenkool en een scheutje melk door de puree zodat de groente slinkt.",
            "Meng de spek erdoor, breng op smaak met peper en zout en serveer.",
        ],
        "ingredients": [
            {"name": "Aardappelen", "keywords": ["aardappel"], "grams_per_serving": 250, "unit": "g"},
            {"name": "Speklapjes", "keywords": ["speklapjes", "spek"], "grams_per_serving": 100, "unit": "g"},
            {"name": "IJsbergsla", "keywords": ["sla", "spinazie"], "grams_per_serving": 100, "unit": "g"},
            {"name": "Melk", "keywords": ["melk", "halfvolle melk"], "grams_per_serving": 30, "unit": "ml"},
        ],
    }


def _frittata_groente() -> RecipeTemplate:
    return {
        "title": "Frittata met courgette en feta",
        "description": "Italiaanse ovenomelet, lekker warm of koud.",
        "meal_type": "lunch",
        "difficulty": "makkelijk",
        "prep_time_minutes": 10,
        "cook_time_minutes": 20,
        "diet_tags": ["vegetarisch", "glutenvrij", "halal"],
        "allergens": ["ei", "lactose"],
        "image_key": "ei",
        "why_smart": "Eieren in de aanbieding + groente uit de folder = een grote frittata voor weinig geld.",
        "serving_tips": ["Serveer met een groene salade en stokbrood.", "Snijd in punten voor borrel of meal prep."],
        "storage_tips": ["2 dagen houdbaar in de koelkast.", "Lekker koud als lunch."],
        "variations": ["Voeg gerookte zalm of ham toe.", "Vervang feta door geitenkaas.", "Voeg gehakte verse munt toe."],
        "instructions": [
            "Verwarm de oven voor op 180°C.",
            "Snijd de courgette in halve maantjes en de rode ui in dunne ringen.",
            "Verhit 1 el olijfolie in een ovenbestendige koekenpan en bak courgette en ui 5-6 minuten op middelhoog vuur.",
            "Klop intussen de eieren los in een kom met peper, zout en eventueel gedroogde oregano.",
            "Verbrokkel de feta en strooi over de groente in de pan.",
            "Giet de eieren erover en laat 3 minuten op het fornuis stollen.",
            "Schuif de pan in de oven en bak 12-15 minuten tot het ei gestold maar nog sappig is.",
            "Laat 2 minuten rusten, snijd in punten en serveer.",
        ],
        "ingredients": [
            {"name": "Eieren", "keywords": ["eieren"], "grams_per_serving": 120, "unit": "g"},
            {"name": "Courgette", "keywords": ["courgette"], "grams_per_serving": 120, "unit": "g"},
            {"name": "Rode ui", "keywords": ["rode ui", "ui"], "grams_per_serving": 50, "unit": "g"},
            {"name": "Mozzarella", "keywords": ["mozzarella", "kaas"], "grams_per_serving": 50, "unit": "g"},
            {"name": "Olijfolie", "keywords": ["olijfolie"], "grams_per_serving": 10, "unit": "ml", "is_pantry": True},
        ],
    }


def _kip_curry() -> RecipeTemplate:
    return {
        "title": "Snelle kip-currie met paprika en rijst",
        "description": "Romige curry zonder kokosmelk-pak, in 25 minuten klaar.",
        "meal_type": "diner",
        "difficulty": "gemiddeld",
        "prep_time_minutes": 10,
        "cook_time_minutes": 20,
        "diet_tags": ["halal"],
        "allergens": ["lactose"],
        "image_key": "curry",
        "why_smart": "Kipfilet en paprika zijn populaire aanbiedingen; met basics maak je een complete curry.",
        "serving_tips": ["Bestrooi met verse koriander.", "Voeg een schijfje limoen toe voor frisse zuur."],
        "storage_tips": ["2 dagen houdbaar, smaak wordt voller op dag 2.", "Goed in te vriezen tot 2 maanden."],
        "variations": ["Vervang kip door tofu.", "Voeg spinazie toe op het laatst.", "Gebruik kokosmelk voor een romige variant."],
        "instructions": [
            "Snijd de kip in blokjes van 2 cm en de paprika in repen.",
            "Snipper de ui en de knoflook.",
            "Verhit 1 el olijfolie in een hapjespan op middelhoog vuur en bak de kip in 5 minuten goudbruin; haal uit de pan.",
            "Bak in dezelfde pan de ui en knoflook 3 minuten glazig.",
            "Voeg 2 tl kerriepoeder en 1 tl paprikapoeder toe en bak kort mee.",
            "Doe de paprika erbij en bak 5 minuten.",
            "Voeg een blik gepelde tomaten en een scheut yoghurt toe, plus de kip terug in de pan.",
            "Laat 10 minuten zachtjes pruttelen en serveer met de basmati rijst.",
        ],
        "ingredients": [
            {"name": "Kipfilet", "keywords": ["kipfilet", "kipgyros"], "grams_per_serving": 130, "unit": "g"},
            {"name": "Paprika", "keywords": ["paprika"], "grams_per_serving": 120, "unit": "g"},
            {"name": "Gepelde tomaten", "keywords": ["gepelde tomaten", "tomaten"], "grams_per_serving": 100, "unit": "g"},
            {"name": "Yoghurt", "keywords": ["yoghurt", "magere yoghurt", "griekse yoghurt"], "grams_per_serving": 40, "unit": "g"},
            {"name": "Basmati rijst", "keywords": ["basmati rijst", "rijst"], "grams_per_serving": 80, "unit": "g"},
            {"name": "Ui", "keywords": ["ui"], "grams_per_serving": 50, "unit": "g"},
            {"name": "Knoflook", "keywords": ["knoflook"], "grams_per_serving": 5, "unit": "g", "is_pantry": True},
        ],
    }


def _smoothie_bowl() -> RecipeTemplate:
    return {
        "title": "Smoothie bowl met aardbei en banaan",
        "description": "Romige fruit-bowl met crunchy topping.",
        "meal_type": "ontbijt",
        "difficulty": "makkelijk",
        "prep_time_minutes": 5,
        "cook_time_minutes": 0,
        "diet_tags": ["vegetarisch", "halal"],
        "allergens": ["lactose"],
        "image_key": "smoothie",
        "why_smart": "Bananen, aardbeien en yoghurt zijn vaak in de aanbieding — perfect voor een snel ontbijt.",
        "serving_tips": ["Strooi muesli en zaadjes voor de crunch.", "Een lepel pindakaas erop is heerlijk."],
        "storage_tips": ["Direct opeten — smoothie scheidt na een paar uur.", "Vries fruit van tevoren in voor extra dik resultaat."],
        "variations": ["Vervang aardbei door blauwe bessen.", "Maak een chocolade-versie met cacaopoeder.", "Gebruik sojadrink voor de vegan versie."],
        "instructions": [
            "Pel de banaan en breek in stukken.",
            "Was de aardbeien en verwijder de kroontjes.",
            "Doe banaan, aardbei en yoghurt in een blender.",
            "Mix 30 seconden tot een dikke, romige massa; voeg eventueel een scheutje melk toe als het te dik is.",
            "Schep de smoothie in een diepe kom.",
            "Verdeel de muesli, extra fruit en eventueel zaden erover.",
            "Werk af met een lepel honing als je het zoeter wilt.",
            "Eet direct met een lepel.",
        ],
        "ingredients": [
            {"name": "Banaan", "keywords": ["bananen", "banaan"], "grams_per_serving": 100, "unit": "g"},
            {"name": "Aardbeien", "keywords": ["aardbeien"], "grams_per_serving": 100, "unit": "g"},
            {"name": "Griekse yoghurt", "keywords": ["griekse yoghurt", "yoghurt", "magere yoghurt"], "grams_per_serving": 150, "unit": "g"},
            {"name": "Muesli", "keywords": ["muesli", "cruesli", "havermout"], "grams_per_serving": 30, "unit": "g"},
        ],
    }


def _meatballs_tomatensaus() -> RecipeTemplate:
    return {
        "title": "Gehaktballetjes in tomatensaus",
        "description": "Klassieker met zelfgedraaide balletjes en een rijke saus.",
        "meal_type": "diner",
        "difficulty": "gemiddeld",
        "prep_time_minutes": 15,
        "cook_time_minutes": 25,
        "diet_tags": ["halal"],
        "allergens": ["ei", "gluten"],
        "image_key": "gehaktballetjes",
        "why_smart": "Gehakt en tomaten zijn vaste prik in de folder; lekker met pasta of aardappel.",
        "serving_tips": ["Strooi Parmezaan en basilicum erover.", "Serveer met spaghetti of stokbrood."],
        "storage_tips": ["3 dagen houdbaar.", "Goed in te vriezen tot 3 maanden — eerst afgekoeld."],
        "variations": ["Vervang rundergehakt door kipgehakt.", "Voeg een ei en paneermeel toe voor zachtere balletjes.", "Doe een scheutje rode wijn in de saus."],
        "instructions": [
            "Doe het gehakt in een kom met een beetje peper, zout en 1 tl Italiaanse kruiden.",
            "Kneed kort tot een gladde massa en draai er 12-15 kleine balletjes van.",
            "Verhit 1 el olijfolie in een hapjespan op middelhoog vuur en bak de balletjes rondom bruin (6-8 minuten).",
            "Haal de balletjes uit de pan en bak in dezelfde pan de gesnipperde ui en knoflook 3 minuten.",
            "Voeg de tomaten en een snufje suiker toe en breng aan de kook.",
            "Doe de balletjes terug in de saus en laat 15 minuten zachtjes pruttelen.",
            "Proef en breng op smaak met peper, zout en eventueel meer kruiden.",
            "Serveer met pasta, brood of aardappels.",
        ],
        "ingredients": [
            {"name": "Rundergehakt", "keywords": ["rundergehakt", "gehakt"], "grams_per_serving": 120, "unit": "g"},
            {"name": "Tomaten", "keywords": ["gepelde tomaten", "cherrytomaten", "tomaten"], "grams_per_serving": 200, "unit": "g"},
            {"name": "Ui", "keywords": ["ui"], "grams_per_serving": 60, "unit": "g"},
            {"name": "Knoflook", "keywords": ["knoflook"], "grams_per_serving": 5, "unit": "g"},
            {"name": "Italiaanse kruiden", "keywords": ["italiaanse kruiden"], "grams_per_serving": 2, "unit": "g", "is_pantry": True},
            {"name": "Olijfolie", "keywords": ["olijfolie"], "grams_per_serving": 10, "unit": "ml", "is_pantry": True},
        ],
    }


def _falafel_bowl() -> RecipeTemplate:
    return {
        "title": "Falafel bowl met couscous en yoghurtsaus",
        "description": "Mediterraanse bowl boordevol smaak en kleur.",
        "meal_type": "diner",
        "difficulty": "makkelijk",
        "prep_time_minutes": 10,
        "cook_time_minutes": 15,
        "diet_tags": ["vegetarisch"],
        "allergens": ["gluten", "lactose", "sesam"],
        "image_key": "bowl",
        "why_smart": "Falafel en couscous zijn ideale aanbieding-basics — combineer met aanbiedingsgroente voor variatie.",
        "serving_tips": ["Strooi pijnboompitten erover.", "Voeg granaatappelpitjes toe voor zoet-zure crunch."],
        "storage_tips": ["Houd onderdelen apart in de koelkast.", "2 dagen houdbaar."],
        "variations": ["Vervang falafel door geroosterde kikkererwten.", "Gebruik bulgur in plaats van couscous.", "Maak vegan met sojayoghurt."],
        "instructions": [
            "Verwarm de oven voor op 200°C en leg de falafel op een met bakpapier beklede plaat; bak 12-15 minuten.",
            "Breng 200 ml water aan de kook, voeg de couscous toe met een snuf zout en laat 5 minuten wellen onder een deksel.",
            "Snijd de tomaten en komkommer in blokjes.",
            "Schep de couscous los met een vork en hussel met een scheut olijfolie.",
            "Maak een snelle yoghurtsaus van 4 el yoghurt, sap van een halve citroen, peper en zout.",
            "Verdeel de couscous over 2 kommen.",
            "Schik tomaten, komkommer en falafel erop.",
            "Lepel de yoghurtsaus erover en strooi peterselie of munt erover.",
        ],
        "ingredients": [
            {"name": "Falafel", "keywords": ["falafel"], "grams_per_serving": 110, "unit": "g"},
            {"name": "Couscous", "keywords": ["couscous", "bulgur"], "grams_per_serving": 70, "unit": "g"},
            {"name": "Cherrytomaten", "keywords": ["cherrytomaten", "tomaten"], "grams_per_serving": 100, "unit": "g"},
            {"name": "Komkommer", "keywords": ["komkommer"], "grams_per_serving": 80, "unit": "g"},
            {"name": "Yoghurt", "keywords": ["yoghurt", "griekse yoghurt"], "grams_per_serving": 60, "unit": "g"},
            {"name": "Olijfolie", "keywords": ["olijfolie"], "grams_per_serving": 5, "unit": "ml", "is_pantry": True},
        ],
    }


def _quinoa_bowl() -> RecipeTemplate:
    return {
        "title": "Quinoa-bowl met zoete aardappel en avocado",
        "description": "Voedzame bowl boordevol eiwit, vezels en goede vetten.",
        "meal_type": "meal-prep",
        "difficulty": "makkelijk",
        "prep_time_minutes": 10,
        "cook_time_minutes": 25,
        "diet_tags": ["vegetarisch", "vegan", "glutenvrij", "lactosevrij", "halal"],
        "allergens": [],
        "image_key": "bowl",
        "why_smart": "Quinoa is sterk in de bonus bij biologische supers; combineer met avocado en aardappel.",
        "serving_tips": ["Strooi zonnebloempitten erover.", "Voeg een dressing van tahini en citroen toe."],
        "storage_tips": ["3 dagen houdbaar, avocado pas op het laatst toevoegen.", "Niet invriezen."],
        "variations": ["Vervang aardappel door geroosterde pompoen.", "Voeg geroosterde kikkererwten toe voor crunch.", "Gebruik bulgur in plaats van quinoa."],
        "instructions": [
            "Verwarm de oven voor op 200°C.",
            "Schil de aardappel en snijd in blokjes van 2 cm; hussel met 1 el olie, peper, zout en paprikapoeder.",
            "Rooster de aardappel 25 minuten op een bakplaat, halverwege keren.",
            "Spoel de quinoa en kook in 15 minuten gaar in dubbele hoeveelheid water.",
            "Halveer de avocado en snijd in plakjes.",
            "Spoel de kikkererwten af en laat uitlekken.",
            "Schep de quinoa in een kom en schik de aardappel, kikkererwten en avocado erop.",
            "Werk af met 1 el olijfolie, citroensap en eventueel zaadjes.",
        ],
        "ingredients": [
            {"name": "Quinoa", "keywords": ["quinoa"], "grams_per_serving": 70, "unit": "g"},
            {"name": "Aardappelen", "keywords": ["aardappel"], "grams_per_serving": 200, "unit": "g"},
            {"name": "Avocado", "keywords": ["avocado"], "grams_per_serving": 80, "unit": "g"},
            {"name": "Kikkererwten", "keywords": ["kikkererwten"], "grams_per_serving": 80, "unit": "g"},
            {"name": "Olijfolie", "keywords": ["olijfolie"], "grams_per_serving": 10, "unit": "ml", "is_pantry": True},
        ],
    }


def _pasta_pesto() -> RecipeTemplate:
    return {
        "title": "Pasta pesto met cherrytomaten en mozzarella",
        "description": "Pasta in 15 minuten — perfecte snelle hap.",
        "meal_type": "diner",
        "difficulty": "makkelijk",
        "prep_time_minutes": 5,
        "cook_time_minutes": 10,
        "diet_tags": ["vegetarisch", "halal"],
        "allergens": ["gluten", "lactose", "noten"],
        "image_key": "pasta",
        "why_smart": "Pesto en pasta in de aanbieding combineren tot een snel diner met aanbiedings-tomaatjes.",
        "serving_tips": ["Strooi pijnboompitten erover.", "Lekker met versgemalen peper."],
        "storage_tips": ["1 dag houdbaar, het lekkerst direct.", "Niet invriezen."],
        "variations": ["Voeg gegrilde kip toe.", "Gebruik rode pesto voor een andere smaak.", "Vervang mozzarella door geitenkaas."],
        "instructions": [
            "Breng een ruime pan water aan de kook met een snuf zout.",
            "Doe de pasta in het kokende water en kook volgens de verpakking.",
            "Halveer de cherrytomaten en snijd de mozzarella in plakjes.",
            "Bewaar voor het afgieten een klein kopje kookvocht.",
            "Giet de pasta af en doe terug in de pan.",
            "Schep de pesto erdoor en voeg een scheutje kookvocht toe voor een romiger resultaat.",
            "Roer de tomaten en mozzarella erdoor zodat de kaas net begint te smelten.",
            "Maal versgemalen peper erover en serveer direct.",
        ],
        "ingredients": [
            {"name": "Pasta", "keywords": ["pasta", "penne", "spaghetti", "tagliatelle"], "grams_per_serving": 100, "unit": "g"},
            {"name": "Pesto", "keywords": ["pesto"], "grams_per_serving": 30, "unit": "g"},
            {"name": "Cherrytomaten", "keywords": ["cherrytomaten", "tomaten"], "grams_per_serving": 100, "unit": "g"},
            {"name": "Mozzarella", "keywords": ["mozzarella"], "grams_per_serving": 50, "unit": "g"},
        ],
    }


def _garnalen_knoflook() -> RecipeTemplate:
    return {
        "title": "Pasta met garnalen en knoflook",
        "description": "Italiaanse klassieker met een vleugje pittigheid.",
        "meal_type": "diner",
        "difficulty": "gemiddeld",
        "prep_time_minutes": 10,
        "cook_time_minutes": 15,
        "diet_tags": ["lactosevrij"],
        "allergens": ["gluten", "schaaldieren"],
        "image_key": "pasta",
        "why_smart": "Garnalen liggen regelmatig met fikse korting; combineer met aanbiedingspasta voor een chique gerecht.",
        "serving_tips": ["Garneer met peterselie en citroenrasp.", "Knijp er vlak voor het serveren extra citroensap over."],
        "storage_tips": ["Het lekkerst direct, maximaal 1 dag.", "Niet invriezen."],
        "variations": ["Vervang garnalen door blokjes vis.", "Voeg cherrytomaten toe.", "Gebruik volkoren pasta voor meer vezels."],
        "instructions": [
            "Breng een grote pan water aan de kook met een snuf zout.",
            "Snipper 3 teentjes knoflook fijn.",
            "Verhit 2 el olijfolie in een koekenpan op middelhoog vuur en fruit de knoflook 30 seconden (niet laten verbranden).",
            "Voeg de garnalen toe en bak ze 3-4 minuten tot ze roze zijn.",
            "Doe de pasta in het kokende water en kook volgens de verpakking.",
            "Knijp het sap van een halve citroen bij de garnalen en voeg eventueel een snufje chili toe.",
            "Bewaar een kopje kookvocht en giet de pasta af.",
            "Schep de pasta door de garnalen, voeg eventueel kookvocht toe voor saus, breng op smaak met peper en zout en serveer.",
        ],
        "ingredients": [
            {"name": "Garnalen", "keywords": ["garnalen"], "grams_per_serving": 100, "unit": "g"},
            {"name": "Pasta", "keywords": ["pasta", "spaghetti", "tagliatelle"], "grams_per_serving": 100, "unit": "g"},
            {"name": "Knoflook", "keywords": ["knoflook"], "grams_per_serving": 10, "unit": "g"},
            {"name": "Citroensap", "keywords": ["citroensap"], "grams_per_serving": 10, "unit": "ml", "is_pantry": True},
            {"name": "Olijfolie", "keywords": ["olijfolie"], "grams_per_serving": 15, "unit": "ml", "is_pantry": True},
        ],
    }


def _huttenkase_salade() -> RecipeTemplate:
    return {
        "title": "Hüttenkäse-salade met komkommer en appel",
        "description": "Eiwitrijke, frisse lunch zonder gedoe.",
        "meal_type": "lunch",
        "difficulty": "makkelijk",
        "prep_time_minutes": 5,
        "cook_time_minutes": 0,
        "diet_tags": ["vegetarisch", "glutenvrij", "halal"],
        "allergens": ["lactose"],
        "image_key": "salade",
        "why_smart": "Hüttenkäse + appel of komkommer uit de aanbieding = veel eiwit voor weinig geld.",
        "serving_tips": ["Strooi zonnebloempitten erover.", "Voeg vers gemalen peper toe."],
        "storage_tips": ["1 dag houdbaar.", "Niet invriezen."],
        "variations": ["Vervang appel door peer.", "Voeg cranberries of rozijnen toe.", "Strooi gehakte walnoten erover."],
        "instructions": [
            "Was de komkommer en snijd in kleine blokjes.",
            "Was de appel en snijd in blokjes — laat de schil zitten voor vezels.",
            "Schep de hüttenkäse in een kom.",
            "Voeg de komkommer en appel toe.",
            "Strooi een snufje peper en eventueel kaneel erover.",
            "Roer kort door zodat alle smaken zich mengen.",
            "Bedek en zet 5 minuten in de koelkast om koud te worden.",
            "Lekker met een sneetje volkoren brood erbij.",
        ],
        "ingredients": [
            {"name": "Hüttenkäse", "keywords": ["huttenkase", "hüttenkäse"], "grams_per_serving": 150, "unit": "g"},
            {"name": "Komkommer", "keywords": ["komkommer"], "grams_per_serving": 80, "unit": "g"},
            {"name": "Appel", "keywords": ["appel", "appels"], "grams_per_serving": 80, "unit": "g"},
        ],
    }


def _pita_kip() -> RecipeTemplate:
    return {
        "title": "Pita met gemarineerde kipgyros",
        "description": "Knapperige pita gevuld met kruidige kip en frisse groente.",
        "meal_type": "diner",
        "difficulty": "makkelijk",
        "prep_time_minutes": 15,
        "cook_time_minutes": 10,
        "diet_tags": ["halal"],
        "allergens": ["gluten", "lactose"],
        "image_key": "pita",
        "why_smart": "Kipgyros, pita en yoghurt staan met enige regelmaat in de folder — samen een complete maaltijd.",
        "serving_tips": ["Lekker met chilisaus of harissa.", "Strooi rode ui en peterselie erover."],
        "storage_tips": ["Best vers, vulling 2 dagen apart in de koelkast.", "Niet invriezen."],
        "variations": ["Vervang kip door falafel.", "Voeg gebakken paprika toe.", "Gebruik tzatziki in plaats van gewone yoghurt."],
        "instructions": [
            "Snijd de kipgyros in reepjes, of als je gewone kipfilet hebt, snijd hem in dunne reepjes en kruid met paprikapoeder, komijn en oregano.",
            "Verhit 1 el olijfolie in een koekenpan op middelhoog vuur en bak de kip in 6-8 minuten goudbruin en gaar.",
            "Verwarm intussen de pita's 1 minuut in een broodrooster of droge koekenpan.",
            "Snijd de komkommer in plakjes en de tomaat in blokjes.",
            "Maak een snelle yoghurtsaus met 4 el yoghurt, een geperst teentje knoflook en peper.",
            "Snijd de pita's open en smeer de binnenkant in met de yoghurtsaus.",
            "Vul met sla, tomaat, komkommer en kip.",
            "Eet meteen op terwijl de pita nog warm is.",
        ],
        "ingredients": [
            {"name": "Kipgyros", "keywords": ["kipgyros", "kipfilet"], "grams_per_serving": 120, "unit": "g"},
            {"name": "Pitabroodjes", "keywords": ["pitabroodjes", "wraps"], "grams_per_serving": 90, "unit": "g"},
            {"name": "Komkommer", "keywords": ["komkommer"], "grams_per_serving": 60, "unit": "g"},
            {"name": "Tomaten", "keywords": ["tomaten", "cherrytomaten"], "grams_per_serving": 60, "unit": "g"},
            {"name": "Yoghurt", "keywords": ["yoghurt"], "grams_per_serving": 60, "unit": "g"},
            {"name": "Knoflook", "keywords": ["knoflook"], "grams_per_serving": 3, "unit": "g", "is_pantry": True},
        ],
    }


def _havermoutpap() -> RecipeTemplate:
    return {
        "title": "Warme havermoutpap met appel en kaneel",
        "description": "Klassiek warm ontbijt voor koude ochtenden.",
        "meal_type": "ontbijt",
        "difficulty": "makkelijk",
        "prep_time_minutes": 3,
        "cook_time_minutes": 7,
        "diet_tags": ["vegetarisch", "halal"],
        "allergens": ["gluten", "lactose"],
        "image_key": "ontbijt",
        "why_smart": "Havermout en melk zijn vrijwel altijd in de bonus; appel/banaan maken het zoet en vezelrijk.",
        "serving_tips": ["Top met geroosterde noten of pindakaas.", "Voeg een lepel honing toe voor zoete tand."],
        "storage_tips": ["Vers maken — niet bewaren.", "Bij meal prep: hete havermout en topping apart."],
        "variations": ["Vervang melk door sojadrink (vegan).", "Voeg rozijnen toe voor extra zoet.", "Roer een lepel cacao erdoor voor chocolade-versie."],
        "instructions": [
            "Schenk de melk in een kleine steelpan en verwarm op middelhoog vuur.",
            "Voeg de havermout toe en breng aan de kook.",
            "Laat 5 minuten zachtjes pruttelen en roer regelmatig zodat de pap niet aanbrandt.",
            "Snijd ondertussen de appel in kleine blokjes (schil mag erop blijven).",
            "Roer de helft van de appel met een snuf kaneel door de pap.",
            "Schep in een kom en verdeel de rest van de appel erover.",
            "Strooi nog een snufje kaneel erover.",
            "Voeg eventueel honing of een lepel pindakaas toe.",
        ],
        "ingredients": [
            {"name": "Havermout", "keywords": ["havermout", "haver"], "grams_per_serving": 50, "unit": "g"},
            {"name": "Melk", "keywords": ["melk", "halfvolle melk"], "grams_per_serving": 250, "unit": "ml"},
            {"name": "Appel", "keywords": ["appel", "appels"], "grams_per_serving": 100, "unit": "g"},
        ],
    }


RECIPE_TEMPLATES: list[RecipeTemplate] = [
    _kip_pasta(),
    _tofu_roerbak(),
    _zalm_oven(),
    _linzensoep(),
    _wrap_hummus(),
    _kikkererwten_curry(),
    _bolognese(),
    _omelet_champignons(),
    _overnight_oats(),
    _scrambled_eggs_toast(),
    _greek_salad(),
    _couscous_groente(),
    _tonijnsalade(),
    _aardappel_ovenschotel(),
    _stamppot_andijvie(),
    _frittata_groente(),
    _kip_curry(),
    _smoothie_bowl(),
    _meatballs_tomatensaus(),
    _falafel_bowl(),
    _quinoa_bowl(),
    _pasta_pesto(),
    _garnalen_knoflook(),
    _huttenkase_salade(),
    _pita_kip(),
    _havermoutpap(),
]
