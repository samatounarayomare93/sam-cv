#!/usr/bin/env python3
"""Get Render runtime logs via SSE endpoint."""
import requests, os, json, time
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY')
service_id = os.getenv('RENDER_SERVICE_ID')
headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'text/event-stream'}

print(f"Fetching live logs from Render service {service_id}...\n")

# Try the SSE logs endpoint
try:
    r = requests.get(
        f'https://api.render.com/v1/services/{service_id}/logs',
        headers={'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'},
        params={'limit': 100},
        timeout=15,
        stream=False
    )
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        try:
            data = r.json()
            if isinstance(data, list):
                for item in data[-50:]:
                    if isinstance(item, dict):
                        ts = item.get('timestamp', '')[:19]
                        msg = item.get('message', item.get('text', str(item)[:100]))
                        print(f"{ts} {msg}")
            else:
                print(json.dumps(data, indent=2)[:3000])
        except:
            print(r.text[:3000])
    else:
        print(f"Error: {r.text[:300]}")
except Exception as e:
    print(f"Exception: {e}")

# Try deploy logs
print("\n\n=== TRYING DEPLOY LOGS ===")
headers2 = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}
r2 = requests.get(
    f'https://api.render.com/v1/services/{service_id}/deploys?limit=1',
    headers=headers2, timeout=15
)
if r2.status_code == 200:
    deploys = r2.json()
    if deploys:
        dep = deploys[0].get('deploy', deploys[0])
        dep_id = dep.get('id')
        status = dep.get('status')
        print(f"Latest deploy: {dep_id} | Status: {status}")
        
        # Try to get logs for this deploy
        for endpoint in [
            f'https://api.render.com/v1/services/{service_id}/deploys/{dep_id}/logs',
            f'https://api.render.com/v1/deploys/{dep_id}/logs',
        ]:
            r3 = requests.get(endpoint, headers=headers2, timeout=15)
            print(f"  {endpoint}: {r3.status_code}")
            if r3.status_code == 200:
                try:
                    data = r3.json()
                    lines = data if isinstance(data, list) else data.get('logs', data.get('lines', []))
                    for line in lines[-30:]:
                        if isinstance(line, dict):
                            print(f"  {line.get('timestamp','')[:19]} {line.get('message', line.get('text',''))}")
                        else:
                            print(f"  {str(line)[:150]}")
                except:
                    print(f"  Raw: {r3.text[:1000]}")
                break
