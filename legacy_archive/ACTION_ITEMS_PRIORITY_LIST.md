# 🎯 SAM JOB AUTOMATOR - IMMEDIATE ACTION ITEMS

**Status:** Ready to execute  
**Est. Time to Complete Phase 1:** 4-6 hours  
**Est. Time to Production Ready:** 2 weeks  

---

## 🔴 PHASE 1: CRITICAL FIXES (TODAY/TOMORROW) - DO THESE FIRST

### Fix #1: Race Condition in Rate Limiter
**Severity:** 🔴 CRITICAL | **Time:** 1 hour | **Impact:** Prevents duplicate applications

**File:** `core/main_bot.py` around line 156

**What to do:**
1. Open `core/main_bot.py`
2. Find the rate limiter initialization (search for `rate_limit`)
3. Add `asyncio.Lock()` for thread safety
4. Wrap all timestamp list operations with the lock

**Before:**
```python
self.rate_limit_timestamps = []
# Later in code:
self.rate_limit_timestamps.append(time.time())
```

**After:**
```python
import asyncio
self.rate_limit_lock = asyncio.Lock()

# Later in code:
async with self.rate_limit_lock:
    self.rate_limit_timestamps.append(time.time())
```

- [ ] Completed
- [ ] Tested with multiple concurrent jobs
- [ ] Committed to feature branch

---

### Fix #2: Telegram Polling Conflict
**Severity:** 🔴 CRITICAL | **Time:** 1 hour | **Impact:** Prevents crash from duplicate pollers

**File:** `core/main_bot.py` in `TelegramNotifier.__init__`

**What to do:**
1. In the `__init__` method, add a process-level lock check
2. This prevents two instances from starting the same bot poll

**Code to add at top of class __init__:**
```python
import os
import sys

# Prevent duplicate polling
try:
    self.lock_file = open('.main_bot.lock', 'w')
    os.flock(self.lock_file.fileno(), os.LOCK_EX | os.LOCK_NB) if sys.platform != 'win32' else None
    if sys.platform == 'win32':
        import msvcrt
        msvcrt.locking(self.lock_file.fileno(), msvcrt.LK_NBLCK, 1)
except (IOError, OSError):
    logging.error("❌ Bot already running - another instance detected!")
    raise RuntimeError("Bot already running on this machine")
```

- [ ] Completed
- [ ] Tested (try running 2 instances - second should fail)
- [ ] Committed to feature branch

---

### Fix #3: Organize Repository Structure
**Severity:** 🟠 HIGH | **Time:** 1.5 hours | **Impact:** Repo looks professional, easier to maintain

**What to do:**

1. **Create new directory:**
   ```powershell
   mkdir src
   mkdir src\core
   mkdir src\ui
   mkdir tests
   mkdir docs
   mkdir scripts
   ```

2. **Move directories:**
   ```
   Move-Item core\* src\core\
   Move-Item ui\* src\ui\
   Move core (empty folder) to legacy_archive
   ```

3. **Keep only ONE launcher in root:**
   - Keep: `launch_sam.py`
   - Move to `scripts/`: All other launchers (RUN_*.bat, etc.)

4. **Move tests to tests/ folder:**
   - Move: `test_*.py` files to `tests/`
   - Move: `verify_*.py` files to `tests/verify/`

5. **Update imports in ALL files:**
   - Change: `from core.` → `from src.core.`
   - Change: `from ui.` → `from src.ui.`
   - Run Find & Replace in VS Code (Ctrl+H)

6. **Update GitHub Actions workflows:**
   - Edit `.github/workflows/*.yml`
   - Change paths from `core/` to `src/core/`

**New Structure:**
```
Sam_Job_Automator/
├── src/
│   ├── core/          (all modules)
│   └── ui/            (dashboard)
├── tests/             (all tests)
├── scripts/           (helper scripts)
├── docs/              (documentation)
├── launch_sam.py     (ONLY launcher in root)
└── requirements.txt
```

- [ ] src/ and subdirectories created
- [ ] All modules moved to src/core/ and src/ui/
- [ ] Old core/ and ui/ directories removed
- [ ] All imports updated (Find & Replace: `from core.` → `from src.core.`)
- [ ] All imports updated (Find & Replace: `from ui.` → `from src.ui.`)
- [ ] Tests moved to tests/
- [ ] Scripts moved to scripts/
- [ ] Root directory has only essential files
- [ ] Launch_sam.py still works
- [ ] GitHub workflows updated
- [ ] All tests still pass
- [ ] Committed to feature branch

---

### Fix #4: Create Essential Documentation
**Severity:** 🟠 HIGH | **Time:** 1.5 hours | **Impact:** Users can actually USE the bot

**What to do:**

Create 4 new documentation files in root:

#### 1. **SETUP.md** - Installation guide
```
# Setup Guide

## Prerequisites
- Windows 10+, macOS, or Linux
- Python 3.11+
- PowerShell (Windows) or Bash (Mac/Linux)

## Installation

1. Clone repository
2. Create virtual environment: `python -m venv .venv`
3. Activate: `.venv\Scripts\Activate.ps1` (Windows)
4. Install: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env`
6. Fill in all API keys (see CONFIGURATION.md)
7. Run: `python launch_sam.py`

