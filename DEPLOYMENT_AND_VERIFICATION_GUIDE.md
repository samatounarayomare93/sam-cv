# 🚀 DEPLOYMENT & VERIFICATION GUIDE

Complete guide to deploy Project Chronos to Render.com and verify functionality.

---

## Phase 1: Pre-Deployment Checklist (Local)

### Step 1: Validate Configuration
```bash
cd Sam_Job_Automator_Local
python deployment_validator.py
```

Expected output:
```
✅ DEPLOYMENT READY: All 5 checks passed!
```

### Step 2: Create Local .env File
```bash
cp .env.example .env
```

Edit `.env` and fill in **ALL** required fields:
- ✅ At least ONE LLM API key (Gemini or Groq)
- ✅ At least ONE email provider (Gmail or Brevo)
- ✅ Telegram bot token

### Step 3: Test Locally
```bash
python run.py
```

You should see:
```
================================================================================
PROJECT CHRONOS: OMEGA-SOVEREIGNTY UNIFIED SWARM
------------------------------------------------------------------------
Status: CONSOLIDATING INTELLIGENCE...
[SYSTEM] Activating Cloud Heartbeat (Port Binding)...
[SYSTEM] Initializing Shared Swarm Intelligence...
[SYSTEM] Launching Unified Swarm Tasks...
```

### Step 4: Test Telegram Bot Locally
1. Open Telegram
2. Send bot: `/status`
3. Bot should respond with automation status

---

## Phase 2: Deploy to Render.com

### Step 1: Prepare GitHub Repository
```bash
# Ensure all changes are committed
git status
# Should show: nothing to commit, working tree clean

# Push to GitHub
git push origin main
```

### Step 2: Create Render Service
1. Go to https://render.com/dashboard
2. Click **New+** → **Web Service**
3. Connect GitHub repository
4. Select **Sam_Job_Automator** repository

### Step 3: Configure Build Settings
Fill in:
- **Name**: `sam-job-automator`
- **Environment**: `Docker` (auto-detected)
- **Region**: Choose closest to users
- **Branch**: `main`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python launch_sam.py`

### Step 4: Add Environment Variables

In Render dashboard, go to **Environment** and add each variable:

```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGc...xxxxx
GEMINI_API_KEY=AIzaSy...xxxxx
GROQ_API_KEY=gsk_...xxxxx
TELEGRAM_BOT_TOKEN=123456789:ABCDefGhIjKlMnOpQrStUvWxYz
TELEGRAM_API_ID=123456789
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890
GMAIL_SMTP_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
BREVO_SMTP_LOGIN=your-email@example.com
BREVO_SMTP_PASSWORD=your-brevo-password
TEST_MODE=false
TEST_RECEIVER_EMAIL=your-test@example.com
```

### Step 5: Deploy
1. Click **Create Web Service**
2. Wait for build to complete (~3-5 minutes)
3. Watch logs in Render dashboard
4. Service should start successfully

---

## Phase 3: Post-Deployment Verification

### Test 1: Telegram Bot Response
```
Send to bot:     /status
Expected result: Bot responds with automation status
Verify:          ✅ Bot is connected and responsive
```

### Test 2: Test Email Delivery
```
Send to bot:     /test_strike
Expected result: Bot shows "GENERATING..." → "Test strike queued"
Check email:     You should receive test email in TEST_RECEIVER_EMAIL
Verify:          ✅ Email delivery working
```

### Test 3: Check Cloud Logs
In Render dashboard:
1. Go to **Logs** tab
2. Should see lines like:
   ```
   [SYSTEM] Activating Cloud Heartbeat...
   [SYSTEM] Launching Unified Swarm Tasks...
   ```
3. Watch for errors:
   - ❌ ImportError → Missing module
   - ❌ KeyError → Missing environment variable
   - ❌ ConnectionError → Service connectivity issue

### Test 4: Verify Leadership Election
```
Send to bot:     /stats
Expected result: Current statistics with node identification
Verify:          ✅ Multi-instance coordination working
```

### Test 5: Test All 50 Commands (Sample)
```
/start            → Welcome message
/menu             → Command menu
/health           → System health status
/logs             → Recent logs
/analyze <job>    → AI job analysis
```

---

## Phase 4: Monitoring & Maintenance

### Daily Monitoring Checklist
- ✅ Send `/status` to bot (verify responsive)
- ✅ Check Render logs for errors
- ✅ Verify no resource exhaustion warnings
- ✅ Monitor email delivery success rate

### Weekly Maintenance
- ✅ Review `/stats` for performance metrics
- ✅ Check for failed job applications
- ✅ Verify follow-ups are being sent
- ✅ Monitor database sync status

### Common Issues & Solutions

#### Issue: Bot Not Responding
```
Cause:           Telegram polling not running
Solution:        
  1. Check Render logs for errors
  2. Verify TELEGRAM_BOT_TOKEN is correct
  3. Restart service: Render dashboard → Restart
