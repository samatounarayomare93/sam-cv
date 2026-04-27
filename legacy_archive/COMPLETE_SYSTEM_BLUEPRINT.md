# 👑 PROJECT CHRONOS: ALPHA & OMEGA - MASTER BLUEPRINT
**System Architecture & End-to-End Execution Guide**
*Version: Royal Divine Supremacy (v3.0)*

This document is the absolute authosamtive source (Blueprint) for the entire **Sam Job Automator** ecosystem. It covers every module, script, and component in the system, explaining exactly how it functions, the flow of data, and how all pieces connect together down to the smallest detail ("bi tafasil moumelle").

---

## 🏗️ 1. ARCHITECTURE OVERVIEW

The system has transitioned from a legacy monolithic script into a **Multi-Tier Agentic Entity**. It operates entirely autonomously, acting as a massive net over the internet to capture job openings, process them through Artificial Intelligence, and launch highly personalized applications via email or web platforms, while avoiding anti-bot detection and maintaining its own health.

### 📁 Directory Layout

```text
Sam_Job_Automator_Local/
├── core/                        # 🧠 The Brain & Orchestrator
│   ├── main_bot.py              # The Alpha node. Controls the infinite scrape-and-strike cycle.
│   ├── self_healer.py           # The Immune System. Monitors files and SMTP health.
│   ├── ai_agent.py              # Omni-Intelligence. Uses Gemini/Groq for Resume-Job matching.
│   ├── db_client.py             # Reality-Shaping PostgREST. Global duplicate checker.
│   └── telegram_dashboard.py    # Remote Control. Telegram bot for absolute sovereign override.
├── scripts/                     # 🔧 Utility & Repair
│   └── CHRONOS_REPAIR.bat       # Triggered by self_healer if virtual environment corrupts.
├── ui/                          # 🌐 Glassmorphism Command Center
│   ├── src/app/globals.css      # Styling, Tailwind, Glass UI configuration.
│   └── src/app/page.js          # The multi-lingual (En/Ar) React web dashboard.
├── scraper.py                   # (Legacy/Fallback) Base website parsing logic.
├── omni_crawler.py              # (Legacy/Fallback) Aggressive deep-web crawler.
└── .env                         # Master Vault. Contains API keys, DB urls, and Proxies.
```

---

## ⚙️ 2. CORE MODULES DEEP STEALTH AND EXECUTION

### 🛡️ `core/main_bot.py` (The Alpha Orchestrator)
**Function:** The heart of the system. It runs 24/7 in an infinite loop (`execute_divine_loop`).
- **Proxy & Evasion:** Uses `aiohttp` combined with highly specific rotational User-Agents and HTTP headers (`Sec-Fetch-Site`, `Accept-Language`, `Upgrade-Insecure-Requests`). It mimics genuine human browsers to bypass Cloudflare and conventional anti-bot perimeters.
- **Concurrency:** Operates on an `asyncio.Semaphore(5)` constraint, meaning it runs exactly 5 scraping instances in parallel to maximize throughput while minimizing the footprint.
- **The Loop Flow:** 
  1. Checks the *Kill Switch* via environment variables or DB.
  2. Acquires targets.
  3. Uses stealth networking to extract HTML/JSON payloads.
  4. Feeds clean outputs into the `ai_agent.py`.
  5. Sleeps to mimic human operational fatigue (temporal cooldown).

### 🩹 `core/self_healer.py` (Temporal Self-Healing)
**Function:** Runs silently in the background continuously diagnosing the ecosystem.
- **Integrity Lock:** On boot, it takes a `SHA256` mathematical hash of `main_bot.py`, `ai_agent.py`, and `.env`. If any of these files are accidentally deleted or maliciously altered, the system detects this.
- **SMTP Ping Test:** Every 5 minutes, it connects to the primary **Brevo SMTP** server. If it receives a timeout or rejection, it instantly falls over the internal variables to the **Gmail App Password** pipeline.
- **Nerve Regeneration:** If it detects massive corruption or missing dependencies (e.g., Python updates breaking a package), it natively executes `CHRONOS_REPAIR.bat` directly in Windows Shell to re-build the `venv`.

