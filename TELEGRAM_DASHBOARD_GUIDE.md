╔═══════════════════════════════════════════════════════════════════════════════╗
║         PROJECT CHRONOS - TELEGRAM DASHBOARD QUICK REFERENCE                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝

🤖 BOT NAME: @SamChronosJobBot
📍 LOCATION: Telegram → Search → @SamChronosJobBot
🔗 START: Send /start to begin

═══════════════════════════════════════════════════════════════════════════════
📊 DASHBOARD COMMANDS & BUTTONS
═══════════════════════════════════════════════════════════════════════════════

COMMAND         BUTTON         WHAT IT DOES
═════════════════════════════════════════════════════════════════════════════════
/start          [HOME]         Show main dashboard menu

/stats          [📊 STATS]     Show real-time metrics:
                               ✅ Total Applications Sent
                               ✅ Total Leads Scouted
                               ✅ Queue Depth (pending leads)
                               ✅ Last System Pulse (8 min ago?)
                               ✅ Active Leader Node ID
                               ✅ Uptime (hours)

/queue          [🎯 QUEUE]     Show 5 next leads waiting:
                               • Job Title
                               • Company Name
                               • Location
                               • Priority Score
                               • Source Platform

/scrape_now     [🌍 SCRAPE]    TRIGGER ALL SCRAPERS MANUALLY
                               ⏱️  Wait 2-3 minutes
                               ⏳ Then check /queue for new leads

/force_strike   [⚡ FORCE]     SEND IMMEDIATE APPLICATION
                               • Takes top lead from queue
                               • Generates personalized email
                               • Sends to company
                               • Updates applications table
                               ⚠️  Use sparingly (rate limits)

/settings       [🔧 CONFIG]    Adjust bot parameters:
                               • MIN_MATCH_SCORE (default: 55)
                               • Scraper interval (minutes)
                               • Email frequency
                               • AI model selection

/health         [💪 HEALTH]    System health check:
                               ✅ Service Status (Live/Down)
                               ✅ Database Connection
                               ✅ Supabase Reachable
                               ✅ Last Pulse Time
                               ✅ Active Leader
                               ✅ Render Uptime

/logs           [📈 LOGS]      Show last 20 system log entries:
                               ✅ [SCRAPER] Found X jobs
                               ✅ [GEMINI] Analysis complete
                               ✅ [EMAIL] Sent to company
                               ⚠️  [WARN] Rate limited (recovers)
                               ❌ [ERROR] Connection failed

/kill           [🛑 KILL]      EMERGENCY STOP (pauses all scraping)
                               ⚠️  Use only if bot misbehaves
                               Recovery: Redeploy on Render

/resume         [▶️  RESUME]   Resume bot after /kill

═══════════════════════════════════════════════════════════════════════════════
🎯 MONITORING CHECKLIST (Check Daily)
═══════════════════════════════════════════════════════════════════════════════

✅ Every Morning:
  [ ] Send /start → Dashboard appears
  [ ] Send /health → All systems green
  [ ] Send /stats → Numbers look reasonable
  [ ] Send /queue → At least 10-20 leads waiting
  [ ] Check: "Last Pulse" shows < 10 minutes ago

✅ Mid-Day:
  [ ] Send /stats → Application count increasing
  [ ] Send /logs → No repeated errors
  [ ] Send /queue → Queue being consumed (old leads disappearing)
  [ ] Check: Active leader is stable (same node ID)

✅ Evening:
  [ ] Send /stats → Total applications for day > 5
  [ ] Send /logs → Tail shows normal activity
  [ ] Send /health → Uptime holding steady
  [ ] Note: Queue may be lower (gets refilled next cycle)

═══════════════════════════════════════════════════════════════════════════════
🚨 TROUBLESHOOTING VIA TELEGRAM
═══════════════════════════════════════════════════════════════════════════════

PROBLEM: Bot doesn't respond to /start
  ❌ Cause 1: Bot crashed on Render
     👉 Solution: Go to Render dashboard → sam-bot-v2 → Redeploy
     
  ❌ Cause 2: Bot token invalid/changed
     👉 Solution: Check Telegram bot token in Render env vars
     
  ❌ Cause 3: Service is in free tier sleep
     👉 Solution: The heartbeat should keep it awake

PROBLEM: /stats shows "Queue: 0" (empty)
  ✅ Normal if: You just started (scrapers run every 30-60 min)
  👉 Solution: Click [🌍 SCRAPE] to manually trigger
     Wait 2-3 minutes, then check /queue again

