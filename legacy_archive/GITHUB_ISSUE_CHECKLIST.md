## Sam Job Automator Launch Checklist

### Environment
- [ ] Python 3.11+ is installed and working
- [ ] `.venv` is created
- [ ] `.venv` is activated
- [ ] `pip install -r requirements.txt` succeeds

### Configuration
- [ ] `.env` exists
- [ ] `TEST_MODE=True` for the first run
- [ ] `KILL_SWITCH_ACTIVE=False`
- [ ] BREVO credentials are set
- [ ] Gmail credentials are set if needed
- [ ] Outlook credentials are set if needed
- [ ] Gemini or Groq API key is set
- [ ] Supabase URL and key are set
- [ ] Telegram token and chat ID are set if notifications are enabled

### Local Verification
- [ ] `core/main_bot.py` starts without import errors
- [ ] Preflight report prints successfully
- [ ] Scraper returns leads
- [ ] AI analysis works
- [ ] Duplicate detection works
- [ ] Test email is sent only to the test inbox
- [ ] Tailored CV HTML is generated
- [ ] PDF is generated
- [ ] DB logging works
- [ ] Follow-up flow works once and does not repeat

### GitHub Actions
- [ ] Workflow file is configured correctly
- [ ] Manual workflow dispatch succeeds
- [ ] Scheduled run succeeds
- [ ] Logs are clean and readable

### Production Readiness
- [ ] `TEST_MODE=False` only after successful dry-run
- [ ] First production cycle is monitored
- [ ] Kill switch is ready in case of failure