## Troubleshooting

### ImportError: No module named 'core'
- Make sure .venv is activated
- Run: `pip install -r requirements.txt` again

### No email providers configured
- See CONFIGURATION.md for setup steps

[Add more troubleshooting as needed]
```

#### 2. **CONFIGURATION.md** - API keys and environment
```
# Configuration Guide

## Required API Keys

### 1. Supabase (Database)
- Go to https://supabase.com
- Create project
- Get URL and Key from Settings → API
- Add to .env:
  ```
  SUPABASE_URL=your_url_here
  SUPABASE_KEY=your_key_here
  ```

### 2. Brevo (Email)
- Go to https://www.brevo.com
- Create account
- Get SMTP key from Settings
- Add to .env:
  ```
  BREVO_SMTP_LOGIN=your_login
  BREVO_SMTP_PASSWORD=your_password
  ```

### 3. Telegram (Notifications)
- Get bot token from @BotFather on Telegram
- Get your chat ID (send /start to bot, check logs)
- Add to .env:
  ```
  TELEGRAM_BOT_TOKEN=your_token
  TELEGRAM_CHAT_ID=your_chat_id
  ```

### 4. Gemini or Groq (AI)
- https://aistudio.google.com/app/apikeys (Gemini)
- https://groq.com (Groq)
- Add to .env:
  ```
  GEMINI_API_KEY=your_key
  # OR
  GROQ_API_KEY=your_key
  ```

[Add Gmail, LinkedIn, etc.]

## Test Configuration
- Set `TEST_MODE=true` to avoid actual applications
- Set `KILL_SWITCH_ACTIVE=false` to allow normal operation
```

#### 3. **TROUBLESHOOTING.md** - Common issues
```
# Troubleshooting Guide

## Issue: Duplicate application sends
**Symptom:** Bot applies twice to same job
**Fix:** See data_validator.py → check_if_applied()

## Issue: Email not sending
**Symptom:** No emails appear in logs
**Solutions:**
1. Check BREVO_SMTP_PASSWORD in .env
2. Check Brevo account not rate-limited (300/day)
3. Enable BREVO_HTTP_FALLBACK=true
4. Check spam folder

## Issue: Scraper returns 0 jobs
**Symptom:** No leads found
**Solutions:**
1. Check internet connection
2. Job portal may be blocking requests
3. CSS selectors outdated (needs fixing)
4. Try TEST_MODE to check logs

## Issue: Telegram not responding
**Symptom:** /status commands ignored
**Solutions:**
1. Check TELEGRAM_BOT_TOKEN is correct
2. Check TELEGRAM_CHAT_ID is correct
3. Restart bot
4. Check if process crashed (see logs/)

[Add more issues]
```

#### 4. **ARCHITECTURE.md** - System design
```
# System Architecture

## High-Level Flow

```
SCRAPER (Get Jobs)
    ↓
AI AGENT (Analyze & Rank)
    ↓
CV TAILOR (Personalize)
    ↓
PDF GENERATOR (Create Cover Letter)
    ↓
EMAIL ENGINE (Send Application)
    ↓
DATABASE (Log Application)
    ↓
FOLLOW-UP SCHEDULER (Track for 2nd email)
```

## Core Modules

### main_bot.py
- Entry point, async loop orchestration
- Manages all workers
- Handles kill switch, graceful shutdown

### ai_agent.py
- Analyzes job descriptions
- Tailors CV content
- Generates personalized messages
- Fallback strategies

### smtp_engine.py
- Multi-provider email (Brevo, Gmail)
- Fallback chain
- Rate limiting

### db_client.py
- Supabase + SQLite local fallback
- Duplicate detection
- Application logging

### scrapers/
- Multiple job portal parsers
- Smart caching
- CSS selector management

## Concurrency Model

- Uses asyncio for concurrent I/O
- Configurable worker count (default: 5)
- Rate limiter prevents bans