PROBLEM: /logs shows repeated "[ERROR]" messages
  ❌ If ERROR = "API rate limited"
     👉 Solution: Normal - system backs off for 60 sec automatically
     
  ❌ If ERROR = "Supabase connection failed"
     👉 Check: SUPABASE_URL and SUPABASE_KEY in Render env
     
  ❌ If ERROR = "[GEMINI] 403 Access Denied"
     👉 Check: GEMINI_API_KEY has quota and is active
     👉 Check: Groq fallback (should activate automatically)

PROBLEM: /health shows "Database: Down"
  ❌ Supabase project paused or no credit
     👉 Solution: Log into Supabase dashboard and check Project Status
     👉 Verify: SUPABASE_URL is correct (should be eu-central-1)

PROBLEM: "Last Pulse" is > 10 minutes old
  ❌ Bot may have crashed
     👉 Solution: Redeploy on Render (Settings → Deploy)
     👉 After 2 min: Send /start again
     👉 Should show updated timestamp

═══════════════════════════════════════════════════════════════════════════════
📈 EXPECTED BEHAVIOR (What's Normal?)
═══════════════════════════════════════════════════════════════════════════════

STAT                    NORMAL RANGE           FREQUENCY
═════════════════════════════════════════════════════════════════════════════════
Applications Sent       +5 to +20/day          Continuous
Leads Scouted           +50 to +200/day        Every 30-60 min
Queue Depth             20-100 leads           Refills every 30 min
Last Pulse              < 10 minutes old       Every 8 min (heartbeat)
Active Leader Node      Stable (same ID)       Changes if node dies
Uptime                  Continuous increase     24/7

LOG ENTRIES             RATE                   WHAT'S OK?
═════════════════════════════════════════════════════════════════════════════════
[SCRAPER] Found X jobs  Every 30-60 min        ✅ Found > 0
[GEMINI] Analysis OK    Every 2-5 min          ✅ Mostly OK
[EMAIL] Sent            Every 1-2 min          ✅ Varies
[WARN] Rate limited     Occasional             ✅ System handles
[ERROR] ...             Rare (<1/hour)         ⚠️ If frequent, check env

═══════════════════════════════════════════════════════════════════════════════
🔧 MANUAL OPERATIONS VIA TELEGRAM
═══════════════════════════════════════════════════════════════════════════════

TO FORCE A SCRAPE RUN:
  1. Send: /scrape_now
  2. Bot responds: "Triggering all scrapers..."
  3. Wait: 2-3 minutes (they run in background)
  4. Send: /queue
  5. See: New leads appear in list

TO SEND AN IMMEDIATE APPLICATION:
  1. Send: /force_strike
  2. Bot finds top lead from queue
  3. Bot generates personalized email
  4. Email sent to company
  5. Lead marked as "SENT" in database
  ⚠️  Rate limit: Use sparingly (max 3-4 per hour)

TO CHECK IF BOT IS ALIVE:
  1. Send: /health
  2. Check: All green checkmarks
  3. If any red: Look at that subsystem
  4. If all down: Render service crashed → Redeploy

═══════════════════════════════════════════════════════════════════════════════
💡 TIPS & BEST PRACTICES
═══════════════════════════════════════════════════════════════════════════════

✅ DO:
  • Check /stats every morning
  • Review /logs daily for patterns
  • Use /queue to see upcoming leads
  • Run /health weekly
  • Keep TELEGRAM_CHAT_ID updated

❌ DON'T:
  • Use /force_strike repeatedly (causes rate limits)
  • Change settings during active scraping
  • Redeploy frequently (let it run)
  • Ignore error messages in /logs
  • Close Telegram (bot uses polling)

⚙️ PERFORMANCE TIPS:
  • Queue typically grows to 80-100 leads per cycle
  • Scraping runs every 30-60 minutes (configurable)
  • Applications are sent in batches every 5-10 minutes
  • AI analysis takes 2-5 sec per job
  • Emails sent at rate 1 per minute (respects rate limits)

═══════════════════════════════════════════════════════════════════════════════
📱 SETTING UP TELEGRAM NOTIFICATIONS
═══════════════════════════════════════════════════════════════════════════════

⚠️  IMPORTANT: By default, bot ONLY sends messages you REQUEST
   (via /start, /stats, /logs, etc.)

TO GET AUTOMATIC ALERTS:
  1. Go to Render → sam-bot-v2 → Environment
  2. Add: TELEGRAM_ALERTS_ENABLED = true
  3. Bot will now send:
     • Daily summary (9 AM UTC)
     • Error alerts (when [ERROR] occurs)
     • Success alerts (50 apps sent, etc.)
     • Warning alerts (rate limited, etc.)

═══════════════════════════════════════════════════════════════════════════════
