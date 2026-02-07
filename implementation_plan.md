# Implementation Plan: Socio-Spatial Freight Forecast (SSFF)

**Status**: Active  
**Date**: 2026-02-06  
**Version**: 2.0

---

## Goal Description

Build **SSFF**, a dashboard that visualizes real-time freight demand and urgency ("desperation") in Vietnam based on social media signals. The system uses a **State-Space Model (SSM)** to estimate a latent "Desperation Index" from noisy social observations.

---

## Project Phases Overview

| Phase | Name | Focus | Deliverable |
|-------|------|-------|-------------|
| **1** | Data Collection & Cleaning | Acquire and prepare data | Clean dataset + embeddings |
| **2** | Analysis & Visualization | Extract signals + build UI | Working dashboard |
| **3** | SSM Application | Apply Kalman Filter + prediction | Desperation Index engine |

---

## Phase 1: Data Collection & Cleaning

### 1.1 Data Acquisition

#### [MODIFY] [crawler.py](file:///Volumes/Personal/Coding/10/ssff-monorepo/crawler/crawler.py)
- Implement real crawler logic (Playwright/Selenium)
- Target sources: Facebook Groups, Zalo, TikTok
- Output: Raw JSON with `{source, timestamp, content, url}`

#### [NEW] `ssff-monorepo/crawler/sources.json`
- Configuration file for target URLs and groups
- Rate limiting and scheduling parameters

### 1.2 Data Cleaning

#### [NEW] `ssff-monorepo/data-pipeline/cleaner.py`
- Text normalization (Vietnamese diacritics, slang)
- Deduplication (hash-based)
- PII removal (phone numbers, names)
- Spam/ad filtering

### 1.3 Embedding Generation

#### [MODIFY] [ingest.py](file:///Volumes/Personal/Coding/10/ssff-monorepo/data-pipeline/ingest.py)
- Generate embeddings using OpenAI or SentenceTransformers
- Store in `vectors` table with metadata
- Batch processing for efficiency

### 1.4 Database Setup

#### [EXISTING] [02-schema.sql](file:///Volumes/Personal/Coding/10/ssff-monorepo/database/02-schema.sql)
- PostgreSQL with PostGIS + pgvector
- Tables: `locations`, `time_buckets`, `signals`, `flows`, `vectors`

**Phase 1 Verification:**
- [ ] Crawler successfully fetches 100+ posts
- [ ] Cleaner removes duplicates and PII
- [ ] Embeddings stored in pgvector (query test)

---

## Phase 2: Analysis & Visualization

### 2.1 Signal Extraction (LLM/NLP)

#### [MODIFY] [ingest.py](file:///Volumes/Personal/Coding/10/ssff-monorepo/data-pipeline/ingest.py)
- LLM prompt to extract:
  - **Origin**: Where the truck is needed
  - **Destination**: Where the truck goes
  - **Commodity**: e.g., Rice, Dragon Fruit
  - **Urgency Score**: 0-100 raw score

#### [NEW] `ssff-monorepo/data-pipeline/signal_aggregator.py`
- Compute observation signals for SSM:
  - **DPS**: Demand Pressure Score
  - **SSS**: Supply Scarcity Score
  - **MS**: Momentum Score (3-day rolling)
  - **TSS**: Temporal Seasonality Score

### 2.2 Backend API

#### [NEW] `ssff-monorepo/backend/main.py`
- FastAPI application
- Endpoints:
  - `GET /api/signals` - Aggregated signals by time/location
  - `GET /api/flows` - Origin-destination flow data
  - `GET /api/locations` - Location reference data
  - `GET /api/desperation` - DI scores by route

### 2.3 Frontend Dashboard

#### [NEW] `ssff-monorepo/frontend/`
- **Framework**: Next.js (App Router)
- **Styling**: Tailwind CSS + Glassmorphism
- **Map**: Mapbox GL JS + Deck.gl (ArcLayer for flows)

