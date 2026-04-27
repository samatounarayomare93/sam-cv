# 🔄 CI/CD AUTOMATION & DEPLOYMENT GUIDE

Complete guide to GitHub Actions CI/CD pipelines, automated testing, and deployment workflows.

---

## GitHub Actions Workflows Overview

Five production-grade workflows managing all automation:

### 1. **Code Quality Pipeline** (ci_quality.yml)
Runs on: Every push to main
- ✅ Python compilation test
- ✅ Syntax validation
- ✅ Unit tests
- ✅ Coverage analysis (70% minimum)
- ✅ Dependency verification

### 2. **Pre-Launch Validation** (pre_launch_test.yml)
Runs on: Before deployment
- ✅ Full environment validation
- ✅ Performance benchmarks
- ✅ Security audit
- ✅ Configuration check

### 3. **Job Bot Runner** (job_bot.yml)
Runs on: Daily schedule (6 AM UTC)
- ✅ Activate lead discovery bot
- ✅ Process job applications
- ✅ Generate personalized CVs
- ✅ Send targeted emails
- ✅ Follow-up reminders

### 4. **24/7 Telegram Bot** (24_7_telegram_bot.yml)
Runs on: Always active (deployment)
- ✅ Telegram command interface (50 commands)
- ✅ Remote operations
- ✅ Health monitoring
- ✅ Status dashboards

### 5. **Release Automation** (release.yml)
Runs on: Git tag push (v*.*.*)
- ✅ Semantic versioning
- ✅ Changelog generation
- ✅ GitHub Release creation
- ✅ Auto release notes

---

## Quick Start - GitHub Actions

### Enable Workflows

Workflows are automatically enabled when pushed to GitHub:

```bash
# All workflows in .github/workflows/ activate automatically
git push origin main
```

### View Workflow Status

In GitHub Repository → Actions tab:
- ✅ Green = Passing
- ❌ Red = Failed
- ⏱️ Yellow = Running

---

## CI/CD Secrets Configuration

### Required GitHub Secrets

Set in Repository Settings → Secrets and variables → Actions:

```
RENDER_API_KEY          (Deploy token from Render.com)
TELEGRAM_BOT_TOKEN      (From BotFather)
GMAIL_APP_PASSWORD      (Gmail app-specific password)
BREVO_API_KEY          (Email delivery)
GROQ_API_KEY           (Fallback LLM)
GOOGLE_API_KEY         (Primary LLM)
SUPABASE_URL           (Database)
SUPABASE_KEY           (Database auth)
HEROKU_API_KEY         (Alternative deployment)
```

### How to Set Secrets

1. Go to GitHub Repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Enter Name (e.g., `TELEGRAM_BOT_TOKEN`)
5. Enter Value (your actual token)
6. Click "Add secret"

**Example**:
```
Name: TELEGRAM_BOT_TOKEN
Value: 123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
```

---

## Code Quality Pipeline (ci_quality.yml)

### What It Does

Runs on every push to main branch:
1. Compile test (verify no syntax errors)
2. Unit tests (if available)
3. Coverage analysis (70% minimum)
4. Dependency check

### Trigger

```yaml
on:
  push:
    branches: [main]
```

### View Results

GitHub Repository → Actions → Latest workflow run

**If All Pass** ✅:
- Code ready for deployment
- Safe to merge PRs

**If Any Fails** ❌:
- Fix issues before deployment
- See error details in logs
- Run locally to debug

### Run Locally (Same as CI)

```bash
# Install dependencies
pip install -r requirements.txt

# Run compilation test
python -m py_compile core/*.py tests/*.py

# Run unit tests
pytest tests/ --cov=core --cov-report=term-missing

# Check dependencies
python -c "import requirements; print('All deps OK')"
```

---

## Pre-Launch Validation (pre_launch_test.yml)

### What It Does

Comprehensive pre-deployment validation:
1. Environment verification
2. Database connectivity
3. API key validation
4. Security checks
5. Configuration audit

### Manual Trigger

GitHub Actions → pre_launch_test → Run workflow

### View Results

Check workflow logs for detailed validation report

### Run Locally

```bash
python pre_deployment_suite.py
```

---

## Job Bot Runner (job_bot.yml)

### What It Does

Automated job application workflow:
- Discovers new jobs (LinkedIn, Indeed, etc.)
- Analyzes job requirements
- Tailors CV with relevant skills
- Personalizes cover letter
- Sends application email
- Schedules follow-ups

### Schedule

