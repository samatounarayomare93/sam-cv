# ✅ DEPLOYMENT CHECKLIST

## Pre-Deployment

- [ ] All API keys obtained
- [ ] .env file configured
- [ ] Git repository initialized
- [ ] GitHub repository created

## GitHub Setup

- [ ] Push code to GitHub
- [ ] Add secrets in GitHub Settings
  - [ ] GEMINI_API_KEY
  - [ ] GROQ_API_KEY
  - [ ] BREVO_SMTP_LOGIN
  - [ ] BREVO_SMTP_PASSWORD
  - [ ] GMAIL_SMTP_USER
  - [ ] GMAIL_APP_PASSWORD
  - [ ] OUTLOOK_USER
  - [ ] OUTLOOK_PASSWORD
  - [ ] TELEGRAM_BOT_TOKEN
  - [ ] TELEGRAM_CHAT_ID
  - [ ] SUPABASE_URL
  - [ ] SUPABASE_KEY
- [ ] Verify GitHub Actions workflow
- [ ] Test manual trigger

## Render Setup (Optional)

- [ ] Create Render account
- [ ] Connect GitHub repository
- [ ] Add environment variables
- [ ] Deploy web service
- [ ] Verify service is running

## Testing

- [ ] Run locally: `python swarm_orchestrator.py --once`
- [ ] Check Telegram notifications
- [ ] Verify database is created
- [ ] Check logs for errors
- [ ] Confirm emails are sending

## Monitoring

- [ ] Telegram bot responding
- [ ] GitHub Actions running
- [ ] Jobs being found
- [ ] Applications being sent
- [ ] Follow-ups working

## Post-Deployment

- [ ] Share Telegram bot with Sam
- [ ] Document any issues
- [ ] Schedule weekly review
- [ ] Monitor API quotas

---

**Status**: ⬜ Not Started | 🟡 In Progress | 🟢 Complete
