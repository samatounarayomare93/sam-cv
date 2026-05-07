#!/usr/bin/env python3
"""Get latest Render logs to diagnose why hourly rate is 0."""
import requests, os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY')
service_id = os.getenv('RENDER_SERVICE_ID')
headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}

# Get latest deploy ID
r = requests.get(f'https://api.render.com/v1/services/{service_id}/deploys?limit=1', headers=headers, timeout=15)
deploys = r.json()
if not deploys:
    print('No deploys found')
    exit()

dep = deploys[0].get('deploy', deploys[0])
deploy_id = dep.get('id')
print(f'Latest deploy: {deploy_id} | Status: {dep.get("status")}')

# Get deploy logs
r2 = requests.get(
    f'https://api.render.com/v1/services/{service_id}/deploys/{deploy_id}/logs',
    headers=headers, timeout=15
)
if r2.status_code == 200:
    logs = r2.json()
    print(f'\n=== DEPLOY LOGS (last 50 lines) ===')
    lines = logs if isinstance(logs, list) else logs.get('logs', [])
    for line in lines[-50:]:
        if isinstance(line, dict):
            print(line.get('message', line))
        else:
            print(line)
else:
    print(f'Logs error: {r2.status_code} - {r2.text[:300]}')
    
    # Try alternative: get service logs
    r3 = requests.get(
        f'https://api.render.com/v1/services/{service_id}/logs?limit=100',
        headers=headers, timeout=15
    )
    if r3.status_code == 200:
        data = r3.json()
        print('\n=== SERVICE LOGS ===')
        lines = data if isinstance(data, list) else data.get('logs', [])
        for line in lines[-50:]:
            if isinstance(line, dict):
                print(f"{line.get('timestamp','')[:19]} {line.get('message','')}")
            else:
                print(line)
    else:
        print(f'Service logs error: {r3.status_code} - {r3.text[:200]}')
