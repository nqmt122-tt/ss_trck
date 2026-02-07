# Socio-Spatial Freight Forecast (SSFF)

**Status**: Phase 1 (Data Collection & Cleaning)  
**Documentation**: [PRD](docs/ssff-prd.md) | [Plan](implementation_plan.md) | [SSM Spec](ssm.md)

---

## 🚀 Vision

**Move from Low-Info Logistics → High-Signal Anticipation.**

Vietnam's logistics market is driven by informal, emotional, and fast-moving signals on social channels (Facebook, Zalo, TikTok). SSFF turns this "social noise" into a structured **Desperation Index**, predicting demand spikes (like Tet flower season or fruit harvests) days before they hit traditional data sources.

---

## 🏗 Architecture (The Social Lakehouse)

We use a "Lakehouse" pattern to separate the fuzzy world of social text from the rigid world of spatial querying.

```
┌─────────────────────────────────────────────────────────────────┐
│                     SSFF Architecture                            │
├─────────────────────────────────────────────────────────────────┤
│  Phase 1: Data Collection & Cleaning                            │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                     │
│  │ Crawler │ -> │ Cleaner │ -> │ Vectors │ (pgvector)          │
│  └─────────┘    └─────────┘    └─────────┘                     │
├─────────────────────────────────────────────────────────────────┤
│  Phase 2: Analysis & Visualization                              │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                     │
│  │ LLM/NLP │ -> │ Signals │ -> │ Map UI  │ (Next.js)           │
│  └─────────┘    └─────────┘    └─────────┘                     │
├─────────────────────────────────────────────────────────────────┤
│  Phase 3: SSM Application                                       │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                     │
│  │ Kalman  │ -> │   DI    │ -> │ Predict │                     │
│  │ Filter  │    │  Score  │    │ Engine  │                     │
│  └─────────┘    └─────────┘    └─────────┘                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📅 Project Phases

### Phase 1: Data Collection & Cleaning
- **Crawler**: Python scripts (Playwright/API) to scrape logistics groups
- **Output**: Raw JSON streams of posts/comments
- **Cleaning**: Text normalization, deduplication, PII removal
- **Storage**: PostgreSQL with `pgvector` for embeddings

### Phase 2: Analysis & Visualization
- **LLM Extractor**: Extract Origin, Destination, Commodity, Urgency
- **Signal Aggregation**: Compute DPS, SSS, MS, TSS scores
- **Backend**: FastAPI serving GeoJSON
- **Frontend**: Next.js with Mapbox/Deck.gl for flow visualization

### Phase 3: SSM Application
- **State-Space Model**: Kalman Filter for latent stress estimation
- **Desperation Index**: 0-100 score mapped from hidden state
- **Prediction Engine**: Forecast demand spikes 2-3 days ahead
- **Multi-Route Extension**: Cross-corridor stress propagation

---

## 📂 Project Structure

```
/ssff-monorepo
├── backend/         # FastAPI Service
├── frontend/        # Next.js Dashboard
├── database/        # Docker + SQL Init (PostGIS/pgvector)
├── crawler/         # Data Acquisition Scripts
├── data-pipeline/   # Ingestion & LLM Extraction Logic
└── ssm/             # State-Space Model Implementation
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| **Language** | Python 3.10+ (Backend/Data), TypeScript (Frontend) |
| **Database** | PostgreSQL 16 |
| **Extensions** | PostGIS, pgvector |
| **ML/Stats** | filterpy, statsmodels, scikit-learn |
| **Frontend** | Next.js, Deck.gl, Mapbox |
| **Infrastructure** | Docker Compose |

---

## ⚡ Quick Start

1. **Start Database**:
   ```bash
   cd ssff-monorepo
   docker compose up -d
   ```

2. **Run Pipeline (Mock Data)**:
   ```bash
   # Generate data
   python ssff-monorepo/crawler/crawler.py
   
   # Ingest to DB
   python ssff-monorepo/data-pipeline/ingest.py
   ```

3. **Start Backend**:
   ```bash
   cd ssff-monorepo/backend
   uvicorn main:app --reload
   ```

---

## 🎯 Key Use Cases

1. **Tet Flower Season**: Predict congestion from Highlands -> Cities
2. **Fruit Harvests**: Spot sudden demand spikes in Mekong Delta
3. **Border Gates**: Identify "red zones" where trucks are stuck
4. **Proactive Pricing**: Adjust rates before desperation surges

---

## 📊 Desperation Index (DI) Scale

| DI Range | Level | Meaning |
|----------|-------|---------|
| 0–30 | 🟢 Stable | Normal operations |
| 31–55 | 🟡 Tight | Monitor closely |
| 56–75 | 🟠 Hot | Prepare capacity |
| 76–100 | 🔴 Critical | Immediate action |

