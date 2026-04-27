# 🔐 DEPLOYMENT SECRETS GUIDE

Complete guide to configure Project Chronos for production deployment.

---

## Table of Contents

1. [Supabase Database](#supabase-database)
2. [Gmail API](#gmail-api)
3. [Brevo SMTP](#brevo-smtp)
4. [Telegram Bot](#telegram-bot)
5. [AI APIs (Gemini / Groq)](#ai-apis)
6. [Render Cloud Deployment](#render-cloud-deployment)
7. [Environment Variables Summary](#environment-variables-summary)

---

## Supabase Database

**Purpose:** Cloud database for leads, applications, and state (optional - SQLite fallback available)

### Setup Steps

1. **Create Supabase Project**
   - Go to [supabase.com](https://supabase.com)
   - Click **New Project**
   - Select Region (closest to your users)
   - Set Database Password (save securely)
   - Wait for project creation (~2 minutes)

2. **Get Credentials**
   - Go to **Settings** → **API**
   - Copy **Project URL** (looks like `https://xxxxx.supabase.co`)
   - Copy **anon public** key (not secret, can be public)

3. **Add to .env**
   ```
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=eyJhbGc...xxxxx
   ```

4. **Test Connection**
   ```bash
   python -c "from core.db_client import RealityShapingDB; db = RealityShapingDB(); print('✅ Connected!' if db.enabled else '⚠️  SQLite fallback')"
   ```

---

## Gmail API

**Purpose:** Email delivery via Gmail (most reliable for testing)

### Setup Steps

1. **Enable Gmail API**
   - Go to [console.cloud.google.com](https://console.cloud.google.com)
   - Create New Project
   - Search for **Gmail API**
   - Click **Enable**

2. **Create Service Account** (Alternative: OAuth credentials)
   - Go to **Credentials** in left sidebar
   - Click **Create Credentials** → **Service Account**
   - Fill in details (any project name OK)
   - Skip optional steps
   - Go to **Keys** tab → **Add Key** → **JSON**
   - Download JSON file

3. **Get Gmail App Password** (Recommended for personal Gmail)
   - Enable 2-Factor Authentication on Gmail account
   - Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   - Select **Mail** and **Windows Computer**
   - Google generates 16-character password
   - **Copy the 16-character password** (no spaces)

4. **Add to .env**
   ```
   GMAIL_SMTP_USER=your-email@gmail.com
   GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
   ```
   ⚠️ **Remove spaces** from app password if present

5. **Test Email Delivery**
   ```bash
   python -c "from core.smtp_engine import send_strike; send_strike('test@example.com', 'Test Subject', 'Test Body')"
   ```

---

## Brevo SMTP

**Purpose:** High-volume email delivery (for production at scale)

### Setup Steps

1. **Create Brevo Account**
   - Go to [brevo.com](https://brevo.com)
   - Sign up (free tier: 300 emails/day)
   - Verify email

2. **Get SMTP Credentials**
   - Go to **SMTP & API**
   - Copy **SMTP Login** (usually your email)
   - Generate **SMTP Password**
   - Note: Host = `smtp-relay.brevo.com`, Port = `587`

3. **Add to .env**
   ```
   BREVO_SMTP_LOGIN=your-email@example.com
   BREVO_SMTP_PASSWORD=your-brevo-password
   ```

4. **Verify Sender Email**
   - Go to **Senders & Emails**
   - Add your sender email
   - Brevo sends verification link
   - Click verification in email

---

## Telegram Bot

**Purpose:** Command & control dashboard for automation

### Setup Steps

1. **Create Bot via BotFather**
   - Open Telegram
   - Search for **@BotFather**
   - Send: `/start`
   - Send: `/newbot`
   - Enter bot name (e.g., "Sam Job Bot")
   - Enter bot username (must be unique, e.g., "sam_job_automator_bot")
   - **Copy the token** (looks like `123456789:ABCDefGhIjKlMnOpQrStUvWxYz`)

2. **Get Chat ID**
   - Open your new bot
   - Send it any message
   - Go to `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find `"chat":{"id":123456789}`
   - **Copy the chat ID**

3. **Get API ID & API Hash** (Optional, for advanced features)
   - Go to [my.telegram.org](https://my.telegram.org)
   - Login with your Telegram account
   - Go to **API Development Tools**
   - Create new application
   - Copy **API ID** and **API Hash**

4. **Add to .env**
   ```
   TELEGRAM_BOT_TOKEN=123456789:ABCDefGhIjKlMnOpQrStUvWxYz
   TELEGRAM_API_ID=123456789
   TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890
   AUTHORIZED_CHATS=123456789
   ```

5. **Test Bot**
   - Start local bot: `python run.py`
   - Send Telegram message: `/status`
   - Bot responds with automation status

---

## AI APIs

### Gemini API (Recommended)

1. **Get Gemini API Key**
   - Go to [ai.google.dev](https://ai.google.dev)
   - Click **Get API key**
   - Create new API key
   - Copy the key

2. **Add to .env**
   ```
   GEMINI_API_KEY=AIzaSy...xxxxx
   ```

3. **Free Quota**
   - ✅ 60 requests/minute
   - ✅ 15 requests/second
   - ✅ No credit card required initially

### Groq API (Fallback)

1. **Get Groq API Key**
   - Go to [console.groq.com](https://console.groq.com)
   - Sign up
   - Go to **API Keys**
   - Create API key
   - Copy the key

2. **Add to .env**
   ```
   GROQ_API_KEY=gsk_...xxxxx
   ```

3. **Free Quota**
   - ✅ 14,400 requests/day
   - ✅ No credit card required

---

## Render Cloud Deployment

**Purpose:** 24/7 execution in the cloud

### Setup Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add environment configuration"
   git push origin main
   ```

2. **Create Render Service**
   - Go to [render.com/dashboard](https://render.com/dashboard)
   - Click **New+** → **Web Service**
   - Select GitHub account and repo
   - Configure:
     - **Name**: `sam-job-automator`
     - **Runtime**: `Python 3.11`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python launch_sam.py`

3. **Add Environment Variables**
   - In Render dashboard, go to **Environment**
   - Click **Add Environment Variable** for each:

   ```
   SUPABASE_URL=...
   SUPABASE_KEY=...
   GEMINI_API_KEY=...
   GROQ_API_KEY=...
   TELEGRAM_BOT_TOKEN=...
   TELEGRAM_API_ID=...
   TELEGRAM_API_HASH=...
   GMAIL_SMTP_USER=...
   GMAIL_APP_PASSWORD=...
   BREVO_SMTP_LOGIN=...
   BREVO_SMTP_PASSWORD=...
   TEST_MODE=false
   TEST_RECEIVER_EMAIL=your-test@example.com
   ```

4. **Deploy**
   - Click **Deploy** button
   - Watch logs (should see "Starting Telegram bot polling...")
   - Takes ~2-3 minutes

5. **Test Cloud Bot**
   - Send Telegram: `/status`
   - If responding: ✅ Cloud deployment successful

---

## Environment Variables Summary

### Required for Operation

```bash
# At least ONE LLM API key (Gemini recommended)
GEMINI_API_KEY=...          # Google Gemini API key
# OR
GROQ_API_KEY=...            # Groq API key (fallback)

# At least ONE email delivery method
# Option 1: Gmail API
GMAIL_SMTP_USER=...         # your-email@gmail.com
GMAIL_APP_PASSWORD=...      # 16-character app password

# Option 2: Brevo SMTP
BREVO_SMTP_LOGIN=...        # your-email@example.com
BREVO_SMTP_PASSWORD=...     # brevo password

# Telegram (for command dashboard)
TELEGRAM_BOT_TOKEN=...      # Bot token from @BotFather
```

### Optional but Recommended

```bash
# Database (optional - SQLite fallback if missing)
SUPABASE_URL=...            # Supabase project URL
SUPABASE_KEY=...            # Supabase anon key

# Telegram advanced features
TELEGRAM_API_ID=...         # From my.telegram.org
TELEGRAM_API_HASH=...       # From my.telegram.org
AUTHORIZED_CHATS=...        # Your chat ID

# Testing & Development
TEST_MODE=true/false        # Route emails to test address
TEST_RECEIVER_EMAIL=...     # Where test emails go
```

### Full .env Template

See `.env.example` in repository root for complete template with defaults.

---

## Verification Checklist

- [ ] Supabase URL and key working
- [ ] Gmail/Brevo email sending verified
- [ ] Telegram bot token valid and responds
- [ ] At least one LLM API key configured
- [ ] Local test: `python run.py` → `/status` works in Telegram
- [ ] Cloud test: Render deployment → `/status` works
- [ ] All email providers tested with `/test_strike` command

---

## Security Best Practices

✅ **Do:**
- Store keys in `.env` (not in git)
- Rotate keys periodically
- Use separate bot tokens for dev/prod
- Enable Telegram 2FA

❌ **Don't:**
- Commit `.env` to git
- Share API keys in issues/PRs
- Use personal Gmail for production
- Hardcode secrets in code

---

## Troubleshooting

**"Failed to connect to Supabase"**
- Database is optional - system uses SQLite fallback
- To debug: Check SUPABASE_URL format and network access

**"Email delivery failed"**
- Verify Gmail app password (16 chars, no spaces)
- Check Brevo SMTP credentials
- Send `/test_strike` in Telegram to test

**"Telegram bot not responding"**
- Verify TELEGRAM_BOT_TOKEN from @BotFather
- Ensure bot is added to your chat
- Check logs: `tail -f logs/orchestrator.log`

**"LLM requests timing out"**
- Check API key validity
- Verify free quota hasn't been exceeded
- Use Gemini as primary, Groq as fallback

---

**Need help?** See [README.md](README.md) or open a GitHub issue.
