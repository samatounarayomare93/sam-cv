# 🎛️ MASTER OPERATIONS & AUTOMATION GUIDE

Complete guide to all automation tools and master operations for Project Chronos.

---

## Quick Reference - All Automation Tools

### 🚀 **One-Command Deployment Prep**
```bash
python master_automation.py --full
```
Runs complete deployment preparation (all checks, backups, optimization)

---

## Available Automation Tools

### 1. **Pre-Deployment Suite** (pre_deployment_suite.py)

**Purpose**: Comprehensive 15-point pre-deployment validation

**Run**:
```bash
python pre_deployment_suite.py
```

**Checks**:
- ✅ Python 3.11+ environment
- ✅ Virtual environment status
- ✅ All dependencies installed (critical packages)
- ✅ Code compilation (0 syntax errors)
- ✅ Security issues (hardcoded secrets)
- ✅ Configuration files present
- ✅ GitHub workflows configured
- ✅ Documentation complete
- ✅ Git repository clean
- ✅ Database setup
- ✅ Telegram bot configuration
- ✅ Code optimization suggestions

**Output**:
- Console report with percentage score
- JSON report with detailed results

---

### 2. **Performance Analyzer** (performance_analyzer.py)

**Purpose**: Real-time performance analysis and bottleneck detection

**Run**:
```bash
python performance_analyzer.py
```

**Features**:
- System metrics (CPU %, Memory %, Disk %)
- Module import benchmarking
- Memory leak detection (10-second monitoring)
- Code structure analysis
- Performance recommendations
- Generates JSON report

**Example Output**:
```
CPU Usage: 45%
Memory: 60% used
Disk: 40% used

Module Benchmarks:
  ✅ core.main_bot (234ms)
  ✅ core.telegram_dashboard (456ms)
  ✅ core.ai_agent (123ms)
```

---

### 3. **Health Check** (health_check.py)

**Purpose**: Real-time health monitoring with continuous mode

**Run** (single check):
```bash
python health_check.py
```

**Run** (continuous monitoring):
```bash
python health_check.py --continuous --interval 60
```

**7-Point Health Score**:
- Git status
- Python syntax
- Dependencies
- File structure
- Documentation
- Code quality
- Configuration

**Output**:
- Health score (0-100)
- Detailed check results
- JSON history file for trending

---

### 4. **Database Manager** (database_manager.py)

**Purpose**: Database backup, restore, and optimization

**Run** (view status):
```bash
python database_manager.py --status
```

**Run** (backup):
```bash
python database_manager.py --backup
```

**Run** (restore):
```bash
python database_manager.py --restore backups/chronos_backup_20260421_120000.sql.gz
```

**Run** (optimize):
```bash
python database_manager.py --optimize
```

**Run** (list backups):
```bash
python database_manager.py --list
```

**Features**:
- Automatic compression with gzip
- SQLite optimization & VACUUM
- Complete backup history
- Point-in-time recovery

---

### 5. **Admin Dashboard** (admin_dashboard.py)

**Purpose**: Interactive menu-driven admin console

**Run**:
```bash
python admin_dashboard.py
```

**Menu Options**:
```
1. Health Check          → Run comprehensive health check
2. Database Status       → View database statistics
3. Performance Analysis  → System performance metrics
4. Backup Database       → Create database backup
5. View Logs             → Recent log entries
6. Deployment Status     → Verify deployment readiness
7. Configuration Check   → Verify all configs
8. Security Audit        → Security assessment
9. Exit                  → Exit menu
```

**Usage**:
- Select option number
- Review results
- Press Enter to continue to next option
- Ctrl+C to exit

---

### 6. **Master Automation** (master_automation.py)

**Purpose**: Orchestrate multiple automation tasks

**Run** (validation only):
```bash
python master_automation.py --validate
```

**Run** (health check only):
```bash
python master_automation.py --health
```

**Run** (backup only):
```bash
python master_automation.py --backup
```

**Run** (performance only):
```bash
python master_automation.py --performance
```

**Run** (optimize only):
```bash
python master_automation.py --optimize
```

**Run** (FULL deployment preparation):
```bash
python master_automation.py --full
```

**Full Deployment Workflow**:
1. Validates project (15 checks)
2. Health check (7 checks)
3. Backups all data (database + configs)
4. Performance analysis
5. Database optimization
6. Generates comprehensive log

**Output**:
- Console report
- JSON automation log with timestamps

---

## Typical Operations Workflows

### 📋 Daily Operations

**Every morning**:
```bash
# Quick health check
python health_check.py

# Or use admin dashboard for interactive view
python admin_dashboard.py
```

**Every week**:
```bash
# Full health analysis
python health_check.py --continuous --interval 3600  # Check hourly for 1 hour

# Backup data
python database_manager.py --backup

# Performance analysis
python performance_analyzer.py
```

**Every month**:
```bash
# Full deployment preparation
python master_automation.py --full

# Security audit
python admin_dashboard.py  # Select option 8
```

---

### 🚀 Before Production Deployment

**Step 1: Validate Everything**
```bash
python master_automation.py --validate
```
Expected: 100% of checks pass

**Step 2: Backup Current Data**
```bash
python master_automation.py --backup
```
Expected: Database backed up successfully

**Step 3: Run Performance Baseline**
```bash
python performance_analyzer.py
```
Expected: CPU < 70%, Memory < 70%

**Step 4: Full Deployment Prep**
```bash
python master_automation.py --full
```
Expected: All systems ready for deployment

---

### 🔧 Troubleshooting

**If health score is low**:
```bash
# Get detailed report
python health_check.py

# Or use interactive dashboard
python admin_dashboard.py
```

