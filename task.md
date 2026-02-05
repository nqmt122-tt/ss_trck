# Engineering Tasks: Socio-Spatial Freight Forecast (SSFF)

- [ ] **Phase 1: Foundation & Data Pipeline** <!-- id: 1 -->
    - [x] Initialize Project Structure (Monorepo/Folder structure) <!-- id: 2 -->
    - [/] Set up Docker Compose (PostgreSQL + PostGIS + pgvector) <!-- id: 3 -->
    - [ ] Create Database Schema (SQL/Migration scripts) <!-- id: 4 -->
    - [ ] Implement Data Ingestion Pipeline (Phase 0 output -> DB) <!-- id: 5 -->

- [ ] **Phase 0: Data Acquisition (Crawler)** <!-- id: 6 -->
    - [x] Create separate crawler directory/job <!-- id: 7 -->
    - [/] Implement basic scraper for mock/sample data <!-- id: 8 -->
    - [ ] Verify output format (JSON/Text) <!-- id: 9 -->

- [ ] **Phase 2: Backend API Layer** <!-- id: 10 -->
    - [ ] Set up FastAPI project <!-- id: 11 -->
    - [ ] Implement `GET /api/network` <!-- id: 12 -->
    - [ ] Implement `GET /api/signals` <!-- id: 13 -->

- [ ] **Phase 3: Frontend Visualization** <!-- id: 14 -->
    - [ ] Set up Next.js Project <!-- id: 15 -->
    - [ ] Implement Map Component (Leaflet/Mapbox) <!-- id: 16 -->
    - [ ] Implement Time Slider <!-- id: 17 -->
    - [ ] Integrate API with Frontend <!-- id: 18 -->

- [ ] **Phase 4: Integration & Polish** <!-- id: 19 -->
    - [ ] Implement "Desperation Index" visual styling <!-- id: 20 -->
    - [ ] Add Drill-down side panel <!-- id: 21 -->
    - [ ] End-to-end testing <!-- id: 22 -->