```

#### Issue: Email Delivery Failing
```
Cause:           Invalid credentials or API issues
Solution:
  1. Verify credentials in Render environment
  2. Test with /test_strike command
  3. Check email provider (Gmail/Brevo) for errors
  4. Ensure email auth is enabled
```

#### Issue: High Memory Usage
```
Cause:           Resource leak or excessive caching
Solution:
  1. Restart service: Render dashboard → Restart
  2. Check logs for memory warnings
  3. Reduce lead processing batch size in config
```

#### Issue: Supabase Connection Failed
```
Cause:           Database service unavailable or wrong credentials
Solution:
  1. System falls back to SQLite (auto-failover)
  2. Verify SUPABASE_URL and SUPABASE_KEY
  3. Check Supabase service status
  4. Local SQLite mode will continue working
```

---

## Phase 5: Scaling & Optimization

### Monitor Performance
```bash
# View key metrics (from Telegram)
/stats              # Cycle statistics
/performance        # Success metrics
/queue              # Lead queue status
/health             # System health
```

### Optimize Settings
In `.env`, adjust these for your needs:
```
MAX_LEADS_PER_CYCLE=15          # Leads per automation cycle
CONCURRENT_EMAIL_WORKERS=3      # Parallel email delivery
REQUEST_JITTER_MIN=2            # Min delay between requests (sec)
REQUEST_JITTER_MAX=5            # Max delay between requests (sec)
SCRAPER_PAGES=3                 # Pages to scrape per source
```

### Scale to Multiple Instances
For higher throughput, create multiple Render services:
1. Each instance will auto-elect a leader
2. Leader coordinates job queue
3. Workers process leads independently
4. All share Supabase database

---

## Troubleshooting Guide

### Check Logs
```bash
# In Render dashboard
Logs tab → Search for keywords:
- ERROR:     Find what went wrong
- WARNING:  Find potential issues
- INFO:     Track execution flow
```

### Test Individual Components

**Test Database**
```
Send: /test_database
Expected: Connection status
```

**Test Email Provider**
```
Send: /test_email
Expected: Email delivery success
```

**Test LLM**
```
Send: /test_ai <text>
Expected: AI response
```

**Test Scraper**
```
Send: /test_scraper
Expected: Sample leads found
```

### Emergency Recovery

If bot is stuck or unresponsive:
1. Restart service: Render dashboard → Restart
2. Clear cache: `/clear_cache` command (if responsive)
3. Reset database: `/reset_db` (admin command, use carefully)
4. Redeploy: Push update to GitHub → auto-redeploy on Render

---

## Security Checklist

- ✅ Never commit `.env` file (in .gitignore)
- ✅ Rotate API keys periodically
- ✅ Use separate bot tokens for dev/prod
- ✅ Enable Telegram 2FA on account
- ✅ Use strong passwords for email accounts
- ✅ Monitor Render logs for suspicious activity
- ✅ Set up alerting for critical errors

---

## Success Indicators

Your deployment is successful when:

✅ Bot responds to `/status` within 2 seconds  
✅ `/test_strike` successfully sends email  
✅ Telegram logs show no errors  
✅ `/stats` shows active job cycle  
✅ Follow-ups are being sent automatically  
✅ All 50 commands are accessible  
✅ Cloud logs show clean operation  

---

## Next Steps After Deployment

1. **Monitor** - Watch logs and performance for first week
2. **Optimize** - Adjust settings based on performance
3. **Scale** - Add more instances if needed
4. **Integrate** - Connect with other services (Slack alerts, etc.)
5. **Automate** - Set up monitoring dashboards

---

## Support & Help

- **Logs**: Check Render dashboard → Logs tab
- **Commands**: Send `/help` to Telegram bot
- **Docs**: See DEPLOYMENT_SECRETS_GUIDE.md
- **Issues**: Check GitHub Issues or create new one

---

**Deployment Complete. Project Chronos is now live and operational.** 🚀
