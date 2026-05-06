import os, sys, requests
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()

render_key = os.getenv('RENDER_API_KEY', '')
service_id = os.getenv('RENDER_SERVICE_ID', '')

if not render_key or not service_id:
    print('ERROR: RENDER_API_KEY or RENDER_SERVICE_ID not set')
    sys.exit(1)

headers = {'Authorization': f'Bearer {render_key}', 'Accept': 'application/json'}

# 1. Service status
r = requests.get(f'https://api.render.com/v1/services/{service_id}', headers=headers, timeout=10)
if r.status_code == 200:
    svc = r.json().get('service', r.json())
    name = svc.get('name', '?')
    suspended = svc.get('suspended', '?')
    url = svc.get('serviceDetails', {}).get('url', 'N/A')
    print(f'Service:   {name}')
    print(f'Suspended: {suspended}')
    print(f'URL:       {url}')
else:
    print(f'Service API error: {r.status_code} - {r.text[:100]}')

print()

# 2. Latest deploys
r2 = requests.get(f'https://api.render.com/v1/services/{service_id}/deploys?limit=5', headers=headers, timeout=10)
if r2.status_code == 200:
    deploys = r2.json()
    print('Latest deploys:')
    for d in deploys:
        dep = d.get('deploy', d)
        did = dep.get('id', '?')[:12]
        status = dep.get('status', '?')
        created = dep.get('createdAt', '?')[:19]
        commit = dep.get('commit', {}).get('message', 'N/A')[:50] if dep.get('commit') else 'N/A'
        print(f'  [{status:12}] {created}  {did}  {commit}')
else:
    print(f'Deploys API error: {r2.status_code}')

print()

# 3. Ping the live URL
try:
    ping = requests.get('https://sam-cv-bot.onrender.com', timeout=15)
    print(f'Live ping: HTTP {ping.status_code} - Bot is {"ONLINE ✅" if ping.status_code == 200 else "responding"}')
except Exception as e:
    print(f'Live ping FAILED: {e}')
