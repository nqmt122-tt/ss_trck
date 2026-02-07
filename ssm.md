# State-Space Model (SSM) for Desperation Index  
**Project**: Socio-Spatial Freight Forecast (SSFF)  
**Status**: Design Specification (v1.1)

---

## 1. Purpose

This document defines the **State-Space Model (SSM)** used to estimate the
**Desperation Index (DI)** — a route-level indicator representing logistics
stress and truck scarcity over time.

The goal is to infer an **unobserved (latent) freight stress state** from noisy
social, temporal, and seasonal signals.

---

## 2. Conceptual Overview

Logistics stress is not directly observable.  
Instead, it manifests indirectly through:

- Urgent freight requests on social platforms
- Signals of truck unavailability
- Rapid increases in posting volume
- Known seasonal demand patterns (Tet, harvest, export windows)

The SSM treats true logistics stress as a **latent dynamic variable** that
evolves over time and is inferred from these observed signals.

---

## 3. Latent State Definition

Let:

$$
x_t \in \mathbb{R}
$$

be the **latent freight stress level** for a specific route at time $t$.

Properties:
- Continuous
- Time-dependent
- Persistent with occasional shocks

---

## 4. State Transition Model (System Dynamics)

### 4.1 Base formulation

$$
x_t = a \cdot x_{t-1} + w_t
$$

Where:
- $a \in (0,1)$: stress persistence coefficient  
- $w_t \sim \mathcal{N}(0, Q)$: process noise (unexpected demand shocks)

Interpretation:
- Stress decays slowly without new demand
- Sudden market pressure appears as stochastic shocks

---

### 4.2 Seasonal extension

$$
x_t = a \cdot x_{t-1} + b \cdot S_t + w_t
$$

Where:
- $S_t$: seasonal indicator (e.g. Tet, harvest)
- $b$: seasonal impact coefficient

---

## 5. Observation Model

Observed signals are treated as **noisy projections** of the latent stress.

### 5.1 Observation vector

$$
\mathbf{y}_t =
\begin{bmatrix}
DPS_t \\
SSS_t \\
MS_t \\
TSS_t
\end{bmatrix}
$$

Where:
- **DPS**: Demand Pressure Score  
- **SSS**: Supply Scarcity Score  
- **MS**: Momentum Score  
- **TSS**: Temporal Seasonality Score  

Each signal is normalized to $[0,1]$.

---

### 5.1.1 Signal Computation

| Signal | Formula | Source |
|--------|---------|--------|
| **DPS** (Demand Pressure) | Count of "urgent" keywords (gấp, cứu, kẹt) normalized by route volume | Social posts |
| **SSS** (Supply Scarcity) | Ratio of "no truck available" posts / total posts | Social posts |
| **MS** (Momentum) | 3-day rolling change in post volume: $(V_t - V_{t-3}) / V_{t-3}$ | Time series |
| **TSS** (Temporal Seasonality) | Lookup from seasonal calendar (Tet=1.0, Harvest=0.7, Normal=0.0) | External calendar |

---

### 5.2 Observation equation

$$
\mathbf{y}_t = \mathbf{C} \cdot x_t + \mathbf{v}_t
$$

Where:
- $\mathbf{C} \in \mathbb{R}^{4 \times 1}$: observation loading matrix  
- $\mathbf{v}_t \sim \mathcal{N}(0, R)$: observation noise  

Example:
$$
\mathbf{C} =
\begin{bmatrix}
0.40 \\
0.35 \\
0.15 \\
0.10
\end{bmatrix}
$$

---

## 6. Complete State-Space Formulation

$$
\begin{aligned}
x_t &= a x_{t-1} + b S_t + w_t, \quad w_t \sim \mathcal{N}(0, Q) \\
\mathbf{y}_t &= \mathbf{C} x_t + \mathbf{v}_t, \quad \mathbf{v}_t \sim \mathcal{N}(0, R)
\end{aligned}
$$

This defines a **Linear Gaussian State-Space Model**.

---

## 7. Inference Method

A **Kalman Filter** is used to estimate the posterior distribution of $x_t$.

