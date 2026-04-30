#!/usr/bin/env python3
"""Check Telegram bot connection"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TELEGRAM_BOT_TOKEN')

print("=" * 70)
print("🔍 CHECKING TELEGRAM BOT CONNECTION")
print("=" * 70)

# 1. Check bot info
response = requests.get(f'https://api.telegram.org/bot{token}/getMe')
if response.status_code == 200:
    bot_info = response.json()
    if bot_info.get('ok'):
        print(f"✅ Bot Info:")
        print(f"   Name: {bot_info['result']['first_name']}")
        print(f"   Username: @{bot_info['result']['username']}")
        print(f"   ID: {bot_info['result']['id']}")
    else:
        print(f"❌ Bot Info Failed: {bot_info}")
else:
    print(f"❌ HTTP Error: {response.status_code}")

# 2. Check webhook status
response = requests.get(f'https://api.telegram.org/bot{token}/getWebhookInfo')
if response.status_code == 200:
    webhook_info = response.json()
    if webhook_info.get('ok'):
        result = webhook_info['result']
        print(f"\n📡 Webhook Info:")
        print(f"   URL: {result.get('url', 'None (polling mode)')}")
        print(f"   Pending updates: {result.get('pending_update_count', 0)}")
        print(f"   Last error: {result.get('last_error_message', 'None')}")
    else:
        print(f"❌ Webhook Info Failed: {webhook_info}")

# 3. Check for pending updates
response = requests.get(f'https://api.telegram.org/bot{token}/getUpdates?limit=1')
if response.status_code == 200:
    updates = response.json()
    if updates.get('ok'):
        print(f"\n📨 Pending Updates: {len(updates.get('result', []))}")
        if updates.get('result'):
            print(f"   Latest update ID: {updates['result'][0].get('update_id')}")
    else:
        print(f"❌ Updates Failed: {updates}")

print("=" * 70)
