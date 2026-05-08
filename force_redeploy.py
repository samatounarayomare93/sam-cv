#!/usr/bin/env python3
"""Force Render to redeploy with latest code."""
import requests, os, time, sys
from dotenv import load_dotenv

# [🛡️ WINDOWS UTF-8 FIX]
if sys.platform == 'win32':
    import io
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

api_key = os.getenv('RENDER_API_KEY')
service_id = os.getenv('RENDER_SERVICE_ID')
headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json', 'Content-Type': 'application/json'}

print("[INFO] Triggering manual redeploy on Render...")

r = requests.post(
    f'https://api.render.com/v1/services/{service_id}/deploys',
    headers=headers,
    json={"clearCache": "do_not_clear"},
    timeout=15
)

if r.status_code in (200, 201, 202):
    try:
        data = r.json()
        dep = data.get('deploy', data)
        print(f"[OK] Deploy triggered!")
        print(f"   ID: {dep.get('id')}")
        print(f"   Status: {dep.get('status')}")
    except:
        print(f"[OK] Deploy triggered (Status: {r.status_code})")
    
    print(f"\n[WAIT] Waiting for deploy to complete (usually 2-3 minutes)...")
    
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
                    print(f"\n[SUCCESS] DEPLOY COMPLETE! Bot is live with new code.")
                    print(f"   Now test via Telegram.")
                    break
                elif status in ('failed', 'canceled'):
                    print(f"\n[ERROR] Deploy {status}!")
                    break
else:
    print(f"[ERROR] Failed to trigger deploy: {r.status_code} - {r.text[:300]}")
