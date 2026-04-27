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

CREATE TABLE IF NOT EXISTS applications (
    id BIGSERIAL PRIMARY KEY,
    company_name TEXT NOT NULL,
    job_title TEXT NOT NULL,
    platform TEXT,
    job_url TEXT,
    company_email TEXT,
    status TEXT DEFAULT 'SENT',
    mission_phase TEXT,
    custom_body_id TEXT,
    psychological_variant TEXT,
    culture_persona TEXT,
    lead_score INTEGER DEFAULT 0,
    cheat_sheet TEXT,
    timestamp TIMESTAMPTZ DEFAULT now(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS system_state (
    id BIGSERIAL PRIMARY KEY,
    key TEXT UNIQUE NOT NULL,
    value TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS system_secrets (
    id BIGSERIAL PRIMARY KEY,
    key TEXT UNIQUE NOT NULL,
    value TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

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

CREATE TABLE IF NOT EXISTS global_recon (
    company_name TEXT PRIMARY KEY,
    manager_name TEXT,
    manager_url TEXT,
    domain TEXT,
    status TEXT,
    last_updated TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS adversarial_blacklist (
    domain TEXT PRIMARY KEY,
    reason TEXT,
    expiry TIMESTAMPTZ,
    last_updated TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS tasks (
    id BIGSERIAL PRIMARY KEY,
    type TEXT,
    target TEXT,
    meta TEXT,
    status TEXT DEFAULT 'PENDING',
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS site_patches (
    domain TEXT PRIMARY KEY,
    patch TEXT,
    repaired_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS platform_registry (
    id BIGSERIAL PRIMARY KEY,
    name TEXT,
    url TEXT UNIQUE,
    type TEXT,
    status TEXT DEFAULT 'ACTIVE',
    last_checked TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS discovered_links (
    url TEXT PRIMARY KEY,
    source TEXT,
    is_platform BOOLEAN DEFAULT FALSE,
    status TEXT DEFAULT 'PENDING',
    created_at TIMESTAMPTZ DEFAULT now()
);
