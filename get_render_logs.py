import requests

RENDER_API_KEY = 'rnd_X4vP0V0M4LOJEGbFiKs2TM72NgTg'
SERVICE_ID = 'srv-d7s6rf6gvqtc73bt431g'

headers = {
    'Authorization': f'Bearer {RENDER_API_KEY}',
    'Accept': 'application/json'
}

# Get logs
print("=== RENDER LOGS (last 100 lines) ===")
r = requests.get(
    f'https://api.render.com/v1/services/{SERVICE_ID}/logs?limit=100',
    headers=headers, timeout=15
)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    logs = data.get('logs', [])
    print(f"Log entries: {len(logs)}")
    for log in logs[-50:]:  # Last 50
        print(log.get('message', ''))
else:
    print(f"Error: {r.text[:300]}")
    
    # Try alternative endpoint
    print("\nTrying alternative logs endpoint...")
    r2 = requests.get(
        f'https://api.render.com/v1/logs?serviceId={SERVICE_ID}&limit=100',
        headers=headers, timeout=15
    )
    print(f"Status: {r2.status_code}")
    print(r2.text[:500])
