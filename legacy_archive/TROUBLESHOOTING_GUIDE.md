# 🔧 SAM JOB AUTOMATOR - TROUBLESHOOTING GUIDE

Solutions for common issues and error messages.

---

## 📋 QUICK DIAGNOSTIC

**When something goes wrong, first run:**

```bash
# Activate virtualenv
.\.venv\Scripts\Activate.ps1

# Check all imports work
python -c "from core.main_bot import AlphaOrchestrator; print('✅ All systems OK')"

# Check logs
Get-Content logs\sam.log -Tail 50
```

---

## ❌ INSTALLATION ISSUES

### "ModuleNotFoundError: No module named..."

**Problem:** Python can't find a package.

**Solutions (in order):**
1. Verify virtualenv is activated
   ```bash
   # Should see (.venv) in prompt:
   (.venv) C:\path\to\project>
   
   # If not, activate:
   .\.venv\Scripts\Activate.ps1
   ```

2. Reinstall requirements
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --force-reinstall
   ```

3. Check Python version ≥ 3.11
   ```bash
   python --version  # Must show 3.11+
   ```

---

### "Permission denied" or "Access denied"

**Problem:** Windows permissions issue.

**Solutions:**
1. Run PowerShell as Administrator
   - Right-click PowerShell → "Run as administrator"
   - Retry command

2. Check file permissions
   ```bash
   # Check if folder is readable
   dir c:\Users\samde\Sam_Job_Automator_Local
   
   # If not, add current user permissions
   icacls c:\Users\samde\Sam_Job_Automator_Local /grant:r "%USERNAME%":F
   ```

---

### "No such file or directory: '.env'"

**Problem:** Configuration file missing.

**Solution:**
```bash
# Copy example to real config
copy launch_config.example.env .env

# Then edit .env with your API keys
notepad .env
```

---

## ❌ RUNTIME ERRORS

### "Bot already running" / "duplicate instance detected"

**Problem:** Another bot instance is already running on this machine.

**Symptoms:**
```
🔴 DUPLICATE BOT DETECTED: Another instance is already running!
```

**Solutions:**
1. Find and kill existing bot process
   ```powershell
   # Find it
   Get-Process python | Where-Object {$_.Name -eq "python"}
   
   # Kill it
   Stop-Process -Id <PID> -Force
   ```

2. Delete lock file
   ```bash
   del .main_bot.lock
   ```

3. Retry
   ```bash
   python launch_sam.py
   ```

---

### "API Key not found" error

**Problem:** Requirement environment variable is missing.

**Symptoms:**
```
KeyError: 'SUPABASE_URL'
KeyError: 'TELEGRAM_BOT_TOKEN'
```

**Solutions:**
1. Check `.env` exists in project root
2. Verify key name matches exactly (case-sensitive)
3. Reload shell after updating .env
   ```bash
   # Deactivate and reactivate virtualenv
   deactivate
   .\.venv\Scripts\Activate.ps1
   ```

4. Verify .env format
   ```
   # Correct format:
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=xxxxxxxx
   
   # Wrong formats (will fail):
   SUPABASE_URL = https://...  # No spaces around =
   supabase_url=...             # Wrong case
   ```

---

### "Could not connect to Supabase"

**Problem:** Database connection failed.

**Symptoms:**
```
ERROR: Failed to connect to Supabase
aiohttp.ClientError: Cannot connect to host
```

**Solutions:**
1. Check internet connection
   ```bash
   ping google.com
   ```

2. Verify Supabase URL is correct
   - Should be: `https://xxxxx.supabase.co` (no trailing /)
   - Go to Supabase dashboard to confirm

3. Check API key is valid
   - Regenerate new key if needed
   - Test URL in browser: `https://xxxxx.supabase.co` should work

4. Try local-only mode (SQLite)
   ```bash
   # In .env:
   TEST_MODE=true
   
   # This uses local SQLite instead of Supabase
   ```

---

## ❌ EMAIL PROBLEMS

### "Email not sending" or "SMTP connection failed"

**Problem:** Email provider is unreachable or credentials wrong.

**Symptoms:**
```
SMTPAuthenticationError: 535 5.7.3 Authentication unsuccessful
SMTPServerDef: (-1, b'error': 'connection timeout')
```

