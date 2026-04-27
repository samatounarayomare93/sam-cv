# Sam Job Automator Launch Kit Index

Use this file as the single entry point for launch prep.

## 1) Quick start
- `LAUNCH_NOTE.txt` — plain checklist for daily use
- `ULTRA_SHORT_LAUNCH.md` — very short go/no-go checklist
- `PRINTABLE_LAUNCH_DOC.md` — one-page printable summary
- `QUICK_START.md` — tells you exactly what to open first, second, and third

## 2) Issue / tracker format
- `GITHUB_ISSUE_CHECKLIST.md` — GitHub issue checklist format
- `FINAL_GO_LIVE_CHECKLIST.md` — strict final production gate

## 3) README integration
- `README_LAUNCH_SECTION.md` — launch section ready to paste into `README.md`

## 4) Test commands and automation
- `LAUNCH_TEST_COMMANDS.md` — copy/paste command list
- `PRE_LAUNCH_TEST.ps1` — PowerShell automation script
- `PRE_LAUNCH_TEST.bat` — Windows batch wrapper
- `AUTO_BOOTSTRAP.ps1` — automated bootstrap and verification script
- `AUTO_BOOTSTRAP.bat` — Windows wrapper for the bootstrap script
- `AUTO_BOOTSTRAP.md` — usage notes for the bootstrap flow
- `launch_config.example.env` — example environment file template

## 5) Recommended execution order
1. Read `QUICK_START.md`
2. Read `ULTRA_SHORT_LAUNCH.md`
3. Run `AUTO_BOOTSTRAP.ps1 -SendTestEmail` or `PRE_LAUNCH_TEST.ps1`
4. Confirm test email delivery to `sam.dev1@hotmail.com`
5. Review `FINAL_GO_LIVE_CHECKLIST.md`
6. Review `GITHUB_ISSUE_CHECKLIST.md`
7. Paste `README_LAUNCH_SECTION.md` into the main README if needed
8. Move to production only after the dry-run is green

## 6) Safety reminder
Do not disable `TEST_MODE` until local and GitHub dry-runs pass.
If anything fails, set `KILL_SWITCH_ACTIVE=True` and stop the workflow.
