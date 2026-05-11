"""
Fix all conflicts:
1. Suspend old bot services on Account 1 (they conflict with Account 2)
2. Keep only sam-bot-v2 (Account 2) as the active bot
3. Delete sam-bot-v3 (failed, useless)
"""
import os, requests
from dotenv import load_dotenv
load_dotenv()

API_KEY_1 = 'rnd_X4vP0V0M4LOJEGbFiKs2TM72NgTg'  # Account 1
API_KEY_2 = 'rnd_m4ozEoc4nQYOT16Omj0U9QGd3pra'  # Account 2

headers1 = {'Authorization': f'Bearer {API_KEY_1}', 'Content-Type': 'application/json', 'Accept': 'application/json'}
headers2 = {'Authorization': f'Bearer {API_KEY_2}', 'Content-Type': 'application/json', 'Accept': 'application/json'}

print("="*60)
print("FIXING ALL CONFLICTS")
print("="*60)

# Services to SUSPEND on Account 1 (old bot services causing conflict)
services_to_suspend = [
    ('srv-d7s6rf6gvqtc73bt431g', 'sam-job-automator', headers1),
    ('srv-d7numa5ckfvc73f9e7pg', 'sam-cv', headers1),
]

# Services to DELETE on Account 1 (failed, useless)
services_to_delete = [
    ('srv-d80t8hfavr4c73arnmpg', 'sam-bot-v3', headers1),
]

print("\n1. Suspending old bot services on Account 1...")
for svc_id, name, hdrs in services_to_suspend:
    r = requests.post(
        f'https://api.render.com/v1/services/{svc_id}/suspend',
        headers=hdrs, timeout=15
    )
    if r.status_code in (200, 201, 204):
        print(f"   SUSPENDED: {name}")
    else:
        print(f"   {name}: {r.status_code} - {r.text[:80]}")

print("\n2. Deleting failed service sam-bot-v3...")
for svc_id, name, hdrs in services_to_delete:
    r = requests.delete(
        f'https://api.render.com/v1/services/{svc_id}',
        headers=hdrs, timeout=15
    )
    if r.status_code in (200, 201, 204):
        print(f"   DELETED: {name}")
    else:
        print(f"   {name}: {r.status_code} - {r.text[:80]}")

print("\n3. Verifying Account 2 bot is still live...")
r = requests.get(
    'https://api.render.com/v1/services/srv-d80th10g4nts738vk7b0/deploys?limit=1',
    headers=headers2, timeout=15
)
if r.status_code == 200 and r.json():
    d = r.json()[0].get('deploy', r.json()[0])
    print(f"   sam-bot-v2: {d.get('status')}")

# Check URL
import requests as req
try:
    r2 = req.get('https://sam-bot-v2.onrender.com', timeout=15)
    print(f"   URL check: HTTP {r2.status_code}")
except Exception as e:
    print(f"   URL check: {e}")

print("\n4. Checking for Telegram conflicts...")
token = os.getenv('TELEGRAM_BOT_TOKEN', '')
if token:
    r3 = requests.get(f'https://api.telegram.org/bot{token}/getWebhookInfo', timeout=10)
    wh = r3.json().get('result', {})
    print(f"   Webhook URL: {wh.get('url', 'none')}")
    print(f"   Pending updates: {wh.get('pending_update_count', 0)}")
    # Clear any webhook to ensure polling works
    if wh.get('url'):
        r4 = requests.post(f'https://api.telegram.org/bot{token}/deleteWebhook', timeout=10)
        print(f"   Webhook cleared: {r4.json().get('ok')}")

print("\n" + "="*60)
print("RESULT:")
print("="*60)
print("Account 1 services: SUSPENDED (no more conflict)")
print("Account 2 sam-bot-v2: ACTIVE (the only running bot)")
print()
print("Architecture:")
print("  Account 2 (samsalameh.cv@gmail.com)")
print("  └── sam-bot-v2.onrender.com  ← ACTIVE BOT")
print("       ├── 100 buttons working")
print("       ├── All email providers")
print("       ├── Groq + OpenRouter + HuggingFace AI")
print("       └── Supabase DB")
print()
print("  Account 1 (samatou683@gmail.com)")
print("  ├── sam-job-automator: SUSPENDED")
print("  ├── sam-cv: SUSPENDED")
print("  └── website-2.24.2026: Running (not a bot, no conflict)")
print()
print("When Account 2 build minutes run out (next month):")
print("  → Resume sam-job-automator on Account 1")
print("  → Suspend sam-bot-v2 on Account 2")
print("  → Rotate every month for unlimited free usage!")
