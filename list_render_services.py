import os, requests
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY')
headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}

r = requests.get('https://api.render.com/v1/services?limit=20', headers=headers, timeout=15)
services = r.json()

print("ALL RENDER SERVICES:")
print("="*70)
for svc in services:
    s = svc.get('service', svc)
    name = s.get('name', '?')
    sid = s.get('id', '?')
    suspended = s.get('suspended', '?')
    url = s.get('serviceDetails', {}).get('url', '?')
    build_cmd = s.get('serviceDetails', {}).get('envSpecificDetails', {}).get('buildCommand', '?')
    print(f"Name: {name}")
    print(f"  ID: {sid}")
    print(f"  Status: {suspended}")
    print(f"  URL: {url}")
    print(f"  Build: {build_cmd[:60]}")
    print()

# Also check pipeline minutes
print("="*70)
print("Checking pipeline minutes...")
r2 = requests.get('https://api.render.com/v1/owners', headers=headers, timeout=15)
print(f"Owners status: {r2.status_code}")
if r2.status_code == 200:
    import json
    print(json.dumps(r2.json(), indent=2)[:500])
