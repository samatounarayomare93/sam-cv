"""Get strike/email logs from last 30 minutes"""
import requests
A2_KEY = 'rnd_m4ozEoc4nQYOT16Omj0U9QGd3pra'
A2_SVC = 'srv-d80th10g4nts738vk7b0'
h = {'Authorization': f'Bearer {A2_KEY}', 'Accept': 'application/json'}

r = requests.get('https://api.render.com/v1/owners', headers=h, timeout=10)
owner_id = r.json()[0].get('owner', r.json()[0]).get('id', '')

r2 = requests.get(
    f'https://api.render.com/v1/logs?ownerId={owner_id}&resource={A2_SVC}&limit=500',
    headers=h, timeout=15
)
logs = r2.json() if isinstance(r2.json(), list) else r2.json().get('logs', [])

# Find strike-related logs (after the build)
strike_logs = [e for e in logs if isinstance(e, dict) and 
               any(k in e.get('message','') for k in 
                   ['STRIKE', 'SINGULARITY', 'BREVO', 'GMAIL', 'ZOHO', 'SUCCESS', 'FAILED', 'SEND', 'SMTP', 'API key'])]

# Only show logs after the build finished
build_done_idx = 0
for i, e in enumerate(logs):
    if isinstance(e, dict) and 'Successfully installed' in e.get('message',''):
        build_done_idx = i

post_build = [e for e in logs[build_done_idx:] if isinstance(e, dict) and 
              any(k in e.get('message','') for k in 
                  ['STRIKE', 'SINGULARITY', 'BREVO', 'GMAIL', 'ZOHO', 'SUCCESS', 'FAILED', 'SEND', 'SMTP', 'API key', 'BOOTSTRAP', 'VAULT', 'SECRET'])]

print(f"Post-build strike/email logs: {len(post_build)}\n")
for e in post_build[-50:]:
    print(e.get('message','')[:300])
