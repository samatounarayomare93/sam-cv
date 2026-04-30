#!/usr/bin/env python3
"""
📧 SEND EMAIL ADDRESS TO BOT
Completes the /test_strike command by sending the email address
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')
test_email = os.getenv('TEST_RECEIVER_EMAIL')

print("=" * 70)
print("📧 SENDING EMAIL ADDRESS TO BOT")
print("=" * 70)
print(f"📧 Email: {test_email}")
print("=" * 70)

# Send email address
response = requests.post(
    f'https://api.telegram.org/bot{token}/sendMessage',
    json={
        'chat_id': chat_id,
        'text': test_email,
        'parse_mode': 'HTML'
    }
)

print(f'\n✅ Email address sent to bot!')
print(f'Status: {response.status_code}')
print(f'Success: {response.json().get("ok")}')

if response.json().get("ok"):
    print('\n' + "=" * 70)
    print("✅ EMAIL ADDRESS SENT!")
    print("=" * 70)
    print("📱 Bot will now send test email")
    print(f"📧 Check {test_email} for test email")
    print("⏰ Email should arrive within 30 seconds")
    print("=" * 70)
else:
    print(f'\n❌ Error: {response.json()}')
