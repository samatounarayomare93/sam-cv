#!/usr/bin/env python3
"""
Clear Telegram webhook to ensure polling works
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

print("🧹 Clearing Telegram webhook...")

# Delete webhook
response = requests.post(
    f"https://api.telegram.org/bot{TOKEN}/deleteWebhook",
    data={"drop_pending_updates": True}
)

if response.status_code == 200:
    result = response.json()
    print(f"✅ Webhook cleared: {result}")
else:
    print(f"❌ Failed: {response.text}")

# Get webhook info
response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo")
if response.status_code == 200:
    info = response.json()
    print(f"\n📊 Webhook Info:")
    print(f"   URL: {info['result'].get('url', 'None')}")
    print(f"   Pending updates: {info['result'].get('pending_update_count', 0)}")
else:
    print(f"❌ Failed to get webhook info")
