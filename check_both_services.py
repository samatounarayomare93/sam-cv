"""Check both services status."""
import requests, os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY', 'rnd_X4vP0V0M4LOJEGbFiKs2TM72NgTg')
headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}

for sid, name, url in [
    ('srv-d7s6rf6gvqtc73bt431g', 'sam-job-automator', 'https://sam-job-automator.onrender.com'),
    ('srv-d7numa5ckfvc73f9e7pg', 'sam-cv', 'https://sam-cv-bot.onrender.com'),
]:
    r = requests.get(f'https://api.render.com/v1/services/{sid}/deploys?limit=2', headers=headers)
    deps = r.json()
    print(f"\n{name}:")
    for d in deps:
        dep = d.get('deploy', d)
        print(f"  {dep.get('id')} | {dep.get('status')} | {dep.get('commit',{}).get('message','')[:50]}")
    
    # HTTP check
    try:
        resp = requests.get(f'{url}/api/stats', timeout=10)
        print(f"  HTTP /api/stats: {resp.status_code} | {resp.text[:80]}")
    except Exception as e:
        print(f"  HTTP check failed: {e}")
