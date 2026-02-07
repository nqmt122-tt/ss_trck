# Socio-Spatial Freight Forecast (SSFF)

**Status**: Phase 1 (Foundation & Database)  
**Documentation**: [PRD](docs/ssff-prd.md) | [Plan](implementation_plan.md)

---

## 🚀 Vision

**Move from Low-Info Logistics → High-Signal Anticipation.**

Vietnam's logistics market is driven by informal, emotional, and fast-moving signals on social channels (Facebook, Zalo, TikTok). SSFF turns this "social noise" into a structured **Desperation Index**, predicting demand spikes (like Tet flower season or fruit harvests) days before they hit traditional data sources.

---

## 🏗 Architecture (The Social Lakehouse)

We use a "Lakehouse" pattern to separate the fuzzy world of social text from the rigid world of spatial querying.

### 1. Data Acquisition (Phase 0)
- **Crawler**: Standalone Python scripts (Playwright/API) that scrape specialized logistics groups.
- **Output**: Raw JSON streams of posts/comments.

### 2. Processing Layer (The Brain)
- **Vector Store (`pgvector`)**: Stores semantic embeddings of raw posts to allow fuzzy matching (e.g., "urgent" ≈ "cứu").
- **LLM Extractor**: Analyzes posts to extract structured data:
    - **Origin**: Where the truck is needed (The "Signal").
    - **Destination**: Where the truck goes (The "Flow").
    - **Commodity**: e.g., Rice, Dragon Fruit.
    - **Urgency Score**: 0-100 (Desperation Index).

### 3. Serving Layer (The Dashboard)
- **Database**: **PostgreSQL** with **PostGIS** (Spatial) + **pgvector** (Semantic).
- **Backend**: **FastAPI** (Python) serving GeoJSON.
- **Frontend**: **Next.js** (React) with Mapbox/Leaflet.
