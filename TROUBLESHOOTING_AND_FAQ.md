# ❓ TROUBLESHOOTING & FAQ

Comprehensive troubleshooting and frequently asked questions for Project Chronos.

---

## Table of Contents
1. [Quick Diagnostics](#quick-diagnostics)
2. [Common Issues](#common-issues)
3. [Frequently Asked Questions](#frequently-asked-questions)
4. [Error Messages](#error-messages)
5. [Performance Issues](#performance-issues)
6. [Emergency Recovery](#emergency-recovery)

---

## Quick Diagnostics

### Run Full Diagnostics
```bash
# Check Python environment
python --version          # Should be 3.11+

# Check dependencies
python -c "import core.main_bot; print('✅ Core imports OK')"

# Check configuration
python -c "from core.utils.config import Config; print('✅ Config loaded')"

# Validate .env
python -c "import os; print('✅ Environment loaded')" && \
echo "  TELEGRAM_BOT_TOKEN: $(echo $TELEGRAM_BOT_TOKEN | head -c 10)..." && \
echo "  SUPABASE_URL: $(echo $SUPABASE_URL | head -c 20)..."

# Test Telegram connection
python -c "from telegram import Bot; import asyncio; \
asyncio.run(Bot('${TELEGRAM_BOT_TOKEN}').get_me())" && echo "✅ Telegram OK"

# Test database
python -c "import asyncio; from core.db_client import RealityShapingDB; \
db = RealityShapingDB(); asyncio.run(db.health_check())" && echo "✅ Database OK"
```

### Quick Health Check
```bash
# 1. Is bot running?
ps aux | grep python | grep -E "run.py|main_bot.py"

# 2. Check logs for errors
tail -50 logs/bot.log | grep ERROR

# 3. Test Telegram response
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe"

# 4. Check cloud status (if deployed)
curl -s "https://your-service.onrender.com/health" | head -c 100
```

---

## Common Issues

### Issue 1: Bot Not Responding to Commands

**Symptoms**:
- Send `/status` → No response
- Telegram shows "Bot is typing..." then timeout
- No error messages visible

**Diagnosis**:
```bash
# Step 1: Check if process is running
ps aux | grep run.py

# Step 2: Check logs
tail -100 logs/bot.log | grep -E "ERROR|CRITICAL|Exception"

# Step 3: Check Telegram token
echo $TELEGRAM_BOT_TOKEN | wc -c  # Should be > 40

# Step 4: Test bot connectivity
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe" | grep ok
```

**Solutions**:

✅ **Solution A**: Restart the bot
```bash
# Stop current process
pkill -f "python run.py"

# Clear any stuck processes
pkill -9 python

# Restart
python run.py
```

✅ **Solution B**: Verify Telegram token
```bash
# 1. Go to BotFather in Telegram
# 2. Send /mybots
# 3. Select your bot
# 4. Click "API Token"
# 5. Copy token
# 6. Update .env with new token
# 7. Restart bot
```

✅ **Solution C**: Check network connectivity
```bash
# Ping Telegram servers
ping api.telegram.org

# Check DNS resolution
nslookup api.telegram.org

# If behind proxy, configure:
# Set TELEGRAM_PROXY in .env
```

---

### Issue 2: Emails Not Sending

**Symptoms**:
- Send `/test_strike` → Success message, but email not received
- `/delivered` shows 0 sent
- Gmail/Brevo credentials seem correct

**Diagnosis**:
```bash
# Step 1: Test email provider individually
python -c "from core.smtp_engine import SMTPEngine; \
import asyncio; \
e = SMTPEngine(); \
asyncio.run(e.send_test_email('test@example.com'))"

# Step 2: Check credentials
echo "Gmail: $GMAIL_SMTP_USER"
echo "Brevo: $BREVO_SMTP_LOGIN"

# Step 3: Check logs
grep -i "email\|smtp\|gmail\|brevo" logs/bot.log | tail -20
```

**Solutions**:

✅ **For Gmail**:
```bash
# 1. Enable 2FA: https://myaccount.google.com/security
# 2. Generate app password: https://myaccount.google.com/apppasswords
# 3. Update .env:
#    GMAIL_SMTP_USER=your-email@gmail.com
#    GMAIL_APP_PASSWORD=your-16-char-password
# 4. Restart bot and retry
```

✅ **For Brevo**:
```bash
# 1. Go to https://app.brevo.com/settings/smtp-tls
# 2. Copy SMTP credentials (login & password)
# 3. Update .env:
#    BREVO_SMTP_LOGIN=your-account
#    BREVO_SMTP_PASSWORD=your-password
# 4. Restart bot and retry
```

✅ **Check spam folder**:
```bash
# Sometimes emails go to spam
# Check Gmail spam/promotions folders
# Mark as "Not Spam" to improve delivery
```

---

### Issue 3: Database Connection Failed

**Symptoms**:
- `/stats` shows "Database: OFFLINE"
- `/test_database` command times out
- SQLite fallback not activating

**Diagnosis**:
```bash
# Step 1: Check Supabase credentials
echo "URL: $SUPABASE_URL"
echo "Key: $(echo $SUPABASE_KEY | head -c 10)..."

# Step 2: Test Supabase connection
curl -H "apikey: $SUPABASE_KEY" \
     "https://$(echo $SUPABASE_URL | cut -d. -f1 | cut -d/ -f3).supabase.co/rest/v1/" 2>/dev/null | head -c 50

# Step 3: Check SQLite file
ls -lh *.db  # Should show database file

# Step 4: Test SQLite directly
python -c "import sqlite3; db = sqlite3.connect('chronos.db'); print('✅ SQLite OK')"
```

**Solutions**:

✅ **If Supabase is down**:
```bash
# System automatically falls back to SQLite
# No action needed - bot will continue working locally
# Once Supabase recovers, sync will happen automatically
```

✅ **If Supabase credentials are wrong**:
```bash
# 1. Go to https://app.supabase.com
# 2. Project Settings → API
# 3. Copy Project URL and anon key
# 4. Update .env:
#    SUPABASE_URL=https://xxxxx.supabase.co
#    SUPABASE_KEY=eyJhbGc...
# 5. Restart bot
```

✅ **Force SQLite-only mode** (temporary):
```bash
# Set environment variable
export USE_SQLITE_ONLY=true

# Restart bot - will use SQLite even if Supabase available
python run.py
```

---

### Issue 4: High Memory/CPU Usage

**Symptoms**:
- `/performance` shows CPU > 80% or Memory > 400MB
- Service becomes slow to respond
- Render shows "Memory limit exceeded" (if deployed)

**Diagnosis**:
```bash
# Check current usage
top -p $(pgrep -f "python run.py") -b -n 1

# Or on macOS
ps aux | grep python

# Check for memory leaks over time
ps aux | grep python | grep -v grep
```

**Solutions**:

✅ **Reduce batch size**:
```bash
# In .env, reduce:
MAX_LEADS_PER_CYCLE=10  # Was 15
CONCURRENT_EMAIL_WORKERS=2  # Was 3

# Restart bot
pkill -f "python run.py"
python run.py
```

✅ **Clear cache**:
```bash
# Send to bot
/clear_cache

# Or restart to reset memory
python run.py
```

✅ **Check for stuck processes**:
```bash
# Find Python processes
ps aux | grep python

# Kill stuck ones
kill -9 <PID>

# Restart cleanly
python run.py
```

✅ **Enable garbage collection logging**:
```bash
# In core/main_bot.py, add:
import gc
gc.set_debug(gc.DEBUG_LEAK)

# Will print unreachable objects
```

---

### Issue 5: Leads Not Being Found

**Symptoms**:
- `/queue` shows 0 pending leads
- `/stats` shows "Leads: 0"
- Scrapers not discovering jobs

**Diagnosis**:
```bash
# Test scraper directly
python -c "from core.scrapers.scraper import DuckDuckGoScraper; \
import asyncio; \
s = DuckDuckGoScraper(); \
leads = asyncio.run(s.scrape('Python Engineer')); \
print(f'Found {len(leads)} leads')"

# Check logs
grep -i "scraper\|discovered\|leads" logs/bot.log | tail -20

# Test individual scrapers
/test_scraper  # Send to bot
```

**Solutions**:

✅ **Check internet connection**:
```bash
ping google.com
curl -I https://www.google.com
```

✅ **Verify scraper is enabled**:
```bash
# In .env, ensure:
ENABLE_SCRAPERS=true
SCRAPER_PAGES=3

# Check config
/config  # Send to bot
```

✅ **Try alternative scraper**:
```bash
# Scrapers available:
# - DuckDuckGo scraper (default)
# - LinkedIn scraper (if enabled)
# - Custom scraper (write your own)

# Send to bot to test
/test_scraper
```

✅ **Increase scraper verbosity**:
```bash
# In .env
LOG_LEVEL=DEBUG

# Will show scraper debug output
```

---

## Frequently Asked Questions

### Q1: Can I run multiple instances?

**A**: Yes! Project Chronos supports multi-instance with leadership election.

```bash
# Instance 1 (becomes leader)
INSTANCE_ID=instance-1 python run.py

# Instance 2 (worker, syncs with instance 1)
INSTANCE_ID=instance-2 python run.py

# Both will share the same database and coordinate work
```

**Benefits**:
- Higher throughput
- Automatic failover
- Distributed processing
- Load balancing

---

### Q2: How do I update the bot code?

**A**: For Render.com:

```bash
# 1. Make changes locally
# 2. Test locally: python run.py
# 3. Commit to GitHub
git add .
git commit -m "feature: Your change"
git push origin main

# 4. Render automatically redeploys
# 5. Watch logs: Render dashboard → Logs
# 6. Test: Send /status to bot
```

---

### Q3: How do I backup my data?

**A**: Supabase handles cloud backups automatically. For local backup:

```bash
# Backup SQLite database
cp chronos.db chronos.db.backup.$(date +%Y%m%d_%H%M%S)

# Or use bot command
/export_data  # Exports all records to JSON

# To restore
/import_data backup.json
```

---

### Q4: Can I change the email template?

**A**: Yes, in `core/smtp_engine.py`:

```python
# Find send_strike() method
# Modify email_body and email_html

# Or create custom template:
def get_email_template(self, cv_name, company):
    return f"""
    Subject: Application for {company}
    
    Dear Hiring Team,
    
    I'm applying for the position at {company}.
    
    Attached is my CV: {cv_name}
    ...
    """
```

---

### Q5: How do I track job applications?

**A**: Use Telegram commands:

```bash
/stats          # Overall statistics
/delivered      # Recently sent applications
/pending        # Pending follow-ups
/analytics      # Trends over time

# Or check database directly
/export_data
```

---

### Q6: What if my API key quota is exceeded?

**A**: 

```bash
# Check current usage
/api_status

# If primary provider (Gemini) is over quota:
# - Automatically switches to Groq
# - OR waits for quota reset

# If both providers over quota:
# - Bot pauses until quota resets
# - Continue with cached analyses

# To prevent this:
# - Use lower REQUEST_JITTER values (faster processing, fewer API calls)
# - Or upgrade to paid tier
```

---

### Q7: How do I monitor production?

**A**: Use the monitoring guide:

```bash
# Daily
/status
/health
/stats

# Weekly
/analytics
/performance
/metrics

# Or read MONITORING_AND_OPERATIONS.md
```

---

### Q8: Can I deploy to other platforms?

**A**: Yes! Currently supported:
- ✅ **Render.com** (default, recommended)
- ✅ **Heroku** (similar to Render)
- ✅ **AWS Lambda** (serverless, experimental)
- ✅ **Local machine** (development)

To deploy elsewhere, modify `render.yaml` for your platform.

---

### Q9: How do I report bugs?

**A**:

```bash
# 1. Enable debug logging
export LOG_LEVEL=DEBUG

# 2. Reproduce the issue
# 3. Collect logs
cat logs/bot.log > bug_report.log

# 4. Go to GitHub Issues
# https://github.com/Sam-Cordahi/Sam_Job_Automator/issues

# 5. Create new issue with:
#    - Steps to reproduce
#    - Expected vs actual behavior
#    - Logs and error messages
#    - Your environment (OS, Python version, etc.)
```

---

### Q10: How do I contribute?

**A**: See `.github/CONTRIBUTING.md`

```bash
# 1. Fork repository
# 2. Create feature branch
git checkout -b feature/my-feature

# 3. Make changes & test
python -m pytest

# 4. Push to your fork
git push origin feature/my-feature

# 5. Create Pull Request on GitHub
# 6. Wait for review & merge
```

---

## Error Messages

### Error: "ModuleNotFoundError: No module named 'core.main_bot'"

**Cause**: Virtual environment not activated or dependencies not installed

**Fix**:
```bash
# 1. Activate virtual environment
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate     # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Try again
python run.py
```

---

### Error: "sqlite3.OperationalError: database is locked"

**Cause**: Multiple instances accessing SQLite simultaneously

**Fix**:
```bash
# Solution 1: Migrate to Supabase
# Set SUPABASE_URL and SUPABASE_KEY in .env

# Solution 2: Use single instance only
# Kill other instances and restart

# Solution 3: Increase SQLite timeout
# In core/db_client.py, change:
# sqlite_connection.timeout = 30  # Increase from 10
```

---

### Error: "TELEGRAM_BOT_TOKEN not found in environment"

**Cause**: .env file not loaded or not present

**Fix**:
```bash
# 1. Check .env exists
ls -la .env

# 2. Load .env before running
export $(cat .env | xargs)

# 3. Or use a .env loader
python -m dotenv run python run.py

# 4. Or ensure .env is set
echo $TELEGRAM_BOT_TOKEN  # Should show token
```

---

### Error: "No module named 'telegram'"

**Cause**: Dependencies not installed

**Fix**:
```bash
pip install -r requirements.txt
# Or specifically:
pip install python-telegram-bot
```

---

### Error: "ConnectionError: Failed to establish connection"

**Cause**: No internet or API server unreachable

**Fix**:
```bash
# 1. Check internet
ping 8.8.8.8

# 2. Check specific service
ping api.telegram.org  # Telegram
ping api.gemini.com     # Gemini API
ping supabase.com       # Supabase

# 3. Check firewall/proxy settings
# 4. If behind proxy, configure in .env
```

---

## Performance Issues

### Issue: Bot Responding Slowly

**Check**:
```bash
/performance  # Command response time

# If > 2 seconds:
# 1. Check CPU/Memory
/health

# 2. Reduce batch size
# MAX_LEADS_PER_CYCLE=10

# 3. Increase workers
# CONCURRENT_EMAIL_WORKERS=3
```

### Issue: High Latency to Render

**Check**:
```bash
# Test latency
time curl https://your-service.onrender.com/health

# If > 1 second:
# 1. Check Render logs
# 2. Upgrade Render plan
# 3. Use CDN
```

---

## Emergency Recovery

### Nuclear Option - Full Reset

```bash
# 1. Stop all processes
pkill -9 python

# 2. Clear database (WARNING: DELETES DATA)
rm chronos.db
rm chronos.db-wal
rm chronos.db-shm

# 3. Clear cache
rm -rf __pycache__
rm -rf .cache

# 4. Restart fresh
python run.py
```

### Rollback to Previous Version

```bash
# 1. Check git history
git log --oneline | head -10

# 2. Rollback to previous commit
git reset --hard <commit-hash>

# 3. Restart
python run.py
```

### Recovery from Corrupted Database

```bash
# 1. Check SQLite integrity
sqlite3 chronos.db "PRAGMA integrity_check;"

# 2. If corrupted, rebuild
sqlite3 chronos.db ".dump" > backup.sql
rm chronos.db
sqlite3 chronos.db < backup.sql

# 3. If Supabase primary is corrupted
# Set USE_SQLITE_ONLY=true in .env
# Operate in SQLite mode until Supabase recovers
```

---

## When All Else Fails

### Contact Support

- **GitHub**: [Issues](https://github.com/Sam-Cordahi/Sam_Job_Automator/issues)
- **Email**: See README.md for contact info
- **Logs**: Collect logs before reporting

### Debug Package

```bash
# Collect full diagnostics
python deployment_validator.py > diagnostics.txt
python -m pytest --tb=short > test_results.txt
cat logs/bot.log >> diagnostics.txt

# Send to support with:
# - diagnostics.txt
# - test_results.txt
# - Description of issue
# - Steps to reproduce
```

---

**Remember**: Most issues have a simple fix. Start with the Quick Diagnostics section above.

If stuck, check MONITORING_AND_OPERATIONS.md for additional troubleshooting commands.

Good luck! 🚀
