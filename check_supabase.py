import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json'
}

print("=== SUPABASE DATABASE CHECK ===\n")

# Check leads table
r = requests.get(f'{SUPABASE_URL}/rest/v1/leads?select=count&limit=1',
    headers={**headers, 'Prefer': 'count=exact'}, timeout=10)
print(f"Leads table: {r.status_code}")
if r.status_code == 200:
    count = r.headers.get('content-range', 'unknown')
    print(f"  Total leads: {count}")

# Check applications table  
r2 = requests.get(f'{SUPABASE_URL}/rest/v1/applications?select=count&limit=1',
    headers={**headers, 'Prefer': 'count=exact'}, timeout=10)
print(f"Applications table: {r2.status_code}")
if r2.status_code == 200:
    count2 = r2.headers.get('content-range', 'unknown')
    print(f"  Total applications: {count2}")

# Check recent leads (last 24h)
yesterday = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
r3 = requests.get(
    f'{SUPABASE_URL}/rest/v1/leads?select=company_name,job_title,status,created_at&order=created_at.desc&limit=10',
    headers=headers, timeout=10)
print(f"\nRecent leads: {r3.status_code}")
if r3.status_code == 200:
    leads = r3.json()
    if leads:
        for l in leads[:5]:
            print(f"  {l.get('company_name','?')} | {l.get('status','?')} | {l.get('created_at','?')[:19]}")
    else:
        print("  NO LEADS IN DATABASE!")

# Check pending leads
r4 = requests.get(
    f'{SUPABASE_URL}/rest/v1/leads?select=company_name,status&status=eq.pending&limit=10',
    headers=headers, timeout=10)
print(f"\nPending leads: {r4.status_code}")
if r4.status_code == 200:
    pending = r4.json()
    print(f"  Count: {len(pending)}")
    for p in pending[:5]:
        print(f"  {p.get('company_name','?')}")

# Check bot_nodes (leadership)
r5 = requests.get(f'{SUPABASE_URL}/rest/v1/bot_nodes?select=*&limit=5',
    headers=headers, timeout=10)
print(f"\nBot nodes: {r5.status_code}")
if r5.status_code == 200:
    nodes = r5.json()
    print(f"  Active nodes: {len(nodes)}")
    for n in nodes:
        print(f"  Node: {n.get('node_id','?')} | Leader: {n.get('is_leader','?')} | Last seen: {str(n.get('last_heartbeat','?'))[:19]}")

print("\n=== CHECK COMPLETE ===")
