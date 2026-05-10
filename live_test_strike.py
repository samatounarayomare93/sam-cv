"""
Send a live test strike through the Telegram bot to verify it works end-to-end.
"""
import requests
import os
import time
from dotenv import load_dotenv
load_dotenv()

token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')
test_email = os.getenv('TEST_RECEIVER_EMAIL', 'samsalameh.cv@gmail.com')

BASE = f'https://api.telegram.org/bot{token}'

def send_msg(text):
    r = requests.post(f'{BASE}/sendMessage', json={
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    })
    return r.json()

print(f"Sending test strike to bot for email: {test_email}")
print("Step 1: Triggering test_strike via callback simulation...")

# Simulate clicking the TEST STRIKE button by sending the email directly
# (the bot is in WAITING_TEST_EMAIL state after clicking the button,
# but we can also just send the email directly since is_email_only check exists)
result = send_msg(test_email)
print(f"Message sent: {result.get('ok')}, message_id: {result.get('result', {}).get('message_id')}")

print("\nWaiting 30 seconds for bot to respond...")
time.sleep(30)

# Check recent messages
r = requests.get(f'{BASE}/getUpdates?limit=5&offset=-5')
updates = r.json().get('result', [])
print(f"\nRecent bot messages ({len(updates)} updates):")
for u in updates:
    msg = u.get('message', {})
    if msg and str(msg.get('chat', {}).get('id', '')) == str(chat_id):
        text = msg.get('text', '')[:100]
        date = msg.get('date', 0)
        from_bot = msg.get('from', {}).get('is_bot', False)
        print(f"  [{'BOT' if from_bot else 'USER'}] {text}")
