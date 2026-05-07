#!/usr/bin/env python3
"""
Trigger bot to start processing immediately via Render redeploy.
Also sends a Telegram message to check bot status.
"""
import requests, os, json
from dotenv import load_dotenv
load_dotenv()

# 1. Send Telegram message to check bot
token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

print("Sending /status command to bot via Telegram...")
# Send a message to the bot
r = requests.post(
    f'https://api.telegram.org/bot{token}/sendMessage',
    json={
        'chat_id': chat_id,
        'text': '/status',
        'parse_mode': 'HTML'
    },
    timeout=10
)
print(f"Telegram message: {r.status_code} - {r.json().get('ok')}")

# 2. Check recent bot messages (getUpdates)
r2 = requests.get(
    f'https://api.telegram.org/bot{token}/getUpdates?limit=5&offset=-5',
    timeout=10
)
if r2.status_code == 200:
    updates = r2.json().get('result', [])
    print(f"\nRecent bot updates ({len(updates)}):")
    for u in updates[-5:]:
        msg = u.get('message', {})
        text = msg.get('text', '')
        date = msg.get('date', 0)
        from_user = msg.get('from', {}).get('username', '?')
        print(f"  [{date}] @{from_user}: {text[:80]}")

# 3. Trigger Render redeploy
api_key = os.getenv('RENDER_API_KEY')
service_id = os.getenv('RENDER_SERVICE_ID')
headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}

print("\nTriggering Render redeploy to restart bot fresh...")
r3 = requests.post(
    f'https://api.render.com/v1/services/{service_id}/deploys',
    json={'clearCache': 'do_not_clear'},
    headers={**headers, 'Content-Type': 'application/json'},
    timeout=15
)
print(f"Redeploy: {r3.status_code}")
if r3.status_code in (200, 201):
    dep = r3.json()
    dep_id = dep.get('id') or dep.get('deploy', {}).get('id', '?')
    print(f"New deploy ID: {dep_id}")
    print("Bot will restart in ~3 minutes and start processing leads immediately!")
else:
    print(f"Response: {r3.text[:200]}")
