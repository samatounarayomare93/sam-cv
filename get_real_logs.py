import os, requests
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY')
service_id = os.getenv('RENDER_SERVICE_ID')
headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}

# Get latest deploy ID
r = requests.get(f'https://api.render.com/v1/services/{service_id}/deploys?limit=1', headers=headers, timeout=15)
deploys = r.json()
if deploys and isinstance(deploys, list):
    deploy = deploys[0].get('deploy', deploys[0])
    print(f"Latest deploy: {deploy.get('id')} | status: {deploy.get('status')} | {deploy.get('createdAt','')[:19]}")

# Try to get logs via SSE endpoint
print("\nFetching logs...")
try:
    r2 = requests.get(
        f'https://api.render.com/v1/services/{service_id}/logs?limit=100',
        headers={**headers, 'Accept': 'application/json'},
        timeout=20
    )
    print(f"Status: {r2.status_code}")
    if r2.status_code == 200:
        data = r2.json()
        logs = data.get('logs', data) if isinstance(data, dict) else data
        if isinstance(logs, list):
            for log in logs[-50:]:
                ts = log.get('timestamp', '')[:19]
                msg = log.get('message', str(log))[:120]
                print(f"[{ts}] {msg}")
        else:
            print(str(data)[:500])
    else:
        print(r2.text[:300])
except Exception as e:
    print(f"Error: {e}")