**If performance is slow**:
```bash
# Run analyzer
python performance_analyzer.py

# Optimize database
python database_manager.py --optimize
```

**If deployment fails**:
```bash
# Validate project completely
python pre_deployment_suite.py

# Check configuration
python admin_dashboard.py  # Option 7

# View recent logs
python admin_dashboard.py  # Option 5
```

---

## Advanced Usage

### Database Backup Strategy

```bash
# Manual backup
python database_manager.py --backup

# Backup before major changes
# (automatically creates timestamped backup)

# Restore if needed
python database_manager.py --restore backups/chronos_backup_20260421_153000.sql.gz

# View all backups
python database_manager.py --list
```

### Performance Optimization Workflow

```bash
# 1. Get baseline
python performance_analyzer.py

# 2. Identify bottlenecks (review recommendations)

# 3. Optimize database
python database_manager.py --optimize

# 4. Verify improvements
python performance_analyzer.py

# 5. Compare reports
# (saved as performance_report_YYYYMMDD_HHMMSS.json)
```

### Continuous Health Monitoring

```bash
# Monitor for 1 hour, checking every 30 seconds
python health_check.py --continuous --interval 30

# Monitor all day, checking every 5 minutes
python health_check.py --continuous --interval 300
```

---

## Reports & Logging

### Report Files Generated

All automation tools generate reports for archival and trending:

```
deployment_report_20260421_140000.json
  └─ Pre-deployment validation results

performance_report_20260421_140000.json
  └─ Performance metrics & recommendations

health_check_history.json
  └─ Historical health scores

automation_log_20260421_140000.json
  └─ Master automation execution log

backups/
  ├─ chronos_backup_20260421_140000.sql.gz
  ├─ chronos_backup_20260421_150000.sql.gz
  └─ .env.example.backup
```

### Reviewing Reports

```bash
# View JSON reports
cat deployment_report_20260421_140000.json | python -m json.tool

# Check health trends
cat health_check_history.json | python -m json.tool
```

---

## Integration with CI/CD

### GitHub Actions Integration

These tools can be integrated into GitHub Actions workflows:

```yaml
name: Pre-Deployment Check

on: [push]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run deployment validation
        run: python pre_deployment_suite.py
      
      - name: Run health check
        run: python health_check.py
      
      - name: Run performance analysis
        run: python performance_analyzer.py
```

---

## Command Cheat Sheet

```bash
# Pre-deployment validation
python pre_deployment_suite.py

# Performance analysis
python performance_analyzer.py

# Health check (single)
python health_check.py

# Health check (continuous, every 60 seconds)
python health_check.py --continuous --interval 60

# Database status
python database_manager.py --status

# Database backup
python database_manager.py --backup

# Database restore
python database_manager.py --restore <backup_file>

# Database optimization
python database_manager.py --optimize

# List all backups
python database_manager.py --list

# Admin dashboard (interactive)
python admin_dashboard.py

# Validation only
python master_automation.py --validate

# Health check only
python master_automation.py --health

# Backup only
python master_automation.py --backup

# Performance only
python master_automation.py --performance

# Optimize only
python master_automation.py --optimize

# FULL deployment prep (all checks)
python master_automation.py --full
```

---

## Troubleshooting Tools

### If something goes wrong:

**Issue: Pre-deployment fails**
```bash
python pre_deployment_suite.py  # See which check failed
```

**Issue: Performance is slow**
```bash
python performance_analyzer.py  # Get bottleneck report
python database_manager.py --optimize  # Optimize
```

**Issue: Need to recover data**
```bash
python database_manager.py --list  # Find backup
python database_manager.py --restore <backup>  # Restore
```

**Issue: Want interactive management**
```bash
python admin_dashboard.py  # Launch interactive menu
```

**Issue: Need comprehensive diagnostics**
```bash
python master_automation.py --full  # Complete analysis
```

---

## Best Practices

### Daily
- ✅ Run `python health_check.py`
- ✅ Review automation logs
- ✅ Check for errors in reports

### Weekly
- ✅ Run `python database_manager.py --backup`
- ✅ Run `python performance_analyzer.py`
- ✅ Review performance trends

### Monthly
- ✅ Run `python master_automation.py --full`
- ✅ Archive old reports
- ✅ Update documentation if needed

### Before Deployment
- ✅ Run `python pre_deployment_suite.py`
- ✅ Verify 100% checks pass
- ✅ Backup database
- ✅ Run performance baseline

---

## Monitoring Dashboard

For 24/7 monitoring with Telegram integration, use:

```bash
# Main bot with Telegram monitoring
python run.py

# Or just Telegram dashboard
python launch_sam.py
```

Then send to bot:
- `/health` - System health
- `/stats` - Performance statistics
- `/performance` - Success metrics
- `/logs` - Recent logs

---

## Summary

**6 powerful automation tools at your command:**
1. **pre_deployment_suite.py** - 15-point validation
2. **performance_analyzer.py** - Real-time metrics
3. **health_check.py** - 7-point health scoring
4. **database_manager.py** - Backup & recovery
5. **admin_dashboard.py** - Interactive management
6. **master_automation.py** - Orchestration & automation

**One-command deployment prep**:
```bash
python master_automation.py --full
```

**Interactive admin console**:
```bash
python admin_dashboard.py
```

**Continuous monitoring**:
```bash
python health_check.py --continuous --interval 60
```

---

## Support

- Read TROUBLESHOOTING_AND_FAQ.md for common issues
- Check MONITORING_AND_OPERATIONS.md for Telegram commands
- Review PRODUCTION_READINESS_CHECKLIST.md before deployment

---

**Master Automation Suite - Enterprise-Grade Operations Ready** 🚀