**Components:**
- `TimeSlider`: Month selector (1-12) with animation
- `FlowMap`: Origin-destination arrows with color heatmaps
- `SidePanel`: Floating glass-panel for insights
- `DesperationGauge`: Visual DI indicator

**Phase 2 Verification:**
- [ ] API returns valid GeoJSON
- [ ] Map renders with flow arrows
- [ ] Time slider updates visualization
- [ ] Side panel shows drill-down snippets

---

## Phase 3: SSM Application

### 3.1 Kalman Filter Implementation

#### [NEW] `ssff-monorepo/ssm/kalman_filter.py`
- Implement Linear Gaussian SSM per [SSM Specification](ssm.md)
- State transition: `x_t = a * x_{t-1} + b * S_t + w_t`
- Observation model: `y_t = C * x_t + v_t`
- Prediction and update steps

#### [NEW] `ssff-monorepo/ssm/parameters.py`
- Parameter configuration:
  - `a = 0.85` (persistence)
  - `b = 0.30` (seasonal impact)
  - `C = [0.40, 0.35, 0.15, 0.10]` (observation weights)
  - `Q = 0.10`, `R = diag(0.15, 0.20, 0.25, 0.10)`

### 3.2 Desperation Index Engine

#### [NEW] `ssff-monorepo/ssm/desperation_index.py`
- Map latent state to DI (0-100): `DI = 100 / (1 + exp(-x))`
- Route-level DI computation
- Historical DI tracking

### 3.3 Prediction Engine

#### [NEW] `ssff-monorepo/ssm/predictor.py`
- Forecast DI for next 1-3 days
- Confidence intervals from covariance
- Alert threshold detection

### 3.4 API Integration

#### [MODIFY] `ssff-monorepo/backend/main.py`
- Add endpoints:
  - `GET /api/desperation/{route_id}` - Current DI
  - `GET /api/forecast/{route_id}` - Predicted DI
  - `GET /api/alerts` - Routes exceeding threshold

### 3.5 Frontend Updates

#### [MODIFY] `ssff-monorepo/frontend/`
- Add DI visualization layer on map
- Add prediction timeline component
- Add alert notification system

**Phase 3 Verification:**
- [ ] Kalman Filter produces valid estimates
- [ ] DI matches expected interpretation table
- [ ] Forecast accuracy on historical "Tet Test" data
- [ ] Alerts trigger correctly for DI > 75

---

## Verification Plan

### Automated Tests
- **Backend**: Pytest for API endpoints
- **SSM**: Unit tests for Kalman math correctness
- **Data Pipeline**: Validation of extractor accuracy

### Manual Verification
- **Visual Check**: Map updates smoothly with slider
- **Tet Test**: Historical replay shows red zones during Tet 2025
- **Performance**: Map responsive with 1000+ signals

---

## Tech Stack Summary

| Component | Technology |
|-----------|------------|
| Crawler | Python + Playwright |
| Database | PostgreSQL + PostGIS + pgvector |
| Backend | Python + FastAPI |
| Frontend | Next.js + Deck.gl + Mapbox |
| SSM Engine | Python + filterpy/numpy |
| Infrastructure | Docker Compose |

---

## File Index

| Path | Purpose |
|------|---------|
| `ssff-monorepo/crawler/crawler.py` | Data acquisition |
| `ssff-monorepo/data-pipeline/cleaner.py` | Text cleaning |
| `ssff-monorepo/data-pipeline/ingest.py` | Embedding + extraction |
| `ssff-monorepo/data-pipeline/signal_aggregator.py` | Compute SSM inputs |
| `ssff-monorepo/backend/main.py` | API server |
| `ssff-monorepo/frontend/` | Dashboard UI |
| `ssff-monorepo/ssm/kalman_filter.py` | Core SSM engine |
| `ssff-monorepo/ssm/desperation_index.py` | DI mapping |
| `ssff-monorepo/ssm/predictor.py` | Forecast engine |
