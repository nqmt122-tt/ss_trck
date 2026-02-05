# Implementation Plan - Draft: Socio-Spatial Freight Forecast (SSFF)

**Status**: DRAFT (Pending User Clarification)
**Date**: 2026-02-05

## Goal Description
Build the MVP for **SSFF**, a dashboard that visualizes real-time freight demand and urgency ("desperation") in Vietnam based on social media signals. The goal is to provide logistics managers with a "weather map" of trucking demand.

## User Review Required
> [!IMPORTANT]
> **Tech Stack Confirmation**: 
> - **Frontend**: Next.js (React) - robust standard for dashboards.
> - **Backend**: Python (FastAPI).
> - **Data Layer**: 
>     - **Processing**: pgvector (PostgreSQL extension) to store/search raw text embeddings.
>     - **Serving**: PostGIS (PostgreSQL extension) for spatial queries.
>     - *Why both?* We need vectors to interpret the "fuzzy" anxiety signals, but rigid SQL for the time-slider/map filtering. They can live in the same Postgres instance.

## Proposed Architecture
- **Frontend**: Single Page Application (Next.js) for map visualization.
- **Backend API**: Python FastAPI service.
- **Data Pipeline (One-off Ingestion)**:
    1. **Raw Text** (Crawled files) -> 
    2. **Vector Store** (Embeddings) -> 
    3. **LLM Classifier** (Extract Location/Time/Sentiment) -> 
    4. **Structured DB** (Signals Table).
- **Database**: PostgreSQL with `postgis` and `vector` extensions.

## Phased Delivery Plan

### Phase 0: Data Acquisition (Crawler)
- **Status**: Standalone "One-off" Job.
- **Goal**: Scrape public signals to build the initial dataset.
- **Tech**: Python scripts (Playwright/Selenium or APIs).
- **Targets**: Facebook Groups, Zalo, TikTok comments.
- **Output**: Raw JSON/Text files containing time, source, and text content.

### Phase 1: Foundation & Data Pipeline
- Initialize Monorepo.
- Set up PostgreSQL (PostGIS + pgvector).
- **Ingestion Script**: 
    - Read Phase 0 output.
    - Generate Embeddings (OpenAI/SentenceTransformers).
    - Store in `vectors` table.
    - Run LLM Extraction:
        - Extract **Origin** and **Destination** (e.g., "Quảng Trị" -> "Nam Định").
        - Map **Urgency/Signal** to the **Origin** location (where the truck is needed).
        - Store route details in `flows` or metadata.
    - Store in `signals` table.

### Phase 2: Backend API Layer
- Set up FastAPI project.
- Implement API Endpoints:
    - `GET /api/network`: Fetch nodes/edges.
    - `GET /api/signals`: Fetch aggregated metrics by time/location.
- Implement filtering logic (Time range, Location bounds).

### Phase 3: Frontend Visualization (Current Task)
- **Setup**: Initialize Next.js (App Router) in `ssff-monorepo/frontend`.
- **Styling**: Tailwind CSS + `frontend-design` aesthetics (Glassmorphism, dark mode).
- **Map Tech**: 
    - **Mapbox GL JS / MapLibre** (Base map).
    - **Deck.gl** (High-performance flow visualization - `ArcLayer`).
- **Components**:
    - `TimeSlider`: Custom month selector (1-12) with animation.
    - `FlowMap`: Visualizes origin-destination arrows with color heatmaps.
    - `SidePanel`: Floating glass-panel for insights (Season, Volume).
- **Data**: Mock data integration for initial build.

### Phase 4: Integration & Polish
- Connect Frontend to Backend API.
- Implement "Desperation Index" visualization (Color coding: Green -> Red).
- Responsive layout adjustments.
- Basic error handling and loading states.

## Verification Plan
### Automated Tests
- Backend: Pytest for API endpoints and aggregation logic.
- Frontend: Jest/React Testing Library for component rendering.

### Manual Verification
- **Visual Check**: Verify map updates instantly when slider moves.
- **Data Accuracy**: Cross-check API responses against database seed data.
- **Performance**: Ensure map remains responsive with simulated high data volume.
