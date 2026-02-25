-- Create medallion-style schemas for core tables (HDB, COE, CPI)

-- =====================================
-- Schemas
-- =====================================
CREATE SCHEMA IF NOT EXISTS raw_data;
CREATE SCHEMA IF NOT EXISTS cleaned_data;
CREATE SCHEMA IF NOT EXISTS analytics;

-- =====================================
-- RAW (Bronze) Tables
-- Store source data as-is, without transformations (JSONB)
-- =====================================
CREATE TABLE IF NOT EXISTS raw_data.hdb_resale (
    id SERIAL PRIMARY KEY,
    source_data JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT NOW(),
    source VARCHAR(100) DEFAULT 'data.gov.sg',
    batch_id VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS raw_data.coe_results (
    id SERIAL PRIMARY KEY,
    source_data JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT NOW(),
    source VARCHAR(100) DEFAULT 'data.gov.sg',
    batch_id VARCHAR(50)
);

-- =====================================
-- CLEANED (Silver) Tables
-- Store cleaned and transformed data with proper data types and structure
-- =====================================
CREATE TABLE IF NOT EXISTS cleaned_data.hdb_resale (
    id SERIAL PRIMARY KEY,
    town VARCHAR(50) NOT NULL,
    flat_type VARCHAR(30) NOT NULL,
    storey_range VARCHAR(20),
    floor_area_sqm DECIMAL(8, 2),
    resale_price DECIMAL(12, 2) NOT NULL,
    lease_commence_year INT,
    remaining_lease_years INT,
    transaction_month DATE NOT NULL,
    processed_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(town, flat_type, storey_range, floor_area_sqm, resale_price, transaction_month)
);

CREATE TABLE IF NOT EXISTS cleaned_data.coe_results (
    id SERIAL PRIMARY KEY,
    month DATE NOT NULL,
    bidding_no INT,
    vehicle_class VARCHAR(50),
    quota INT,
    bid_success INT,
    bid_received INT,
    premium DECIMAL(12, 2),
    processed_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(month, bidding_no, vehicle_class)
);

CREATE TABLE IF NOT EXISTS cleaned_data.cpi_data (
    id SERIAL PRIMARY KEY,
    month DATE NOT NULL,
    category VARCHAR(50) NOT NULL,
    cpi_value DECIMAL(8, 2),
    mom_pct_change DECIMAL(6, 2),
    yoy_pct_change DECIMAL(6, 2),
    processed_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(month, category)
);

-- =====================================
-- ANALYTICS (Gold) Tables
-- Store aggregated and analysis-ready data for reporting and visualization
-- =====================================
CREATE TABLE IF NOT EXISTS analytics.monthly_hdb_summary (
    id SERIAL PRIMARY KEY,
    town VARCHAR(50),
    flat_type VARCHAR(30),
    month DATE,
    avg_price DECIMAL(12, 2),
    median_price DECIMAL(12, 2),
    min_price DECIMAL(12, 2),
    max_price DECIMAL(12, 2),
    transactions_count INT,
    avg_price_per_sqm DECIMAL(10, 2),
    mom_pct_change DECIMAL(6, 2),
    yoy_pct_change DECIMAL(6, 2),
    computed_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(town, flat_type, month)
);

CREATE TABLE IF NOT EXISTS analytics.monthly_coe_summary (
    id SERIAL PRIMARY KEY,
    month DATE,
    vehicle_class VARCHAR(50),
    avg_premium DECIMAL(12, 2),
    mom_pct_change DECIMAL(6, 2),
    computerd_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(month, vehicle_class)
);

CREATE TABLE IF NOT EXISTS analytics.monthly_cpi_summary (
    id SERIAL PRIMARY KEY,
    month DATE,
    category VARCHAR(50),
    cpi_value DECIMAL(8, 2),
    mom_pct_change DECIMAL(6, 2),
    yoy_pct_change DECIMAL(6, 2),
    computed_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(month, category)
);

CREATE TABLE IF NOT EXISTS analytics.dashboard_kpis (
    id SERIAL PRIMARY KEY,
    kpi_name VARCHAR(100),
    kpi_value DECIMAL(14, 2),
    kpi_change_pct DECIMAL(6, 2),
    period DATE,
    computed_at TIMESTAMP DEFAULT NOW()
);

-- =====================================
-- Indexes for common query patterns
-- =====================================
CREATE INDEX IF NOT EXISTS idx_hdb_cleaned_town ON cleaned_data.hdb_resale(town);
CREATE INDEX IF NOT EXISTS idx_hdb_cleaned_month ON cleaned_data.hdb_resale(transaction_month);
CREATE INDEX IF NOT EXISTS idx_hdb_cleaned_flat_type ON cleaned_data.hdb_resale(flat_type);

CREATE INDEX IF NOT EXISTS idx_coe_cleaned_month on cleaned_data.coe_results(month);

CREATE INDEX IF NOT EXISTS idx_cpi_cleaned_month on cleaned_data.cpi_data(month);
CREATE INDEX IF NOT EXISTS idx_cpi_cleaned_category on cleaned_data.cpi_data(category);

CREATE INDEX IF NOT EXISTS idx_hdn_summary_month ON analytics.monthly_hdb_summary(month);
CREATE INDEX IF NOT EXISTS idx_coe_summary_month ON analytics.monthly_coe_summary(month);
CREATE INDEX IF NOT EXISTS idx_cpi_summary_month ON analytics.monthly_cpi_summary(month);

