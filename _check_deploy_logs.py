import os, sys, requests
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()

render_key = os.getenv('RENDER_API_KEY', '')
service_id = os.getenv('RENDER_SERVICE_ID', '')
headers = {'Authorization': f'Bearer {render_key}', 'Accept': 'application/json'}

# Get the failed deploy ID
r = requests.get(f'https://api.render.com/v1/services/{service_id}/deploys?limit=3', headers=headers, timeout=10)
deploys = r.json()

failed = None
for d in deploys:
    dep = d.get('deploy', d)
    if dep.get('status') == 'update_failed':
        failed = dep
        break

if not failed:
    print('No failed deploy found')
    sys.exit(0)

print(f'Failed deploy: {failed.get("id")}')
print(f'Commit: {failed.get("commit", {}).get("message", "N/A") if failed.get("commit") else "N/A"}')
print()

# Get logs for this deploy
deploy_id = failed.get('id')
r2 = requests.get(
    f'https://api.render.com/v1/services/{service_id}/deploys/{deploy_id}/logs',
    headers=headers, timeout=10
)
if r2.status_code == 200:
    logs = r2.json()
    # Print last 50 lines
    lines = logs if isinstance(logs, list) else logs.get('logs', [])
    print(f'Last {min(50, len(lines))} log lines:')
    for line in lines[-50:]:
        if isinstance(line, dict):
            print(line.get('message', line))
        else:
            print(line)
else:
    print(f'Logs API: {r2.status_code} - {r2.text[:300]}')