Runs daily at 6 AM UTC:
```yaml
schedule:
  - cron: '0 6 * * *'
```

### Modify Schedule

Edit `.github/workflows/job_bot.yml`:
```yaml
schedule:
  - cron: '0 9 * * *'  # 9 AM UTC
  - cron: '0 14 * * *' # 2 PM UTC
  - cron: '0 20 * * *' # 8 PM UTC
```

### Monitor Execution

GitHub Repository → Actions → job_bot workflow

### Troubleshooting

**If bot doesn't run**:
- Check secrets are configured
- Verify schedule format
- Check workflow file syntax

**If emails not sending**:
- Verify `GMAIL_APP_PASSWORD` or `BREVO_API_KEY`
- Check SMTP configuration
- Review error logs

---

## 24/7 Telegram Bot (24_7_telegram_bot.yml)

### What It Does

Deploys bot to Render.com for 24/7 operation:
- Accepts 50 tactical commands
- Remote job management
- Health monitoring
- Real-time status

### Deploy Configuration

Uses `render.yaml`:
```yaml
services:
  - type: web
    name: sam-telegram-bot
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: python launch_sam.py
    healthCheckPath: /health
```

### 50 Available Commands

**Bot Control**:
- `/start` - Start bot
- `/help` - Show commands
- `/status` - Current status
- `/health` - System health

**Job Management**:
- `/jobs` - List active jobs
- `/apply [ID]` - Apply to job
- `/cv` - Generate CV
- `/follow_up [ID]` - Follow-up reminder

**Analytics**:
- `/stats` - Success metrics
- `/performance` - Application performance
- `/trends` - Job market trends
- `/reports` - Generate reports

**Admin**:
- `/config` - View configuration
- `/logs` - Recent logs
- `/restart` - Restart bot
- `/backup` - Backup data

*Plus 36+ more commands*

### Continuous Monitoring

The bot continuously:
- Monitors Telegram for messages
- Responds to commands
- Tracks application status
- Sends reminders
- Logs all operations

### View Logs

```bash
# Local logs directory
ls logs/

# View latest log
tail -f logs/latest.log
```

---

## Release Automation (release.yml)

### What It Does

Automatic versioning and release creation:
1. Parse version from tag
2. Generate changelog
3. Create GitHub release
4. Auto-generate release notes

### How to Release

```bash
# Create release tag
git tag -a v1.1.0 -m "Release v1.1.0: Major new features"

# Push tag to GitHub
git push origin v1.1.0
```

### Automatic Actions

GitHub automatically:
1. Runs tests (ci_quality.yml)
2. Creates release (release.yml)
3. Generates release notes
4. Deploys to Render.com (24_7_telegram_bot.yml)

### Version Format

Use semantic versioning:
- `v1.0.0` - Major release (breaking changes)
- `v1.1.0` - Minor release (new features)
- `v1.0.1` - Patch release (bug fixes)
- `v1.0.0-beta` - Pre-release

### View Releases

GitHub Repository → Releases tab

---

## Deployment to Render.com

### Prerequisites

1. Render.com account
2. GitHub repository connected
3. `render.yaml` configured
4. Secrets set in GitHub

### Auto-Deployment Workflow

```
Push to main
    ↓
CI tests pass (ci_quality.yml)
    ↓
Automatically deploy to Render.com
    ↓
Telegram bot goes live 24/7
    ↓
Health checks every 5 minutes
    ↓
Auto-restart on failure
```

### Manual Deployment

Render.com Dashboard:
1. Select "Sam Job Automator" service
2. Click "Deploy" button
3. Monitor build progress
4. View live logs

### Check Deployment Status

```bash
# View service status
curl https://your-render-service.onrender.com/health

# View logs
# Render Dashboard → Logs tab
```

---

## Monitoring & Alerting

### Health Checks

All workflows include health checks:

```yaml
healthCheckPath: /health
healthCheckProtocol: http
```

Runs every 5 minutes to verify bot is alive

### Alert Configuration

Configure alerts in GitHub:
Settings → Code security → Dependabot alerts

### Workflow Status Notifications

GitHub sends notifications for:
- Workflow failures
- Deployment errors
- Test failures

Configure in: Settings → Notifications

---

## Advanced CI/CD Usage

### Custom Environment Variables

In workflow files:
```yaml
env:
  PYTHON_VERSION: '3.11'
  ENVIRONMENT: production
  LOG_LEVEL: INFO
```

### Matrix Testing (Multiple Python Versions)

