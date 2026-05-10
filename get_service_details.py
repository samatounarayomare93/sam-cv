"""Get full details of both failing services."""
import requests, os, json
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY', 'rnd_X4vP0V0M4LOJEGbFiKs2TM72NgTg')
headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}

for sid, name in [
    ('srv-d7s6rf6gvqtc73bt431g', 'sam-job-automator'),
    ('srv-d7numa5ckfvc73f9e7pg', 'sam-cv'),
]:
    print(f"\n{'='*60}")
    print(f"SERVICE: {name}")
    print('='*60)
    r = requests.get(f'https://api.render.com/v1/services/{sid}', headers=headers)
    svc = r.json().get('service', r.json())
    print(f"  Type: {svc.get('type')}")
    print(f"  Status: {svc.get('suspended')}")
    print(f"  URL: {svc.get('serviceDetails', {}).get('url', 'N/A')}")
    
    # Get env vars (just keys, not values)
    env_r = requests.get(f'https://api.render.com/v1/services/{sid}/env-vars', headers=headers)
    if env_r.status_code == 200:
        env_data = env_r.json()
        keys = [e.get('envVar', {}).get('key', '') for e in env_data if isinstance(e, dict)]
        print(f"  Env vars ({len(keys)}): {keys[:10]}")
    
    # Get latest deploy details
    dep_r = requests.get(f'https://api.render.com/v1/services/{sid}/deploys?limit=1', headers=headers)
    deps = dep_r.json()
    if deps:
        dep = deps[0].get('deploy', deps[0])
        print(f"  Latest deploy: {dep.get('id')} | {dep.get('status')}")
        reason = dep.get('finishedAt') or dep.get('updatedAt')
        print(f"  Finished: {reason}")
        # Check for error details
        details = dep.get('details') or dep.get('error') or ''
        if details:
            print(f"  Error: {details}")