### 7.1 Prediction step

$$
\hat{x}_{t|t-1} = a \hat{x}_{t-1|t-1} + b S_t
$$

$$
P_{t|t-1} = a^2 P_{t-1|t-1} + Q
$$

---

### 7.2 Update step

**Kalman Gain:**
$$
K_t = P_{t|t-1} \mathbf{C}^\top
(\mathbf{C} P_{t|t-1} \mathbf{C}^\top + R)^{-1}
$$

**State Update:**
$$
\hat{x}_{t|t} = \hat{x}_{t|t-1} + K_t(\mathbf{y}_t - \mathbf{C}\hat{x}_{t|t-1})
$$

**Covariance Update:**
$$
P_{t|t} = (I - K_t \mathbf{C}) P_{t|t-1}
$$

---

### 7.3 Parameter Initialization

| Parameter | Suggested Initial Value | Rationale |
|-----------|------------------------|-----------|
| $a$ (persistence) | 0.85 | Demand stress decays ~15% per day |
| $b$ (seasonal) | 0.30 | Tet/harvest adds ~30% to base stress |
| $Q$ (process noise) | 0.10 | Small random shocks expected |
| $R$ (observation noise) | diag(0.15, 0.20, 0.25, 0.10) | SSS/MS noisier than DPS/TSS |
| $x_0$ (initial state) | 0.0 | Start at neutral stress |
| $P_0$ (initial covariance) | 1.0 | High initial uncertainty |

---

## 8. Desperation Index Mapping

The Desperation Index (DI) is a normalized representation of the latent state.

### Option A: Sigmoid scaling (Recommended)

$$
DI_t = 100 \cdot \frac{1}{1 + e^{-x_t}}
$$

### Option B: Rolling Min–Max Scaling

$$
DI_t = 100 \cdot \frac{x_t - \min(x)}{\max(x) - \min(x)}
$$

---

## 9. Interpretation

| DI Range | Level | Color | Operational Meaning |
|----------|-------|-------|---------------------|
| 0–30 | Stable | 🟢 Green | No action needed |
| 31–55 | Tight | 🟡 Yellow | Monitor closely |
| 56–75 | Hot | 🟠 Orange | Prepare capacity & pricing |
| 76–100 | Critical | 🔴 Red | Immediate intervention |

---

## 10. Model Extensions (Future Work)

### 10.1 Multi-Route State Vector

For N routes, extend to vector state:

$$
\mathbf{x}_t = [x_t^{(1)}, x_t^{(2)}, ..., x_t^{(N)}]^\top
$$

With cross-route spillover matrix $\mathbf{A}$ capturing:
- Geographic adjacency effects (neighboring provinces)
- Supply chain dependencies (origin-destination pairs)

### 10.2 Advanced Extensions

- **Switching State-Space Model**: Regime-dependent dynamics (normal vs crisis mode)
- **Hidden Markov Model**: Discrete stress states instead of continuous
- **Bayesian Parameter Estimation**: Learn $a$, $b$, $\mathbf{C}$ from historical data
- **Non-linear Extensions**: Extended Kalman Filter (EKF) or Unscented Kalman Filter (UKF)

---

## 11. Rationale

This SSM framework:
- Is grounded in control theory and econometrics
- Is widely used in traffic, finance, and stress monitoring
- Provides explainable and stable estimates
- Aligns with SSFF's social + spatial data architecture

---

## 12. Implementation Notes

### 12.1 Phased Approach

| Version | Approach | Complexity |
|---------|----------|------------|
| **v1** | Weighted EWMA approximation | Low |
| **v2** | Full Kalman Filter (single route) | Medium |
| **v3** | Multi-route with interaction | High |

### 12.2 Python Libraries

- `filterpy`: Kalman Filter implementation
- `pykalman`: Alternative with EM learning
- `statsmodels.tsa.statespace`: Built-in SSM support

### 12.3 Data Requirements

- Minimum 30 days of historical signals for parameter tuning
- Daily granularity recommended for v1
- Hourly granularity for real-time v2+

---
