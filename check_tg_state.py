"""Check Telegram bot state and test the test_strike flow."""
import requests
import os
from dotenv import load_dotenv
load_dotenv()

token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

print(f"Token: {token[:20]}...")
print(f"Chat ID: {chat_id}")

# Get bot info
r = requests.get(f'https://api.telegram.org/bot{token}/getMe')
print(f"\nBot info: {r.json()}")

# Get recent updates
r2 = requests.get(f'https://api.telegram.org/bot{token}/getUpdates?limit=10&offset=-10')
data = r2.json()
print(f"\nRecent updates ({len(data.get('result', []))} items):")
for u in data.get('result', []):
    msg = u.get('message', {})
    if msg:
        text = msg.get('text', '')
        user = msg.get('from', {}).get('username', '?')
        date = msg.get('date', 0)
        print(f"  [{date}] {user}: {text[:80]}")
    cb = u.get('callback_query', {})
    if cb:
        print(f"  [CALLBACK] {cb.get('data', '')}")
