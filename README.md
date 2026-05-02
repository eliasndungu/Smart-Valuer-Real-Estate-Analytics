# Smart Valuer – Kenya Real Estate Analytics

> An end-to-end Real Estate Data Analytics platform for the Kenyan property market.

---

## Project Structure

```
Smart-Valuer-Real-Estate-Analytics/
├── scraper/                        # Scrapy data collection layer
│   ├── scrapy.cfg
│   └── kenyan_listings/
│       ├── settings.py             # Scrapy settings (rate-limiting, pipelines)
│       ├── items.py                # PropertyItem schema
│       ├── pipelines.py            # Validation + JSONL writer
│       └── spiders/
│           ├── buyrentkenya_spider.py   # BuyRentKenya spider
│           └── jiji_spider.py           # Jiji Kenya spider
│
├── backend/                        # FastAPI REST API + ML model
│   ├── app/
│   │   ├── main.py                 # App factory + CORS
│   │   ├── database.py             # SQLAlchemy engine / session
│   │   ├── api/
│   │   │   ├── predict.py          # POST /predict – price estimation
│   │   │   └── analytics.py        # GET /analytics/* – dashboard data
│   │   ├── models/
│   │   │   └── property.py         # ORM model for `properties` table
│   │   ├── schemas/
│   │   │   └── prediction.py       # Pydantic request/response schemas
│   │   └── services/
│   │       └── predictor.py        # Placeholder Scikit-learn price model
│   ├── migrations/
│   │   ├── env.py                  # Alembic env
│   │   ├── script.py.mako
│   │   └── versions/
│   │       └── 0001_create_properties.py   # Initial DB migration
│   ├── tests/
│   │   └── test_predict.py         # pytest test suite
│   ├── alembic.ini
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/                       # Next.js 15 (App Router) + Tailwind CSS
    ├── src/
    │   ├── app/
    │   │   ├── layout.tsx           # Root layout (nav + footer)
    │   │   ├── page.tsx             # Home page (hero + search + estimator)
    │   │   └── dashboard/
    │   │       └── page.tsx         # Analytics dashboard
    │   ├── components/
    │   │   ├── SearchBar.tsx        # Global search bar
    │   │   ├── PredictionForm.tsx   # Price estimation form
    │   │   ├── AvgPriceChart.tsx    # Bar chart – avg price per bedroom
    │   │   ├── NeighborhoodChart.tsx # Horizontal bar chart – neighbourhood trends
    │   │   └── StatCard.tsx         # KPI stat card
    │   └── lib/
    │       └── api.ts               # Typed API client + formatters
    └── .env.local.example
```

---

## Quickstart

### 1 · Scraper

```bash
cd scraper
pip install -r requirements.txt

# Crawl BuyRentKenya (for-sale listings, up to 50 pages)
scrapy crawl buyrentkenya

# Crawl Jiji Nairobi (for-rent listings)
scrapy crawl jiji -a category=houses-apartments-for-rent -a location=nairobi

# Output: scraper/output/properties.jsonl
```

### 2 · Backend (FastAPI)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run DB migrations (creates SQLite by default)
python -m alembic upgrade head

# Start API server
uvicorn app.main:app --reload --port 8000

# Interactive docs → http://localhost:8000/docs
```

#### Key Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/` | Health check |
| `POST` | `/predict` | Price prediction |
| `GET`  | `/analytics/avg-price-by-bedrooms` | Avg price per bedroom |
| `GET`  | `/analytics/neighborhood-trends` | Neighbourhood price trends |

#### Sample `/predict` Request

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Kilimani",
    "size_sqft": 1200,
    "bedrooms": 3,
    "bathrooms": 2,
    "property_type": "apartment",
    "listing_type": "sale",
    "amenities": ["parking", "gym"]
  }'
```

#### Run Tests

```bash
cd backend
python -m pytest tests/ -v
```

### 3 · Frontend (Next.js)

```bash
cd frontend
cp .env.local.example .env.local   # set NEXT_PUBLIC_API_URL if needed

npm install
npm run dev        # → http://localhost:3000
npm run build      # production build
npm run start      # serve production build
```

---

## Architecture

```
Browser  ──►  Next.js (App Router)  ──►  FastAPI  ──►  SQLite / PostgreSQL
                                              │
                              Scikit-learn predictor
                                              │
                           Scrapy spiders ──► JSONL / DB ingest
```

## Replacing the Placeholder Model

`backend/app/services/predictor.py` contains a rule-based heuristic.
To swap in a real trained model:

1. Train a `Pipeline` (preprocessor + regressor) with scikit-learn.
2. Save it: `joblib.dump(pipeline, "model.joblib")`.
3. In `predictor.py` load it at module import time and call `pipeline.predict(X)`.

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./smart_valuer.db` | SQLAlchemy DB URL |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | FastAPI base URL |
