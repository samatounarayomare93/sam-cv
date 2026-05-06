import os, sys, requests, json
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()

render_key = os.getenv('RENDER_API_KEY', '')
service_id = os.getenv('RENDER_SERVICE_ID', '')
headers = {'Authorization': f'Bearer {render_key}', 'Accept': 'application/json'}

# Try different log endpoints
endpoints = [
    f'https://api.render.com/v1/services/{service_id}/logs?limit=100',
    f'https://api.render.com/v1/logs?serviceId={service_id}&limit=100',
    f'https://api.render.com/v1/services/{service_id}/events?limit=20',
]

for ep in endpoints:
    r = requests.get(ep, headers=headers, timeout=10)
    print(f'GET {ep[-60:]} -> {r.status_code}')
    if r.status_code == 200:
        data = r.json()
        if isinstance(data, list):
            for item in data[-30:]:
                if isinstance(item, dict):
                    msg = item.get('message') or item.get('text') or item.get('type') or str(item)[:100]
                    ts = item.get('timestamp', item.get('createdAt', ''))[:19]
                    print(f'  {ts}  {msg}')
                else:
                    print(f'  {str(item)[:120]}')
        else:
            print(json.dumps(data, indent=2)[:1000])
        break
    print()
