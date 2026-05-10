"""Get Render deploy logs for both failing services."""
import requests
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY', 'rnd_X4vP0V0M4LOJEGbFiKs2TM72NgTg')
headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}

# Get all services
r = requests.get('https://api.render.com/v1/services?limit=20', headers=headers)
services = r.json()

print("=== ALL SERVICES ===")
service_ids = {}
for s in services:
    svc = s.get('service', s)
    name = svc.get('name', 'unknown')
    sid = svc.get('id', '')
    print(f"  {name}: {sid}")
    service_ids[name] = sid

print("\n=== LATEST DEPLOYS ===")
for name, sid in service_ids.items():
    if not sid:
        continue
    r2 = requests.get(f'https://api.render.com/v1/services/{sid}/deploys?limit=3', headers=headers)
    deploys = r2.json()
    print(f"\n--- {name} ---")
    for d in deploys:
        dep = d.get('deploy', d)
        dep_id = dep.get('id', '')
        status = dep.get('status', '')
        commit = dep.get('commit', {})
        msg = commit.get('message', '')[:60] if commit else ''
        print(f"  Deploy {dep_id}: {status} | {msg}")

        # Try to get build logs
        if status in ('build_failed', 'update_failed', 'deactivated', 'live'):
            log_r = requests.get(
                f'https://api.render.com/v1/services/{sid}/deploys/{dep_id}/logs',
                headers=headers
            )
            if log_r.status_code == 200:
                logs = log_r.json()
                print(f"  LOGS ({len(logs)} lines):")
                # Show last 30 lines
                for line in logs[-30:]:
                    print(f"    {line.get('timestamp','')} {line.get('text','')}")
            else:
                print(f"  Log fetch: {log_r.status_code} {log_r.text[:200]}")
