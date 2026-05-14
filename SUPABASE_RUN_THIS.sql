-- ═══════════════════════════════════════════════════════════════════════════════
-- PROJECT CHRONOS: COMPLETE DATABASE SETUP
-- 🚀 INSTRUCTIONS:
-- 1. Go to: https://supabase.com/dashboard/project/lckiazbadymeikmxesit/sql/new
-- 2. Copy ALL of this file (Ctrl+A, Ctrl+C)
-- 3. Paste into Supabase SQL Editor
-- 4. Click "Run" button
-- 5. Wait for "Success" message
-- ═══════════════════════════════════════════════════════════════════════════════

-- 1️⃣ Create system_logs table (for dashboard live logs)
CREATE TABLE IF NOT EXISTS system_logs (
    id BIGSERIAL PRIMARY KEY,
    level TEXT NOT NULL,
    message TEXT,
    timestamp TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_system_logs_timestamp ON system_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_system_logs_level ON system_logs(level);

ALTER TABLE system_logs ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Enable all for service_role" ON system_logs;
CREATE POLICY "Enable all for service_role" ON system_logs FOR ALL USING (true);

-- 2️⃣ Create vip_tracking table (for VIP lead tracking)
CREATE TABLE IF NOT EXISTS vip_tracking (
    id BIGSERIAL PRIMARY KEY,
    target_id TEXT UNIQUE,
    company_name TEXT,
    hit_count INTEGER DEFAULT 0,
    last_seen TIMESTAMPTZ DEFAULT now(),
    meta TEXT
);

ALTER TABLE vip_tracking ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Enable all for service_role vip" ON vip_tracking;
CREATE POLICY "Enable all for service_role vip" ON vip_tracking FOR ALL USING (true);

-- 3️⃣ Create userbot_outreach table (for Telegram outreach tracking)
CREATE TABLE IF NOT EXISTS userbot_outreach (
    id BIGSERIAL PRIMARY KEY,
    username TEXT,
    group_name TEXT,
    pitch TEXT,
    sent_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE userbot_outreach ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Enable all for service_role userbot" ON userbot_outreach;
CREATE POLICY "Enable all for service_role userbot" ON userbot_outreach FOR ALL USING (true);

-- 4️⃣ Create applications table
CREATE TABLE IF NOT EXISTS applications (
    id BIGSERIAL PRIMARY KEY,
    company_name TEXT,
    job_title TEXT,
    company_email TEXT,
    job_url TEXT UNIQUE,
    status TEXT DEFAULT 'SENT',
    mission_phase TEXT,
    custom_body_id TEXT,
    psychological_variant TEXT,
    culture_persona TEXT,
    lead_score INTEGER DEFAULT 0,
    cheat_sheet TEXT,
    timestamp TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_applications_timestamp ON applications(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status);
CREATE INDEX IF NOT EXISTS idx_applications_company ON applications(company_name);

ALTER TABLE applications ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Enable all for service_role apps" ON applications;
CREATE POLICY "Enable all for service_role apps" ON applications FOR ALL USING (true);

-- 5️⃣ Create leads table
CREATE TABLE IF NOT EXISTS leads (
    id BIGSERIAL PRIMARY KEY,
    company_name TEXT NOT NULL,
    job_title TEXT,
    email TEXT,
    job_url TEXT UNIQUE,
    description TEXT,
    location TEXT,
    status TEXT DEFAULT 'pending',
    priority_score INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE INDEX IF NOT EXISTS idx_leads_priority ON leads(priority_score DESC);
CREATE INDEX IF NOT EXISTS idx_leads_created ON leads(created_at DESC);

ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Enable all for service_role leads" ON leads;
CREATE POLICY "Enable all for service_role leads" ON leads FOR ALL USING (true);

-- 6️⃣ Create system_settings table
CREATE TABLE IF NOT EXISTS system_settings (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE system_settings ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Enable all for service_role settings" ON system_settings;
CREATE POLICY "Enable all for service_role settings" ON system_settings FOR ALL USING (true);

-- 7️⃣ Create nodes table
CREATE TABLE IF NOT EXISTS nodes (
    node_id TEXT PRIMARY KEY,
    node_name TEXT,
    last_active TIMESTAMPTZ DEFAULT now(),
    ip_hint TEXT
);

ALTER TABLE nodes ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Enable all for service_role nodes" ON nodes;
CREATE POLICY "Enable all for service_role nodes" ON nodes FOR ALL USING (true);

-- 8️⃣ Create system_state table
CREATE TABLE IF NOT EXISTS system_state (
    id BIGSERIAL PRIMARY KEY,
    key TEXT UNIQUE NOT NULL,
    value TEXT,
    updated_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE system_state ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Enable all for service_role state" ON system_state;
CREATE POLICY "Enable all for service_role state" ON system_state FOR ALL USING (true);

-- 9️⃣ Seed initial system_state values
INSERT INTO system_state (key, value) VALUES ('LAST_PULSE', now()::text) ON CONFLICT (key) DO NOTHING;
INSERT INTO system_state (key, value) VALUES ('applications_sent_total', '0') ON CONFLICT (key) DO NOTHING;
INSERT INTO system_state (key, value) VALUES ('scouted_leads_total', '0') ON CONFLICT (key) DO NOTHING;

-- 🔟 Insert default settings
INSERT INTO system_settings (key, value) VALUES ('kill_switch', 'false') ON CONFLICT (key) DO NOTHING;
INSERT INTO system_settings (key, value) VALUES ('active_bot_leader', 'none') ON CONFLICT (key) DO NOTHING;
INSERT INTO system_settings (key, value) VALUES ('active_bot_heartbeat', '2020-01-01T00:00:00') ON CONFLICT (key) DO NOTHING;
INSERT INTO system_settings (key, value) VALUES ('MIN_MATCH_SCORE', '55') ON CONFLICT (key) DO NOTHING;

-- ═══════════════════════════════════════════════════════════════════════════════
-- ✅ VERIFICATION: Run this AFTER the above completes successfully
-- ═══════════════════════════════════════════════════════════════════════════════

SELECT 
    'system_logs' as table_name, COUNT(*) as row_count FROM system_logs
UNION ALL
SELECT 'vip_tracking', COUNT(*) FROM vip_tracking
UNION ALL
SELECT 'userbot_outreach', COUNT(*) FROM userbot_outreach
UNION ALL
SELECT 'applications', COUNT(*) FROM applications
UNION ALL
SELECT 'leads', COUNT(*) FROM leads
UNION ALL
SELECT 'system_settings', COUNT(*) FROM system_settings
UNION ALL
SELECT 'nodes', COUNT(*) FROM nodes
UNION ALL
SELECT 'system_state', COUNT(*) FROM system_state;
