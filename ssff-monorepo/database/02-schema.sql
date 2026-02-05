-- 1. Locations
CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    geo GEOGRAPHY(POINT, 4326) GENERATED ALWAYS AS (ST_MakePoint(longitude, latitude)::geography) STORED
);

-- 2. Time Buckets
CREATE TABLE time_buckets (
    time_id SERIAL PRIMARY KEY,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    granularity TEXT NOT NULL -- 'day', 'week', 'month'
);

-- 3. AI-Extracted Signals (The core MVP table)
CREATE TABLE signals (
    signal_id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES locations(location_id),
    time_id INTEGER REFERENCES time_buckets(time_id),
    quantity_score FLOAT, -- Relative demand level
    sentiment_score FLOAT, -- -1.0 to +1.0
    urgency_score FLOAT, -- 0 to 100 (Desperation Index)
    source_type TEXT, -- 'facebook', 'zalo', 'tiktok'
    evidence_snippet TEXT, -- Original text snippet for "Drill Down"
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Network Flows (Optional/Visual)
CREATE TABLE flows (
    flow_id SERIAL PRIMARY KEY,
    origin_location_id INTEGER REFERENCES locations(location_id),
    destination_location_id INTEGER REFERENCES locations(location_id),
    time_id INTEGER REFERENCES time_buckets(time_id),
    flow_intensity FLOAT,
    urgency_score FLOAT
);

-- 5. Raw Vectors (Lakehouse Layer)
-- Stores the raw embeddings before they are condensed into signals
CREATE TABLE vectors (
    vector_id BIGSERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1536), -- Assuming OpenAI dimension
    metadata JSONB, -- {source, timestamp, author}
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_signals_loc_time ON signals(location_id, time_id);
CREATE INDEX idx_locations_geo ON locations USING GIST(geo);
CREATE INDEX idx_vectors_embedding ON vectors USING hnsw (embedding vector_cosine_ops);
