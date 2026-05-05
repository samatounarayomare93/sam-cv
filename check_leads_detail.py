import requests
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SERVICE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

headers = {
    'apikey': SERVICE_KEY,
    'Authorization': f'Bearer {SERVICE_KEY}',
    'Content-Type': 'application/json'
}

# Check all lead statuses
r = requests.get(
    f'{SUPABASE_URL}/rest/v1/leads?select=status&limit=1000',
    headers=headers, timeout=15
)
if r.status_code == 200:
    leads = r.json()
    from collections import Counter
    statuses = Counter(l.get('status') for l in leads)
    print("Lead status breakdown:")
    for status, count in sorted(statuses.items(), key=lambda x: -x[1]):
        print(f"  {status}: {count}")
    print(f"  TOTAL: {len(leads)}")

# Check pending leads with email
r2 = requests.get(
    f'{SUPABASE_URL}/rest/v1/leads?status=eq.pending&email=not.is.null&email=neq.&select=company_name,email,job_title&limit=10',
    headers=headers, timeout=15
)
print(f"\nPending leads with email: {r2.status_code}")
if r2.status_code == 200:
    pending = r2.json()
    print(f"Count: {len(pending)}")
    for l in pending[:5]:
        print(f"  - {l.get('company_name')} | {l.get('email')} | {l.get('job_title','')[:30]}")
