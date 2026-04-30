#!/usr/bin/env python3
"""Send /test_strike command via Telegram"""
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')
test_email = os.getenv('TEST_RECEIVER_EMAIL')

print("=" * 70)
print("🧪 SENDING TEST STRIKE VIA TELEGRAM")
print("=" * 70)

# Step 1: Send /test_strike command
print("\n📤 Step 1: Sending /test_strike command...")
response = requests.post(
    f'https://api.telegram.org/bot{token}/sendMessage',
    json={
        'chat_id': chat_id,
        'text': '/test_strike',
    }
)

if response.json().get('ok'):
    print("✅ Command sent!")
else:
    print(f"❌ Failed: {response.json()}")
    exit(1)

# Wait for bot to respond
print("\n⏳ Waiting 3 seconds for bot to respond...")
time.sleep(3)

# Step 2: Send email address
print(f"\n📤 Step 2: Sending email address: {test_email}")
response = requests.post(
    f'https://api.telegram.org/bot{token}/sendMessage',
    json={
        'chat_id': chat_id,
        'text': test_email,
    }
)

if response.json().get('ok'):
    print("✅ Email address sent!")
else:
    print(f"❌ Failed: {response.json()}")
    exit(1)

print("\n" + "=" * 70)
print("✅ TEST STRIKE INITIATED!")
print("=" * 70)
print(f"\n📱 Check Telegram for bot response")
print(f"📧 Check {test_email} for test email")
print("\n⏰ Email should arrive within 30 seconds!")
print("\n💡 This time it will use Gmail SMTP directly!")
print("=" * 70)
