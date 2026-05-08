#!/usr/bin/env python3
"""Get Render logs using the correct API endpoint."""
import requests, os, json
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY')
service_id = os.getenv('RENDER_SERVICE_ID')
headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}

print(f"Service ID: {service_id}")

# Try the correct logs endpoint
endpoints = [
    f'https://api.render.com/v1/services/{service_id}/logs',
    f'https://api.render.com/v1/logs?serviceId={service_id}&limit=100',
    f'https://api.render.com/v1/services/{service_id}/events',
]

for url in endpoints:
    print(f"\nTrying: {url}")
    r = requests.get(url, headers=headers, timeout=15)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"Response type: {type(data)}")
        if isinstance(data, list):
            print(f"Items: {len(data)}")
            for item in data[-20:]:
                if isinstance(item, dict):
                    msg = item.get('message', item.get('text', str(item)[:100]))
                    ts = item.get('timestamp', item.get('time', ''))[:19]
                    print(f"  {ts} {msg}")
        elif isinstance(data, dict):
            print(json.dumps(data, indent=2)[:2000])
        break
    else:
        print(f"Error: {r.text[:200]}")

# Also check service status
print("\n\n=== SERVICE STATUS ===")
r = requests.get(f'https://api.render.com/v1/services/{service_id}', headers=headers, timeout=15)
if r.status_code == 200:
    svc = r.json()
    service = svc.get('service', svc)
    print(f"Name: {service.get('name')}")
    print(f"Status: {service.get('suspended', 'unknown')}")
    print(f"URL: {service.get('serviceDetails', {}).get('url', 'N/A')}")
    print(f"Type: {service.get('type')}")
    print(f"Created: {service.get('createdAt', '')[:19]}")
    print(f"Updated: {service.get('updatedAt', '')[:19]}")
else:
    print(f"Error: {r.status_code} - {r.text[:200]}")