**Solutions:**
1. Verify SMTP credentials in .env
   ```bash
   # Correct:
   BREVO_SMTP_LOGIN=your_email@brevo.com
   BREVO_SMTP_PASSWORD=your_brevo_app_password  # NOT account password
   
   # Wrong:
   BREVO_SMTP_PASSWORD=your_account_password  # This WON'T work
   ```

2. Test SMTP connection
   ```bash
   python -c "from core.smtp_engine import test_email_connection; test_email_connection()"
   ```

3. Check Brevo limits
   - Login to https://www.brevo.com
   - Dashboard → Campaign → Transactional
   - Verify you have credits left (300/day free)

4. Try Gmail fallback
   ```bash
   # In .env, add:
   GMAIL_SENDER_EMAIL=your.email@gmail.com
   
   # Follow Gmail API setup in CONFIGURATION.md
   ```

---

### "Email rate limited (429 error)"

**Problem:** Too many emails sent too quickly.

**Symptoms:**
```
HTTP 429: Too Many Requests
Brevo rate limit exceeded
```

**Solutions:**
1. Increase delay between emails
   ```bash
   # In .env:
   EMAIL_DELAY_MINUTES=5  # Wait 5 min between emails
   ```

2. Reduce parallel workers
   ```bash
   # In .env:
   MAX_PARALLEL_STRIKES=2  # Was 5, now 2
   ```

3. Check daily limits
   - Brevo free: 300/day
   - Time: 300 ÷ 16 hours = ~1 email every 3 minutes
   - If hitting limit, space emails out more

---

## ❌ SCRAPING PROBLEMS

### "Scraper returns 0 jobs"

**Problem:** No jobs found by web scrapers.

**Symptoms:**
```
⚠️ Vanguard Scrape failed: 0 leads acquired
```

**Causes & Fixes:**

1. **Website blocking**
   - Solution: Use proxies (see CONFIGURATION.md)

2. **CSS selectors outdated**
   - Solution: Auto-repair kicks in automatically
   - Check logs for repair attempts

3. **Website requires JavaScript**
   - Solution: This is normal, bot handles it
   - Check if site requires login

4. **Internet connection issue**
   ```bash
   ping linkedin.com
   ping indeed.com
   ```

5. **Test single scraper**
   ```bash
   python -c "
   from core.scrapers import scraper
   jobs = scraper.get_latest_jobs()
   print(f'Found: {len(jobs)} jobs')
   for j in jobs[:3]:
       print(f\"  - {j['company_name']}: {j['job_title']}\")
   "
   ```

---

## ❌ TELEGRAM ISSUES

### "/status command not working"

**Problem:** Bot isn't responding to Telegram messages.

**Symptoms:**
```
Bot doesn't reply to /status
Message sent but no response
```

**Solutions:**

1. Verify Telegram credentials
   ```bash
   # In .env:
   TELEGRAM_BOT_TOKEN=123456789:ABCDEFghijklmn
   TELEGRAM_CHAT_ID=987654321
   
   # Both required, check for typos
   ```

2. Restart bot
   ```bash
   # Stop bot (Ctrl+C)
   # Then:
   python launch_sam.py
   ```

3. Check if bot has permission to message you
   - In Telegram, send a message to your bot FIRST
   - Then restart bot

4. Check logs for errors
   ```bash
   Get-Content logs\sam.log | Select-String "Telegram"
   ```

---

### "109: Too many requests (Telegram)"

**Problem:** Rate-limited by Telegram API.

**Symptoms:**
```
ERROR 109: Too many requests to do operation
```

**Solution:**
- This is temporary, bot auto-recovers
- Wait a few minutes before sending more commands
- Reduce message frequency if recurring

---

## ❌ AI PROBLEMS

### "Gemini API Error" or "Groq API Error"

**Problem:** AI provider unreachable or quota exceeded.

**Symptoms:**
```
google.auth.exceptions.DefaultCredentialsError
ConfigurationError: Missing API key
```

**Solutions:**

1. Verify API key is set
   ```bash
   python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GEMINI_API_KEY'))"
   ```

2. Check key is in correct .env location
   - Must be: `C:\Users\samde\Sam_Job_Automator_Local\.env`
   - Reload shell after editing

3. Regenerate API key
   - Go to https://aistudio.google.com/app/apikeys
   - Delete old key
   - Create new key
   - Update .env

