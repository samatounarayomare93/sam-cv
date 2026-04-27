# 🧬 PROJECT CHRONOS: ULTIMATE SYSTEM BLUEPRINT (v2.4)

This document provides a hyper-detailed architectural mapping of the Project Chronos Sovereign Intelligence Swarm.

---

## 1. 📂 Core Architecture Overlay

The system is a distributed, cloud-native automation engine running on **Render Immortal Infrastructure**. It is designed for 24/7 autonomous operation with zero-latency human oversight.

### 📍 [Entry Point] `run.py`
- **Role**: Process Orchestrator.
- **Protocol**: 
    1. Synchronizes the local SQLite database (`sam_ultimate.db`) with the **Supabase Cloud Mirror**.
    2. Initializes the **API Gateway** (`keep_alive.py`) back-end.
    3. Launches the **Sovereign Dashboard** (`telegram_dashboard.py`) in a separate thread.
    4. Launches the **Mission Engine** (`main_bot.py`) with a self-healing watchdog.

### 🧠 [The Brain] `core/telegram_dashboard.py`
- **Role**: Command & Control (C2) Hub.
- **Special Functions**:
    - **Neural Watchdog**: Polls the SQLite `tasks` table every 5s to detect HUD clicks.
    - **Interactive Linking**: Handles `/link_userbot` and `/code` for Phantom Activation.
    - **Telemetry Stream**: Broadcasts system health (CPU, RAM, Uptime) to the HUD.

### 📟 [The Interface] `core/web_app/index.html` (Matrix HUD)
- **Role**: Real-time Tactical Visualization.
- **Tech Stack**: HTML5, Vanilla JS, CSS3 (Glassmorphism + Matrix Scrollers).
- **Tactical Bridge**: 
    - **Primary**: Uses `fetch('/api/action')` to send commands to the backend via POST.
    - **Visual Feedback**: Matrix-style "Toasts" confirm `TRANSMITTING...` and `SUCCESS`.

---

## 2. ⚡ The Dual-Channel C2 Protocol

Project Chronos utilizes a redundant communication bridge to ensure 100% command deliverability.

### A. Web-Push Layer (Browser -> Render)
1. User clicks "Execute Tactical Pulse" on HUD.
2. HUD sends a JSON payload to `https://sam-job-automator.onrender.com/api/action`.
3. `keep_alive.py` intercepts the POST request and inserts a new row into the `tasks` table with `status='pending'`.

### B. Neural Watchdog Layer (Render -> Bot)
1. The **Neural Watchdog** (inside `dashboard.py`) sees the new task.
2. It marks the task as **QUEUED** and notifies the Telegram Master chat.
3. The **Main Bot** picks up the task, executes the mission, and marks it **COMPLETED**.

---

## 3. 🛡️ Persistence & Sovereignty

### 💾 Hybrid Database Tuning
- **SQLite (`sam_ultimate.db`)**: Primary read/write speed for logs and tasks.
- **Supabase Cloud Mirror**: Every 10 minutes, the local SQLite database is mirrored to the cloud.
- **Render Ephemeral Hardening**: On system reboot, the bot automatically downloads the latest DB from Supabase to prevent data loss.

### 👤 The Phantom Layer (UserBot)
- **Engine**: Telethon (Python Telegram API).
- **Credentials**: `TELEGRAM_API_ID` & `TELEGRAM_API_HASH`.
- **Persistence**: Uses "String Sessions" stored as environment variables. This allows the UserBot to stay logged in across cloud redeploys without re-verifying the SMS code.

---

## 4. 🤖 AI Intelligence Core

- **Orchestration**: `core/ai_agent.py`
- **Engines**: Dual-Model Support (Gemini 1.5 Pro + Groq LPU).
- **Tactical NLP**:
    - **CV Tailoring**: Dynamically rewrites resumes based on job descriptions.
    - **Bait & Switch**: Generates psychological interview questions to maintain social dominance.

---

## 5. 🛠️ Critical Dependencies
```
python-telegram-bot>=20.0  # Bot Control
telethon>=1.30.0           # UserBot (Ghost)
google-generativeai        # LLM Support
curl-cffi                  # Stealth Browsing
supabase                   # Persistence
psutil                     # Hardware Telemetry
```

---

**Status: SOVEREIGNTY VERIFIED | ARCHITECTURE STABLE | VERSION 2.4** 🚀⚖️🎯
