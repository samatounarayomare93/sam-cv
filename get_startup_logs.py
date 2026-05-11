"""Get startup logs from Account 2 to see what happened at boot"""
import requests
A2_KEY = 'rnd_m4ozEoc4nQYOT16Omj0U9QGd3pra'
A2_SVC = 'srv-d80th10g4nts738vk7b0'
h = {'Authorization': f'Bearer {A2_KEY}', 'Accept': 'application/json'}

r = requests.get('https://api.render.com/v1/owners', headers=h, timeout=10)
owner_id = r.json()[0].get('owner', r.json()[0]).get('id', '')

# Get 500 lines from the beginning (startup)
r2 = requests.get(
    f'https://api.render.com/v1/logs?ownerId={owner_id}&resource={A2_SVC}&limit=500&direction=forward',
    headers=h, timeout=15
)
if r2.status_code == 200:
    logs = r2.json() if isinstance(r2.json(), list) else r2.json().get('logs', [])
    print(f"Total: {len(logs)} entries\n")
    # Show first 100 (startup)
    print("=== STARTUP LOGS (first 100) ===")
    for entry in logs[:100]:
        msg = entry.get('message', str(entry)) if isinstance(entry, dict) else str(entry)
        print(msg[:300])
