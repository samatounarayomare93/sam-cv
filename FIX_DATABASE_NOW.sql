-- ==========================================
-- PROTOCOL GENESIS: SUPABASE SCHEMA RESTORATION
-- ==========================================

-- 1. Restore Applications Schema (Fixes 400 Errors on POST)
ALTER TABLE applications ADD COLUMN IF NOT EXISTS company_email TEXT;
ALTER TABLE applications ADD COLUMN IF NOT EXISTS job_url TEXT;
ALTER TABLE applications ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'SENT';
ALTER TABLE applications ADD COLUMN IF NOT EXISTS mission_phase TEXT;
ALTER TABLE applications ADD COLUMN IF NOT EXISTS custom_body_id TEXT;
ALTER TABLE applications ADD COLUMN IF NOT EXISTS psychological_variant TEXT;
ALTER TABLE applications ADD COLUMN IF NOT EXISTS culture_persona TEXT;
ALTER TABLE applications ADD COLUMN IF NOT EXISTS lead_score INTEGER DEFAULT 0;
ALTER TABLE applications ADD COLUMN IF NOT EXISTS cheat_sheet TEXT;
ALTER TABLE applications ADD COLUMN IF NOT EXISTS timestamp TIMESTAMPTZ DEFAULT now();

-- 2. Create Core Operational Tables (Fixes 404 Errors on Heartbeat)
CREATE TABLE IF NOT EXISTS nodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    node_id TEXT UNIQUE,
    node_name TEXT,
    last_active TIMESTAMPTZ DEFAULT now(),
    ip_hint TEXT
);

CREATE TABLE IF NOT EXISTS system_settings (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- 3. Restore Leads Schema (Ensures priority tracking works)
ALTER TABLE leads ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT now();
ALTER TABLE leads ADD COLUMN IF NOT EXISTS priority_score INTEGER DEFAULT 0;

-- 4. Seed System State
INSERT INTO system_state (key, value) VALUES ('LAST_PULSE', now()::text) ON CONFLICT (key) DO NOTHING;
