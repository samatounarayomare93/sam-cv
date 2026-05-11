import os, requests
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY')
service_id = os.getenv('RENDER_SERVICE_ID')
headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}

# Get latest failed deploy
r = requests.get(f'https://api.render.com/v1/services/{service_id}/deploys?limit=3', headers=headers, timeout=15)
deploys = r.json()

for dep in deploys[:2]:
    d = dep.get('deploy', dep)
    deploy_id = d.get('id')
    status = d.get('status')
    print(f"\nDeploy: {deploy_id} | Status: {status}")
    
    # Get deploy logs
    r2 = requests.get(
        f'https://api.render.com/v1/services/{service_id}/deploys/{deploy_id}',
        headers=headers, timeout=15
    )
    if r2.status_code == 200:
        data = r2.json()
        deploy_data = data.get('deploy', data)
        print(f"Commit: {deploy_data.get('commit', {}).get('message', 'N/A')[:60]}")
        print(f"Error: {deploy_data.get('error', 'N/A')}")
