# 🔑 SAM JOB AUTOMATOR - CONFIGURATION GUIDE

Complete guide to getting all required API keys and environment variables.

---

## 📌 OVERVIEW

**Required APIs:**
1. ✅ Supabase (Database) - FREE
2. ✅ Brevo (Email) - FREE (300/day)
3. ✅ Telegram (Bot) - FREE
4. ✅ Gemini or Groq (AI) - FREE tier available
5. ✅ Gmail API (Optional fallback email) - FREE

**Setup Time: ~30 minutes total**

---

## 1️⃣ SUPABASE DATABASE

### What it is:
Cloud database for tracking applications, logging, and deduplication.

### Setup:

**Step 1: Create account**
- Go to https://supabase.com
- Click "Start your project"
- Login with GitHub or email
- Create new project

**Step 2: Get credentials**
- Dashboard → Settings → API
- Copy: **Project URL** (looks like `https://xxxxx.supabase.co`)
- Copy: **API Key** (anon public)

**Step 3: Add to .env**
```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your_api_key_here
```

**Test connection:**
```bash
python -c "from core.db_client import RealityShapingDB; print('✅ Supabase connected')"
```

---

## 2️⃣ BREVO EMAIL

### What it is:
Primary email provider. 300 free emails/day (plenty for job applications).

### Setup:

**Step 1: Create account**
- Go to https://www.brevo.com
- Sign up (free account)
- Verify email

