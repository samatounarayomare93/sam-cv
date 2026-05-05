import requests
import os
from dotenv import load_dotenv

load_dotenv()

RENDER_API_KEY = 'rnd_X4vP0V0M4LOJEGbFiKs2TM72NgTg'
SERVICE_ID = 'srv-d7s6rf6gvqtc73bt431g'

headers = {
    'Authorization': f'Bearer {RENDER_API_KEY}',
    'Accept': 'application/json'
}

# Check latest deploy status
r = requests.get(
    f'https://api.render.com/v1/services/{SERVICE_ID}/deploys?limit=1',
    headers=headers, timeout=15
)
if r.status_code == 200:
    deploys = r.json()
    if deploys:
        d = deploys[0].get('deploy', {})
        print(f"Latest deploy: {d.get('id')}")
        print(f"Status: {d.get('status')}")
        print(f"Created: {d.get('createdAt')}")
        print(f"Finished: {d.get('finishedAt')}")

# Check env vars - verify service role key is set
r2 = requests.get(
    f'https://api.render.com/v1/services/{SERVICE_ID}/env-vars',
    headers=headers, timeout=15
)
if r2.status_code == 200:
    vars_list = r2.json()
    print(f"\nTotal env vars: {len(vars_list)}")
    for item in vars_list:
        key = item.get('envVar', {}).get('key', '')
        val = item.get('envVar', {}).get('value', '')
        if 'SUPABASE' in key or 'SERVICE' in key:
            masked = val[:8] + '...' if len(val) > 8 else val
            print(f"  {key} = {masked}")
