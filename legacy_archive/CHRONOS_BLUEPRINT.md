# 🪐 Project Chronos: The Sovereign Blueprint

Welcome to the **Master Architecture** of the Sam Job Automator. This document provides a "boring level of detail" on every gear and piston in your autonomous job-seeking machine.

---

## 🏛️ 1. The Core Infrastructure

The system is a **Hybrid-Cloud Autopilot** designed to run either on GitHub Actions (Cloud) or your local machine (Sovereign).

### ☁️ Cloud Layer (GitHub Actions)
- **Workflow**: `job_bot.yml`
- **Function**: Triggers Every 2 Hours. It fires up a virtual Ubuntu server, installs Python, pulls your latest code, and executes `python main_bot.py`.
- **Secrets**: Securely stores your API keys (Gemini, Supabase, Brevo, Telegram).

### 💾 Persistence Layer (Supabase)
- **Engine**: `database.py`
- **Tables**:
  - `leads`: Stores discovered jobs. Prevents re-scraping the same job.
  - `applications`: The "Black Box." Logs every sent email. **If a company is in this table, the bot will NEVER email them again.**
  - `system_state`: Stores remote settings (like the Kill Switch or API keys).

---

## 🔄 2. The Operational Loop (The Heartbeat)

Every run follows the **"Scout & Strike"** methodology orchestrated by `main_bot.py`:

### Phase A: The Scout (Discovery)
1. **Multi-Source Scraping**: `scraper.py` hits Daleel Madani, HireLebanese, LinkedIn, and Bayt.
2. **Deep Intelligence**: `omni_crawler.py` uses DuckDuckGo to find "Hidden" HR emails on the open web.
3. **Database Check**: Before saving a lead, it queries Supabase. If the job exists, it skips it.

### Phase B: The AI Triage (Thinking)
1. **The Brain**: `ai_agent.py` sends the job description to **Gemini Pro** or **Groq (Llama 3)**.
2. **Analysis**:
   - Is it an HR/Ops/Admin role?
   - Does it match Sam's salary expectations ($500+ / $1500+)?
   - Is it located in a "Prime" city?

### Phase C: The Strike (Delivery)
1. **Document Generation**: `pdf_generator.py` builds a **Dynamic Cover Letter** as a PDF.
2. **The SMTP Cannon**: `main_bot.py` sends the professional HTML email via **Brevo** or **Gmail**.
3. **Sovereign Shield**: The bot checks `database` millisecond before sending. If the company was already contacted, it stops.

---

## 🛰️ 3. Telegram Command Command Center

The bot is a **Remote Command Center** via `main_bot.py`:

- **📊 Live Status**: Reports leads and apps from Supabase to your phone.
- **💓 Pulse**: Confirms the bot is alive.
- **🛑 Emergency Stop**: A remote Kill Switch from your phone.

---

## 🛠️ 4. File Technical Breakdown

| File | Technical Role |
| :--- | :--- |
| `main_bot.py` | **Orchestrator**. Manages loops, Telegram, and error handling. |
| `scraper.py` | **Scout**. Handles Request/BeautifulSoup parsing. |
| `omni_crawler.py` | **Scavenger**. Deep web searching for HR info. |
| `database.py` | **Guardian**. All communication with Supabase. |
| `ai_agent.py` | **Intelligence**. Manages LLM key rotation. |
| `config.py` | **Command&Control**. All thresholds, cities, and filters. |
| `CHRONOS_REPAIR.bat` | **Medic**. Rebuilds the environment and fixes corruption. |

---

## 🛡️ 5. The "Million Percent" Security

1. **Anti-Duplicate**: Verified by `UNIQUE` constraints in Supabase + `Check-Before-Strike` in code.
2. **Rate Limiting**: Waits 3-7 minutes between emails to avoid spam filters.
3. **Ghost Mode**: Uses custom User-Agents to mimic a human.

**End of Blueprint.** 🦾🛡️⚖️🚀
