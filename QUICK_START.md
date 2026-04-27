# 🚀 QUICK START GUIDE

Get Project Chronos running in 5 minutes.

## Prerequisites

- **Python 3.11+** installed
- **Git** for cloning
- **API Keys** (Gemini, Telegram token) - see [Deployment Secrets Guide](DEPLOYMENT_SECRETS_GUIDE.md)

---

## Option 1: Local Development (5 minutes)

### Step 1: Clone & Enter Directory
```bash
git clone https://github.com/Sam-Cordahi/Sam_Job_Automator.git
cd Sam_Job_Automator
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
# Copy template
cp .env.example .env

# Edit .env with your credentials
# Required:
# - SUPABASE_URL and SUPABASE_KEY (or leave blank for SQLite-only mode)
# - GEMINI_API_KEY or GROQ_API_KEY (at least one LLM)
# - TELEGRAM_BOT_TOKEN (for Telegram dashboard)
# - GMAIL_SMTP_USER + GMAIL_APP_PASSWORD OR BREVO_SMTP_LOGIN + BREVO_SMTP_PASSWORD
```

### Step 5: Run Locally
```bash
python run.py
```

**Expected Output:**
```
================================================================================
PROJECT CHRONOS: OMEGA-SOVEREIGNTY UNIFIED SWARM
------------------------------------------------------------------------
Status: CONSOLIDATING INTELLIGENCE...
Memory Mode: SLIM-PROCESS (OOM Protection Active)
================================================================================
[SYSTEM] Activating Cloud Heartbeat (Port Binding)...
[SYSTEM] Initializing Shared Swarm Intelligence...
[SYSTEM] Launching Unified Swarm Tasks...
```

### Step 6: Test Telegram Dashboard
1. Open your Telegram bot (configured in `.env` with `TELEGRAM_BOT_TOKEN`)
2. Send: `/status`
3. Bot responds with current automation status

---

## Option 2: Cloud Deployment (Render.com - 10 minutes)

### Prerequisites
- GitHub account with this repo forked
- Render.com account (free tier OK)
- All environment variables configured

### Step 1: Create Render Service

1. Go to [render.com/dashboard](https://render.com/dashboard)
2. Click **New+** → **Web Service**
3. Select **GitHub** and connect this repository
4. Configure:
   - **Name**: `sam-job-automator`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python launch_sam.py`
   - **Python Version**: `3.11` (set in `render.yaml`)

### Step 2: Add Environment Variables

In Render dashboard → **Environment**:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-public-key
GEMINI_API_KEY=your-gemini-key
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_API_ID=your-api-id
TELEGRAM_API_HASH=your-api-hash
GMAIL_SMTP_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-char-password
TEST_MODE=false
```

See [Deployment Secrets Guide](DEPLOYMENT_SECRETS_GUIDE.md) for detailed instructions.

### Step 3: Deploy

1. Click **Deploy**
2. Watch logs in Render dashboard
3. Service starts in ~2-3 minutes
4. Test with Telegram: `/status`

---

## Common Issues

### "ModuleNotFoundError: No module named 'core'"

**Solution:**
```bash
# Ensure you're in the correct directory
cd Sam_Job_Automator

# Ensure venv is activated
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate  # Windows
```

### "SUPABASE connection failed"

**Solution:** 
- Database is **optional** - system falls back to SQLite
- To enable Supabase:
  1. Create [Supabase project](https://supabase.com)
  2. Copy URL and anon key to `.env`
  3. Restart bot

### "Telegram bot not responding"

**Solution:**
1. Verify `TELEGRAM_BOT_TOKEN` in `.env`
2. Telegram bot must be created via [@BotFather](https://t.me/BotFather)
3. Ensure `AUTHORIZED_CHATS` includes your chat ID
4. Check Render logs: `tail -f logs/orchestrator.log`

### Email delivery fails

**Solution:** Use at least ONE of:
- Gmail API: `GMAIL_SMTP_USER` + `GMAIL_APP_PASSWORD` (16 chars from Gmail app passwords)
- Brevo SMTP: `BREVO_SMTP_LOGIN` + `BREVO_SMTP_PASSWORD`

---

## Next Steps

- 📖 **Full Documentation**: See [COMPREHENSIVE_A_TO_Z_TECHNICAL_DOCUMENTATION.md](docs/COMPREHENSIVE_A_TO_Z_TECHNICAL_DOCUMENTATION.md)
- 🔧 **Configuration**: See [Deployment Secrets Guide](DEPLOYMENT_SECRETS_GUIDE.md)
- 🧪 **Testing**: Run `python -m coverage run --source=core -m unittest discover`
- 🐛 **Issues**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- 💬 **Questions**: Open a GitHub Issue

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                  PROJECT CHRONOS                        │
├─────────────────────────────────────────────────────────┤
│ Intelligence Engine (core/main_bot.py)                  │
│  ├─ Lead Discovery (DuckDuckGo, LinkedIn, Web)         │
│  ├─ AI Filtering (Gemini / Groq LLMs)                  │
│  ├─ CV Generation (FPDF2 + Tailoring)                  │
│  └─ Email Dispatch (Gmail API / Brevo)                 │
├─────────────────────────────────────────────────────────┤
│ Telegram Dashboard (core/telegram_dashboard.py)         │
│  ├─ 50+ Tactical Commands                              │
│  ├─ Real-time Status Updates                           │
│  └─ Leadership Election (Multi-instance)               │
├─────────────────────────────────────────────────────────┤
│ Backend Storage (Supabase / SQLite)                     │
│  ├─ Lead Database                                       │
│  ├─ Application Tracking                               │
│  └─ Performance Telemetry                              │
└─────────────────────────────────────────────────────────┘
```

---

## File Structure

```
Sam_Job_Automator/
├── run.py                     ← Start here (local dev)
├── launch_sam.py            ← Cloud launcher
├── requirements.txt          ← Dependencies
├── .env.example              ← Config template
├── render.yaml               ← Cloud config
├── README.md                 ← Full documentation
├── core/
│   ├── main_bot.py          ← Automation engine
│   ├── telegram_dashboard.py ← Command & control
│   ├── ai_agent.py          ← LLM integration
│   ├── db_client.py         ← Database layer
│   └── [18+ more modules]
└── tests/
    └── [Unit tests]
```

---

**Ready to automate? Get started now!** 🚀
