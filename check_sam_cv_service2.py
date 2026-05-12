import os, requests, json
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY')
# sam-cv service
service_id = 'srv-d7numa5ckfvc73f9e7pg'
headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}

print("SAM-CV SERVICE STATUS:")
r = requests.get(f'https://api.render.com/v1/services/{service_id}', headers=headers, timeout=15)
svc = r.json()
print(f"Name: {svc.get('name')}")
print(f"Status: {svc.get('suspended')}")
print(f"URL: {svc.get('serviceDetails',{}).get('url')}")
print(f"Repo: {svc.get('repo')}")
print(f"Branch: {svc.get('branch')}")

print("\nLatest deploys:")
r2 = requests.get(f'https://api.render.com/v1/services/{service_id}/deploys?limit=5', headers=headers, timeout=15)
for dep in r2.json():
    d = dep.get('deploy', dep)
    started = d.get('startedAt','?')
    finished = d.get('finishedAt','?')
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

# Check if it's live
print("\nChecking if service is responding...")
try:
    r3 = requests.get('https://sam-cv-bot.onrender.com', timeout=15)
    print(f"HTTP Status: {r3.status_code}")
    print(f"Response: {r3.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

# Check events for pipeline minutes
print("\nChecking events...")
r4 = requests.get(f'https://api.render.com/v1/services/{service_id}/events?limit=5', headers=headers, timeout=15)
if r4.status_code == 200:
    for evt in r4.json()[:5]:
        e = evt.get('event', evt)
        print(f"  {e.get('type')} | {e.get('timestamp','?')[:19]}")
