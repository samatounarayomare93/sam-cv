"""Fast cleanup of junk leads"""
import requests, os
from dotenv import load_dotenv
load_dotenv()

URL = os.getenv('SUPABASE_URL','').rstrip('/')
KEY = os.getenv('SUPABASE_KEY','')
h = {'apikey': KEY, 'Authorization': f'Bearer {KEY}',
     'Content-Type': 'application/json', 'Prefer': 'return=minimal'}

print("Cleaning junk leads...")

# Delete leads with null description (old scraper garbage)
r1 = requests.delete(f'{URL}/rest/v1/leads?description=is.null', headers=h, timeout=15)
print(f"Deleted null-description: HTTP {r1.status_code}")

# Delete leads with fake/generic emails
for domain in ['tech.com', 'automatically.com', 'glassdoor.com', 'linkedin.com',
               'indeed.com', 'google.com', 'microsoft.com', 'wikipedia.org',
               'areaswhereseedfundingisstrong.com', 'doingbusiness.com',
               'when.com', 'install.com', 'word.com', 'new.com', 'my.com']:
    r = requests.delete(f'{URL}/rest/v1/leads?email=like.*%40{domain}', headers=h, timeout=8)

# Check remaining
r2 = requests.get(f'{URL}/rest/v1/leads?status=eq.pending&select=id', headers=h, timeout=10)
print(f"Pending leads after cleanup: {len(r2.json())}")

# Show sample
r3 = requests.get(f'{URL}/rest/v1/leads?status=eq.pending&select=company_name,email,job_title&limit=5', headers=h, timeout=10)
print("\nSample:")
for l in r3.json():
    print(f"  {l.get('company_name','?')} | {l.get('email','?')}")

print("Done!")
