---
marp: true
theme: gaia
class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.jpg')
style: |
  section { font-family: 'Arial', sans-serif; }
  code { font-size: 18px; }
---

# SSFF: Socio-Spatial Freight Forecast
### Turning Social Chatter into Logistics Intelligence

**Presenter**: [Your Name]  
**Date**: February 2026

---

# Slide 2: The Problem

## The Logistics "Blind Spot"

*   **Lagging Data**: Traditional logistics relies on contracts and historical statistics (weeks/months old).
*   **The Reality**: The market moves fast. Real-time demand spikes happen in informal channels:
    *   Facebook Trucking Groups ("Cần xe gấp!")
    *   Zalo Driver Chats
    *   TikTok comments
*   **The Consequence**:
    *   **Shippers**: Panic booking & surge pricing (+30% costs).
    *   **Carriers**: Empty return legs because they missed the signal.

**We are optimizing based on the past, while the market lives in the present.**

---

# Slide 3: The Solution

## From Noise to Signal

We propose a **"Lakehouse" Architecture** that converts unstructured social text into a structured **Desperation Index**.

```mermaid
graph LR
    A[("Social Media Noise\n(Chaos)")] -->|Crawl & Embed| B[("AI Processing\n(The Brain)")]
    B -->|Extract & Filter| C[("Structured Signals\n(The Data)")]
    C -->|SSM & Map| D[("Logistics Intelligence\n(The Map)")]
    
    style A fill:#ffdddd,stroke:#333,stroke-width:2px
    style B fill:#ddffdd,stroke:#333,stroke-width:2px
    style C fill:#ddddff,stroke:#333,stroke-width:2px
    style D fill:#ffffdd,stroke:#333,stroke-width:2px
```

*   **Listen**: Monitor social channels 24/7.
*   **Understand**: Use AI to detect urgency and location.
*   **Predict**: Forecast demand before it hits the mainstream market.

---

# Slide 4: Data Pipeline

## Phase 1: Acquisition (The "Lake")

We ingest data from where the drivers and shippers actually talk.

```mermaid
flowchart TD
    subgraph Sources
    FB[Facebook Groups]
    ZL[Zalo Chats]
    TT[TikTok]
    end

    subgraph Ingestion
    Crawler[Python Crawler]
    Cleaner[PII Removal & De-dupe]
    end

    subgraph Storage
    DB[(PostgreSQL + pgvector)]
    end

    FB & ZL & TT --> Crawler
    Crawler --> Cleaner
    Cleaner --> DB
```

*   **Raw Input**: Unstructured text, slang, emojis.
*   **Storage**: Vector embeddings allow semantic search (e.g., matching "cứu" with "urgency").

---

# Slide 5: Processing Phase

## Phase 2: Signal Extraction (The "Refinery")

Turning text into data points.

```mermaid
sequenceDiagram
    participant Raw as Raw Text
    participant LLM as LLM Extractor
    participant DB as Signal Table
    
    Raw->>LLM: "Need 5 trucks HCM->Hanoi ASAP!"
    LLM->>LLM: Analyze Content
    Note over LLM: Origin: HCM<br/>Dest: Hanoi<br/>Urgency: Critical (90/100)
    LLM->>DB: Insert Signal {Lat, Long, Score}
```

**Key Outputs**:
1.  **Origin/Destination**: Where is the demand?
2.  **Commodity**: What is moving? (Rice, Fruit, Steel)
3.  **Urgency Score**: How desperate is the shipper?

---

# Slide 6: The Innovation - SSM

## Phase 3: State-Space Model (SSM)

Social data is noisy. We use **Kalman Filtering** to find the truth.

```mermaid
graph TD
    Obs[("Noisy Observations\n(What people say)")] -->|Input| KF[("Kalman Filter\n(The Math)")]
    Seas[("Seasonality\n(Tet/Harvest)")] -->|Context| KF
    
    KF -->|Estimate| State[("Latent State\n(True Demand)")]
    State -->|Map| DI(("Desperation Index\n(0-100)"))

    style Obs fill:#f9f,stroke:#333
    style State fill:#bbf,stroke:#333
    style DI fill:#f00,stroke:#333,color:#fff
```

*   **The Problem**: One person spamming "URGENT" isn't a crisis. 100 people doing it is.
*   **The Fix**: SSM smooths out the noise and combines it with seasonal baselines (Tet, Harvest) to produce a stable **Desperation Index**.

---

# Slide 7: Conclusion

## Moving from Reaction to Anticipation

**SSFF** gives logistics leaders a weather map for market volatility.

*   **Predict** congestion before it happens.
*   **Position** fleets proactively.
*   **Price** dynamically based on Desperation Index.

### Next Steps:
1.  Deploy Data Crawler (Phase 1)
2.  Calibrate Desperation Model
3.  Launch Pilot Dashboard

**Thank You.**