**Step 2: Get SMTP credentials**
- Dashboard **→ Settings → SMTP & API**
- Enable SMTP
- Copy: **SMTP Login** (your Brevo email)
- Copy: **SMTP Password** (NOT your account password - it's unique)

**Step 3: Test SMTP credentials work**
- Keep browser open, noting credentials
- Will test via Python in Step 4

**Step 4: Add to .env**
```
BREVO_SMTP_LOGIN=your_brevo_email@brevo.com
BREVO_SMTP_PASSWORD=xxxxxxxxxxxxxx
USE_BREVO_HTTP_FALLBACK=true
```

**Test email sending:**
```bash
python -c "from core.smtp_engine import test_email_connection; test_email_connection()"
```

**Expected output:**
```
✅ Email provider Brevo: SUCCESS
```

---

## 3️⃣ TELEGRAM BOT

### What it is:
Remote control interface. Send `/status` to bot to check bot status.

### Setup:

**Step 1: Create Telegram Bot**
- Open Telegram app (or https://web.telegram.org)
- Search for: `@BotFather`
- Send: `/newbot`
- Follow prompts (choose name like "SamJobBot")
- **Copy the token** (looks like `123456789:ABCDEFghijklmn...`)

**Step 2: Get your Chat ID**
- Search for: `@userinfobot`
- Send any message
- **Copy your user ID** (number)

**Step 3: Add to .env**
```
TELEGRAM_BOT_TOKEN=123456789:ABCDEFghijklmn...
TELEGRAM_CHAT_ID=987654321
```

**Test bot:**
```bash
# Start bot
python launch_sam.py

# In Telegram, send to your bot:
/status

# Should get response showing bot status
```

---

## 4️⃣ GEMINI AI (Google)

### What it is:
Analyzes job descriptions and generates personalized cover letters.

### Setup:

**Step 1: Enable API**
- Go to https://aistudio.google.com/app/apikeys
- Click "Create API Key"
- **Copy the key**

**Step 2: Add to .env**
```
GEMINI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
```

**Test AI:**
```bash
python -c "from core.ai_agent import OmniIntelligence; ai = OmniIntelligence(); print('✅ AI initialized')"
```

---

## 5️⃣ GROQ AI (Alternative to Gemini)

### What it is:
Fast AI alternative. Use if Gemini is slow or rate-limited.

### Setup:

**Step 1: Create account**
- Go to https://groq.com
- Sign up
- Create API key in console

**Step 2: Add to .env**
```
GROQ_API_KEY=xxxxxxxxxxxxx
```

**Note:** Set EITHER `GEMINI_API_KEY` OR `GROQ_API_KEY`, not both.

---

## 6️⃣ GMAIL API (Optional - Fallback Email)

### What it is:
Backup email provider if Brevo fails. More reliable but slower.

### Setup:

**Step 1: Enable Gmail API**
- Go to https://console.cloud.google.com/apis/library/gmail.googleapis.com
- Click "Enable"

**Step 2: Create OAuth credentials**
- Go to https://console.cloud.google.com/apis/credentials
- Click "Create Credentials" → "OAuth Client ID"
- Choose "Desktop application"
- Download JSON file
- Save as `credentials.json` in project root

**Step 3: First-time auth**
- Run: `python core/gmail_auth.py`
- Browser opens
- Grant permission
- Token saved automatically

**Test Gmail:**
```bash
python -c "from core.gmail_auth import get_gmail_service; get_gmail_service(); print('✅ Gmail ready')"
```

---

## 7️⃣ LINKEDIN PROFILE (Manual Setup)

### What it is:
For targeted outreach and recruiter detection (manual setup, no API).

### Setup:

No API setup needed. Bot uses browser automation.

**To enable LinkedIn features:**
```
# In .env, ensure these are set:
LINKEDIN_EMAIL=your.email@linkedin.com
LINKEDIN_PASSWORD=your_password
```

**First run:**
- Bot may ask for 2FA code
- Enter when prompted
- Credentials stored securely

---

## 🧪 COMPLETE .env TEMPLATE

```bash
# ============ CRITICAL (REQUIRED) ============
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=xxxxxxxxxxxxxx

BREVO_SMTP_LOGIN=your_email@brevo.com
BREVO_SMTP_PASSWORD=xxxxxxxxxxxxxx

TELEGRAM_BOT_TOKEN=123456789:ABCDEFghijklmn
TELEGRAM_CHAT_ID=987654321

GEMINI_API_KEY=xxxxxxxxxxxxxx
# OR set one of:
#GROQ_API_KEY=xxxxxxxxxxxxxx

# ============ OPTIONAL ============
TEST_MODE=true              # true for testing, false for production
KILL_SWITCH_ACTIVE=false    # true to stop bot

MAX_PARALLEL_STRIKES=5      # Concurrent jobs processed
DECOY_FLEET_SIZE=2          # Support applications

# Gmail fallback (if using Gmail API)
#GMAIL_SENDER_EMAIL=your.email@gmail.com

# LinkedIn (optional)
#LINKEDIN_EMAIL=your@email.com
#LINKEDIN_PASSWORD=your_password

# Proxy (if using residential proxies)
#RESIDENTIAL_PROXIES=proxy1:port,proxy2:port

# Logging
DIVINE_LOG_LEVEL=INFO       # DEBUG, INFO, WARNING, ERROR
```

---

## ✅ VERIFICATION CHECKLIST

After filling `.env`, verify all keys:

```bash
# Test each provider:
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

# Supabase
assert os.getenv('SUPABASE_URL'), '❌ Missing SUPABASE_URL'
assert os.getenv('SUPABASE_KEY'), '❌ Missing SUPABASE_KEY'
print('✅ Supabase configured')

# Brevo
assert os.getenv('BREVO_SMTP_LOGIN'), '❌ Missing BREVO_SMTP_LOGIN'
assert os.getenv('BREVO_SMTP_PASSWORD'), '❌ Missing BREVO_SMTP_PASSWORD'
print('✅ Brevo configured')

# Telegram
assert os.getenv('TELEGRAM_BOT_TOKEN'), '❌ Missing TELEGRAM_BOT_TOKEN'
assert os.getenv('TELEGRAM_CHAT_ID'), '❌ Missing TELEGRAM_CHAT_ID'
print('✅ Telegram configured')

# AI
assert os.getenv('GEMINI_API_KEY') or os.getenv('GROQ_API_KEY'), '❌ Missing AI API key'
print('✅ AI configured')

print('\n✨ All critical configs present!')
"
```

---

## 🆘 TROUBLESHOOTING

### "API Key invalid"
- Regenerate new key from service
- Paste EXACTLY (no extra spaces)
- Reload shell after .env changes

### "Authentication failed"
- Double-check spelling
- Verify you copied FULL key
- Check key wasn't rotated/deleted

### "Rate limited"
- Brevo: Max 300/day, space out applications
- Gemini: Free tier has ~1000 tokens/min
- Use Groq as backup if hitting limits

### ".env file not found"
- Must be in project root: `C:\Users\samde\Sam_Job_Automator_Local\.env`
- Check it's NOT in `.gitignore` (local configs shouldn't be committed)

---

## 🔐 SECURITY BEST PRACTICES

1. **Never commit .env** - Already in `.gitignore`
2. **Rotate API keys** - Every 3-6 months
3. **Use least permissions** - Don't grant unnecessary scopes
4. **Monitor usage** - Check Brevo/Gemini dashboards for abuse
5. **Keep secrets local** - Don't share .env or keys with others

---

## 🚀 NEXT STEPS

1. ✅ Get all API keys above
2. ✅ Fill `.env` file
3. ✅ Run verification script
4. ✅ Test in TEST_MODE: `python launch_sam.py`
5. ✅ Check logs for errors
6. 🎉 Ready to deploy!

---

**Questions?** Check TROUBLESHOOTING.md next.
