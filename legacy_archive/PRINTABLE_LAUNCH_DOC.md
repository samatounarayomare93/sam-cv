# Sam Job Automator Launch Summary

## Objective
Run the bot safely in test mode first, verify every module, then move to production only after successful dry-run validation.

## Required setup
- Python 3.11+
- `.venv`
- `requirements.txt` installed
- `.env` populated
- `TEST_MODE=True` initially

## Must validate
- AI analysis
- scraper
- SMTP sending
- DB logging
- PDF generation
- CV tailoring
- follow-up flow
- GitHub Actions workflow

## Go-live rule
Do not disable `TEST_MODE` until:
- local run succeeds
- GitHub manual run succeeds
- test inbox receives email
- DB writes are confirmed
- no duplicate sends occur
- no follow-up loops occur

## Rollback
If anything misbehaves:
- set `KILL_SWITCH_ACTIVE=True`
- stop GitHub schedule
- return to `TEST_MODE=True`
- inspect logs and fix