### 🧠 `core/ai_agent.py` (Omni-Intelligence)
**Function:** Converts raw job listings into lethal, highly-converting PDF/HTML cover letters.
- **Primary Node:** Utilizes Google's **Gemini-2.5-Flash** via standard RAG (Retrieval-Augmented Generation). It maps your HR Operations background directly against the scraped job description's soft/hard skills.
- **The Fallback (Groq):** If Gemini is rate-limited (HTTP 429), the exact same prompt is mathematically shifted via `aiohttp` to **Groq**. Groq executes `llama3-8b` entirely asynchronously to keep the mission pipeline from stalling.
- **Outputs:** Strictly JSON (`is_relevant`, `reason`, `extracted_salary`, `cover_letter_body`).

### 🕋 `core/db_client.py` (Reality-Shaping Database)
**Function:** Supabase PostgreSQL cloud memory.
- **Supabase REST:** Uses raw PostgREST over HTTPS (`aiohttp`). This is lighter and significantly faster than using the heavy python standard library.
- **De-Duplication:** Checks the target URL and company email against thousands of previous records. Prevents the system from embarrassing you by applying to the same job twice in a 30-day window.

---

## 🕹️ 3. COMMAND AND CONTROL SURFACES

### 🌌 Next.js Glassmorphism Dashboard (`ui/`)
**Function:** The modern front-end for visual telemetry and metrics tracking.
- **Tech Stack:** React, Next.js, TailwindCSS 4.0.
- **Aesthetics:** Uses extreme dark-mode, Slate/Sky/Purple color gradients, glowing particle backgrounds (`rgba` gradients), and dynamic pulse animations to provide a "Cyberpunk Command" feel.
- **Bilingual Core:** The `page.js` utilizes standard React state hooks to completely flip the UI between English (`ltr`) and Arabic (`rtl`). The translations swap the entire page instantly.
- **Commands:** Contains the visual equivalent to the Emergency Kill switch and live metrics visualization (success rates vs deployed applications).

### 📱 Sovereign Telegram Override (`core/telegram_dashboard.py`)
**Function:** 100% remote control capability when away from the computer.
- Uses `python-telegram-bot` to establish a direct socket via the Telegram API.
- Upon hitting `/start`, gives you inline keyboard buttons.
- Features physical DB connection toggling: Pressing "Kill Switch" engages `db.activate_kill_switch(True)`, cascading a complete worldwide halt to the Orchestrator loop within milliseconds.

---

## ⚡ 4. THE 24/7 MISSION LOOP (STEP-BY-STEP CYCLE)

Here is exactly how a single iteration (cycle) of Project Chronos executes:

1. **Vigilance Check:** `self_healer.py` verifies the network and SMTP are stable.
2. **Launch:** `core/main_bot.py` awakes.
3. **Scouting:** Scrapers (`scraper.py` / `omni_crawler.py` / Stealth routing) gather raw links from LinkedIn, Indeed, and direct enterprise ATS panels.
4. **Filtration:** The Orchestrator forwards links to `core/db_client.py`. If `is_duplicate()` returns True, the lead is incinerated.
5. **AI Synthesis:** The raw, unformatted job text is beamed to `ai_agent.py`. The Gemini/Groq LLM reads the description and scores it against your CV.
6. **Execution (Strike):** If `is_relevant == True`, the system renders the personalized JSON cover letter body into a PDF (utilizing the internal configuration).
7. **Delivery:** The `smtp_engine` authenticates with Brevo. The email is assembled strictly conforming to MIME standards, bypassing spam filters, and dispatched directly to the hiring manager.
8. **Logging:** `db_client.py` updates the Supabase tracking database to `SENT`.
9. **Cooldown:** The system enters a brief sleep state to preserve stealth footprint.

---

## 🔑 5. THE MASTER VAULT (`.env` Configuration)
The `.env` file is your control panel. 
* Never expose your `TELEGRAM_BOT_TOKEN_`.
* The `SUPABASE_KEY` must always be the `service_role` key (to bypass RLS limits).
* Ensure `ROTATING_USER_AGENT_SEED` is updated every few months to generate fresh hardware fingerprints for the scrape engine evasion.

## ✅ FINAL NOTES ON MAINTENANCE
If you ever encounter package conflicts (`import` errors, `ModuleNotFoundError`), simply execute the `CHRONOS_REPAIR.bat` located in the `scripts/` folder. It will forcefully purge all discrepancies and reinstall the exact dependencies needed. 

**Welcome to Absolute Automaton Supremacy.**
