# Supermarkt Recepten Tool

Nederlandse webapp die actuele supermarktaanbiedingen verzamelt van **Jumbo,
Albert Heijn, Lidl, Hoogvliet, Aldi, Ekoplaza, Plus, Dirk, Vomar en Coop**, en
op basis daarvan automatisch recepten voorstelt met voedingsinformatie en een
gezondheidsscore.

De MVP draait direct lokaal met realistische **mock-aanbiedingen**, zonder dat
er ook maar één externe scraper hoeft te werken. Per supermarkt is er een
modulaire scraper-klasse waarin je later de echte ophaal-logica plaatst.

## Functies

- **Aanbiedingen** verzamelen van 10 Nederlandse supermarkten (MVP: mockdata).
- **Receptgenerator** die aanbiedingen combineert tot logische recepten in het
  Nederlands, inclusief bereidingsstappen, kosten, ingrediënten en
  ontbrekende standaardproducten.
- **Filters**: aantal personen, dieet (vegetarisch, vegan, halal, lactosevrij,
  glutenvrij), max bereidingstijd, min eiwit, max kcal, max budget per portie,
  favoriete supermarkten en uit te sluiten ingrediënten.
- **Voedingsinformatie** per portie (kcal, eiwit, koolhydraten, suiker, vet,
  verzadigd vet, vezels, zout) via een fallback-tabel met Open Food Facts als
  optionele bron.
- **Gezondheidsscore (0–100)** met transparante uitleg en labels als
  *eiwitrijk*, *vezelrijk*, *caloriearm*, *veel zout*, *veel suiker*,
  *budgetvriendelijk*.
- **AI-fallback**: optioneel een LLM (OpenAI-compatible) inschakelen voor
  creatievere recepten. Zonder API-key blijft de rule-based engine actief.
- **Scheduled job** voor dagelijkse refresh, geschikt voor Render Cron Jobs.
- **Frontend** in React + Vite met overzicht, filters, receptgenerator en
  detailpagina, responsive voor mobiel.

## Architectuur

```
supermarket-recipe-tool/
├── backend/                 FastAPI + SQLAlchemy + Alembic
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/          ORM-modellen (supermarkets, products, offers, …)
│   │   ├── schemas/         Pydantic-schemas (incl. LLM-validatie)
│   │   ├── routers/         FastAPI endpoints
│   │   ├── services/
│   │   │   ├── scrapers/    10 modulaire scrapers + base + registry
│   │   │   ├── offer_matcher.py
│   │   │   ├── nutrition.py
│   │   │   ├── health_score.py
│   │   │   ├── recipe_generator.py   (rule-based)
│   │   │   └── ai_service.py         (optionele LLM)
│   │   ├── jobs/
│   │   │   ├── fetch_offers.py       (Render Cron entrypoint)
│   │   │   └── scheduler.py          (in-process, lokaal)
│   │   ├── data/            fallback nutrition + pantry + recept-sjablonen
│   │   └── tests/           pytest-suite
│   ├── alembic/             database-migraties
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                React + Vite + react-router
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── styles/
│   │   └── types/
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
├── render.yaml              Render Blueprint
└── .env.example
```

## Lokaal starten

### Vereisten

- Python 3.11+ aanbevolen (3.9 werkt met `eval_type_backport`).
- Node.js 18+ voor de frontend.

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp ../.env.example .env       # pas waardes aan indien nodig

# Migraties: bij sqlite kun je ook gewoon de app starten — die maakt
# tabellen automatisch via init_db(). Voor productie:
alembic upgrade head

