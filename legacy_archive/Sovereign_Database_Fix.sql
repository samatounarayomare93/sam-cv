-- 🛡️ PROJECT CHRONOS: SOVEREIGN DATABASE RESTORATION SCRIPT
-- RUN THIS IN YOUR SUPABASE SQL EDITOR TO ACHIEVE 100% MISSION INTEGRITY.

-- 1. Ensure 'leads' table is fully hardened with all expert columns
CREATE TABLE IF NOT EXISTS leads (
    id BIGSERIAL PRIMARY KEY,
    company_name TEXT NOT NULL,
    job_title TEXT NOT NULL,
    email TEXT,
    location TEXT,
    salary TEXT,
    description TEXT,
    status TEXT DEFAULT 'pending',
    mission_type TEXT DEFAULT 'global',
    priority_score INTEGER DEFAULT 0,
    follow_up_sent BOOLEAN DEFAULT FALSE,
    platform TEXT,
    job_url TEXT UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(company_name, job_title)
);

-- 2. Add missing columns to 'leads' if they were created by older scripts
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='leads' AND column_name='priority_score') THEN
        ALTER TABLE leads ADD COLUMN priority_score INTEGER DEFAULT 0;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='leads' AND column_name='follow_up_sent') THEN
        ALTER TABLE leads ADD COLUMN follow_up_sent BOOLEAN DEFAULT FALSE;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='leads' AND column_name='platform') THEN
        ALTER TABLE leads ADD COLUMN platform TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='leads' AND column_name='job_url') THEN
        ALTER TABLE leads ADD COLUMN job_url TEXT;
        ALTER TABLE leads ADD CONSTRAINT leads_job_url_key UNIQUE (job_url);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='leads' AND column_name='mission_type') THEN
        ALTER TABLE leads ADD COLUMN mission_type TEXT DEFAULT 'global';
    END IF;
END $$;

-- 3. Ensure 'applications' table tracks every elite strike
CREATE TABLE IF NOT EXISTS applications (
    id BIGSERIAL PRIMARY KEY,
    company_name TEXT NOT NULL,
    job_title TEXT NOT NULL,
    platform TEXT,
    job_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Ensure 'system_state' vault is indestructible
CREATE TABLE IF NOT EXISTS system_state (
    id BIGSERIAL PRIMARY KEY,
    key TEXT UNIQUE NOT NULL,
    value TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Legacy Bridge: system_secrets
CREATE TABLE IF NOT EXISTS system_secrets (
    id BIGSERIAL PRIMARY KEY,
    key TEXT UNIQUE NOT NULL,
    value TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ✅ SCHEMA HANDSHAKE COMPLETE. PROJECT CHRONOS IS NOW FULLY SOVEREIGN.
