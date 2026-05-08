import requests, os, time
from dotenv import load_dotenv
load_dotenv()

render_key = os.getenv('RENDER_API_KEY')
service_id  = os.getenv('RENDER_SERVICE_ID')
api_key     = os.getenv('BREVO_API_KEY')
gmail       = os.getenv('GMAIL_SMTP_USER')
sb_url      = os.getenv('SUPABASE_URL')
sb_key      = os.getenv('SUPABASE_KEY')
h = {'apikey': sb_key, 'Authorization': 'Bearer ' + sb_key}

print("=== DEPLOY STATUS ===")
r = requests.get('https://api.render.com/v1/services/' + service_id + '/deploys?limit=3',
    headers={'Authorization': 'Bearer ' + render_key}, timeout=10)
for d in r.json()[:3]:
    dep = d.get('deploy', d)
    print(dep.get('status'), '|', str(dep.get('createdAt',''))[:19], '|', str(dep.get('commit',{}).get('message',''))[:55])

print()
print("=== BOT HEARTBEAT ===")
from datetime import datetime, timezone
r2 = requests.get(sb_url + '/rest/v1/system_settings?key=eq.active_bot_heartbeat&select=updated_at', headers=h, timeout=10)
hb = r2.json()
if hb:
    dt = datetime.fromisoformat(hb[0].get('updated_at','').replace('Z','+00:00'))
    age = int((datetime.now(timezone.utc) - dt).total_seconds())
    print('Age:', age, 'sec -', 'ALIVE' if age < 120 else 'DEAD')

print()
print("=== SEND DIRECT TEST EMAIL ===")
html = "<html><body><h2>Sam Salameh</h2><p>Senior Network Engineer</p>"
html += "<p>Dear Hiring Team, this is a test from the bot.</p>"
html += "<p>Best regards, Sam Salameh</p></body></html>"

payload = {
    'sender': {'email': 'samatou683@gmail.com', 'name': 'Sam Salameh'},
    'to': [{'email': gmail}],
    'subject': 'Application: Lead Automation Engineer - Future Tech Industries [STRIKE-2771]',
    'htmlContent': html,
    'replyTo': {'email': gmail, 'name': 'Sam Salameh'}
}
r3 = requests.post('https://api.brevo.com/v3/smtp/email',
    headers={'api-key': api_key, 'Content-Type': 'application/json'},
    json=payload, timeout=15)
print('Status:', r3.status_code, '| MsgId:', r3.json().get('messageId','?')[:35])

print('Waiting 15s for delivery...')
time.sleep(15)

r4 = requests.get('https://api.brevo.com/v3/smtp/emails',
    params={'email': gmail, 'limit': 1, 'sort': 'desc'},
    headers={'api-key': api_key}, timeout=15)
emails = r4.json().get('transactionalEmails', [])
if emails:
    uuid = emails[0].get('uuid')
    r5 = requests.get('https://api.brevo.com/v3/smtp/emails/' + uuid, headers={'api-key': api_key}, timeout=10)
    events = [ev.get('name') for ev in r5.json().get('events', [])]
    status = 'DELIVERED' if 'delivered' in events else 'ERROR'
    print('Delivery:', status, events)
    print('CHECK GMAIL NOW for:', gmail)
else:
    print('No emails found in Brevo')

print()
print("=== LEAD COUNTS ===")
for s in ['pending', 'processed', 'error']:
    r6 = requests.get(sb_url + '/rest/v1/leads?status=eq.' + s + '&select=id',
        headers={**h, 'Prefer': 'count=exact', 'Range': '0-0'}, timeout=10)
    print(s + ':', r6.headers.get('Content-Range', '?').split('/')[-1])
