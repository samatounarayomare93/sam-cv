"""Get Render logs via SSE endpoint"""
import os, requests, json
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY')
service_id = os.getenv('RENDER_SERVICE_ID')

# Get latest deploy ID
headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}
r = requests.get(f'https://api.render.com/v1/services/{service_id}/deploys?limit=1', headers=headers, timeout=15)
dep = r.json()[0].get('deploy', r.json()[0])
deploy_id = dep.get('id')
print(f"Deploy: {deploy_id} | Status: {dep.get('status')}")

# Try SSE logs
sse_headers = {
    'Authorization': f'Bearer {api_key}',
    'Accept': 'text/event-stream',
}

endpoints = [
    f'https://api.render.com/v1/services/{service_id}/logs?tail=100',
    f'https://api.render.com/v1/services/{service_id}/deploys/{deploy_id}/logs',
    f'https://api.render.com/v1/logs?serviceId={service_id}&tail=50',
    f'https://api.render.com/v1/services/{service_id}/events',
]

for ep in endpoints:
    try:
        r = requests.get(ep, headers=sse_headers, timeout=10, stream=False)
        print(f"\n{ep}")
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            content = r.text[:2000]
            print(content)
            break
        else:
            print(r.text[:200])
    except Exception as e:
        print(f"Error: {e}")
