"""
Clean junk leads from Supabase:
- Fake domains (tech.com, automatically.com, glassdoor.com, etc.)
- No description
- Generic/invalid company names
"""
import requests, os
from dotenv import load_dotenv
load_dotenv()

URL = os.getenv('SUPABASE_URL','').rstrip('/')
KEY = os.getenv('SUPABASE_KEY','')
h = {'apikey': KEY, 'Authorization': f'Bearer {KEY}',
     'Content-Type': 'application/json', 'Prefer': 'return=minimal'}

print("=" * 55)
print("CLEANING JUNK LEADS FROM SUPABASE")
print("=" * 55)

# Junk domains to delete
JUNK_DOMAINS = [
    'tech.com', 'automatically.com', 'glassdoor.com', 'glassdoor.com.mx',
    'linkedin.com', 'indeed.com', 'stackoverflow.com', 'windows.com',
    'google.com', 'microsoft.com', 'apple.com', 'amazon.com',
    'facebook.com', 'twitter.com', 'wikipedia.org', 'youtube.com',
    'zippia.com', 'crunchbase.com', 'monster.com', 'ziprecruiter.com',
    'areaswhereseedfundingisstrong.com', 'doingbusiness.com',
    'newofficelondon.com', 'stravavaluationpowersupto.com',
    'when.com', 'install.com', 'arizona.com', 'word.com',
    'new.com', 'my.com', 'it.com', 'top.com', 'list.com',
    'well.com', 'future.com', 'common.com', 'venture.com',
    'best.com', 'homepage.com', 'home.com', 'wight.com',
    'airedale.com', 'heimdal.com', 'rhodeisland.com',
]

# Junk company name patterns
JUNK_COMPANIES = [
    'areas where seed funding', 'doing business', 'new office london',
    'automatically', 'when ', 'install ', 'arizona ', 'biggest companies',
    'murray company mechanical', 'hensley beverage', 'gulf digest',
    'linkedin recruiter', 'official travel', 'strategic interview',
    'newest questions', 'welcome to windows', 'periodic labs',
    'google hiring', 'understanding companies', 'gulf recruitment',
]

total_deleted = 0

# Delete by junk domain
for domain in JUNK_DOMAINS:
    r = requests.delete(
        f'{URL}/rest/v1/leads?email=like.*@{domain}',
        headers=h, timeout=10
    )
    if r.status_code == 204:
        total_deleted += 1

# Delete leads with no email
r2 = requests.delete(f'{URL}/rest/v1/leads?email=is.null', headers=h, timeout=10)
r3 = requests.delete(f'{URL}/rest/v1/leads?email=eq.', headers=h, timeout=10)

# Delete leads with description = null (from old scraper)
# But keep the ones from auto_queue_refill (they have descriptions)
r4 = requests.delete(f'{URL}/rest/v1/leads?description=is.null&status=eq.pending', headers=h, timeout=10)
print(f"Deleted null-description leads: HTTP {r4.status_code}")

# Check remaining
r5 = requests.get(f'{URL}/rest/v1/leads?status=eq.pending&select=id', headers=h, timeout=10)
print(f"\nPending leads after cleanup: {len(r5.json())}")

# Show sample of remaining leads
r6 = requests.get(f'{URL}/rest/v1/leads?status=eq.pending&select=company_name,email,job_title&limit=10', headers=h, timeout=10)
print("\nSample remaining leads:")
for l in r6.json():
    print(f"  {l.get('company_name','?')} | {l.get('email','?')} | {l.get('job_title','?')}")

print(f"\nTotal junk domains processed: {len(JUNK_DOMAINS)}")
print("Cleanup complete!")
