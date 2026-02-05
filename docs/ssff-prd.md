# Product Requirements Document: Socio-Spatial Freight Forecast (SSFF)

**Version**: 1.0
**Date**: 2026-02-05
**Author**: Sarah (Product Owner)
**Quality Score**: 92/100

---

## Executive Summary

SSFF is a "Socio-Spatial" dashboard designed to give Vietnamese logistics managers a real-time "weather map" of trucking demand. By analyzing social media signals (Facebook, Zalo, TikTok) for urgency keywords and location data, SSFF predicts demand spikes—like the Tet flower rush or fruit harvest congestion—before they appear in traditional lagging statistics. This allows shippers to secure capacity early and carriers to position trucks where they are needed most, reducing "desperation pricing" and empty backhauls.

---

## Problem Statement

**Current Situation**: Logistics planning in Vietnam relies on static contracts and lagging government data. Real-time market shifts happen on informal social channels (Facebook groups, Drivers' Zalo chats), leaving managers blind to sudden spikes until prices surge or trucks become unavailable.

**Proposed Solution**: A dashboard that visualizes an aggregated "Desperation Index" on a map of Vietnam. It ingests unstructured social chatter, translates it into structured demand signals (Time, Location, Intensity, Urgency), and displays it on a time-slider map.

**Business Impact**:
- **For Shippers**: Avoid panic booking premiums (approx. 20-30% surges).
- **For Carriers**: Reduce empty miles by positioning fleets in high-demand zones proactively.

---

## Success Metrics

**Primary KPIs:**
1.  **Prediction Lead Time**: Signals appear on dashboard 2-3 days before standard rate hikes.
2.  **Signal Accuracy**: >80% of "High Heat" zones correlate with actual price surges or congestion (validated by user feedback).
3.  **User Trust**: Users mistakenly clicking "Drill Down" < 10% of the time (indicating they trust the aggregated color code).

**Validation**:
- Manual replay of historical "Tet 2025" data to verify if the heatmap lights up correctly during known peak days.

---

## User Personas

### Primary: The Logistics Manager (Shipper Side)
- **Role**: Head of Logistics for an FMCG or Agriculture company.
- **Goal**: Ensure 100% order fulfillment at budgeted cost.
- **Pain Points**: Sudden inability to find trucks; being forced to pay 2x rates due to "surprise" market shortages.
- **Behavior**: Checks the dashboard on Monday morning to plan the week's bookings.

### Secondary: The Fleet Planner (Carrier Side)
- **Role**: Dispatcher for a trucking fleet (10-50 trucks).
- **Goal**: Keep trucks full in both directions.
- **Pain Points**: Sending trucks to a harvest area only to find the season ended yesterday.
- **Behavior**: Uses the map to decide where to send empty trucks returning from deliveries.

---

## Functional Requirements

### Core Features

**Feature 1: Interactive Time-Travel Map**
- **Description**: A map of Vietnam with a timeline slider at the bottom.
- **User Flow**: User drags slider to "Next Week" -> Map heatmap updates to show predicted hot zones.
- **Visualization**:
    - **Green**: Normal activity.
    - **Yellow**: Rising chatter/activity.
    - **Red**: High "Desperation" (Keywords: "gấp", "cứu", "kẹt").

**Feature 2: Desperation Index & Drill-Down**
- **Description**: Aggregated score (0-100) of market anxiety.
- **User Flow**: User sees a "Red" zone in Long An. They click the zone. A side panel opens showing the "Evidence": anonymous snippets like *"Need 5 trucks for dragon fruit ASAP at unreasonable price!"* or *"Border gate stuck for 3 days"*.
- **Purpose**: Builds trust in the AI's "Red" rating.

**Feature 3: Filters**
- **Description**: Toggle view by Commodity (if detected) or Vehicle Type.
- **Scope (MVP)**: Simple filter for "General Freight" vs "Perishables" (if distinction exists in data), otherwise global aggregate.

### Out of Scope (MVP)
- Real-time live streaming (Data is batched/one-off for MVP).
- Automated booking/bidding matching.
- User accounts (Open access demo).

---

## Technical Constraints & Architecture

### Architecture (Lakehouse Pattern)
1.  **Crawler (Phase 0)**: Standalone Python scripts targeting public groups. Outputs raw JSON.
2.  **Ingestion & Processing**:
    - **Vector Store (pgvector)**: Stores embeddings of raw posts to cluster similar signals.
    - **LLM/Classifier**: Python script extracts `(Lat, Long, Time, UrgencyScore)` from text.
3.  **Serving**:
    - **DB**: PostgreSQL with PostGIS (for map queries).
    - **Backend**: FastAPI (Python).
    - **Frontend**: Next.js (React).

### Performance
- Map tiles/points must load in < 1s.
- Time slider animation must be smooth (60fps).

### Privacy
- **Strict Rule**: No PII (Personally Identifiable Information) displayed. Snippets must be anonymized or aggregated.

---

## Verification Plan

### Automated
- **Backend**: Pytest for API response formats.
- **Data Pipeline**: Unit tests for the "Text -> Lat/Long" extractor to ensure it doesn't map "Hanoi" to "Ho Chi Minh City".

### Manual
- **"The Tet Test"**: Load a dataset from a past Tet holiday. The map *must* light up red in the days leading up to the holiday. If it stays green, the Desperation Algorithm is wrong.

---

## Roadmap

**Phase 0**: Data Crawling (Standalone Job)
**Phase 1**: Data Pipeline (Vector -> Structured)
**Phase 2**: Backend API & Map Tiles
**Phase 3**: Frontend Dashboard & Polish

---
*This PRD defines the scope for the initial MVP of SSFF, focusing on the "Weather Map" visualization of logistics anxiety.*
