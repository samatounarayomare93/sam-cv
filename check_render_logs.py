import requests

RENDER_API_KEY = 'rnd_X4vP0V0M4LOJEGbFiKs2TM72NgTg'
SERVICE_ID = 'srv-d7s6rf6gvqtc73bt431g'

headers = {
    'Authorization': f'Bearer {RENDER_API_KEY}',
    'Accept': 'application/json'
}

# Get latest deploy status
print("=== LATEST DEPLOY STATUS ===")
r = requests.get(
    f'https://api.render.com/v1/services/{SERVICE_ID}/deploys?limit=3',
    headers=headers, timeout=15
)
if r.status_code == 200:
    deploys = r.json()
    for d in deploys:
        deploy = d.get('deploy', {})
        print(f"Deploy: {deploy.get('id')}")
        print(f"  Status: {deploy.get('status')}")
        print(f"  Created: {deploy.get('createdAt')}")
        print(f"  Finished: {deploy.get('finishedAt')}")
        print()

# Get service status
print("=== SERVICE STATUS ===")
r2 = requests.get(
    f'https://api.render.com/v1/services/{SERVICE_ID}',
    headers=headers, timeout=15
)
if r2.status_code == 200:
    svc = r2.json()
    details = svc.get('serviceDetails', {})
    print(f"Name: {svc.get('name')}")
    print(f"Status: {svc.get('suspended')}")
    print(f"URL: {details.get('url')}")
    print(f"Last deploy: {svc.get('updatedAt')}")
