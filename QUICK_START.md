# 🚀 QUICK START GUIDE

## For Sam Salameh - Senior Network Engineer

### Step 1: Get API Keys (5 minutes)

1. **Gemini AI** (Free)
   - Go to: https://aistudio.google.com/app/apikey
   - Click "Create API Key"
   - Copy the key

2. **Brevo Email** (Free - 300 emails/day)
   - Go to: https://www.brevo.com
   - Sign up with your email
   - Go to SMTP settings
   - Copy login and password

3. **Telegram Bot** (Free)
   - Message @BotFather on Telegram
   - Send /newbot
   - Follow instructions
   - Copy the token
   - Message @userinfobot to get your chat ID

### Step 2: Configure (2 minutes)

1. Copy `.env.example` to `.env`
2. Fill in your API keys
3. Save the file

### Step 3: Deploy (3 minutes)

**Option A: GitHub Actions (Recommended)**
```bash
# 1. Push to GitHub
git add .
git commit -m "Initial setup"
git push origin main

# 2. Add secrets on GitHub
# Go to: Settings → Secrets → Actions
# Add all keys from .env

# 3. Done! Runs every 6 hours automatically
```

**Option B: Local Run**
```bash
# Install dependencies
pip install -r requirements.txt

# Run once
python swarm_orchestrator.py --once

# Run continuously
python swarm_orchestrator.py
```

### Step 4: Monitor

- Check Telegram for notifications
- Check `swarm.log` for detailed logs
- Check GitHub Actions for run status

### Expected Results

| Metric | Value |
|--------|-------|
| Jobs Found | 50-100/day |
| Applications | 10-20/day |
| Response Rate | 5-10% |
| Cost | $0 |

### Troubleshooting

**Problem**: No jobs found
- Check internet connection
- Verify API keys are correct
- Check logs for errors

**Problem**: Emails not sending
- Verify email credentials
- Check email provider limits
- Try different email provider

**Problem**: AI not working
- Verify Gemini/Groq API keys
- Check API quotas
- System will fallback to keyword matching

### Support

For help:
1. Check logs: `swarm.log`
2. Telegram notifications
3. GitHub Issues

---

**You're all set! The system will now work 24/7 automatically.**
