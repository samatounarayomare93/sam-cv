#!/usr/bin/env python3
"""
🧪 TEST TELEGRAM /test_strike COMMAND
Sends /test_strike command to bot to verify email delivery
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

print("=" * 70)
print("🧪 TESTING /test_strike COMMAND")
print("=" * 70)
print(f"📧 Test email will be sent to: {os.getenv('TEST_RECEIVER_EMAIL')}")
print(f"📤 From: {os.getenv('SENDER_EMAIL')}")
print("=" * 70)

# Send /test_strike command
response = requests.post(
    f'https://api.telegram.org/bot{token}/sendMessage',
    json={
        'chat_id': chat_id,
        'text': '/test_strike',
        'parse_mode': 'HTML'
    }
)

print(f'\n✅ Command sent to Telegram!')
print(f'Status: {response.status_code}')
print(f'Success: {response.json().get("ok")}')

if response.json().get("ok"):
    print('\n' + "=" * 70)
    print("✅ /test_strike COMMAND SENT!")
    print("=" * 70)
    print("📱 Check your Telegram for bot response")
    print(f"📧 Check {os.getenv('TEST_RECEIVER_EMAIL')} for test email")
    print("⏰ Email should arrive within 30 seconds")
    print("=" * 70)
else:
    print(f'\n❌ Error: {response.json()}')
