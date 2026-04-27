# SAM JOB AUTOMATOR - COMPLETE SYSTEM BLUEPRINT

**Version:** 99.0 - MAXIMUM POWER EDITION  
**Owner:** Sam Salameh - HR & Operations Professional  
**Last Updated:** April 2026

---

## TABLE OF CONTENTS

1. [System Overview](#1-system-overview)
2. [Architecture](#2-architecture)
3. [Core Modules](#3-core-modules)
4. [Features](#4-features)
5. [Configuration](#5-configuration)
6. [Telegram Commands](#6-telegram-commands)
7. [API Integrations](#7-api-integrations)
8. [Safety Features](#8-safety-features)
9. [Performance Metrics](#9-performance-metrics)
10. [Setup Guide](#10-setup-guide)

---

## 1. SYSTEM OVERVIEW

SAM Job Automator is a **fully autonomous job application system** that:
- Scrapes 50+ job platforms worldwide
- Sends personalized applications via multiple email providers
- Uses AI for intelligent job matching
- Operates 24/7 via Telegram control
- Self-heals and self-repairs automatically

### Key Capabilities
| Feature | Capability |
|---------|-----------|
| Job Sources | 50+ platforms, 195 countries |
| Email Providers | Brevo, Gmail, Outlook, 15+ SMTP |
| Email Patterns | 100+ patterns per company |
| AI Matching | Gemini + Groq powered |
| Control | Telegram Dashboard |
| Uptime | 24/7 autonomous |

---

## 2. ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                    SAM JOB AUTOMATOR                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌────────────┐ │
│  │   SCRAPER     │───▶│  AI FILTER   │───▶│  EMAIL     │ │
│  │   ENGINE      │    │  & MATCHER   │    │  ENGINE    │ │
│  └──────────────┘    └──────────────┘    └────────────┘ │
│         │                   │                   │          │
│         ▼                   ▼                   ▼          │
│  ┌──────────────────────────────────────────────────────┐ │
│  │              TELEGRAM DASHBOARD                        │ │
│  │  Status | Run | Stop | Health | Stats | Companies   │ │
│  └──────────────────────────────────────────────────────┘ │
│                            │                              │
│                            ▼                              │
│  ┌──────────────────────────────────────────────────────┐ │
│  │              SELF-HEALING ENGINE                      │ │
│  │  Auto-repair | Backup | Recovery | Monitoring        │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. CORE MODULES

### 3.1 main_bot.py
**Purpose:** Main orchestration engine

**Features:**
- Mission loop (auto-scout every 5 minutes)
- Parallel scraping with semaphore control
- Rate limiting (max 10 emails/minute)
- Company duplicate prevention
- Health monitoring
- Telegram command handlers

**Key Functions:**
| Function | Purpose |
|----------|---------|
| `auto_strike_mission()` | Main mission loop |
| `parallel_scrape_jobs()` | Multi-source scraping |
| `process_strike_candidate()` | Email delivery |
| `send_strike_with_fallover()` | Multi-provider SMTP |
| `health_check()` | System diagnostics |

### 3.2 config.py
**Purpose:** Central configuration

**Settings:**
```python
# Email Limits
MAX_EMAILS_PER_RUN = 50
MAX_EMAILS_PER_MINUTE = 20

# Scraper Settings
SCRAPER_MAX_PAGES = 50
MAX_DEEP_SCRAPES_PER_RUN = 500

# Salary Requirements
MIN_SALARY_LEBANON_PRIME = 1500
MIN_SALARY_LEBANON_OTHER = 1000
MIN_SALARY_GLOBAL = 6000
```

### 3.3 scraper.py
**Purpose:** Job discovery from multiple sources

**Sources:**
| Source | Type | Priority |
|--------|------|----------|
| Daleel Madani | Lebanon | Primary |
| HireLebanese | Lebanon | Primary |
| LinkedIn | Global | Primary |
| Bayt | Gulf | Primary |
| Monster | Global | Secondary |
| Indeed | Global | Secondary |
| Glassdoor | Global | Secondary |
| GulfTalent | Gulf | Secondary |
| Dubizzle | UAE | Secondary |

### 3.4 smtp_engine.py
**Purpose:** Multi-provider email delivery

**Providers:**
1. **Brevo** (Primary - Free 300/day)
2. **Gmail** (Alternative)
3. **Outlook** (Tertiary)

**Features:**
- Auto-fallback on failure
- Rate limiting
- PDF attachment
- HTML + Plain text
- Exponential retry

### 3.5 ai_agent.py
**Purpose:** Intelligent job analysis

**AI Models:**
- **Gemini** (Primary)
- **Groq** (Fallback)

**Capabilities:**
- Job relevance scoring
- Salary estimation
- Cover letter generation
- Interview prep
- Key pool rotation

### 3.6 database.py
**Purpose:** Data persistence

**Storage:**
- Supabase PostgreSQL (Primary)
- Local JSON files (Fallback)

**Tables:**
- `applications` - Sent applications
- `leads` - Job opportunities
- `system_state` - Config & flags
- `system_secrets` - API keys

### 3.7 telegram_dashboard.py
**Purpose:** User interface

**Commands:**
| Command | Action |
|---------|--------|
| `/start` | Welcome message |
| `/status` | Live metrics |
| `/runnow` | Start mission |
| `/stop` | Emergency stop |
| `/resume` | Resume operations |
| `/health` | System health |
| `/stats` | Statistics |
| `/companies` | Company database |

### 3.8 self_healer.py
**Purpose:** Auto-repair and recovery

**Features:**
- File system check
- Network diagnostics
- SMTP testing
- Backup/restore
- Auto-restart on failure

---

## 4. FEATURES

### 4.1 Job Discovery
- **50+ job platforms** scraped
- **195 countries** covered
- **Multi-language** support (AR/FR/EN)
- **Parallel scraping** for speed
- **Duplicate prevention**

### 4.2 Email System
- **100+ email patterns** per company
- **Professional HTML templates**
- **Personalized PDFs**
- **Rate limiting** protection
- **Multi-provider fallback**

### 4.3 AI Matching
- **Keyword filtering**
- **Salary validation**
- **Location filtering**
- **Title relevance**
- **Cover letter generation**

### 4.4 Control Interface
- **Telegram Dashboard**
- **Real-time status**
- **Emergency stop**
- **Manual override**
- **Statistics view**

### 4.5 Safety Features
- **Kill Switch** - Instant stop
- **Rate Limiting** - Prevent bans
- **Duplicate Check** - No double-apply
- **Auto-Retry** - Self-healing
- **Backup System** - Data protection

---

## 5. CONFIGURATION

### 5.1 Environment Variables

Create `.env` file:

```env
# Email - Brevo (Primary - Free)
BREVO_API_KEY=your_brevo_api_key
BREVO_SMTP_PASSWORD=your_smtp_password
BREVO_SMTP_LOGIN=your_email@smtp-brevo.com

# Email - Gmail (Alternative)
GMAIL_APP_PASSWORD=your_gmail_app_password
GMAIL_SMTP_USER=your_email@gmail.com

# Email - Outlook (Tertiary)
OUTLOOK_USER=your_email@outlook.com
OUTLOOK_PASSWORD=your_password

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# AI (Optional but recommended)
GEMINI_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key

# Database (Optional)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Performance
MAX_EMAILS_PER_RUN=50
MISSION_INTERVAL_SECONDS=300
```

### 5.2 Target Rules

**Valid Job Titles:**
```python
SAM_JOB_TITLES = [
    "hr manager", "human resources manager", "hr director",
    "hr business partner", "hrbp", "hr specialist",
    "recruitment manager", "talent acquisition",
    "operations manager", "chief of staff",
    "office manager", "executive assistant",
    "customer service manager", "admin manager"
]
```

**Banned Titles:**
```python
BANNED_TITLES = [
    "software", "developer", "engineer",  # Tech
    "nurse", "doctor", "medical",        # Medical
    "driver", "delivery", "warehouse",   # Labor
    "chef", "cook", "waiter"             # Food
]
```

**Target Locations:**
```python
GOD_MODE_LOCATIONS = [
    "uae", "dubai", "abu dhabi",
    "qatar", "doha",
    "saudi arabia", "riyadh", "jeddah",
    "kuwait", "oman", "bahrain",
    "gcc", "gulf", "middle east",
    "remote", "worldwide", "relocation"
]
```

---

## 6. TELEGRAM COMMANDS

### 6.1 Basic Commands

| Command | Description |
|---------|-------------|
| `/start` | Open control center |
| `/help` | Show all commands |
| `/status` | View current status |
| `/health` | System diagnostics |

### 6.2 Control Commands

| Command | Description |
|---------|-------------|
| `/runnow` | Start mission immediately |
| `/stop` | Emergency stop |
| `/resume` | Resume operations |
| `/scout` | Scout for jobs |

### 6.3 Information Commands

| Command | Description |
|---------|-------------|
| `/stats` | Detailed statistics |
| `/companies` | View company database |
| `/report` | Daily health report |
| `/backup` | Create backup |
| `/restore` | Restore from backup |

### 6.4 Dashboard Buttons

**Reply Keyboard:**
```
📊 Status    🏥 Health
📈 Stats     🏢 Companies
⏰ Next Run  🎯 Targets
⚡ Run Now   ✅ Resume
🧠 Interview Prep   🚨 Emergency Stop
```

---

## 7. API INTEGRATIONS

### 7.1 Email Providers

**Brevo (Sendinblue)**
- Free 300 emails/day
- SMTP: smtp-relay.brevo.com:587
- HTTP API available

**Gmail**
- 500 emails/day limit
- SMTP: smtp.gmail.com:587
- Requires App Password

**Outlook**
- 300 emails/day limit
- SMTP: smtp-mail.outlook.com:587

### 7.2 AI Services

**Gemini (Google)**
- Primary AI processor
- 60 requests/minute
- Fallback pool support

**Groq**
- Secondary AI processor
- Fast inference
- Free tier available

### 7.3 Database

**Supabase (PostgreSQL)**
- Cloud database
- Real-time sync
- Row-level security

---

## 8. SAFETY FEATURES

### 8.1 Kill Switch
- Instant stop of all operations
- Remote control via Telegram
- One-command activation

### 8.2 Rate Limiting
```python
MAX_EMAILS_PER_MINUTE = 10
DELAY_BETWEEN_EMAILS_MIN = 1
DELAY_BETWEEN_EMAILS_MAX = 3
```

### 8.3 Duplicate Prevention
- URL-based deduplication
- Company email tracking
- 30-day reapply window

### 8.4 Auto-Healing
- File system repair
- Network diagnostics
- SMTP testing
- Auto-restart

### 8.5 Backup System
- Automatic backups
- Local + cloud storage
- One-click restore

---

## 9. PERFORMANCE METRICS

### 9.1 Expected Output

| Metric | Daily | Weekly | Monthly |
|--------|-------|--------|---------|
| Applications | 25-50 | 175-350 | 750-1500 |
| Companies Reached | 50-100 | 350-700 | 1500-3000 |
| Interviews | 2-5 | 14-35 | 60-150 |

### 9.2 Success Factors
- Quality job matching
- Personalized emails
- Professional PDFs
- Multi-provider delivery
- Follow-up sequences

---

## 10. SETUP GUIDE

### 10.1 Prerequisites
- Python 3.11+
- Telegram Bot Token
- Email Provider Account

### 10.2 Installation

```bash
# 1. Clone repository
git clone <repo_url>
cd Sam_Job_Automator

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 4. Run the bot
START_MAX_POWER.bat
```

### 10.3 Quick Start
1. Create Telegram bot via @BotFather
2. Get your Chat ID via @userinfobot
3. Set up Brevo account (free)
4. Configure .env file
5. Run START_MAX_POWER.bat

---

## FILE STRUCTURE

```
Sam_Job_Automator/
├── main_bot.py              # Main orchestration
├── config.py                # Central configuration
├── scraper.py               # Job scraping
├── smtp_engine.py           # Email delivery
├── ai_agent.py              # AI analysis
├── database.py               # Data persistence
├── telegram_dashboard.py     # UI interface
├── self_healer.py           # Auto-repair
├── uplink.py                # Telegram bridge
├── pdf_generator.py         # PDF creation
├── omni_crawler.py          # Web search
├── global_company_scraper.py # Company discovery
├── system_health.py         # Health monitoring
├── .env                     # Environment variables
├── START_MAX_POWER.bat      # Launch script
└── README.md                # This documentation
```

---

## SUPPORT

For questions or issues:
1. Check `/health` command
2. Review logs in `bot.log`
3. Verify credentials in `.env`
4. Check Telegram bot setup

---

**Built for Sam Salameh - HR & Operations Professional**  
**Powered by Autonomous AI**  
**Version 99.0 - MAXIMUM POWER EDITION**
