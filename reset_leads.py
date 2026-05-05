"""Reset rate_limited leads so bot can retry them"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SERVICE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

headers = {
    'apikey': SERVICE_KEY,
    'Authorization': f'Bearer {SERVICE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=representation'
}

print("=== RESETTING LEADS ===\n")

# Count rate_limited leads
r = requests.get(f'{SUPABASE_URL}/rest/v1/leads?status=eq.rate_limited&select=id',
    headers={**headers, 'Prefer': 'count=exact'}, timeout=10)
count = r.headers.get('content-range', '0/0').split('/')[-1]
print(f"Rate-limited leads: {count}")

# Reset rate_limited → pending
r2 = requests.patch(
    f'{SUPABASE_URL}/rest/v1/leads?status=eq.rate_limited',
    headers=headers,
    json={"status": "pending"},
    timeout=15
)
print(f"Reset rate_limited: {r2.status_code}")

# Count circadian_hold leads
r3 = requests.get(f'{SUPABASE_URL}/rest/v1/leads?status=eq.circadian_hold&select=id',
    headers={**headers, 'Prefer': 'count=exact'}, timeout=10)
count3 = r3.headers.get('content-range', '0/0').split('/')[-1]
print(f"Circadian hold leads: {count3}")

# Reset circadian_hold → pending
r4 = requests.patch(
    f'{SUPABASE_URL}/rest/v1/leads?status=eq.circadian_hold',
    headers=headers,
    json={"status": "pending"},
    timeout=15
)
print(f"Reset circadian_hold: {r4.status_code}")

# Check new pending count
r5 = requests.get(f'{SUPABASE_URL}/rest/v1/leads?status=eq.pending&select=id',
    headers={**headers, 'Prefer': 'count=exact'}, timeout=10)
new_count = r5.headers.get('content-range', '0/0').split('/')[-1]
print(f"\nNew pending leads: {new_count}")
print("✅ Bot will now process these leads!")
