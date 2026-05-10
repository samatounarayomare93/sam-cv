import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
headers = {'apikey': key, 'Authorization': f'Bearer {key}'}

print("=" * 80)
print("📧 EMAIL STATUS CHECK")
print("=" * 80)

# Check last 20 emails
print("\n📨 Last 20 Emails Sent:")
print("-" * 80)
r = requests.get(
    f'{url}/rest/v1/email_log?select=*&order=sent_at.desc&limit=20',
    headers=headers,
    timeout=15
)

if r.status_code == 200:
    emails = r.json()
    if emails:
        for i, email in enumerate(emails, 1):
            company = email.get('company_name', 'Unknown')[:30]
            status = email.get('status', 'unknown')
            sent_at = email.get('sent_at', 'unknown')[:19]
            provider = email.get('provider', 'unknown')
            print(f"  {i}. {company:30} | {status:10} | {provider:8} | {sent_at}")
        
        # Count by status
        print("\n📊 Email Status Summary:")
        print("-" * 80)
        statuses = {}
        for email in emails:
            status = email.get('status', 'unknown')
            statuses[status] = statuses.get(status, 0) + 1
        
        for status, count in statuses.items():
            print(f"  {status}: {count}")
        
        # Check last email time
        last_email_time = emails[0].get('sent_at', '')
        if last_email_time:
            print(f"\n⏰ Last Email Sent: {last_email_time}")
    else:
        print("  ❌ No emails found in database!")
else:
    print(f"  ❌ Error: {r.status_code} - {r.text[:200]}")

# Check leads status
print("\n" + "=" * 80)
print("🎯 LEADS STATUS CHECK")
print("=" * 80)

r = requests.get(
    f'{url}/rest/v1/job_leads?select=status&order=created_at.desc&limit=100',
    headers=headers,
    timeout=15
)

if r.status_code == 200:
    leads = r.json()
    if leads:
        print(f"\n📊 Last 100 Leads Status:")
        print("-" * 80)
        statuses = {}
        for lead in leads:
            status = lead.get('status', 'unknown')
            statuses[status] = statuses.get(status, 0) + 1
        
        for status, count in sorted(statuses.items(), key=lambda x: x[1], reverse=True):
            print(f"  {status:20} : {count:3} leads")
    else:
        print("  ❌ No leads found!")
else:
    print(f"  ❌ Error: {r.status_code}")

# Check system settings
print("\n" + "=" * 80)
print("⚙️ SYSTEM SETTINGS CHECK")
print("=" * 80)

r = requests.get(
    f'{url}/rest/v1/system_settings?select=*',
    headers=headers,
    timeout=15
)

if r.status_code == 200:
    settings = r.json()
    if settings:
        print("\n🔧 Current Settings:")
        print("-" * 80)
        for setting in settings:
            key = setting.get('key', 'unknown')
            value = setting.get('value', 'unknown')
            print(f"  {key:30} : {value}")
    else:
        print("  ⚠️ No settings found")
else:
    print(f"  ❌ Error: {r.status_code}")

print("\n" + "=" * 80)
print("✅ CHECK COMPLETE")
print("=" * 80)
