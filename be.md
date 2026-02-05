# SSFF – Backend Requirements

---

## 1. Purpose

The backend serves as a **data access and aggregation layer** between
the existing data-crawling module and the frontend application.

It does **not** handle crawling, scraping, or raw data ingestion.

---

## 2. System Scope

### Included
- API layer for frontend consumption
- Querying and aggregating pre-existing datasets
- Time-based and spatial filtering

### Excluded
- Social data crawling
- Data collection pipelines
- Machine learning or optimization logic (Phase 1)

---

## 3. Data Assumptions

- Data is already available in a database managed by a separate module
- Backend has:
  - Read-only access to relevant tables or views
- Data includes (at minimum):
  - Time dimension
  - Geographic identifiers
  - Network relationships (origin → destination)

---

## 4. Core Responsibilities

### 4.1 API Layer

The backend must expose APIs to support:

- Time-range queries
- Spatial queries
- Network data retrieval

Example responsibilities:
- Fetch network state at a given time
- Aggregate demand or activity by location
- Return data in frontend-friendly formats

---

### 4.2 Time-Based Aggregation

- Support queries by:
  - Start time
  - End time
- Aggregate data according to requested granularity:
  - Daily
  - Weekly
  - Monthly

---

### 4.3 Spatial & Network Modeling

Backend should return:
- Nodes:
  - ID
  - Location (province / coordinates)
  - Aggregated metrics
- Edges:
  - Origin
  - Destination
  - Weight / intensity values

---

## 5. API Design (High-Level)

### Example Endpoints (Illustrative)

- `GET /api/network?start_time=&end_time=`
- `GET /api/nodes?time=`
- `GET /api/edges?time=`

Exact schema and naming are implementation-dependent.

---

## 6. Performance & Reliability

- APIs should support:
  - Fast read queries
  - Caching where applicable
- Must handle:
  - Frequent slider-driven requests
  - Concurrent users

---

## 7. Security & Access

- Read-only access to database
- No data mutation endpoints in Phase 1
- Authentication not required in initial version

---

## 8. Extensibility (Future Phases)

Backend architecture should allow future integration of:
- Desperation index computation
- Predictive models
- Optimization and recommendation engines

---

## 9. Out of Scope (Phase 1)

- Optimization logic
- AI agents
- Price recommendation
- Alerting or notification systems

---

## 10. Success Criteria

- Backend reliably serves:
  - Time-filtered
  - Spatially-aggregated
  - Network-structured data
- Frontend can render map and time slider without additional processing

---
