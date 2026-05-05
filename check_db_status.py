import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SERVICE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

headers = {
    'apikey': SERVICE_KEY,
    'Authorization': f'Bearer {SERVICE_KEY}',
    'Content-Type': 'application/json'
}

print("=== SUPABASE DB STATUS ===\n")

# 1. Total leads
r = requests.get(f'{SUPABASE_URL}/rest/v1/leads?select=status',
    headers={**headers, 'Prefer': 'count=exact'}, timeout=10)
print(f"Total leads: {r.headers.get('content-range', 'error')} | Status: {r.status_code}")

# 2. Pending leads
r2 = requests.get(f'{SUPABASE_URL}/rest/v1/leads?status=in.(pending,circadian_hold)&select=company_name,status,created_at&order=created_at.desc&limit=10',
    headers=headers, timeout=10)
print(f"\nPending leads: {r2.status_code}")
if r2.status_code == 200:
    pending = r2.json()
    print(f"Count: {len(pending)}")
    for l in pending[:5]:
        print(f"  - {l.get('company_name','?')} | {l.get('status','?')} | {l.get('created_at','?')[:19]}")

# 3. Recent applications (last 24h)
yesterday = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
r3 = requests.get(
    f'{SUPABASE_URL}/rest/v1/applications?select=company_name,job_title,status,timestamp&order=timestamp.desc&limit=10',
    headers=headers, timeout=10)
print(f"\nRecent applications: {r3.status_code}")
if r3.status_code == 200:
    apps = r3.json()
    print(f"Count: {len(apps)}")
    for a in apps[:5]:
        print(f"  - {a.get('company_name','?')} | {a.get('job_title','?')[:30]} | {a.get('timestamp','?')[:19]}")

# 4. Leads added in last hour
r4 = requests.get(
    f'{SUPABASE_URL}/rest/v1/leads?select=company_name,email,status&order=created_at.desc&limit=20',
    headers=headers, timeout=10)
print(f"\nLatest leads in DB: {r4.status_code}")
if r4.status_code == 200:
    latest = r4.json()
    print(f"Count: {len(latest)}")
    for l in latest[:5]:
        print(f"  - {l.get('company_name','?')} | {l.get('email','?')} | {l.get('status','?')}")

print("\n=== DONE ===")