[Add more detail]
```

**Checklist:**
- [ ] SETUP.md created
- [ ] CONFIGURATION.md created
- [ ] TROUBLESHOOTING.md created
- [ ] ARCHITECTURE.md created
- [ ] All files proofread
- [ ] Links between docs work
- [ ] Code examples accurate

---

## 🟠 PHASE 2: IMPORTANT FEATURES (This Week) - DO THESE NEXT

### Task #1: Fix LinkedIn Automator
**Severity:** 🔴 CRITICAL | **Time:** 2 hours | **Status:** Incomplete

**File:** `core/linkedin_automator.py`

**Issue:** Methods incomplete, missing error handling, likely not working

**Fix:**
1. Review the file - see what's partially done
2. Complete generate_nudge() method with error handling
3. Complete record_nudge_task() 
4. Add proper logging
5. Add unit tests in `tests/test_linkedin_automator.py`

- [ ] File reviewed
- [ ] All methods completed
- [ ] Error handling added
- [ ] Unit tests added
- [ ] Tested with real LinkedIn scenario

---

### Task #2: Update Scraper Selectors
**Severity:** 🔴 CRITICAL | **Time:** 2 hours | **Status:** Outdated

**File:** `core/scrapers/` (all files)

**Issue:** CSS selectors break when sites update (LinkedIn, Indeed, etc.)

**Fix:**
1. Test each scraper on live website
2. Update broken CSS selectors
3. Use ScrapePatrol auto-repair where possible
4. Add version numbers to selector configs

- [ ] All 5 main job portals tested
- [ ] Broken selectors fixed
- [ ] ScrapePatrol auto-repair working
- [ ] Scraper returns ≥5 test jobs

---

### Task #3: Add Type Hints
**Severity:** 🟡 MEDIUM | **Time:** 2 hours | **Status:** 40% complete

**What:** Add type annotations to all functions

**Using VS Code + Pylance:**
```python
# Before:
def process_job(job):
    return result

# After:
def process_job(job: Dict[str, Any]) -> Optional[ProcessedJob]:
    return result
```

**Steps:**
1. Open each file in `src/core/`
2. Use Pylance: Command Palette → "Pylance: Add Type Annotations"
3. Review and accept suggestions
4. Run `mypy src/ --strict` to verify

- [ ] All public functions have type hints
- [ ] mypy passes with --strict flag
- [ ] No `Any` types used except where necessary
- [ ] All imports typed

---

### Task #4: Add Unit Tests
**Severity:** 🟡 MEDIUM | **Time:** 2 hours | **Status:** 35% coverage

**Create tests for:**
1. `tests/test_ai_agent.py` - Job analysis
2. `tests/test_smtp_engine.py` - Email sending
3. `tests/test_db_client.py` - Database operations
4. `tests/test_scrapers.py` - Web scraping

**Run tests:**
```bash
pytest tests/ -v
pytest tests/ --cov=src  # Coverage report
```

**Target:** 80%+ code coverage

- [ ] 8+ new test files created
- [ ] All core modules have tests
- [ ] pytest run: all pass
- [ ] Coverage ≥ 80%

---

### Task #5: Create Architecture Diagram
**Severity:** 🟡 MEDIUM | **Time:** 1 hour | **Status:** Missing

**Tool:** Create using Mermaid (best for GitHub)

**Create:** `docs/ARCHITECTURE_DIAGRAM.md`

```
Graph showing:
- Main bot loop
- Module interactions
- Data flow
- Error handling paths
```

- [ ] Diagram created in Mermaid
- [ ] Rendered in docs/
- [ ] Linked from README.md
- [ ] Accurately represents system

---

## 🟢 VALIDATION CHECKLIST

### Before committing ANY code:

- [ ] No `console.log()` or print statements (use logging)
- [ ] All error cases handled with try-except
- [ ] No hardcoded values (use config.py)
- [ ] Type hints on all new functions
- [ ] Docstrings on all public functions
- [ ] Code passes: `pylint src/ --score=9.0`
- [ ] Code passes: `mypy src/ --strict`
- [ ] New tests written for new code
- [ ] All tests pass: `pytest tests/`
- [ ] No secrets committed to git

---

## 🚀 GITHUB WORKFLOW

### For each fix:

1. **Create branch:**
   ```bash
   git checkout -b feature/fix-race-condition
   ```

2. **Make changes:**
   - Implement fix
   - Add tests
   - Update docs

3. **Commit:**
   ```bash
   git add .
   git commit -m "Fix: add asyncio.Lock to rate limiter"
   ```

4. **Push:**
   ```bash
   git push origin feature/fix-race-condition
   ```

5. **Create Pull Request:**
   - Write description
   - Reference issue
   - Request review

6. **Merge when:**
   - All checks pass
   - Tests pass
   - Code reviewed

---

## 📊 PROGRESS TRACKING

**Phase 1 Completion:** 0%
```
[||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||] 0%
```

**Current Task:** Not started
**Estimated Completion:** TBD

---

## 🎯 DEFINITION OF DONE

Each task is complete when:

1. ✅ Code written and tested locally
2. ✅ All unit tests pass
3. ✅ Code follows style guide (black formatted, mylint 8.0+)
4. ✅ Docstrings added
5. ✅ No console logs (logging only)
6. ✅ Git committed with clear message
7. ✅ GitHub PR created with description
8. ✅ Code reviewed by team
9. ✅ Merged to development branch
10. ✅ Verified working on develop

---

## 📞 NEED HELP?

1. Check `TROUBLESHOOTING.md` first
2. Review existing issues on GitHub
3. Create new issue with:
   - What you tried
   - What happened
   - Error messages
   - Environment (OS, Python version)
4. Tag me with @mention

---

**Let's make this production-ready! 🚀**

Execute this checklist in order → All phase 1 fixes should take 4-6 hours → Then move to Phase 2 tasks
