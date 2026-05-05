"""Fix stuck leads in Supabase - mark them as processed so bot can move on"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SERVICE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', SUPABASE_KEY)

headers = {
    'apikey': SERVICE_KEY,
    'Authorization': f'Bearer {SERVICE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=representation'
}

print("=== FIXING STUCK LEADS ===\n")

# 1. Check what's pending
r = requests.get(
    f'{SUPABASE_URL}/rest/v1/leads?select=id,company_name,status&status=eq.pending&limit=20',
    headers=headers, timeout=15
)
print(f"Pending leads query: {r.status_code}")
if r.status_code == 200:
    pending = r.json()
    print(f"Found {len(pending)} pending leads:")
    for l in pending[:10]:
        print(f"  - {l.get('company_name','?')} (id: {l.get('id','?')})")
    
    if pending:
        # Mark all pending as 'stale' so bot stops retrying them
        r2 = requests.patch(
            f'{SUPABASE_URL}/rest/v1/leads?status=eq.pending',
            headers=headers,
            json={"status": "stale_reset"},
            timeout=15
        )
        print(f"\nReset pending leads: {r2.status_code}")
        if r2.status_code in (200, 204):
            print(f"✅ Cleared {len(pending)} stuck leads!")
        else:
            print(f"Error: {r2.text[:200]}")
else:
    print(f"Error: {r.status_code} - {r.text[:200]}")

# 2. Check total leads count
r3 = requests.get(
    f'{SUPABASE_URL}/rest/v1/leads?select=status',
    headers={**headers, 'Prefer': 'count=exact'},
    timeout=15
)
print(f"\nTotal leads: {r3.headers.get('content-range', 'unknown')}")

print("\n=== DONE ===")
print("Bot will now find new leads instead of retrying stuck ones")