```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11', '3.12']
steps:
  - uses: actions/setup-python@v2
    with:
      python-version: ${{ matrix.python-version }}
```

### Conditional Execution

```yaml
if: github.event_name == 'push' && github.ref == 'refs/heads/main'
```

### Artifacts & Uploads

```yaml
- name: Upload test reports
  uses: actions/upload-artifact@v2
  with:
    name: test-reports
    path: reports/
```

---

## Debugging Failed Workflows

### View Detailed Logs

GitHub Actions → Workflow run → Click job → Expand steps

### Common Issues & Solutions

**Issue: Secret not found**
- Verify secret name in GitHub Settings
- Check secret is visible to workflow
- Restart workflow after adding secret

**Issue: Python version mismatch**
- Update `actions/setup-python@v2` to specify version
- Use `python-version: '3.11'`

**Issue: Dependencies not installing**
- Check requirements.txt syntax
- Verify pip is updated
- See error logs for specific package

**Issue: Tests failing**
- Run tests locally: `pytest tests/`
- Check for environment-specific issues
- Verify database connection

### Run Workflow Manually

GitHub Actions tab → Select workflow → "Run workflow" button

### Workflow Logs

Click on any workflow run to see:
- ✅ Passed steps
- ❌ Failed steps
- 📝 Detailed output
- ⏱️ Execution time

---

## Best Practices

### Commit Best Practices

```bash
# Write descriptive commit messages
git commit -m "Feature: Add job scraper for ZipRecruiter

- Implements ZipRecruiter API integration
- Adds job filtering and ranking
- Improves email delivery success rate

Fixes #123"

# Push to trigger CI
git push origin feature/ziprecruiter
```

### PR Review

Before merging PR:
- ✅ All GitHub Actions pass
- ✅ Code review approved
- ✅ No merge conflicts
- ✅ Tests cover changes

### Deployment Checklist

Before pushing to main:
- ✅ All local tests pass
- ✅ Code compiles without errors
- ✅ Secrets configured in GitHub
- ✅ render.yaml is valid
- ✅ No hardcoded credentials

---

## Command Cheat Sheet

```bash
# Push to main (triggers CI)
git push origin main

# Create release tag
git tag -a v1.1.0 -m "Release message"
git push origin v1.1.0

# View workflow status
# GitHub Repository → Actions tab

# Run workflow manually
# GitHub Actions → Select workflow → Run workflow

# Deploy to Render.com
# Render Dashboard → Select service → Deploy

# View live logs
# Render Dashboard → Logs tab

# Check bot health
curl https://your-service.onrender.com/health

# View Telegram commands
/help  # (Send in Telegram chat with bot)
```

---

## Troubleshooting Workflows

### Workflow Won't Start

**Check**:
- Push was to main branch
- .github/workflows/ files exist
- YAML syntax is valid

**Fix**:
```bash
# Validate YAML
python -m yaml .github/workflows/ci_quality.yml

# Retry workflow
# GitHub Actions → Select workflow → "Re-run all jobs"
```

### Tests Failing in CI but Passing Locally

**Possible Issues**:
- Environment differences
- Missing secrets
- Path issues

**Debug**:
```bash
# Run with same environment as CI
python -m pytest tests/ -v

# Check imports
python -c "import core; import tests"

# Verify secrets
echo $TELEGRAM_BOT_TOKEN  # Should show value or be empty
```

### Deployment Stuck

**Check**:
- Render.com dashboard for build logs
- GitHub Actions for deployment errors
- Network connectivity

**Fix**:
- Cancel build: Render Dashboard → Services → Cancel
- Retry: Click Deploy button again
- Check logs: Render Dashboard → Logs

---

## Integration with Local Development

### Pre-Commit Hooks

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python -m py_compile core/*.py tests/*.py
```

### Local CI Simulation

Run same checks as GitHub Actions:
```bash
# Compile check
python -m py_compile core/*.py

# Tests
pytest tests/ --cov=core

# Health check
python health_check.py
```

---

## Summary

**5 Production-Grade CI/CD Pipelines:**
1. **Code Quality** - Every push to main
2. **Pre-Launch** - Before deployment
3. **Job Bot** - Daily automation
4. **24/7 Bot** - Continuous Telegram service
5. **Release** - Automatic versioning

**One-Command Deployment**:
```bash
git tag -a v1.1.0 -m "Release"
git push origin v1.1.0
# Automatically deploys and goes live
```

---

**CI/CD Infrastructure - Enterprise-Grade Automation Ready** 🚀
