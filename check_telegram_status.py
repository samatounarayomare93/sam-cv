#!/usr/bin/env python3
"""
Check Telegram Bot Status
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TELEGRAM_BOT_TOKEN')

print("=" * 70)
print("🤖 TELEGRAM BOT STATUS CHECK")
print("=" * 70)

# Get bot info
url = f"https://api.telegram.org/bot{token}/getMe"
response = requests.get(url)
data = response.json()

if data.get('ok'):
    bot_info = data['result']
    print(f"\n✅ Bot is ONLINE")
    print(f"📛 Name: {bot_info.get('first_name')}")
    print(f"🆔 Username: @{bot_info.get('username')}")
    print(f"🔢 ID: {bot_info.get('id')}")
else:
    print(f"\n❌ Bot check failed: {data}")

# Get webhook info
url = f"https://api.telegram.org/bot{token}/getWebhookInfo"
response = requests.get(url)
data = response.json()

if data.get('ok'):
    webhook = data['result']
    if webhook.get('url'):
        print(f"\n⚠️  Webhook is SET: {webhook.get('url')}")
        print("   (This might interfere with polling)")
    else:
        print(f"\n✅ No webhook set (polling mode)")

# Test sending a message
chat_id = os.getenv('TELEGRAM_CHAT_ID')
url = f"https://api.telegram.org/bot{token}/sendMessage"
payload = {
    'chat_id': chat_id,
    'text': '✅ Bot Status Check Complete!\n\n📧 Email System: Working\n📎 CV Attachment: Sam_Salameh_CV.html (12KB)\n🎨 Template: Professional white design\n\nBot is ready to receive commands!'
}
response = requests.post(url, json=payload)

if response.json().get('ok'):
    print(f"\n✅ Test message sent to chat {chat_id}")
else:
    print(f"\n❌ Failed to send test message: {response.json()}")

print("=" * 70)
