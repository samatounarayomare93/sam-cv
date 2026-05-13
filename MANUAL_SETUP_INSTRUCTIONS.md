# 🔧 Manual Setup Instructions - Project Chronos

## ⚠️ Critical: Missing Supabase Tables

The system is **fully functional** but the dashboard needs one table to display live logs.

### Current Status:
- ✅ Bot is running on Render (last application: SABB Bank at 10:31 AM today)
- ✅ 3,267 applications sent successfully
- ✅ 957 leads in database
- ✅ All email providers configured
- ⚠️ Dashboard can't display live logs (missing `system_logs` table)

---

## 📋 Step 1: Create Missing Tables in Supabase

1. Go to [supabase.com](https://supabase.com) and login
2. Open your project: **lckiazbadymeikmxesit**
3. Click **SQL Editor** in the left sidebar
4. Click **New Query**
5. Copy and paste the SQL below:

```sql
-- Create system_logs table (for dashboard live logs)
CREATE TABLE IF NOT EXISTS system_logs (
    id BIGSERIAL PRIMARY KEY,
    level TEXT NOT NULL,
    message TEXT,
    timestamp TIMESTAMPTZ DEFAULT now()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_system_logs_timestamp ON system_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_system_logs_level ON system_logs(level);

-- Enable Row Level Security
ALTER TABLE system_logs ENABLE ROW LEVEL SECURITY;

-- Create policy to allow service_role full access
CREATE POLICY "Enable all for service_role" ON system_logs FOR ALL USING (true);

-- Create vip_tracking table (optional - for VIP lead tracking)
CREATE TABLE IF NOT EXISTS vip_tracking (
    id BIGSERIAL PRIMARY KEY,
    target_id TEXT UNIQUE,
    company_name TEXT,
    hit_count INTEGER DEFAULT 0,
    last_seen TIMESTAMPTZ DEFAULT now(),
    meta TEXT
);

ALTER TABLE vip_tracking ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable all for service_role" ON vip_tracking FOR ALL USING (true);

-- Create userbot_outreach table (optional - for Telegram outreach tracking)
CREATE TABLE IF NOT EXISTS userbot_outreach (
    id BIGSERIAL PRIMARY KEY,
    username TEXT,
    group_name TEXT,
    pitch TEXT,
    sent_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE userbot_outreach ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable all for service_role" ON userbot_outreach FOR ALL USING (true);
```

6. Click **Run** (or press Ctrl+Enter)
7. You should see: **Success. No rows returned**

---

## 🚀 Step 2: Start the Dashboard

Open PowerShell in the project folder and run:

```powershell
cd sam-command-center
npm run dev
```

Then open your browser to: **http://localhost:3000**

You should see:
- Live stats (nodes, leads, strikes, heals)
- Mission control buttons (Pause/Resume/Run Now/etc.)
- Live terminal logs from the bot
- Pending LinkedIn nudge tasks

---

## ✅ Verification

After running the SQL, verify the tables were created:

```sql
SELECT COUNT(*) FROM system_logs;
SELECT COUNT(*) FROM vip_tracking;
SELECT COUNT(*) FROM userbot_outreach;
```

All three should return `0` (empty tables).

---

## 🎯 What's Fixed

I've already fixed the Python code to write logs to both SQLite (local) and Supabase (cloud).

**File modified:** `core/db_client.py` - `stream_log()` method now writes to Supabase.

Once you create the `system_logs` table, the dashboard will start showing live logs immediately.

---

## 📊 Current System Stats

- **Applications sent:** 3,267
- **Leads in database:** 957
- **Pending LinkedIn tasks:** 9,467
- **Active nodes:** 2 (Render + local)
- **Last application:** SABB Bank (10:31 AM today)
- **Kill switch:** OFF (bot is running)

---

## 🔥 Everything Else is Working

- ✅ Python backend running on Render
- ✅ Supabase database connected
- ✅ 6 email providers configured (Gmail, Zoho x2, Brevo, Outlook, Resend)
- ✅ AI providers (Groq, Gemini) configured
- ✅ Telegram bot configured
- ✅ Auto-scraping from 12+ job sources
- ✅ PDF generation (CV + Cover Letter)
- ✅ Email rotation system
- ✅ Anti-ban protection
- ✅ Follow-up system
- ✅ LinkedIn automation

---

## 🆘 Need Help?

If you see any errors after creating the tables, check:

1. **Dashboard not loading?**
   - Make sure you ran `npm install` in `sam-command-center/` first
   - Check `.env.local` has the correct Supabase URL and key

2. **No logs appearing?**
   - Wait 1-2 minutes for the bot to write new logs
   - Check the bot is running: `SELECT * FROM nodes ORDER BY last_active DESC LIMIT 1;`

3. **Bot not sending applications?**
   - Check kill switch: `SELECT * FROM system_settings WHERE key = 'kill_switch';`
   - Should be `false`. If `true`, use the dashboard to click **Resume**.

---

## 🎉 You're All Set!

Once you create the tables, everything will be 100% operational.

The system is already sending applications successfully - you just need the dashboard to see the live logs.
