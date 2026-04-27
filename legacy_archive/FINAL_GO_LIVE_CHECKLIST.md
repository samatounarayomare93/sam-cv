# Final Go-Live Checklist

Do **not** switch out of test mode until every item below is green.

## 1) Local Environment
- [ ] Python 3.11+ works on the machine
- [ ] `.venv` is created and activated
- [ ] `pip install -r requirements.txt` succeeds
- [ ] `python -m py_compile` passes for the core modules

## 2) Configuration
- [ ] `.env` exists locally
- [ ] GitHub Secrets are set for every required key
- [ ] `TEST_MODE=True`
- [ ] `KILL_SWITCH_ACTIVE=False`
- [ ] At least one mail provider is configured
- [ ] Supabase URL and key are configured if using remote DB
- [ ] Gemini or Groq API key is configured if AI is enabled
- [ ] Telegram token and chat ID are configured if notifications are enabled

## 3) Local Runtime Validation
- [ ] `core/main_bot.py` starts without import errors
- [ ] Preflight report prints successfully
- [ ] Scraper returns at least one lead
- [ ] AI analysis returns a valid result tuple
- [ ] Duplicate detection works
- [ ] Tailored CV HTML is generated
- [ ] PDF is generated
- [ ] DB logging works
- [ ] Follow-up scan runs without errors

## 4) Email Verification
- [ ] `send_test_email()` succeeds
- [ ] Test email is delivered to `sam.dev1@hotmail.com`
- [ ] No real recipient gets a test message
- [ ] Provider fallback works if the first mail path fails

## 5) GitHub Actions Verification
- [ ] `Pre-Launch Test` workflow exists
- [ ] `Pre-Launch Test` workflow completes successfully
- [ ] `24/7 Scout & Strike Autopilot` workflow is healthy
- [ ] Workflow logs show no hidden errors
- [ ] Workflow uses the correct secrets

## 6) Production Safety
- [ ] No duplicate application sends observed
- [ ] No repeated follow-up sends observed
- [ ] Kill switch can stop the bot instantly
- [ ] Rollback plan is ready
- [ ] Monitoring is active for the first production cycles

## 7) Go-Live Decision
Only switch to production if **all** of these are true:
- [ ] Local dry-run passed
- [ ] GitHub manual workflow passed
- [ ] Test email arrived correctly
- [ ] No runtime errors appeared
- [ ] No configuration secrets are missing
- [ ] No duplicate/follow-up issues were seen

## 8) If Something Fails
- [ ] Keep `TEST_MODE=True`
- [ ] Set `KILL_SWITCH_ACTIVE=True`
- [ ] Stop the workflow
- [ ] Fix the exact failing step
- [ ] Re-run the pre-launch test before trying again
