# Ultra-Short Launch Checklist

- [ ] Activate `.venv`
- [ ] Verify `.env` is loaded
- [ ] Keep `TEST_MODE=True`
- [ ] Run bot locally once
- [ ] Confirm scraper + AI + SMTP + DB all pass
- [ ] Trigger GitHub Actions manual run
- [ ] Confirm test inbox delivery
- [ ] Confirm no duplicates / no follow-up loop
- [ ] Switch to `TEST_MODE=False` only after all checks pass
- [ ] Monitor first production cycles
- [ ] If issues: set `KILL_SWITCH_ACTIVE=True` and rollback to test mode
