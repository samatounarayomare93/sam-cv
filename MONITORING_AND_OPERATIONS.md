# 📊 MONITORING & OPERATIONS DASHBOARD

Real-time monitoring guide for Project Chronos in production.

---

## Telegram Command Reference - Monitoring

### Status & Health Commands

```
/status              → Overall automation status (QUICK CHECK)
/health              → Detailed system health report
/ping                → Connectivity check (response time)
/uptime              → Service uptime statistics
/performance         → Success rate metrics
```

**Example Usage**:
```
User:  /status
Bot:   ✅ OPERATIONAL - Cycle: 2/4 | Leads: 12 | Success: 94.2%

User:  /health
Bot:   System Health Report:
       CPU: 34% | Memory: 412MB/512MB | Disk: 234MB/1GB
       Database: Connected | Email: Active | Telegram: Connected
       Last Cycle: 5m ago | Errors: 0
```

---

### Queue & Processing Commands

```
/queue               → Lead queue status
/current             → Currently processing lead details
/delivered           → Recently sent applications
/failed              → Failed applications (with reasons)
/pending             → Pending follow-ups
```

**Example Usage**:
```
User:  /queue
Bot:   Lead Queue: 23 pending
       - 5 ready for processing
       - 12 waiting for next cycle
       - 6 in review queue

User:  /delivered
Bot:   Last 5 Deliveries:
       ✅ Tech Lead @ Google (2 mins ago)
       ✅ Engineer @ Amazon (15 mins ago)
       ...
```

---

### Performance & Analytics Commands

```
/stats               → Cycle statistics & performance
/analytics           → Long-term trends
/performance         → Success rate breakdown
/metrics             → Key performance indicators
```

**Example Usage**:
```
User:  /stats
Bot:   Cycle Statistics (Today):
       ├─ Cycles Completed: 4
       ├─ Leads Processed: 47
       ├─ Applications Sent: 42
       ├─ Success Rate: 89.4%
       ├─ Email Delivery: 100%
       └─ Avg Response Time: 1.2s
```

---

### Diagnostic Commands

```
/test_email          → Test email delivery
/test_database       → Verify database connection
/test_ai             → Test LLM integration
/test_scraper        → Test lead discovery
/api_status          → Check external API health
```

**Example Usage**:
```
User:  /test_email
Bot:   ✅ Primary Provider (Gmail): OK
       ✅ Backup Provider (Brevo): OK
       Testing email sent to test@example.com

User:  /test_ai
Bot:   Testing with: "Machine Learning Engineer"
       ✅ Primary (Gemini): Response OK (245ms)
       ✅ Backup (Groq): Response OK (312ms)
```

---

### Configuration & System Commands

```
/config              → Current configuration
/settings            → Configurable parameters
/logs                → Recent system logs
/events              → Recent system events
```

**Example Usage**:
```
User:  /config
Bot:   Active Configuration:
       - Max Leads/Cycle: 15
       - Email Workers: 3
       - Request Jitter: 2-5s
       - Scraper Pages: 3
       - Database: Supabase (Connected)
```

---

### Administrative Commands

```
/restart             → Restart bot service
/clear_cache         → Clear memory cache
/pause               → Pause automation
/resume              → Resume automation
/force_cycle         → Force immediate cycle
```

**Example Usage**:
```
User:  /pause
Bot:   ⏸️ Automation paused. Current jobs will complete.
       
User:  /force_cycle
Bot:   🔄 Forcing immediate cycle...
       Processing 15 leads...
       [████████████████] 100% - Complete!
       ✅ 14/15 successful
```

---

## Monitoring Cadence

### Real-Time Monitoring (Continuous)
- **Every 5 minutes**: Send `/status` to check bot is responsive
- **On errors**: Immediate `/health` diagnostic
- **On failures**: Check `/logs` for error details

### Hourly Monitoring
```bash
/stats              # Check cycle progress
/queue              # Verify leads are processing
/performance        # Confirm success rates
```

### Daily Monitoring
```bash
/analytics          # Review daily performance
/delivered          # Confirm all emails sent
/api_status         # Verify all integrations
/health             # Full system health check
```

### Weekly Monitoring
```bash
/metrics            # Long-term KPIs
/performance        # Weekly success rate trend
Review logs         # Look for patterns
Backup database     # Data protection
```

---

## Key Metrics to Track

### Availability Metrics
| Metric | Target | Action If Below |
|--------|--------|-----------------|
| Uptime | 99.5% | Investigate crashes |
| Bot Response | < 2s | Check resource usage |
| Email Response | < 1s | Verify provider status |
| Database Response | < 500ms | Check connection |

### Performance Metrics
| Metric | Target | Action If Below |
|--------|--------|-----------------|
| Leads/Cycle | 10+ | Verify scraper working |
| Success Rate | > 85% | Review job filtering |
| Email Delivery | 95%+ | Check credentials |
| LLM Response Time | < 5s | Verify API keys |

### Resource Metrics
| Metric | Target | Action If Over |
|--------|--------|-----------------|
| CPU Usage | 70% | Reduce batch size |
| Memory Usage | 400MB | Clear cache/restart |
| Disk Usage | 80% | Review logs/cleanup |
| Error Rate | 1% | Check logs for issues |

