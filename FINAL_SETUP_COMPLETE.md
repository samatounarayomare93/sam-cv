╔═══════════════════════════════════════════════════════════════════════════════╗
║                   PROJECT CHRONOS - FINAL SETUP GUIDE                          ║
║                          May 14, 2026                                           ║
╚═══════════════════════════════════════════════════════════════════════════════╝

🎯 OBJECTIVE: Complete the 3 remaining setup tasks to make Project Chronos 100% operational

═══════════════════════════════════════════════════════════════════════════════
📋 TASK 1: RUN SQL SCRIPT IN SUPABASE
═══════════════════════════════════════════════════════════════════════════════

⏱️  Time Required: 2-3 minutes
✅ Expected Result: All 8 database tables created and seeded

STEP 1: Open Supabase Project
  • URL: https://supabase.com/dashboard/project/lckiazbadymeikmxesit
  • Project ID: lckiazbadymeikmxesit
  • Region: eu-central-1 (Ireland)

STEP 2: Navigate to SQL Editor
  • Click "SQL Editor" in left sidebar
  • Click "New Query" or "+"
  • Click "Create new SQL file"

STEP 3: Copy & Paste SQL Script
  • File location: SUPABASE_RUN_THIS.sql (in this workspace)
  • Select all text in that file (Ctrl+A)
  • Copy it (Ctrl+C)
  • Paste into Supabase SQL Editor (Ctrl+V)

STEP 4: Execute
  • Click blue "Run" button (top right)
  • Wait for "Success" notification (usually <10 seconds)
  • See green checkmark ✅

STEP 5: Verify
  • At the bottom, you'll see a table showing:
    - system_logs: COUNT
    - vip_tracking: COUNT
    - applications: COUNT
    - leads: COUNT
    - system_settings: COUNT
    - nodes: COUNT
    - system_state: COUNT
  • If all show numbers (even 0), you're done! ✅

COMMON ISSUES:
  ❌ "Permission denied": Use service_role key (should be automatic)
  ❌ "Table already exists": That's OK - script uses "IF NOT EXISTS"
  ❌ "Timeout": Run the script again

═══════════════════════════════════════════════════════════════════════════════
🔧 TASK 2: VERIFY RENDER ENVIRONMENT VARIABLES
═══════════════════════════════════════════════════════════════════════════════

⏱️  Time Required: 1-2 minutes
✅ Expected Result: All secrets properly configured in Render

STEP 1: Open Render Dashboard
  • URL: https://dashboard.render.com
  • Find service: "sam-bot-v2" (or similar)
  • Click on it

STEP 2: Check Environment Variables
  Go to Settings → Environment → Environment Variables section
  
  REQUIRED VARIABLES (must all exist):
  ✅ GEMINI_API_KEY        → Set to your Google Generative AI key
  ✅ GROQ_API_KEY          → Set to your Groq API key (for fallback)
  ✅ TELEGRAM_BOT_TOKEN    → Set to your Telegram bot token
  ✅ TELEGRAM_CHAT_ID      → Set to your personal Telegram chat ID
  ✅ SUPABASE_URL          → https://lckiazbadymeikmxesit.supabase.co
  ✅ SUPABASE_KEY          → Your Supabase service_role key (full access)
  ✅ GMAIL_ADDRESS         → Your Gmail address
  ✅ GMAIL_APP_PASSWORD    → Your Gmail app-specific password (16 chars)

OPTIONAL (but recommended):
  ⚪ DEEPSEEK_API_KEY       → For additional AI fallback
  ⚪ MAILJET_API_KEY        → For email delivery
  ⚪ RESEND_API_KEY         → For Resend email service
  ⚪ BREVO_API_KEY          → For Brevo email service

STEP 3: If Any Are Missing
  • Copy the value from local .env file
  • Add it to Render → Environment Variables
  • Click "Save" (it auto-redeploys)

STEP 4: Verify Deployment
  • Go to Deployments tab
  • Latest deployment should show "Live"
  • Status: Green checkmark ✅

COMMON ISSUES:
  ❌ Bot crashes after env update: Wait 1 min for Render to redeploy
  ❌ API key rejected: Copy exactly (no extra spaces)
  ❌ Keys shown as "redacted": That's normal - Render hides them

═══════════════════════════════════════════════════════════════════════════════
📊 TASK 3: MONITOR BOT VIA TELEGRAM DASHBOARD
═══════════════════════════════════════════════════════════════════════════════

⏱️  Time Required: 1 minute
✅ Expected Result: Bot responds to /start command with interactive dashboard

