import os, requests
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY')
# sam-cv service (different from sam-job-automator)
service_id = 'srv-d7numa5ckfvc73f9e7pg'
headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}

print("SAM-CV SERVICE DEPLOYS:")
r = requests.get(f'https://api.render.com/v1/services/{service_id}/deploys?limit=10', headers=headers, timeout=15)
deploys = r.json()
for dep in deploys:
    d = dep.get('deploy', dep)
    started = d.get('startedAt', '')
    finished = d.get('finishedAt', '')
    duration = 0
    if started and finished:
        from datetime import datetime
        try:
            s = datetime.fromisoformat(started.replace('Z', '+00:00'))
            f = datetime.fromisoformat(finished.replace('Z', '+00:00'))
            duration = (f - s).total_seconds()
        except Exception:
            pass
    status = d.get('status', '?')
    msg = d.get('commit', {}).get('message', '?')[:50]
    print(f"  {status:20} | {duration:.0f}s | {msg}")

# Check events for pipeline_minutes_exhausted
print("\nEvents:")
r2 = requests.get(f'https://api.render.com/v1/services/{service_id}/events?limit=10', headers=headers, timeout=15)
if r2.status_code == 200:
    for evt in r2.json()[:10]:
        e = evt.get('event', evt)
        print(f"  {e.get('type')} | {e.get('timestamp','?')[:19]}")
