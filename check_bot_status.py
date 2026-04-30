#!/usr/bin/env python3
"""
Check if bot is responding
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

print("🔍 Checking bot status...")
print()

# Get bot info
response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getMe")
if response.status_code == 200:
    bot_info = response.json()['result']
    print(f"✅ Bot Info:")
    print(f"   ID: {bot_info['id']}")
    print(f"   Username: @{bot_info['username']}")
    print(f"   Name: {bot_info['first_name']}")
    print()
else:
    print(f"❌ Failed to get bot info")
    print()

# Get updates
response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates")
if response.status_code == 200:
    updates = response.json()['result']
    print(f"📊 Recent Updates: {len(updates)}")
    if updates:
        last_update = updates[-1]
        print(f"   Last update ID: {last_update['update_id']}")
        if 'message' in last_update:
            msg = last_update['message']
            print(f"   Last message: {msg.get('text', 'N/A')}")
            print(f"   From: {msg['from']['first_name']}")
    print()
else:
    print(f"❌ Failed to get updates")
    print()

# Send test message
print("📧 Sending test message to bot...")
response = requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    json={
        "chat_id": CHAT_ID,
        "text": "🤖 Bot Status Check\n\nBot is online and responding!"
    }
)

if response.status_code == 200:
    print("✅ Test message sent successfully!")
else:
    print(f"❌ Failed to send test message: {response.text}")
