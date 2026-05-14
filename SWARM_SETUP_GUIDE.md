# 🚀 SWARM AGENTS - SETUP GUIDE
## 0 Investment | 24/7 Cloud | Maximum Performance

---

## 📋 OVERVIEW

This swarm system uses **GitHub Actions** (free) to run distributed agents that:
- **Scout**: Find jobs every 30 minutes
- **Writer**: Analyze and qualify jobs every hour
- **Sender**: Send applications every 2 hours
- **Tracker**: Monitor responses daily

**Total Cost: $0** | **Uptime: 24/7** | **Maintenance: Minimal**

---

## 🔑 STEP 1: GET FREE API KEYS

### 1. Gemini API (Free - 60 requests/min)
1. Go to: https://aistudio.google.com/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key

### 2. Groq API (Free - 20 requests/min)
1. Go to: https://console.groq.com/keys
2. Sign up (free)
3. Create API key
4. Copy the key

### 3. Telegram Bot (Free)
1. Open Telegram
2. Search: @BotFather
3. Send: `/newbot`
4. Follow instructions
5. Copy the bot token
6. Send any message to @userinfobot
7. Copy your chat ID

### 4. Email Providers (Free)

**Option A: Brevo (300 emails/day)**
- Go to: https://www.brevo.com
- Sign up (free)
- Go to Settings → SMTP & API
- Copy SMTP login and password

**Option B: Gmail (100 emails/day)**
- Go to: https://myaccount.google.com/apppasswords
- Generate app password
- Use your Gmail + app password

**Option C: Outlook (100 emails/day)**
- Use your Outlook email + password

### 5. Supabase (Optional - Free Database)
- Go to: https://supabase.com
- Sign up (free)
- Create project
- Copy URL and anon key

---

## 🔧 STEP 2: CONFIGURE GITHUB SECRETS

1. Go to your GitHub repo
2. Click: **Settings** → **Secrets and variables** → **Actions**
3. Click: **New repository secret**
4. Add these secrets:

| Secret Name | Value |
|-------------|-------|
| `GEMINI_API_KEY` | Your Gemini API key |
| `GROQ_API_KEY` | Your Groq API key |
| `TELEGRAM_BOT_TOKEN` | Your bot token |
| `TELEGRAM_CHAT_ID` | Your chat ID |
| `BREVO_SMTP_LOGIN` | Brevo SMTP login |
| `BREVO_SMTP_PASSWORD` | Brevo SMTP password |
| `GMAIL_SMTP_USER` | Gmail address |
| `GMAIL_APP_PASSWORD` | Gmail app password |
| `OUTLOOK_USER` | Outlook email |
| `OUTLOOK_PASSWORD` | Outlook password |
| `SUPABASE_URL` | Supabase URL (optional) |
| `SUPABASE_KEY` | Supabase key (optional) |
| `CANDIDATE_NAME` | Rita's full name |
| `CANDIDATE_EMAIL` | Rita's email |

---

## 🚀 STEP 3: DEPLOY

### Option A: GitHub Actions Only (Recommended)

1. Push code to GitHub:
```bash
git add .
git commit -m "Add swarm agents"
git push origin main
```

2. Go to **Actions** tab
3. Enable workflows
4. Agents will start automatically!

### Option B: Render + GitHub Actions

1. Go to: https://render.com
2. Sign up (free)
3. Create new **Web Service**
4. Connect your GitHub repo
5. Set environment variables
6. Deploy

**To keep Render awake 24/7:**
1. Go to: https://uptimerobot.com
2. Sign up (free)
3. Add monitor: Your Render URL
4. Set interval: 10 minutes
5. Done! Render stays awake forever

---

## 📊 MONITORING

### Telegram Commands
Send these to your bot:
- `/start` - Start the bot
- `/stats` - Get daily statistics
- `/status` - Check system status

### GitHub Actions Monitoring
1. Go to **Actions** tab
2. Click any workflow
3. See real-time logs

---

## ⚙️ CUSTOMIZATION

### Edit Job Search
Open `swarm_orchestrator.py` and modify:

```python
JOB_TITLES = [
    "network engineer",
    "senior network engineer",
    # Add more titles...
]

LOCATIONS = [
    "lebanon",
    "beirut",
    "remote",
    # Add more locations...
]
```

### Change Schedule
Edit workflow files in `.github/workflows/`:

```yaml
# Scout: Every 30 minutes
cron: '*/30 * * * *'

# Writer: Every hour
cron: '0 * * * *'

# Sender: Every 2 hours
cron: '0 */2 * * *'

# Tracker: Daily at 9 AM
cron: '0 9 * * *'
```

---

## 📈 EXPECTED RESULTS

| Metric | Daily | Monthly |
|--------|-------|---------|
| Jobs Found | 50-100 | 1,500-3,000 |
| Jobs Qualified | 10-20 | 300-600 |
| Applications Sent | 10-20 | 300-600 |
| Cost | $0 | $0 |

---

## 🆘 TROUBLESHOOTING

### Agent Not Running
1. Check **Actions** tab for errors
2. Verify secrets are set correctly
3. Check logs for specific errors

### No Jobs Found
1. Check if scrapers are working
2. Verify job titles match market
3. Check location settings

### Emails Not Sending
1. Verify email provider credentials
2. Check daily limits not exceeded
3. Try different provider

---

## 🎉 SUCCESS!

Your swarm is now running 24/7 on free cloud infrastructure!

**Next Steps:**
1. Monitor Telegram for notifications
2. Check GitHub Actions logs weekly
3. Adjust job titles/locations as needed
4. Add more email providers for higher volume

---

**Questions?** Check the logs or message me on Telegram!
