# SSFF – Frontend Requirements

---

## 1. Purpose

The frontend provides an interactive web interface for exploring
**time-based socio-spatial freight patterns** in Vietnam.

It focuses on **visualization and usability**, not data processing or crawling.

---

## 2. Application Structure

### 2.1 Main Layout

- Web-based single-page application (SPA)
- Desktop-first design
- Responsive for tablet screens
- Persistent navigation with **collapsible / dropdown menu**

---

## 3. Navigation

### 3.1 Sections

The navigation menu must contain two entries:

1. **Visualization**
2. **Optimization**

- Menu must be collapsible
- Only one section visible at a time

---

## 4. Visualization Section (Main Page)

### 4.1 Time Control Component

- A **time slider** allowing users to:
  - Select a specific time range
  - Move forward / backward in time
- Slider updates visualizations immediately
- Time granularity configurable (e.g. day / week / month)

---

### 4.2 Map Visualization

- Interactive map of Vietnam
- Displays:
  - Nodes (e.g. provinces, hubs, ports)
  - Edges (freight connections between nodes)

#### Map Behavior
- Zoom and pan
- Hover to view summary data
- Click to select a node or route

#### Visual Encoding
- Color, thickness, or opacity to represent:
  - Activity level
  - Demand intensity
  - Stress / imbalance (if available)

---

### 4.3 Data Handling (Frontend)

- Frontend **does not process raw data**
- Data is retrieved via backend APIs
- Frontend only:
  - Requests data
  - Renders visual components
  - Handles user interaction

---

## 5. Optimization Section (Placeholder)

### 5.1 Current State

- Accessible via navigation
- Displays:
  - “Under Development” / “Coming Soon” message
- No functional components required

---

## 6. Non-Functional Requirements

### 6.1 Performance
- Time slider interaction should feel instant
- Map redraw latency should be minimal

### 6.2 Usability
- Intuitive controls
- Clear legends and labels
- Suitable for non-technical logistics managers

### 6.3 Extensibility
- UI should allow future additions:
  - New data layers
  - Filters
  - Optimization controls

---

## 7. Out of Scope

- Authentication
- Role-based access
- Editing or writing data
- Crawling or ingestion logic

---