---

## Alert Conditions

### Critical Alerts (Immediate Action Required)
```
❌ Bot Not Responding      → Restart service immediately
❌ Database Connection Lost → Check Supabase/SQLite
❌ Email Delivery: 0%      → Verify credentials, test
❌ CPU > 90%               → Restart or reduce load
❌ Memory > 90%            → Restart and investigate leak
```

### Warning Alerts (Monitor & Act Within 1 Hour)
```
⚠️ Email Delivery < 95%    → Check provider status
⚠️ Success Rate < 75%      → Review job filtering
⚠️ Leads/Cycle < 5         → Verify scraper health
⚠️ Disk Usage > 75%        → Clean up old files
⚠️ Error Rate > 2%         → Review error logs
```

### Info Alerts (Log & Review)
```
ℹ️ API Rate Limit Approaching
ℹ️ Scheduled Maintenance Needed
ℹ️ Configuration Change Recommended
ℹ️ Long Response Time Observed
```

---

## Dashboards to Create (Optional)

### Render.com Dashboard
1. Open https://render.com/dashboard
2. Go to your service
3. Monitor:
   - **Logs**: Real-time event stream
   - **Metrics**: CPU, Memory, Disk (if available)
   - **Events**: Deployments, restarts, errors

### Supabase Dashboard (If Using)
1. Open https://app.supabase.com
2. Go to your project
3. Monitor:
   - **Logs**: Database query logs
   - **Realtime**: Active connections
   - **Storage**: Data usage
   - **Backups**: Database snapshots

### Custom Telegram Dashboard
Create a private Telegram channel:
1. Create group: "Sam Monitoring"
2. Add bot as admin
3. Bot can post alerts and reports

---

## Troubleshooting Decision Tree

```
Issue: Bot Not Responding
├─ Check: /ping (does it respond?)
│  ├─ YES → Issue elsewhere
│  └─ NO → Step 2
├─ Step 2: Check Render logs for errors
│  ├─ Build Error → Fix and redeploy
│  ├─ Runtime Error → Fix code/config
│  └─ Timeout → Increase timeout limits
├─ Step 3: Restart service
│  ├─ Success → Monitor closely
│  └─ Still fails → Step 4
└─ Step 4: Redeploy from GitHub
   ├─ Success → Investigate what failed
   └─ Still fails → Contact support

Issue: Email Not Sending
├─ Check: /test_email (primary provider)
│  ├─ OK → Check credentials, may timeout occasionally
│  └─ FAIL → Step 2
├─ Step 2: Verify credentials in .env
│  ├─ Correct → Step 3
│  └─ Wrong → Update and restart
├─ Step 3: Check backup provider
│  ├─ OK → Use fallback mode
│  └─ FAIL → Step 4
└─ Step 4: Check provider status online
   ├─ Provider Down → Wait for recovery
   └─ Provider OK → Check logs for details

Issue: High CPU/Memory
├─ Check: /stats (active load)
│  ├─ High → Processing large batch
│  └─ Low → Memory leak suspected
├─ Step 2: /clear_cache (free memory)
│  ├─ Better → Continue monitoring
│  └─ Same → Step 3
├─ Step 3: Restart service
│  ├─ Better → Was memory leak
│  └─ Immediate spike → Same issue
└─ Step 4: Reduce batch sizes in config
   └─ Lower: MAX_LEADS_PER_CYCLE from 15 to 10
```

---

## Reporting & Escalation

### Daily Report Template
```
Date: 2026-04-21
Period: 24 hours

✅ Status Summary
   - Uptime: 99.8%
   - Leads Processed: 142
   - Success Rate: 92.3%
   - Errors: 3 (all resolved)

📊 Key Metrics
   - CPU Avg: 45%
   - Memory Avg: 380MB
   - Response Time Avg: 1.1s
   - Email Delivery: 100%

⚠️ Issues Found
   - None (nominal operation)

🔄 Actions Taken
   - Routine log cleanup
   - Configuration review

Status: ✅ HEALTHY
```

### Escalation Procedure
1. **Warning Level** (Yellow): Team alerted, monitor closely
2. **Critical Level** (Red): Immediate response required
3. **Outage Level** (Black): Full team mobilization

---

## Automation Tips

### Set Up Telegram Notifications
```bash
# In your monitoring bot/cron:
if cpu_usage > 75:
    send_telegram("⚠️ CPU HIGH: " + cpu_usage)
if error_rate > 2:
    send_telegram("❌ ERROR RATE: " + error_rate)
```

### Automated Daily Report
```bash
# Cron job daily at 9 AM:
0 9 * * * /usr/bin/python3 /path/to/daily_report.py
```

### Backups
```bash
# Weekly backup script:
0 3 * * 0 /usr/bin/python3 /path/to/backup_database.py
```

---

## Key Contacts & Escalation

| Service | Provider | Status Page |
|---------|----------|-------------|
| Telegram | Telegram | https://status.telegram.org |
| Gmail/Google | Google Cloud | https://status.cloud.google.com |
| Brevo | Brevo | https://status.brevo.com |
| Supabase | Supabase | https://status.supabase.com |
| Render | Render | https://render-status.com |

---

**Happy Monitoring! Bot is operational and ready for production.** 🚀
