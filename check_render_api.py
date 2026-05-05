import requests, os
from dotenv import load_dotenv
load_dotenv()

render_key = os.getenv('RENDER_API_KEY', '')
print(f'Render API key in .env: {"SET - " + render_key[:20] if render_key else "NOT SET"}')

# Try to get services list if key exists
if render_key:
    r = requests.get(
        'https://api.render.com/v1/services',
        headers={'Authorization': f'Bearer {render_key}', 'Accept': 'application/json'},
        timeout=10
    )
    print(f'Services API: {r.status_code}')
    if r.status_code == 200:
        services = r.json()
        for s in services:
            svc = s.get('service', {})
            print(f'  Service: {svc.get("name")} | ID: {svc.get("id")}')
    else:
        print(f'Response: {r.text[:200]}')
else:
    print('Need RENDER_API_KEY to update env vars automatically')
    print('Get it from: dashboard.render.com → Account Settings → API Keys')
