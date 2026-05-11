import os, requests
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY')
service_id = os.getenv('RENDER_SERVICE_ID')
headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}

print(f"Checking service: {service_id}")
r = requests.get(f'https://api.render.com/v1/services/{service_id}/deploys?limit=5', headers=headers, timeout=15)
data = r.json()

if isinstance(data, list):
    print("Deploys:")
    for item in data:
        if isinstance(item, dict):
            d = item.get('deploy', item)
            started = d.get('startedAt', '')
            finished = d.get('finishedAt', '')
            duration = 0
            if started and finished:
                from datetime import datetime
                try:
                    s = datetime.fromisoformat(started.replace('Z', '+00:00'))
                    f = datetime.fromisoformat(finished.replace('Z', '+00:00'))
                    duration = (f - s).total_seconds()
                except Exception:
                    pass
            status = d.get('status', '?')
            msg = d.get('commit', {}).get('message', '?')[:40] if isinstance(d.get('commit'), dict) else '?'
            print(f"  {status:20} | {duration:.0f}s | {msg}")
else:
    print(f"Response: {data}")

# Check URL
print("\nChecking URL: https://sam-bot-v2.onrender.com")
try:
    r2 = requests.get('https://sam-bot-v2.onrender.com', timeout=20)
    print(f"HTTP: {r2.status_code}")
    if r2.status_code == 200:
        print("SERVICE IS LIVE!")
except Exception as e:
    print(f"Not ready yet: {str(e)[:60]}")
