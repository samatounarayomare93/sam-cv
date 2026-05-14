╔═══════════════════════════════════════════════════════════════════════════════╗
║         RENDER ENVIRONMENT VARIABLES - CONFIGURATION GUIDE                     ║
║                  Add these to: Render → sam-bot-v2 → Settings                  ║
╚═══════════════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════════
🔑 REQUIRED VARIABLES (MUST SET - Bot won't run without these)
═══════════════════════════════════════════════════════════════════════════════

1️⃣  GEMINI_API_KEY
    Purpose:    Primary AI engine for job analysis and email generation
    Get from:   https://aistudio.google.com/apikey
    Format:     Long alphanumeric string (50+ chars)
    Example:    AIzaSyDx... (redacted for security)
    Test:       Send /start to Telegram, should respond within 5 sec

2️⃣  GROQ_API_KEY
    Purpose:    Fallback AI engine when Gemini fails
    Get from:   https://console.groq.com/keys
    Format:     Long alphanumeric string (40+ chars)
    Example:    gsk_... (redacted for security)
    Test:       Logs should show "[GROQ FALLBACK]" occasionally

3️⃣  TELEGRAM_BOT_TOKEN
    Purpose:    Allows Telegram messages to reach the bot
    Get from:   Telegram → @BotFather → /mybots → Your Bot → API Token
    Format:     123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
    Test:       /start command should work immediately

4️⃣  TELEGRAM_CHAT_ID
    Purpose:    Your personal ID to receive bot messages
    Get from:   Send any message to @userinfobot, copy "id" field
    Format:     9-11 digit number (e.g., 123456789)
    Test:       /stats should return numbers to you

5️⃣  SUPABASE_URL
    Purpose:    Connect to database
    Value:      https://lckiazbadymeikmxesit.supabase.co
    ⚠️  DON'T CHANGE - Use exact value above

6️⃣  SUPABASE_KEY
    Purpose:    Authenticate with Supabase (full access)
    Get from:   Supabase Dashboard → Settings → API → service_role key
    Format:     Long base64 string (150+ chars)
    ⚠️  SECURITY: This is like a master password - keep secret!
    Test:       Logs should show "[SUPABASE] Connected"

7️⃣  GMAIL_ADDRESS
    Purpose:    Gmail account for email authentication
    Value:      Your full Gmail address (e.g., user@gmail.com)
    Test:       Logs should show "[GMAIL] Authenticated"

8️⃣  GMAIL_APP_PASSWORD
    Purpose:    App-specific password for Gmail
    Get from:   Gmail → Account → Security → App passwords (generate new)
    Format:     16-character code (with spaces) - EXACTLY as shown
    Example:    abcd efgh ijkl mnop
    ⚠️  This is NOT your regular Gmail password
    Test:       Logs should show "[SMTP] Connected"

═══════════════════════════════════════════════════════════════════════════════
⚪ OPTIONAL VARIABLES (Enhance functionality, bot works without them)
═══════════════════════════════════════════════════════════════════════════════

9️⃣  DEEPSEEK_API_KEY
    Purpose:    Third-tier AI fallback (after Gemini & Groq fail)
    Get from:   https://platform.deepseek.com/api_keys
    Optional:   If omitted, falls back to static responses
    Test:       Should not see in normal logs (only if Gemini + Groq both fail)

🔟 MAILJET_API_KEY
    Purpose:    Alternative email service
    Get from:   Mailjet → Account → API Key & Private Key
    Optional:   If omitted, uses Resend or Gmail SMTP
    Format:     API_KEY:SECRET_KEY (separated by colon)

1️⃣1️⃣ RESEND_API_KEY
    Purpose:    Another email service option
    Get from:   Resend → API Keys → Copy "Re_" key
    Optional:   If omitted, uses Gmail or Mailjet
    Test:       Logs show "[RESEND] Configured"

1️⃣2️⃣ BREVO_API_KEY
    Purpose:    Yet another email fallback
    Get from:   Brevo (formerly Sendinblue) → Settings → API Keys
    Optional:   If omitted, uses other email services
    Test:       Logs show "[BREVO] Ready"

═══════════════════════════════════════════════════════════════════════════════
📝 STEP-BY-STEP: HOW TO ADD VARIABLES IN RENDER
═══════════════════════════════════════════════════════════════════════════════

1. Go to: https://dashboard.render.com
2. Click: sam-bot-v2 (your service)
3. Go to: Settings tab (top right)
4. Scroll to: "Environment Variables" section
5. Click: "Add Environment Variable" button
6. For EACH variable:
   • Key field: Type the variable name (e.g., GEMINI_API_KEY)
   • Value field: Paste the value (e.g., AIzaSy...)
   • Click: "Save" button
   ⏳ Wait 30-60 seconds for auto-redeploy

7. After all variables added:
   • Go to: "Deployments" tab
   • Latest deployment should show "Live" (green)
   • Check: Bot responds to /start

═══════════════════════════════════════════════════════════════════════════════
✅ VERIFICATION CHECKLIST
═══════════════════════════════════════════════════════════════════════════════

After adding all required variables, verify:

[ ] 1. All 8 required variables shown in Render (Settings → Environment)
[ ] 2. No typos in variable NAMES (case-sensitive)
[ ] 3. Values copied exactly (no extra spaces or quotes)
[ ] 4. Latest deployment is "Live" (green status)
[ ] 5. Bot responds to /start command in Telegram
[ ] 6. /stats shows reasonable numbers
[ ] 7. /logs shows no repeated "[ERROR]" messages
[ ] 8. System shows "SUPABASE Connected" in logs

═══════════════════════════════════════════════════════════════════════════════
🔐 SECURITY BEST PRACTICES
═══════════════════════════════════════════════════════════════════════════════

✅ DO:
  • Regenerate GMAIL_APP_PASSWORD every 3 months
  • Rotate SUPABASE_KEY if compromised
  • Use strong passwords for service accounts (Gmail, Groq, etc.)
  • Review Render logs weekly for suspicious activity
  • Keep email services (Gmail, Mailjet) secure

❌ DON'T:
  • Share SUPABASE_KEY with anyone
  • Commit .env file to GitHub
  • Paste keys into public forums
  • Use personal Gmail password (use app password)
  • Leave old keys in Render after rotation

═══════════════════════════════════════════════════════════════════════════════
🆘 TROUBLESHOOTING ENVIRONMENT VARIABLES
═══════════════════════════════════════════════════════════════════════════════

PROBLEM: Bot doesn't start after adding variables
  ❌ Check:
     • Render "Deployments" shows error? → Click deploy → View logs
     • Any variable spelled wrong? → Compare with variable names above
     • Any quotes or extra spaces? → Paste exactly as provided
  ✅ Solution:
     • Remove suspicious variables one by one
     • Test /start after each removal
     • Identify which variable causes issue

PROBLEM: "Authentication failed" errors in logs
  ❌ Check:
     • GMAIL_APP_PASSWORD: Did you use app password (not regular password)?
     • SUPABASE_KEY: Is it service_role (not anon)?
     • GEMINI_API_KEY: Does it still have quota?
  ✅ Solution:
     • Regenerate the specific key
     • Update in Render
     • Wait 1 min for redeploy
     • Test again

PROBLEM: /stats shows "Database: Down"
  ❌ Check:
     • SUPABASE_URL: Should be https://lckiazbadymeikmxesit.supabase.co
     • SUPABASE_KEY: Should start with "eyJ..." (base64)
  ✅ Solution:
     • Copy exact value from Supabase Settings → API → service_role key
     • Paste into Render (no manual editing)
     • Redeploy

═══════════════════════════════════════════════════════════════════════════════
🔗 EXTERNAL RESOURCES
═══════════════════════════════════════════════════════════════════════════════

Gmail Setup:
  https://support.google.com/accounts/answer/185833 (App Passwords)

Groq API:
  https://console.groq.com/keys

Gemini API:
  https://aistudio.google.com/apikey

Supabase:
  https://supabase.com/dashboard/project/lckiazbadymeikmxesit/settings/api

Telegram Bot:
  https://core.telegram.org/bots#botfather

Render Dashboard:
  https://dashboard.render.com

═══════════════════════════════════════════════════════════════════════════════
