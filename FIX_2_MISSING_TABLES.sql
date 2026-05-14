-- ============================================================
-- FIX: Create 2 missing tables in Supabase
-- Run this in: https://app.supabase.com/project/lckiazbadymeikmxesit/sql/new
-- ============================================================

CREATE TABLE IF NOT EXISTS vip_tracking (
    id BIGSERIAL PRIMARY KEY,
    target_id TEXT UNIQUE,
    company_name TEXT,
    hit_count INTEGER DEFAULT 0,
    last_seen TIMESTAMPTZ DEFAULT now(),
    meta TEXT
);
ALTER TABLE vip_tracking ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "all_vip" ON vip_tracking;
CREATE POLICY "all_vip" ON vip_tracking FOR ALL USING (true);

CREATE TABLE IF NOT EXISTS userbot_outreach (
    id BIGSERIAL PRIMARY KEY,
    username TEXT,
    group_name TEXT,
    pitch TEXT,
    sent_at TIMESTAMPTZ DEFAULT now()
);
ALTER TABLE userbot_outreach ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "all_userbot" ON userbot_outreach;
CREATE POLICY "all_userbot" ON userbot_outreach FOR ALL USING (true);

-- Verify
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