STEP 1: Send /start to Bot
  • Open Telegram
  • Find: @SamChronosJobBot (or your bot name)
  • Send: /start
  • You should get a dashboard with interactive buttons

STEP 2: Main Dashboard Commands
  Button                 Action
  ═════════════════════════════════════════════════════════════
  📊 STATS               Show real-time statistics (applications sent, leads scouted)
  🎯 QUEUE               Show pending leads in queue (title, company, score)
  🌍 SCRAPE NOW          Manually trigger all scrapers (⏱️ 2-3 min)
  ⚡ FORCE STRIKE        Send immediate application to top lead
  🔧 SETTINGS            Configure bot parameters
  📈 HEALTH              Check system health (uptime, last pulse, leader)
  💾 LOGS                View live system logs (tail -f)

STEP 3: Monitor Stats
  ✅ Check these numbers regularly:
    • Applications Sent: Should increase over time
    • Leads Scouted: Should grow with scrapers
    • Queue Depth: Number of pending leads
    • Last Pulse: Should update every 8 minutes
    • Active Leader: Should show node ID (e.g., "9F977915")

STEP 4: Review Logs
  • /logs command shows last 20 system log entries
  • Look for:
    ✅ "[GEMINI] Response successful"
    ✅ "[SCRAPER-DALEEL] Found X jobs"
    ✅ "[EMAIL] Sent to X@company.com"
    ❌ "[ERROR] Failed to..."
    ⚠️  "[WARN] Rate limited"

STEP 5: Manual Scrape Test
  • Click "🌍 SCRAPE NOW"
  • Wait 2-3 minutes
  • Check Queue again
  • New leads should appear

COMMON ISSUES:
  ❌ Bot doesn't respond: 
    - Check Telegram bot token in Render env
    - Bot may be down (check Render Deployments)
  ❌ Queue empty: Run "SCRAPE NOW" manually
  ❌ Logs show "[ERROR]": Check specific error message, usually temporary
  ⚠️  Rate limited: System backs off automatically, try again in 5 min

═══════════════════════════════════════════════════════════════════════════════
✅ FINAL VERIFICATION CHECKLIST
═══════════════════════════════════════════════════════════════════════════════

After completing all 3 tasks, verify:

  [ ] 1. Supabase SQL script ran successfully (all tables exist)
  [ ] 2. Render environment variables are set (service is Live)
  [ ] 3. Telegram bot responds to /start
  [ ] 4. Dashboard shows real data (stats, queue, logs)
  [ ] 5. "SCRAPE NOW" can be triggered and returns results
  [ ] 6. No error messages in logs
  [ ] 7. System shows active leader node
  [ ] 8. Last Pulse updates every 8 minutes

═══════════════════════════════════════════════════════════════════════════════
🚀 STATUS: READY TO DEPLOY
═══════════════════════════════════════════════════════════════════════════════

Once all checks pass:
  ✅ Project Chronos is 100% operational
  ✅ Bot runs 24/7 on Render
  ✅ Scrapers collect leads every cycle
  ✅ AI engines process applications
  ✅ Email system sends outreach
  ✅ Dashboard monitors everything

🎉 YOU'RE DONE! The bot is now LIVE and OPERATIONAL.

═══════════════════════════════════════════════════════════════════════════════
📚 REFERENCE: SUPABASE PROJECT INFO
═══════════════════════════════════════════════════════════════════════════════

Project ID:     lckiazbadymeikmxesit
Region:         eu-central-1 (Ireland)
URL:            https://lckiazbadymeikmxesit.supabase.co
API URL:        https://lckiazbadymeikmxesit.supabase.co/rest/v1
Tables Created: 8 (system_logs, vip_tracking, applications, leads, etc.)
RLS Enabled:    Yes (all policies set to service_role)

═══════════════════════════════════════════════════════════════════════════════
📚 REFERENCE: RENDER SERVICE INFO
═══════════════════════════════════════════════════════════════════════════════

Service:        sam-bot-v2
URL:            https://sam-bot-v2.onrender.com
Runtime:        Python 3.11.0
Uptime:         24/7 (free tier with heartbeat)
Deployment:     Automatic on git push
Heartbeat:      Every 8 minutes to keep service warm

═══════════════════════════════════════════════════════════════════════════════
📚 REFERENCE: TELEGRAM BOT INFO
═══════════════════════════════════════════════════════════════════════════════

Bot Name:       @SamChronosJobBot (or your bot name)
Dashboard:      Interactive Telegram menu
Polling:        Every message gets real-time response
24/7 Uptime:    Maintained via Render heartbeat + Python event loop

═══════════════════════════════════════════════════════════════════════════════
