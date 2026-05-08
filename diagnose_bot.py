#!/usr/bin/env python3
"""
BOT DIAGNOSTICS
Check bot status and find issues
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

print("=" * 70)
print("BOT DIAGNOSTICS")
print("=" * 70)
print()

if not TOKEN:
    print("CRITICAL: TELEGRAM_BOT_TOKEN missing in .env")
    exit(1)

# 1. Check bot info
print("1. Checking bot info...")
response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getMe")
if response.status_code == 200:
    bot_info = response.json()['result']
    print(f"   [OK] Bot: @{bot_info['username']}")
    print(f"   [OK] ID: {bot_info['id']}")
    print(f"   [OK] Name: {bot_info['first_name']}")
else:
    print(f"   [FAIL] Failed: {response.text}")
print()

# 2. Check webhook
print("2. Checking webhook status...")
response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo")
if response.status_code == 200:
    webhook = response.json()['result']
    if webhook.get('url'):
        print(f"   [WARN] WEBHOOK ACTIVE: {webhook['url']}")
        print(f"   [WARN] This prevents polling from working!")
        print(f"   [WARN] Pending updates: {webhook.get('pending_update_count', 0)}")
    else:
        print(f"   [OK] No webhook (polling mode)")
        print(f"   [OK] Pending updates: {webhook.get('pending_update_count', 0)}")
else:
    print(f"   [FAIL] Failed: {response.text}")
print()

# 3. Check recent updates
print("3. Checking recent updates...")
response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates?limit=5")
if response.status_code == 200:
    updates = response.json()['result']
    if updates:
        print(f"   [OK] Found {len(updates)} recent updates:")
        for update in updates:
            if 'message' in update:
                msg = update['message']
                print(f"      - {msg.get('from', {}).get('first_name', 'Unknown')}: {msg.get('text', 'No text')}")
    else:
        print(f"   [WARN] No recent updates")
else:
    print(f"   [FAIL] Failed: {response.text}")
print()

# 4. Delete webhook if exists
print("4. Clearing webhook (if exists)...")
response = requests.post(
    f"https://api.telegram.org/bot{TOKEN}/deleteWebhook",
    data={"drop_pending_updates": True}
)
if response.status_code == 200:
    print(f"   [OK] Webhook cleared")
else:
    print(f"   [FAIL] Failed: {response.text}")
print()

# 5. Check commands
print("5. Checking bot commands...")
response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getMyCommands")
if response.status_code == 200:
    commands = response.json()['result']
    if commands:
        print(f"   [OK] Found {len(commands)} commands:")
        for cmd in commands[:5]:
            print(f"      - /{cmd['command']}: {cmd['description']}")
    else:
        print(f"   [WARN] No commands set")
else:
    print(f"   [FAIL] Failed: {response.text}")
print()

print("=" * 70)
print("DIAGNOSIS COMPLETE")
print("=" * 70)
print()
print("RECOMMENDATIONS:")
print("   1. If webhook is active, it's been cleared now")
print("   2. Restart your bot: python bot_full_featured.py")
print("   3. Try sending /start to the bot")
print()
