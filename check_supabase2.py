import requests
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SERVICE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', '')

print(f"URL: {SUPABASE_URL}")
print(f"Anon key: {SUPABASE_KEY[:30]}...")
print(f"Service key: {SERVICE_KEY[:30] if SERVICE_KEY else 'NOT SET'}...")

# Try with anon key
headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
}

# Test basic connection
r = requests.get(f'{SUPABASE_URL}/rest/v1/', headers=headers, timeout=10)
print(f"\nBasic connection: {r.status_code}")

# Try leads table
r2 = requests.get(f'{SUPABASE_URL}/rest/v1/leads?limit=5', headers=headers, timeout=10)
print(f"Leads query: {r2.status_code}")
if r2.status_code == 200:
    data = r2.json()
    print(f"  Leads found: {len(data)}")
    for l in data[:3]:
        print(f"  - {l.get('company_name','?')} | {l.get('status','?')}")
elif r2.status_code == 401:
    print(f"  Auth error: {r2.text[:200]}")
elif r2.status_code == 404:
    print("  Table 'leads' does not exist!")
else:
    print(f"  Error: {r2.text[:200]}")

# Try applications table
r3 = requests.get(f'{SUPABASE_URL}/rest/v1/applications?limit=5', headers=headers, timeout=10)
print(f"Applications query: {r3.status_code}")
if r3.status_code == 200:
    data3 = r3.json()
    print(f"  Applications found: {len(data3)}")
    for a in data3[:3]:
        print(f"  - {a.get('company_name','?')} | {a.get('status','?')}")
elif r3.status_code == 404:
    print("  Table 'applications' does not exist!")
else:
    print(f"  Error: {r3.text[:200]}")
