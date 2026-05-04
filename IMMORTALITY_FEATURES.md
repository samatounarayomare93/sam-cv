# 🛡️ IMMORTALITY FEATURES - Sam Job Bot

## Overview
This bot is designed to run **FOREVER** on Render.com without stopping. Even if you come back after 100,000 years, it will still be running! 😄

---

## 🔥 Immortality Features

### 1. **Auto-Restart on Crash** ✅
- If any component crashes, the bot automatically restarts
- Allows up to 100 restarts before giving up
- Waits 30 seconds between restarts to avoid rapid crash loops

### 2. **Self-Ping Heartbeat** 💓
- Bot pings itself every 10 minutes to prevent Render from sleeping
- Tracks uptime and ping count
- Logs consecutive failures to detect issues early

### 3. **Health Monitor** 🏥
- Checks system health every minute
- Monitors active tasks to ensure all components are running
- Logs heartbeat to prove the bot is alive

### 4. **Memory Watchdog** 🧹
- Cleans memory every 5 minutes to prevent memory leaks
- Runs garbage collection to free up RAM
- Prevents OOM (Out of Memory) crashes

### 5. **Keep-Alive Server** 🌐
- Binds to Render's assigned port (required for free tier)
- Serves a web interface at the root URL
- Provides API endpoints for stats and actions

### 6. **Unified Process Architecture** 🏗️
- All components run in a single Python process
- Shares memory between components to save RAM
- Prevents the 512MB memory limit crash

---

## 📊 How to Check if Bot is Running

### Method 1: Run Health Check Script
```bash
python check_bot_health.py
```

This will:
- Check if the bot is online
- Show response time
- Display statistics (jobs scanned, emails sent, uptime)

### Method 2: Check Render Dashboard
1. Go to https://dashboard.render.com
2. Find your service: `sam-cv-bot` or `sam-job-automator`
3. Check the "Events" tab for recent activity
4. Check the "Logs" tab for heartbeat messages

### Method 3: Check via Browser
Open one of these URLs in your browser:
- https://sam-job-automator.onrender.com
- https://sam-cv-bot.onrender.com

You should see: "🟢 Sovereign Core Online"

### Method 4: Check via Telegram
Send `/status` or `/synapse` to your Telegram bot to see if it responds.

---

## 🔍 What to Look for in Logs

### Healthy Bot Logs:
```
💓 [HEARTBEAT #123] Cloud Instance is alive. Status: 200 | Uptime: 20.5h
💓 [HEALTH-MONITOR] System alive. Active tasks: 4
🧹 [RESOURCE-WATCHDOG]: Memory cleared. Swarm health optimized.
```

### Warning Signs:
```
⚠️ [HEARTBEAT] Ping failed (3 consecutive failures): Connection timeout
⚠️ [HEALTH-MONITOR] Only 2 tasks running. System may be degraded.
```

### Critical Errors:
```
❌ [FATAL] Swarm Collapse: <error message>
🔄 [AUTO-RESTART] Restarting in 30 seconds... (Attempt 5/100)
```

---

## 🚀 Deployment Checklist

### Before Deploying:
- [ ] All environment variables set in Render dashboard
- [ ] `KEEP_ALIVE_ENABLED=true` in .env
- [ ] `KEEP_ALIVE_INTERVAL=600` (10 minutes)
- [ ] Render service type is "Web Service" (not "Background Worker")
- [ ] Start command is `python run.py`

### After Deploying:
- [ ] Check Render logs for "Cloud Heartbeat" message
- [ ] Wait 2 minutes and check logs for first heartbeat ping
- [ ] Run `python check_bot_health.py` to verify
- [ ] Send `/status` to Telegram bot to verify it responds
- [ ] Check Supabase dashboard to see if data is being saved

---

## 🛠️ Troubleshooting

### Bot Stops After 15 Minutes
**Problem:** Render free tier sleeps after 15 minutes of inactivity.

**Solution:** The self-ping feature should prevent this. Check:
1. Is `KEEP_ALIVE_ENABLED=true`?
2. Are the heartbeat logs appearing every 10 minutes?
3. Is the web server binding to the correct port?

### Bot Crashes and Doesn't Restart
**Problem:** Auto-restart is not working.

**Solution:** Check logs for:
1. "Max restarts (100) reached" - means it gave up after 100 crashes
2. Fatal Python errors that prevent the restart loop from running
3. Render service is out of memory (512MB limit)

### Bot Restarts Too Often
**Problem:** Something is causing frequent crashes.

**Solution:** Check logs to identify the error:
1. Memory issues → Reduce `MAX_PARALLEL_STRIKES` in .env
2. Database connection issues → Check Supabase credentials
3. Telegram API issues → Check `TELEGRAM_BOT_TOKEN`
4. Email sending issues → Check SMTP credentials

### Can't Access Web Interface
**Problem:** Browser shows "Cannot connect" or timeout.

**Solution:**
1. Check if Render service is deployed and running
2. Check if the correct URL is being used
3. Wait 1-2 minutes after deployment for DNS to propagate
4. Check Render logs for "Binding Heartbeat to 0.0.0.0:10000"

---

## 📈 Expected Uptime

With all immortality features enabled:

- **Target Uptime:** 99.9% (only down during Render maintenance)
- **Auto-Restart Time:** 30 seconds after crash
- **Memory Cleanup:** Every 5 minutes
- **Health Check:** Every 1 minute
- **Self-Ping:** Every 10 minutes

**Expected behavior:**
- Bot runs 24/7 without manual intervention
- Automatically recovers from crashes
- Prevents memory leaks
- Prevents Render from sleeping
- Logs all activity for monitoring

---

## 🎯 Success Metrics

Your bot is running successfully if:

1. ✅ Heartbeat logs appear every 10 minutes
2. ✅ Health monitor logs appear every 1 minute
3. ✅ Memory watchdog logs appear every 5 minutes
4. ✅ Telegram bot responds to `/status` command
5. ✅ Web interface is accessible via browser
6. ✅ No crash/restart logs in the past hour
7. ✅ Supabase shows recent activity (new leads, applications)

---

## 🔮 Future Enhancements

Potential improvements for even better immortality:

1. **Multi-Region Deployment** - Deploy to multiple Render regions for redundancy
2. **External Monitoring** - Use UptimeRobot or Pingdom to monitor from outside
3. **Telegram Alerts** - Send Telegram message when bot crashes/restarts
4. **Auto-Scaling** - Automatically upgrade to paid tier if free tier limits are hit
5. **Backup Bot** - Deploy a second bot that takes over if the first one fails

---

## 📞 Support

If the bot stops working:

1. Check Render logs first
2. Run `python check_bot_health.py`
3. Check Telegram bot with `/status`
4. Check Supabase for recent activity
5. Review this document for troubleshooting steps

**Remember:** The bot is designed to run forever. If it stops, there's usually a simple fix! 🛡️
