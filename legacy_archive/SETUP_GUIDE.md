# ⚙️ SAM JOB AUTOMATOR - SETUP GUIDE

**Quick Start in 5 Minutes** ⚡

---

## 📋 PREREQUISITES

- **Windows 10+** (PowerShell), macOS, or Linux (Bash)
- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Git** (optional, for version control)
- **API Keys** (see CONFIGURATION.md)

---

## 🚀 INSTALLATION STEPS

### Step 1: Clone or Download Project
```bash
# If using Git:
git clone <repository_url>
cd Sam_Job_Automator_Local

# Or download ZIP and extract
cd path/to/Sam_Job_Automator_Local
```

### Step 2: Create Virtual Environment
```powershell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

**Expected Output:**
```
(.venv) C:\path\to\Sam_Job_Automator_Local>
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Troubleshooting if this fails:**
- Windows: Run PowerShell as Administrator
- macOS: May need `python3 -m pip install ...`
- Linux: May need `sudo apt-get install python3-pip`

### Step 4: Configure Environment
```bash
# Copy example to real config
cp launch_config.example.env .env

# OR on Windows:
copy launch_config.example.env .env
```

**Edit `.env` file with your API keys:**
```
# Essential
SUPABASE_URL=your_url_here
SUPABASE_KEY=your_key_here
BREVO_SMTP_LOGIN=your_email
BREVO_SMTP_PASSWORD=your_password
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
GEMINI_API_KEY=your_key

# See CONFIGURATION.md for complete list
```

### Step 5: Verify Installation
```bash
# Test Python imports
python -c "import requests; import dotenv; print('✅ Dependencies OK')"

# Check main bot initializes
python -c "from core.main_bot import AlphaOrchestrator; print('✅ Core modules OK')"

# Run preflight check
python launch_sam.py --check
```

**Expected Output:**
```
✅ Dependencies OK
✅ Core modules OK
✅ Preflight Check Passed
```

---

## ▶️ RUNNING THE BOT

### Option 1: Direct Python (Recommended for debugging)
```bash
python launch_sam.py
```

### Option 2: Using Batch File (Windows)
```powershell
START.bat
```

### Option 3: Using Scheduled Tasks (24/7 Running)
- See documentation in `.github/workflows/24_7_telegram_bot.yml`

---

## 🧪 TEST MODE (SAFE PRACTICE)

**Always test before production:**

```powershell
# Enable test mode in .env
TEST_MODE=true
KILL_SWITCH_ACTIVE=false

# Run bot
python launch_sam.py

# Check logs
Get-Content logs\sam.log -Tail 20
```

**What TEST_MODE does:**
- ✅ Logs applications but doesn't send emails
- ✅ Validates all systems work
- ✅ No real applications sent
- ✅ Safe to run anytime

---

## ✅ VALIDATION CHECKLIST

After installation, verify:

- [ ] Virtual environment activated (see `(.venv)` in prompt)
- [ ] All dependencies installed (`pip list` shows packages)
- [ ] `.env` file created and filled with API keys
- [ ] `python -c "from core.main_bot import AlphaOrchestrator"` works
- [ ] `TEST_MODE=true` set in `.env`
- [ ] Bot starts: `python launch_sam.py`
- [ ] Get no import errors
- [ ] Logs appear in `logs/` folder

---

## 🛑 COMMON ISSUES & FIXES

### ❌ Issue: "No module named 'core'"

**Symptoms:** `ModuleNotFoundError: No module named 'core'`

**Solutions:**
1. Verify `.venv` is activated: should see `(.venv)` in prompt
2. Reinstall: `pip install --force-reinstall -r requirements.txt`
3. Check Python version: `python --version` (must be 3.11+)

---

### ❌ Issue: "API Key not found"

**Symptoms:** `KeyError: 'SUPABASE_URL'` or similar

**Solutions:**
1. Verify `.env` file exists in project root
2. Check `.env` is NOT listed in `.gitignore` (config is local-only)
3. Reload shell: Deactivate & reactivate virtualenv
4. See: CONFIGURATION.md for all required keys

---

### ❌ Issue: "pyTelegramBotAPI import fails"

**Symptoms:** `ImportError: No module named 'telebot'`

**Solutions:**
```bash
# Explicitly install:
pip install pyTelegramBotAPI==4.14.0

# Verify:
python -c "import telebot; print('OK')"
```

---

### ❌ Issue: "Could not connect to Supabase"

**Symptoms:** `Failed to connect to Supabase` or timeout errors

**Solutions:**
1. Check internet connection: `ping google.com`
2. Verify Supabase URL is correct (no trailing `/`)
3. Check Supabase API key has correct permissions
4. Try local-only mode: `TEST_MODE=true` uses local SQLite

---

## 🔄 UNINSTALLING / RESETTING

**To completely reset:**

```powershell
# Deactivate virtualenv
deactivate

# Remove virtualenv
Remove-Item -Recurse .venv

# Start fresh from Step 2 above
```

**To reset just the environment:**
```bash
# Backup your custom .env if you want to keep it
# Then:
rm .env
cp launch_config.example.env .env
# Re-fill with your keys
```

---

## 📞 NEED HELP?

1. Check **TROUBLESHOOTING.md** first
2. Review logs: `Get-Content logs\sam.log | Select-Object -Last 50`
3. Try TEST_MODE: Run with `TEST_MODE=true` to isolate issues
4. Create GitHub issue with:
   - Error message (full traceback)
   - Python version: `python --version`
   - OS: Windows/macOS/Linux
   - Steps you took

---

## ✨ NEXT STEPS

1. ✅ Installation complete
2. 🔑 Go to **CONFIGURATION.md** to get all API keys
3. 🧪 Run in TEST_MODE to validate
4. 🚀 Read TROUBLESHOOTING.md for common issues
5. 💼 Check ARCHITECTURE.md to understand how it works

---

**Installation should take ~10 minutes total.** 

If stuck longer, check TROUBLESHOOTING.md or check logs for specific errors.