---

## 🧠 SSM & Kalman Filter Methodology

### The Core Problem

**Logistics stress is not directly observable** — you can't measure "desperation" directly. Instead, you observe noisy signals (social posts, urgency keywords, etc.) and **infer** the underlying stress level.

We have 4 observable signals:
| Signal | Description | Example |
|--------|-------------|---------|
| **DPS** | Demand Pressure Score | Urgent keywords: "gấp", "cứu", "kẹt" |
| **SSS** | Supply Scarcity Score | "No truck available" posts |
| **MS** | Momentum Score | Rate of change in post volume |
| **TSS** | Temporal Seasonality Score | Tet, harvest periods |

But these are **noisy** — a single viral post might spike DPS without reflecting actual market stress.

### State-Space Model Formulation

**Hidden State** (`x_t`): The "true" freight stress level you want to estimate.

**State Transition** (how stress evolves over time):
```
x_t = a × x_{t-1} + b × S_t + w_t
```
- `a = 0.85`: Stress persists but decays ~15%/day without new demand
- `b = 0.30`: Seasonal events (Tet) add ~30% to base stress
- `w_t`: Random shocks (unexpected demand spikes)

**Observation Model** (how signals relate to hidden state):
```
y_t = C × x_t + v_t
```
- `C = [0.40, 0.35, 0.15, 0.10]`: Weights for each signal
- `v_t`: Observation noise (social data is messy)

### Why Kalman Filter?

The Kalman Filter is an optimal algorithm for this setup:

1. **Prediction Step**: "Given yesterday's stress, what do I expect today?"
   ```
   x̂_predicted = a × x̂_yesterday + b × S_today
   ```

2. **Update Step**: "Now I see today's signals — how do I correct my prediction?"
   ```
   K = (how much to trust new observations vs. prediction)
   x̂_updated = x̂_predicted + K × (actual_signals - expected_signals)
   ```

The **Kalman Gain (K)** automatically balances:
- High noise in observations → trust the prediction more
- High uncertainty in prediction → trust observations more

### Key Benefits

| Feature | Benefit |
|---------|---------|
| **Noise filtering** | Smooths out viral/spam posts |
| **Uncertainty tracking** | Provides confidence intervals |
| **Optimal estimation** | Mathematically proven best linear estimator |
| **Temporal coherence** | Stress can't jump 0→100 instantly |

### DI Mapping

The latent state `x_t` (which can be any real number) is mapped to 0-100 using sigmoid:

```
DI = 100 / (1 + exp(-x))
```

This ensures DI stays bounded and has smooth transitions.

---

## � Signal Computation Strategy

Each signal is computed from raw social media data and normalized to [0, 1] before entering the SSM.

### 1. DPS (Demand Pressure Score)
**Formula**: `(Urgent Keyword Count) / (Total Route Posts)`
- **Keywords**: "gấp" (urgent), "cứu" (help), "kẹt" (stuck), "khẩn" (emergency)
- **Weighting**: High-urgency words like "cứu" get 1.2x weight

### 2. SSS (Supply Scarcity Score)
**Formula**: `(No-Truck Posts) / (Total Supply-Related Posts)`
- **Indicators**: "không có xe", "hết xe", "giá tăng", "xe khó tìm"
- **Context**: Ratio of negative supply sentiment to neutral/positive

### 3. MS (Momentum Score)
**Formula**: `Sigmoid( (V_today - V_3days_ago) / V_3days_ago )`
- **Goal**: Capture the *acceleration* of social chatter
- **Correction**: Normalized so a 50% volume spike maps to ~0.7 MS

### 4. TSS (Temporal Seasonality Score)
**Formula**: `Lookup(Current_Date, Seasonal_Calendar)`
- **Tet Holiday**: 1.0 (Peak stress)
- **Fruit Harvest (Mekong)**: 0.7
- **Month-End**: 0.3
- **Normal Day**: 0.0

---

## ❓ Q&A
      
**(Q) How does social chatter represent the whole market when much is contract logistics?**

Social groups act as the **"overflow valve"** of the logistics market.
- **Contract Logistics (Hidden)**: Large stable flows (FDI factories, big retail) operate on fixed contracts and rarely appear on Facebook.
- **Spot Market (Visible)**: When contract fleets are full, shippers flood into social groups to find trucks.
- **The Insight**: A 10% overflow into the spot market often signals 100% saturation of contract capacity. We don't need to see *all* freight to know the system is stressed—we just need to measure the pressure at the valve.

---

## �📚 Documentation

- [Product Requirements (PRD)](docs/ssff-prd.md)
- [Implementation Plan](implementation_plan.md)
- [State-Space Model Specification](ssm.md)
- [Database Schema](ssff-monorepo/database/02-schema.sql)
