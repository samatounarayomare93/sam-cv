"""Get email-specific errors from Render logs"""
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

# Find email-related logs
email_logs = [e for e in logs if isinstance(e, dict) and 
              any(k in e.get('message','').upper() for k in 
                  ['SMTP','EMAIL','BREVO','ZOHO','GMAIL','RESEND','DELIVERY','STRIKE','SEND'])]

print(f"Email-related logs: {len(email_logs)}\n")
for e in email_logs[-40:]:
    print(e.get('message','')[:300])
