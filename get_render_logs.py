"""Get logs from the ACTIVE Render service (Account 2 - sam-bot-v2)"""
import requests, os
from dotenv import load_dotenv
load_dotenv()

# Always use Account 2 (active)
A2_KEY = os.getenv('RENDER_API_KEY', 'rnd_m4ozEoc4nQYOT16Omj0U9QGd3pra')
A2_SVC = os.getenv('RENDER_SERVICE_ID', 'srv-d80th10g4nts738vk7b0')
h = {'Authorization': f'Bearer {A2_KEY}', 'Accept': 'application/json'}

# Get owner ID
r = requests.get('https://api.render.com/v1/owners', headers=h, timeout=10)
owner_id = r.json()[0].get('owner', r.json()[0]).get('id', '')

# Get logs
r2 = requests.get(
    f'https://api.render.com/v1/logs?ownerId={owner_id}&resource={A2_SVC}&limit=200',
    headers=h, timeout=15
)
if r2.status_code == 200:
    logs = r2.json() if isinstance(r2.json(), list) else r2.json().get('logs', [])
    print(f"=== RENDER LOGS (last {len(logs)} lines) ===")
    for entry in logs[-100:]:
        msg = entry.get('message', str(entry)) if isinstance(entry, dict) else str(entry)
        print(msg[:300])
else:
    print(f"Error: HTTP {r2.status_code} - {r2.text[:200]}")
