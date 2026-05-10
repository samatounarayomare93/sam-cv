import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
headers = {'apikey': key, 'Authorization': f'Bearer {key}'}

print("=" * 80)
print("🔍 DIAGNOSTIC REPORT - Why Emails Not Sending")
print("=" * 80)

# 1. Check environment variables
print("\n1️⃣ ENVIRONMENT VARIABLES:")
print("-" * 80)
print(f"  KILL_SWITCH_ACTIVE: {os.getenv('KILL_SWITCH_ACTIVE', 'NOT SET')}")
print(f"  MAX_EMAILS_PER_DAY: {os.getenv('MAX_EMAILS_PER_DAY', 'NOT SET')}")
print(f"  MAX_EMAILS_PER_HOUR: {os.getenv('MAX_EMAILS_PER_HOUR', 'NOT SET')}")
print(f"  MAX_APPLICATIONS_PER_DAY: {os.getenv('MAX_APPLICATIONS_PER_DAY', 'NOT SET')}")
print(f"  USE_AI_ANALYSIS: {os.getenv('USE_AI_ANALYSIS', 'NOT SET')}")
print(f"  GROQ_API_KEY: {'SET' if os.getenv('GROQ_API_KEY') else 'NOT SET'}")
print(f"  GMAIL_SMTP_USER: {os.getenv('GMAIL_SMTP_USER', 'NOT SET')}")

# 2. Check database leads
print("\n2️⃣ DATABASE LEADS STATUS:")
print("-" * 80)
r = requests.get(
    f'{url}/rest/v1/applications?select=status&order=created_at.desc&limit=500',
    headers=headers,
    timeout=15
)

if r.status_code == 200:
    leads = r.json()
    print(f"  Total leads in DB: {len(leads)}")
    
    # Count by status
    statuses = {}
    for lead in leads:
        status = lead.get('status', 'unknown')
        statuses[status] = statuses.get(status, 0) + 1
    
    print("\n  Status breakdown:")
    for status, count in sorted(statuses.items(), key=lambda x: x[1], reverse=True):
        print(f"    {status:20} : {count:4} leads")
    
    # Check if any sent today
    today = datetime.now().date().isoformat()
    r2 = requests.get(
        f'{url}/rest/v1/applications?select=*&status=eq.sent&order=created_at.desc&limit=10',
        headers=headers,
        timeout=15
    )
    
    if r2.status_code == 200:
        sent_today = r2.json()
        print(f"\n  Emails sent (last 10):")
        if sent_today:
            for app in sent_today[:10]:
                company = app.get('company_name', 'Unknown')[:30]
                created = app.get('created_at', 'unknown')[:19]
                print(f"    • {company:30} - {created}")
        else:
            print("    ❌ NO EMAILS SENT!")
else:
    print(f"  ❌ Error accessing database: {r.status_code}")

# 3. Check system settings
print("\n3️⃣ SYSTEM SETTINGS:")
print("-" * 80)
r = requests.get(
    f'{url}/rest/v1/system_settings?select=*',
    headers=headers,
    timeout=15
)

if r.status_code == 200:
    settings = r.json()
    settings_dict = {s['key']: s['value'] for s in settings}
    
    print(f"  kill_switch: {settings_dict.get('kill_switch', 'NOT SET')}")
    print(f"  active_bot_leader: {settings_dict.get('active_bot_leader', 'NOT SET')}")
    print(f"  active_bot_heartbeat: {settings_dict.get('active_bot_heartbeat', 'NOT SET')}")
    
    # Check if bot is active
    heartbeat = settings_dict.get('active_bot_heartbeat', '')
    if heartbeat:
        try:
            hb_time = datetime.fromisoformat(heartbeat.replace('Z', '+00:00'))
            now = datetime.now(hb_time.tzinfo)
            diff = (now - hb_time).total_seconds()
            print(f"\n  Bot last heartbeat: {int(diff)} seconds ago")
            if diff > 300:  # 5 minutes
                print(f"    ⚠️ WARNING: Bot may be stuck or not running!")
            else:
                print(f"    ✅ Bot is active")
        except:
            print(f"    ⚠️ Could not parse heartbeat time")

# 4. Check Render service
print("\n4️⃣ RENDER SERVICE STATUS:")
print("-" * 80)
try:
    r = requests.get('https://sam-job-automator.onrender.com', timeout=10)
    print(f"  sam-job-automator: HTTP {r.status_code}")
except Exception as e:
    print(f"  sam-job-automator: ❌ {str(e)[:50]}")

try:
    r = requests.get('https://sam-cv-bot.onrender.com', timeout=10)
    print(f"  sam-cv-bot: HTTP {r.status_code}")
    if r.status_code == 200:
        print(f"    ✅ Bot service is UP")
except Exception as e:
    print(f"  sam-cv-bot: ❌ {str(e)[:50]}")

# 5. Possible issues
print("\n5️⃣ POSSIBLE ISSUES:")
print("-" * 80)

issues_found = []

# Check if leads are stuck in pending
if statuses.get('pending', 0) > 100:
    issues_found.append("❌ Too many leads stuck in 'pending' status")
    issues_found.append("   → Bot may not be processing leads")

# Check if no emails sent
if statuses.get('sent', 0) == 0:
    issues_found.append("❌ NO emails have been sent")
    issues_found.append("   → Email sending is completely blocked")

# Check if bot heartbeat is old
if heartbeat:
    try:
        hb_time = datetime.fromisoformat(heartbeat.replace('Z', '+00:00'))
        now = datetime.now(hb_time.tzinfo)
        diff = (now - hb_time).total_seconds()
        if diff > 300:
            issues_found.append(f"❌ Bot heartbeat is {int(diff/60)} minutes old")
            issues_found.append("   → Bot may have crashed or stopped")
    except:
        pass

if not issues_found:
    issues_found.append("✅ No obvious issues detected")

for issue in issues_found:
    print(f"  {issue}")

# 6. Recommended actions
print("\n6️⃣ RECOMMENDED ACTIONS:")
print("-" * 80)
print("  1. Check Render logs:")
print("     .sovereign_runtime\\python.exe get_render_logs.py")
print()
print("  2. Force process pending leads:")
print("     .sovereign_runtime\\python.exe force_process_leads.py")
print()
print("  3. Test email sending manually:")
print("     .sovereign_runtime\\python.exe test_email_now.py")
print()
print("  4. Restart the bot via Telegram:")
print("     Send /resume to @samcvbot")
print()
print("  5. Check if bot is paused:")
print("     Send /status to @samcvbot")

print("\n" + "=" * 80)
print("✅ DIAGNOSTIC COMPLETE")
print("=" * 80)
