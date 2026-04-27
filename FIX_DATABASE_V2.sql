ALTER TABLE "applications" ADD COLUMN IF NOT EXISTS "company_email" TEXT;
ALTER TABLE "applications" ADD COLUMN IF NOT EXISTS "job_url" TEXT;
ALTER TABLE "applications" ADD COLUMN IF NOT EXISTS "status" TEXT DEFAULT 'SENT';
ALTER TABLE "applications" ADD COLUMN IF NOT EXISTS "mission_phase" TEXT;
ALTER TABLE "applications" ADD COLUMN IF NOT EXISTS "custom_body_id" TEXT;
ALTER TABLE "applications" ADD COLUMN IF NOT EXISTS "psychological_variant" TEXT;
ALTER TABLE "applications" ADD COLUMN IF NOT EXISTS "culture_persona" TEXT;
ALTER TABLE "applications" ADD COLUMN IF NOT EXISTS "lead_score" INTEGER DEFAULT 0;
ALTER TABLE "applications" ADD COLUMN IF NOT EXISTS "cheat_sheet" TEXT;
ALTER TABLE "applications" ADD COLUMN IF NOT EXISTS "timestamp" TIMESTAMPTZ DEFAULT now();

CREATE TABLE IF NOT EXISTS "nodes" (
    "id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "node_id" TEXT UNIQUE,
    "node_name" TEXT,
    "last_active" TIMESTAMPTZ DEFAULT now(),
    "ip_hint" TEXT
);

CREATE TABLE IF NOT EXISTS "system_settings" (
    "key" TEXT PRIMARY KEY,
    "value" TEXT,
    "updated_at" TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE "leads" ADD COLUMN IF NOT EXISTS "created_at" TIMESTAMPTZ DEFAULT now();
ALTER TABLE "leads" ADD COLUMN IF NOT EXISTS "priority_score" INTEGER DEFAULT 0;

INSERT INTO "system_state" ("key", "value") VALUES ('LAST_PULSE', now()::text) ON CONFLICT ("key") DO NOTHING;