# Start de API
uvicorn app.main:app --reload --port 8000
```

De app seed bij eerste start automatisch alle 10 supermarkten met mockdata zodat
je meteen recepten kunt genereren. Bezoek <http://localhost:8000/docs> voor de
Swagger-UI.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

De frontend draait nu op <http://localhost:5173> en proxiet `/api/*` naar de
backend op poort 8000.

### Tests

```bash
cd backend
.venv/bin/python -m pytest app/tests -v
```

De suite dekt onder andere:
- `test_health_score.py` – berekening van de score en labels
- `test_nutrition.py` – fallback-cascade en aggregatie
- `test_recipe_validation.py` – Pydantic-validatie voor LLM-output
- `test_recipe_generator.py` – rule-based generatie met filters
- `test_scrapers.py` – alle 10 mock-scrapers leveren valide aanbiedingen

## API

| Methode | Pad                          | Beschrijving                          |
|---------|------------------------------|---------------------------------------|
| GET     | `/api/supermarkets`          | Lijst van alle supermarkten            |
| GET     | `/api/offers`                | Aanbiedingen met filters               |
| GET     | `/api/offers/categories`     | Unieke categorieën in aanbiedingen     |
| POST    | `/api/offers/refresh`        | Trigger handmatig de scrapers          |
| POST    | `/api/recipes/generate`      | Genereer recepten o.b.v. filters       |
| GET     | `/api/recipes/health`        | Check of LLM beschikbaar is            |
| GET     | `/healthz`                   | Liveness                               |

Voorbeeld:

```bash
curl -X POST http://localhost:8000/api/recipes/generate \
  -H 'Content-Type: application/json' \
  -d '{"servings": 2, "diets": ["vegetarisch"], "max_prep_minutes": 25, "count": 3}'
```

## Echte scrapers toevoegen

Elke supermarkt heeft een eigen klasse in `backend/app/services/scrapers/`. Een
nieuwe live-scraper voeg je toe door `fetch_live()` te implementeren:

```python
def fetch_live(self) -> list[ScrapedOffer]:
    with httpx.Client(timeout=self.timeout, headers={"User-Agent": self.user_agent}) as c:
        r = c.get("https://www.jumbo.com/api/...")
        r.raise_for_status()
        data = r.json()
    return [
        ScrapedOffer(
            product_name=item["title"],
            sale_price=item["price"]["now"],
            original_price=item["price"]["was"],
            category=item.get("category"),
            unit=item.get("unit"),
            amount=item.get("amount"),
            valid_from=...,
            valid_until=...,
            image_url=item.get("imageUrl"),
            source_url=item.get("url"),
        )
        for item in data["offers"]
    ]
```

Zet daarna `USE_MOCK_SCRAPERS=false`. De `scrape()` methode vangt fouten op en
valt automatisch terug op `mock_offers()` zodat de app door blijft werken.

Houd je aan **robots.txt** en gebruik rate-limiting (`tenacity` is al
geïnstalleerd). Sla per aanbieding minimaal op: productnaam, supermarkt, oude
prijs, aanbiedingsprijs, korting, eenheid/hoeveelheid, categorie, looptijd,
afbeelding, bron-url en timestamp — dit zit allemaal in het `Offer`-model.

## Deployment naar Render

1. Push het project naar GitHub.
2. Maak op Render een **Blueprint** aan op basis van de repo. Render leest
   `render.yaml` en maakt aan:
   - PostgreSQL-database (`supermarkt-recepten-db`)
   - FastAPI web service (`supermarkt-recepten-api`)
   - Frontend web service (`supermarkt-recepten-web`)
   - Cron Job die elke nacht om 04:00 UTC `python -m app.jobs.fetch_offers` runt
3. Stel handmatig de geheime variabelen in via het Render dashboard:
   - `CORS_ORIGINS` → de URL van de frontend (bijv. `https://supermarkt-recepten-web.onrender.com`)
   - `VITE_API_URL` → de URL van de API
   - `LLM_API_KEY` → optioneel, voor AI-recepten
   - `OPENFOODFACTS_USER_AGENT` → bv. `SupermarktReceptenTool/0.1 (jouw@email)`

### Environment variables

| Variabele                  | Beschrijving                                 |
|----------------------------|----------------------------------------------|
| `DATABASE_URL`             | Postgres URL op Render, sqlite lokaal        |
| `LLM_API_KEY`              | OpenAI-key, leeg = rule-based fallback       |
| `OPENFOODFACTS_USER_AGENT` | User-Agent voor Open Food Facts              |
| `SCRAPER_INTERVAL_HOURS`   | Interval voor in-process scheduler           |
| `CORS_ORIGINS`             | Komma-gescheiden whitelist                   |
| `USE_MOCK_SCRAPERS`        | `true` = mockdata; `false` = live scrapers   |

## Gezondheidsscore

De score wordt berekend in [`app/services/health_score.py`](backend/app/services/health_score.py).
Het is bewust een lineair, transparant model zodat je in tests precies kunt
verifiëren hoe een gerecht punten krijgt of verliest. Gebruikte factoren:

- kcal per portie
- eiwitgehalte
- vezels
- groente/fruit aandeel
- verzadigd vet
- zout
- suiker
- ratio ultrabewerkte ingrediënten

Naast de score worden labels meegegeven (eiwitrijk, vezelrijk, caloriearm, veel
zout, veel suiker, budgetvriendelijk, vegetarisch, vegan).

## AI-veiligheid

`ai_service.py` verstuurt **alleen** de huidige aanbiedingen naar de LLM, met
een systeemprompt die afdwingt dat:

- de LLM uitsluitend ingredienten gebruikt die in de aanbiedingen voorkomen,
- prijzen niet door de LLM verzonnen mogen worden (de backend reken die zelf),
- ontbrekende ingredienten apart in `missing_pantry_items` belanden,
- de output geldig JSON is volgens een Pydantic-schema (`LLMRecipeList`).

Bij elke afwijking valt de service terug op de rule-based generator.

## Roadmap

Het project is iteratief opgezet (zie de specificatie). Status:

1. ✅ MVP met mock-aanbiedingen die lokaal werkt
2. ✅ Database-opslag (SQLite/PG via SQLAlchemy + Alembic)
3. 🟡 Echte scrapers toevoegen — modules staan klaar, `fetch_live()` per
   supermarkt nog te implementeren
4. ✅ Voedingsinformatie met fallback en Open Food Facts-hook
5. ✅ AI-receptgeneratie met safe prompt + Pydantic-validatie
6. ✅ Render deployment (`render.yaml`, Dockerfile, cron job)

## Licentie

Privé/scriptieproject — vrij voor educatief gebruik.
