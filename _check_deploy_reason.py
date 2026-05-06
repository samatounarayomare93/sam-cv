import os, sys, requests, json
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()

render_key = os.getenv('RENDER_API_KEY', '')
service_id = os.getenv('RENDER_SERVICE_ID', '')
headers = {'Authorization': f'Bearer {render_key}', 'Accept': 'application/json'}

r = requests.get(f'https://api.render.com/v1/services/{service_id}/events?limit=20', headers=headers, timeout=10)
events = r.json()

print('=== DEPLOY EVENTS (detailed) ===\n')
for item in events:
    evt = item.get('event', item)
    details = evt.get('details', {})
    etype = evt.get('type', '?')
    
    deploy_id = details.get('deployId', '')
    deploy_status = details.get('deployStatus', '')
    build_status = details.get('buildStatus', '')
    reason = details.get('reason', {})
    
    if deploy_status or build_status:
        print(f'Type: {etype}')
        if deploy_id: print(f'  Deploy: {deploy_id}')
        if deploy_status: print(f'  Deploy Status: {deploy_status}')
        if build_status: print(f'  Build Status:  {build_status}')
        if reason: print(f'  Reason: {json.dumps(reason, indent=4)}')
        print()
