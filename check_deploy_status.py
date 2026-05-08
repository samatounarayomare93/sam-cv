#!/usr/bin/env python3
import requests, os, time
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY')
service_id = os.getenv('RENDER_SERVICE_ID')
headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}

time.sleep(3)
r = requests.get(f'https://api.render.com/v1/services/{service_id}/deploys?limit=3', headers=headers, timeout=15)
deploys = r.json()
print("Latest deploys:")
for d in deploys[:3]:
    dep = d.get('deploy', d)
    dep_id = dep.get('id', 'N/A')
    status = dep.get('status', 'N/A')
    created = dep.get('createdAt', 'N/A')[:19]
    print(f"  {dep_id} | {status} | {created}")
