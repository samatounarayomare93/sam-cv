"""Check today's applications and system status"""
import requests, os
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()

URL = os.getenv('SUPABASE_URL','').rstrip('/')
KEY = os.getenv('SUPABASE_KEY','')
h = {'apikey': KEY, 'Authorization': f'Bearer {KEY}', 'Accept': 'application/json'}

today = datetime.now(timezone.utc).strftime('%Y-%m-%dT00:00:00')

# Today's applications
r = requests.get(
    f'{URL}/rest/v1/applications?select=company_name,job_title,timestamp'
    f'&timestamp=gte.{today}&order=timestamp.desc&limit=50',
    headers=h, timeout=10
)
apps = r.json() if r.status_code == 200 else []
print(f'Applications today: {len(apps)}')
for a in apps[:10]:
    cn = a.get('company_name', '?')
    jt = a.get('job_title', '?')
    ts = a.get('timestamp', '?')[:19]
    print(f'  {cn} | {jt} | {ts}')

# Total (real count from Supabase)
h_count = {**h, 'Prefer': 'count=exact'}
r2 = requests.get(f'{URL}/rest/v1/applications?select=id&limit=1', headers=h_count, timeout=10)
cr = r2.headers.get('Content-Range', '0-0/0')
total = cr.split('/')[-1]
print(f'\nTotal applications ever: {total}')

# Leads by status
for status in ['pending', 'processed', 'rejected', 'rate_limited', 'no_contact']:
    r3 = requests.get(f'{URL}/rest/v1/leads?status=eq.{status}&select=id', headers=h, timeout=8)
    count = len(r3.json()) if r3.status_code == 200 else 0
    if count > 0:
        print(f'Leads [{status}]: {count}')

# Brevo credits
brevo_key = os.getenv('BREVO_API_KEY', '')
r4 = requests.get('https://api.brevo.com/v3/account', headers={'api-key': brevo_key}, timeout=8)
if r4.status_code == 200:
    plan = r4.json().get('plan', [{}])
    credits = plan[0].get('credits', '?') if plan else '?'
    print(f'\nBrevo credits remaining today: {credits}/300')