4. Try alternative AI provider
   ```bash
   # In .env, set:
   # GEMINI_API_KEY=  (leave blank)
   # GROQ_API_KEY=your_groq_key
   
   # Bot will use Groq instead
   ```

---

## ❌ DATABASE PROBLEMS

### "Duplicate application detected"

**Problem:** Bot thinks job was already applied to.

**Symptoms:**
```
⏭️ Skipping duplicate target: CompanyName
```

**Solutions:**

1. **False positive** (if it's NOT actually a duplicate):
   - Clear database in TEST_MODE:
     ```bash
     rm company_database.json
     rm tracker.json
     ```

2. **Real duplicate** (if it IS a duplicate):
   - This is CORRECT behavior
   - Bot is preventing duplicate applications
   - This is a FEATURE, not a bug

3. **Clear all history** (manual reset):
   ```bash
   # DELETE everything: (backup first!)
   rm *.json  # Delete all JSON databases
   rm logs/*.log  # Delete logs
   ```

---

### "Supabase quota exceeded"

**Problem:** Exceeded free tier limits.

**Symptoms:**
```
ERROR 413: Payload too large
ERROR 429: Too many requests
```

**Solutions:**

1. **Switch to local-only mode**
   ```bash
   # In .env:
   TEST_MODE=true
   # Uses SQLite, no cloud database
   ```

2. **Upgrade Supabase plan**
   - Go to https://supabase.com
   - Dashboard → Settings → Billing
   - Upgrade to paid tier

3. **Delete old data**
   - Login to Supabase dashboard
   - Delete old application records
   - This frees up space

---

## 🟡 WARNING MESSAGES

These aren't errors but worth noting:

### "Certificate verify failed" (Proxy warning)
```
SSL: CERTIFICATE_VERIFY_FAILED
```
- **Cause:** Using proxies, normal
- **Fix:** Nothing needed, expected behavior

### "UserWarning: Decompressing..." (Encoding warning)
```
UserWarning: Decompressing gzip-encoded response body...
```
- **Cause:** Compressed HTTP response
- **Fix:** Nothing needed, handled automatically

---

## 📊 CHECKING LOGS

**View latest errors:**
```bash
# Last 50 lines
Get-Content logs\sam.log -Tail 50

# Search for errors
Get-Content logs\sam.log | Select-String ERROR

# Search for warnings
Get-Content logs\sam.log | Select-String WARNING

# Real-time monitoring (newer versions)
Get-Content -Path logs\sam.log -Wait
```

---

## 🆘 WHEN ALL ELSE FAILS

1. **Enable DEBUG logging**
   ```bash
   # In .env:
   DIVINE_LOG_LEVEL=DEBUG
   
   # Run bot and check logs for more details
   python launch_sam.py
   Get-Content logs\sam.log | Select-String DEBUG
   ```

2. **Clear cache and restart**
   ```bash
   # Delete all cache
   Remove-Item -Recurse cache/
   Remove-Item -Recurse logs/
   
   # Restart bot
   python launch_sam.py
   ```

3. **Nuclear option: Full reset**
   ```bash
   # BACKUP .env FIRST!
   copy .env .env.backup
   
   # Delete everything except core + .env
   Remove-Item -Recurse .venv
   Remove-Item -Recurse logs/
   Remove-Item -Recurse cache/
   
   # Start from SETUP_GUIDE Step 2
   ```

---

## 📞 GETTING HELP

When posting issue on GitHub, include:

1. **Full error message** (copy-paste traceback)
2. **Python version**: `python --version`
3. **OS**: Windows/macOS/Linux
4. **Steps to reproduce**:
   - What command did you run?
   - What happened?
5. **Last 20 lines from logs**
   ```bash
   Get-Content logs\sam.log -Tail 20 | Out-String
   ```

Example:
```
**Environment:**
- Python 3.11.9
- Windows 11
- Bot version: main_bot.py v2.5

**Error:**
ModuleNotFoundError: No module named 'telebot'

**Steps:**
1. Activated virtualenv
2. Ran `python launch_sam.py`
3. Got error above

**Logs:**
[paste last 20 lines]
```

---

**Most issues self-resolve in TEST_MODE.** If stuck, always try:
```bash
# In .env
TEST_MODE=true

# Then rerun
python launch_sam.py
```
