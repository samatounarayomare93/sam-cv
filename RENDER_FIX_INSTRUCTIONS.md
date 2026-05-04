# 🔧 URGENT FIX: Add Gmail Credentials to Render

## THE PROBLEM
Your bot on Render is using Brevo instead of Gmail because Gmail credentials are MISSING on Render.

## THE SOLUTION (2 minutes)

### Option 1: Render Dashboard (EASIEST)
1. Go to: https://dashboard.render.com
2. Click on your service: **sam-job-automator** (or sam-cv-bot)
3. Click **"Environment"** tab (left sidebar)
4. Click **"Add Environment Variable"** button
5. Add these TWO variables:

```
Key: GMAIL_SMTP_USER
Value: samsalameh.cv@gmail.com
```

```
Key: GMAIL_APP_PASSWORD
Value: oimuanudzzngklnf
```

6. Click **"Save Changes"**
7. Render will automatically redeploy (wait 2-3 minutes)

### Option 2: Render CLI (FASTER)
Run this command in your terminal:

```bash
render env set GMAIL_SMTP_USER=samsalameh.cv@gmail.com GMAIL_APP_PASSWORD=oimuanudzzngklnf --service=sam-job-automator
```

---

## VERIFY IT WORKED

After Render redeploys, check the logs. You should see:

```
✅ [GMAIL-CHECK] User: ✅ SET (samsalameh... if set)
✅ [GMAIL-CHECK] Pass: ✅ SET (16 chars)
📧 [GMAIL-SMTP] ⭐ PRIORITY 1A: Attempting Gmail SMTP Port 465 (SSL)...
✅ ⭐ GMAIL SMTP 465 SUCCESS — Delivered via Gmail directly to INBOX!
```

Instead of:

```
❌ [GMAIL-CHECK] User: ❌ MISSING
❌ [GMAIL-SMTP] SKIPPED - Credentials not configured!
```

---

## WHY THIS HAPPENED

Render does NOT automatically read `.env` files from GitHub for security reasons.
You must manually add sensitive credentials as Environment Variables in Render dashboard.

---

## AFTER YOU FIX THIS

1. Test email from Telegram bot
2. Email will be sent via Gmail SMTP (not Brevo)
3. Email will arrive in INBOX (not spam)
4. Problem solved! 🎉
