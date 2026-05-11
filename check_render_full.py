import os, requests, json
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY')
service_id = os.getenv('RENDER_SERVICE_ID')
headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}

print("="*60)
print("RENDER FULL DIAGNOSTIC")
print("="*60)

# 1. Service details
r = requests.get(f'https://api.render.com/v1/services/{service_id}', headers=headers, timeout=15)
svc = r.json()
print(f"\nService: {svc.get('name')}")
print(f"Status: {svc.get('suspended')}")
print(f"Build command: {svc.get('serviceDetails',{}).get('envSpecificDetails',{}).get('buildCommand','?')}")
print(f"Start command: {svc.get('serviceDetails',{}).get('envSpecificDetails',{}).get('startCommand','?')}")

# 2. Latest deploys with timing
r2 = requests.get(f'https://api.render.com/v1/services/{service_id}/deploys?limit=5', headers=headers, timeout=15)
deploys = r2.json()
print(f"\nLatest deploys:")
for dep in deploys:
    d = dep.get('deploy', dep)
    started = d.get('startedAt','?')
    finished = d.get('finishedAt','?')
    # Calculate duration
    if started and finished and started != '?' and finished != '?':
        from datetime import datetime
        try:
            s = datetime.fromisoformat(started.replace('Z','+00:00'))
            f = datetime.fromisoformat(finished.replace('Z','+00:00'))
            duration = (f - s).total_seconds()
        except:
            duration = 0
    else:
        duration = 0
    print(f"  {d.get('status','?'):15} | {duration:.0f}s | {d.get('commit',{}).get('message','?')[:50]}")

# 3. Check if there's a deploy hook or auto-deploy issue
print(f"\nAuto deploy: {svc.get('autoDeploy')}")
print(f"Auto deploy trigger: {svc.get('autoDeployTrigger')}")
print(f"Branch: {svc.get('branch')}")
print(f"Repo: {svc.get('repo')}")

# 4. Try to manually trigger a deploy
print("\nTriggering manual deploy...")
r3 = requests.post(
    f'https://api.render.com/v1/services/{service_id}/deploys',
    headers={**headers, 'Content-Type': 'application/json'},
    json={"clearCache": "do_not_clear"},
    timeout=15
)
print(f"Trigger status: {r3.status_code}")
if r3.status_code in (200, 201):
    dep_data = r3.json()
    new_dep = dep_data.get('deploy', dep_data)
    print(f"New deploy ID: {new_dep.get('id')}")
    print(f"Status: {new_dep.get('status')}")
else:
    print(f"Error: {r3.text[:200]}")
