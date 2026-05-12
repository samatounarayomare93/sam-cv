"""Check leads and applications status in Supabase"""
import requests, os
from dotenv import load_dotenv
load_dotenv()

URL = os.getenv('SUPABASE_URL','').rstrip('/')
KEY = os.getenv('SUPABASE_KEY','')
h = {'apikey': KEY, 'Authorization': f'Bearer {KEY}', 'Accept': 'application/json'}

print("=" * 55)
print("SUPABASE STATUS CHECK")
print("=" * 55)

# Check pending leads
r = requests.get(f'{URL}/rest/v1/leads?status=eq.pending&select=company_name,email,job_title,description&limit=5', headers=h, timeout=10)
leads = r.json()
print(f"\nSample pending leads ({len(leads)} shown):")
for l in leads:
    cn = l.get('company_name', '?')
    em = l.get('email', '?')
    jt = l.get('job_title', '?')
    desc = str(l.get('description', ''))[:80]
    print(f"  {cn} | {em} | {jt}")
    print(f"  desc: {desc}")

# Count by status
for status in ['pending', 'sent', 'rejected', 'no_contact', 'error']:
    r2 = requests.get(f'{URL}/rest/v1/leads?status=eq.{status}&select=id', headers=h, timeout=10)
    count = len(r2.json())
    print(f"\nLeads [{status}]: {count}")

# Applications
r3 = requests.get(f'{URL}/rest/v1/applications?select=company_name,job_title,timestamp&order=timestamp.desc&limit=5', headers=h, timeout=10)
apps = r3.json()
print(f"\nLatest applications ({len(apps)} shown):")
for a in apps:
    print(f"  {a.get('company_name','?')} | {a.get('job_title','?')} | {a.get('timestamp','?')[:19]}")

# Total applications
r4 = requests.get(f'{URL}/rest/v1/applications?select=id', headers=h, timeout=10)
print(f"\nTotal applications ever sent: {len(r4.json())}")
