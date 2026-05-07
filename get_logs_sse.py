#!/usr/bin/env python3
"""Get Render logs via SSE streaming endpoint."""
import requests, os, json, time
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY')
service_id = os.getenv('RENDER_SERVICE_ID')

headers = {
    'Authorization': f'Bearer {api_key}',
    'Accept': 'text/event-stream',
}

print(f"Fetching logs for service {service_id}...")
print("=" * 60)

try:
    # Try the SSE logs endpoint
    r = requests.get(
        f'https://api.render.com/v1/services/{service_id}/logs-stream',
        headers=headers,
        stream=True,
        timeout=15
    )
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        count = 0
        for line in r.iter_lines(decode_unicode=True):
            if line and count < 100:
                print(line)
                count += 1
    else:
        print(r.text[:500])
except Exception as e:
    print(f"SSE error: {e}")

# Try alternative endpoint
print("\nTrying alternative endpoint...")
try:
    r2 = requests.get(
        f'https://api.render.com/v1/services/{service_id}/events?limit=20',
        headers={'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'},
        timeout=15
    )
    print(f"Events status: {r2.status_code}")
    if r2.status_code == 200:
        events = r2.json()
        for e in events:
            print(f"  {e.get('createdAt','')[:19]} | {e.get('type','?')} | {str(e.get('details',''))[:80]}")
    else:
        print(r2.text[:300])
except Exception as e:
    print(f"Events error: {e}")
