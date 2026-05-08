#!/usr/bin/env python3
"""Force Render to redeploy with latest code."""
import requests, os, time
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY')
service_id = os.getenv('RENDER_SERVICE_ID')
headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json', 'Content-Type': 'application/json'}

print("🚀 Triggering manual redeploy on Render...")

r = requests.post(
    f'https://api.render.com/v1/services/{service_id}/deploys',
    headers=headers,
    json={"clearCache": "do_not_clear"},
    timeout=15
)

if r.status_code in (200, 201):
    data = r.json()
    dep = data.get('deploy', data)
    print(f"✅ Deploy triggered!")
    print(f"   ID: {dep.get('id')}")
    print(f"   Status: {dep.get('status')}")
    print(f"\n⏳ Waiting for deploy to complete (usually 2-3 minutes)...")
    
    dep_id = dep.get('id')
    for i in range(20):
        time.sleep(15)
        r2 = requests.get(
            f'https://api.render.com/v1/services/{service_id}/deploys?limit=1',
            headers=headers, timeout=15
        )
        if r2.status_code == 200:
            deploys = r2.json()
            if deploys:
                latest = deploys[0].get('deploy', deploys[0])
                status = latest.get('status', 'unknown')
                print(f"   [{i*15}s] Status: {status}")
                if status == 'live':
                    print(f"\n✅ DEPLOY COMPLETE! Bot is live with new code.")
                    print(f"   Now test via Telegram: send samsalameh.cv@gmail.com")
                    break
                elif status in ('failed', 'canceled'):
                    print(f"\n❌ Deploy {status}!")
                    break
else:
    print(f"❌ Failed to trigger deploy: {r.status_code} - {r.text[:300]}")
