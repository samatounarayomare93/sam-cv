#!/usr/bin/env python3
"""Check Render deployment status."""
import requests, os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY')
service_id = os.getenv('RENDER_SERVICE_ID')

headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}

# Check service
r = requests.get(f'https://api.render.com/v1/services/{service_id}', headers=headers, timeout=15)
if r.status_code == 200:
    svc = r.json()
    name = svc.get('name', '?')
    suspended = svc.get('suspended', '?')
    url = svc.get('serviceDetails', {}).get('url', 'N/A')
    print(f'[OK] Service: {name}')
    print(f'[OK] Suspended: {suspended}')
    print(f'[OK] URL: {url}')
else:
    print(f'[ERR] Service check: {r.status_code} - {r.text[:200]}')

# Check latest deploys
r2 = requests.get(f'https://api.render.com/v1/services/{service_id}/deploys?limit=5', headers=headers, timeout=15)
if r2.status_code == 200:
    deploys = r2.json()
    print(f'\nLatest {len(deploys)} deploys:')
    for item in deploys:
        dep = item.get('deploy', item)
        did = dep.get('id', '?')
        status = dep.get('status', '?')
        created = dep.get('createdAt', '?')[:19]
        commit = dep.get('commit', {})
        msg = commit.get('message', '')[:50] if commit else ''
        print(f'  {did} | {status} | {created} | {msg}')
else:
    print(f'[ERR] Deploys: {r2.status_code}')
