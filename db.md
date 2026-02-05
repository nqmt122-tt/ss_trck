# SSFF – Database Requirements (MVP / Demo)

---

## 1. Purpose

This database supports a **demo-level SSFF system** that:
- Stores AI-processed signals from raw social posts
- Aggregates them by **time** and **location**
- Feeds a **map + time slider** visualization

The design prioritizes:
- Simplicity
- Explainability
- Fast iteration

---

## 2. Architecture Context

Data flow:

Raw Social Posts  
→ AI Processing Layer (NLP / LLM)  
→ Structured Signals (this database)  
→ Visualization / Analytics

This database **does not store raw posts**.

---

## 3. Core Concepts (Keep This Simple)

SSFF MVP tracks only **4 things**:

1. **Where** (location)
2. **When** (time bucket)
3. **How intense** (quantity / volume)
4. **How stressed** (sentiment / urgency)

---

## 4. Core Tables

---

## 4.1 Locations

#### `locations`

Minimal spatial reference.

| Column | Type | Description |
|-----|----|----|
| location_id | PK | Unique ID |
| name | TEXT | Province / city name |
| latitude | FLOAT | Latitude |
| longitude | FLOAT | Longitude |

---

## 4.2 Time Buckets

#### `time_buckets`

Predefined aggregation windows.

| Column | Type | Description |
|-----|----|----|
| time_id | PK | Unique ID |
| start_time | TIMESTAMP | Start of window |
| end_time | TIMESTAMP | End of window |
| granularity | TEXT | day / week / month |

---

## 4.3 AI-Extracted Signals

This is the **heart of the MVP**.

#### `signals`

Each row = AI summary of *many posts*.

| Column | Type | Description |
|-----|----|----|
| signal_id | PK | Unique ID |
| location_id | FK | Where the demand appears |
| time_id | FK | When it appears |
| quantity_score | FLOAT | Relative demand level |
| sentiment_score | FLOAT | -1 (negative) → +1 (positive) |
| urgency_score | FLOAT | 0–100 stress level |
| source_type | TEXT | facebook / zalo / tiktok |

---

## 4.4 Network Aggregation (Optional but Visual)

Only include if you want lines on the map.

#### `flows`

| Column | Type | Description |
|-----|----|----|
| flow_id | PK | Unique ID |
| origin_location_id | FK | From |
| destination_location_id | FK | To |
| time_id | FK | Time bucket |
| flow_intensity | FLOAT | Relative volume |

---

## 5. What the AI Layer Does (Explicit)

The AI / NLP layer is responsible for:

- Extracting:
  - Location references
  - Time references
  - Quantity hints (e.g. “20 xe”, “rất nhiều”)
- Scoring:
  - Sentiment
  - Urgency / desperation
- Normalizing outputs into numeric scores

The database **only stores the final structured result**.

---

## 6. Indexing (Minimal)

Required indexes:
- `signals(location_id, time_id)`
- `flows(origin_location_id, destination_location_id, time_id)`

No partitioning required for demo.

---

## 7. Out of Scope (MVP)

- Raw text storage
- Post-level traceability
- Complex commodity models
- Contract vs spot differentiation
- Real-time streaming

---

## 8. Why This Works for a Demo

- Easy to explain
- Easy to visualize
- Easy to extend
- AI value is obvious
- Map + time slider works immediately

---

## 9. Extension Path (Not Implemented)

Later phases may add:
- Commodity type
- Season labels (Tết, harvest)
- Contract stress overlays
- Optimization outputs

No schema redesign required.

---
