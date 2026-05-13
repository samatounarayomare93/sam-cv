-- ==========================================
-- COMPLETE DATABASE FIX - Project Chronos
-- Run this in Supabase SQL Editor
-- ==========================================

-- 1. Create system_logs table (CRITICAL - dashboard needs this)
CREATE TABLE IF NOT EXISTS system_logs (
    id BIGSERIAL PRIMARY KEY,
    level TEXT NOT NULL,
    message TEXT,
    timestamp TIMESTAMPTZ DEFAULT now()
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_system_logs_timestamp ON system_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_system_logs_level ON system_logs(level);

-- 2. Create vip_tracking table
CREATE TABLE IF NOT EXISTS vip_tracking (
    id BIGSERIAL PRIMARY KEY,
    target_id TEXT UNIQUE,
    company_name TEXT,
    hit_count INTEGER DEFAULT 0,
    last_seen TIMESTAMPTZ DEFAULT now(),
    meta TEXT
);

-- 3. Create userbot_outreach table
CREATE TABLE IF NOT EXISTS userbot_outreach (
    id BIGSERIAL PRIMARY KEY,
    username TEXT,
    group_name TEXT,
    pitch TEXT,
    sent_at TIMESTAMPTZ DEFAULT now()
);

-- 4. Ensure all applications columns exist
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

-- 5. Ensure leads columns exist
ALTER TABLE leads ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT now();
ALTER TABLE leads ADD COLUMN IF NOT EXISTS priority_score INTEGER DEFAULT 0;
ALTER TABLE leads ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'pending';

-- 6. Ensure nodes table exists
CREATE TABLE IF NOT EXISTS nodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    node_id TEXT UNIQUE,
    node_name TEXT,
    last_active TIMESTAMPTZ DEFAULT now(),
    ip_hint TEXT
);

-- 7. Ensure system_settings exists
CREATE TABLE IF NOT EXISTS system_settings (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- 8. Seed initial system settings
INSERT INTO system_settings (key, value) VALUES ('kill_switch', 'false') ON CONFLICT (key) DO NOTHING;
INSERT INTO system_settings (key, value) VALUES ('kill_switch_active', 'false') ON CONFLICT (key) DO NOTHING;

-- 9. Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_applications_timestamp ON applications(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status);
CREATE INDEX IF NOT EXISTS idx_leads_created_at ON leads(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at DESC);

-- 10. Enable Row Level Security (RLS) - IMPORTANT for Supabase
ALTER TABLE system_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE vip_tracking ENABLE ROW LEVEL SECURITY;
ALTER TABLE userbot_outreach ENABLE ROW LEVEL SECURITY;

-- Create policies to allow service_role full access
CREATE POLICY "Enable all for service_role" ON system_logs FOR ALL USING (true);
CREATE POLICY "Enable all for service_role" ON vip_tracking FOR ALL USING (true);
CREATE POLICY "Enable all for service_role" ON userbot_outreach FOR ALL USING (true);

-- ==========================================
-- VERIFICATION QUERIES
-- ==========================================
-- Run these after executing the above to verify:
-- SELECT COUNT(*) FROM system_logs;
-- SELECT COUNT(*) FROM vip_tracking;
-- SELECT COUNT(*) FROM applications;
-- SELECT COUNT(*) FROM leads;
-- SELECT * FROM system_settings WHERE key LIKE 'kill%';
