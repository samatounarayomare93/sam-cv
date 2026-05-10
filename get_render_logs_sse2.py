"""Get Render logs via SSE endpoint."""
import requests
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY', 'rnd_X4vP0V0M4LOJEGbFiKs2TM72NgTg')
headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'text/event-stream'}

# Try the logs endpoint for sam-job-automator
service_id = 'srv-d7s6rf6gvqtc73bt431g'
service_id2 = 'srv-d7numa5ckfvc73f9e7pg'  # sam-cv

for sid, name in [(service_id, 'sam-job-automator'), (service_id2, 'sam-cv')]:
    print(f"\n{'='*60}")
    print(f"SERVICE: {name} ({sid})")
    print('='*60)
    
    # Try different log endpoints
    endpoints = [
        f'https://api.render.com/v1/services/{sid}/logs?limit=100',
        f'https://api.render.com/v1/logs?serviceId={sid}&limit=100',
        f'https://api.render.com/v1/services/{sid}/events?limit=20',
    ]
    
    for url in endpoints:
        r = requests.get(url, headers={'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}, timeout=10)
        print(f"\nURL: {url}")
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            try:
                data = r.json()
                if isinstance(data, list):
                    print(f"Items: {len(data)}")
                    for item in data[-20:]:
                        if isinstance(item, dict):
                            # Try to extract useful info
                            text = item.get('text') or item.get('message') or item.get('details') or str(item)[:100]
                            ts = item.get('timestamp') or item.get('createdAt') or ''
                            print(f"  [{ts}] {text[:120]}")
                elif isinstance(data, dict):
                    print(str(data)[:500])
            except:
                print(r.text[:500])
        else:
            print(r.text[:200])
