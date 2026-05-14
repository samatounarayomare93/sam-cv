# 🚀 RITA JOB AUTOMATOR - COMPLETE SETUP

## ⚡ ONE-CLICK SETUP

### Step 1: Prepare Tokens File (Optional)
1. Copy `tokens.config.template` to `tokens.config`
2. Edit `tokens.config` and add your tokens:
```json
{
  "GitHubToken": "ghp_YOUR_TOKEN_HERE",
  "RenderAPIKey1": "rnd_YOUR_RENDER_KEY_1",
  "RenderAPIKey2": "rnd_YOUR_RENDER_KEY_2"
}
```
3. Save file

### Step 2: Double-Click Setup
1. Go to project folder
2. **Double-click** `setup.bat`
3. Follow prompts
4. Enter API keys when asked (if not in config file)
5. Wait 5 minutes
6. Done! ✅

---

## 📋 BEFORE YOU START

### Get These Free API Keys:

| Service | URL | Free Tier |
|---------|-----|-----------|
| **Gemini AI** | https://aistudio.google.com/apikey | 60 requests/min |
| **Groq AI** | https://console.groq.com/keys | 20 requests/min |
| **Telegram Bot** | @BotFather | Unlimited |
| **Brevo SMTP** | https://www.brevo.com | 300 emails/day |
| **Gmail** | https://myaccount.google.com/apppasswords | 100 emails/day |

---

## 🔧 MANUAL SETUP (If Auto Fails)

### 1. GitHub Secrets
Go to: https://github.com/samatounarayomare93/sam-cv/settings/secrets/actions

Add these secrets:
```
GEMINI_API_KEY = your-key
GROQ_API_KEY = your-key
TELEGRAM_BOT_TOKEN = your-token
TELEGRAM_CHAT_ID = your-chat-id
BREVO_SMTP_LOGIN = your-login
BREVO_SMTP_PASSWORD = your-password
GMAIL_SMTP_USER = your-email
GMAIL_APP_PASSWORD = your-password
CANDIDATE_NAME = Rita Salameh
CANDIDATE_EMAIL = rita@email.com
SUPABASE_URL = (optional)
SUPABASE_KEY = (optional)
```

### 2. Enable GitHub Actions
1. Go to: https://github.com/samatounarayomare93/sam-cv/actions
2. Click "I understand my workflows, go ahead and enable them"
3. Done!

### 3. Render Setup
1. Go to: https://dashboard.render.com
2. New → Web Service
3. Connect GitHub repo
4. Add environment variables (same as GitHub secrets)
5. Deploy

---

## ✅ VERIFICATION

### Test GitHub Actions
1. Go to Actions tab
2. Click "Swarm Scout Agent"
3. Click "Run workflow"
4. Check if it runs successfully

### Test Telegram
1. Open Telegram
2. Find your bot
3. Send `/start`
4. Should get response

### Test Render
1. Go to your Render dashboard
2. Check if service is "Live"
3. Visit the URL

---

## 🆘 TROUBLESHOOTING

### "GitHub CLI not found"
- Install from: https://cli.github.com/
- Or run: `winget install GitHub.cli`

### "Authentication failed"
- Check your GitHub token
- Make sure token has `repo` scope
- Try: `gh auth login`

### "Workflow not found"
- Make sure `.github/workflows/` folder exists
- Check if YAML files are valid

### "Secrets not set"
- Go to Settings → Secrets → Actions
- Add secrets manually

---

## 📞 SUPPORT

If setup fails:
1. Check `setup.log` file
2. Read error messages carefully
3. Try manual setup steps
4. Check GitHub Actions logs

---

## 🎉 SUCCESS!

After setup:
- ✅ Jobs found every 30 minutes
- ✅ Applications sent automatically
- ✅ Telegram notifications
- ✅ 24/7 cloud operation
- ✅ $0 cost

**Your swarm is ready!** 🚀
