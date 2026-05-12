"""Get full logs from Account 2 - sam-bot-v2"""
import requests
A2_KEY = 'rnd_m4ozEoc4nQYOT16Omj0U9QGd3pra'
A2_SVC = 'srv-d80th10g4nts738vk7b0'
h = {'Authorization': f'Bearer {A2_KEY}', 'Accept': 'application/json'}

try:
    # Get owner ID
    r = requests.get('https://api.render.com/v1/owners', headers=h, timeout=20)
    owner_id = r.json()[0].get('owner', r.json()[0]).get('id', '')

    # Get 500 log lines
    r2 = requests.get(
        f'https://api.render.com/v1/logs?ownerId={owner_id}&resource={A2_SVC}&limit=500',
        headers=h, timeout=30
    )
    if r2.status_code == 200:
        logs = r2.json() if isinstance(r2.json(), list) else r2.json().get('logs', [])
        print(f"Total log entries: {len(logs)}\n")
        errors = [e for e in logs if isinstance(e, dict) and
                  any(k in e.get('message','') for k in ['ERROR','CRITICAL','Traceback','Exception'])]
        print(f"=== ERRORS ({len(errors)}) ===")
        for e in errors[-20:]:
            print(e.get('message','')[:300])
        print("\n=== LAST 50 LINES ===")
        for entry in logs[-50:]:
            msg = entry.get('message', str(entry)) if isinstance(entry, dict) else str(entry)
            print(msg[:250])
    else:
        print(f"Logs: HTTP {r2.status_code}")
except Exception as e:
    print(f"Error fetching logs: {e}")
    print("Try again in a moment (Render API timeout)")
