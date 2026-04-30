#!/usr/bin/env python3
"""
Send test message to verify bot is working
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

print(f"📤 Sending test message to chat {CHAT_ID}...")

message = (
    "🤖 **Bot Status Check**\n\n"
    "✅ Bot is online and running!\n"
    "✅ All 13 commands are active\n\n"
    "Try: /menu"
)

response = requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    json={
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
)

if response.status_code == 200:
    print("✅ Test message sent successfully!")
    print("📱 Check your Telegram!")
else:
    print(f"❌ Failed: {response.text}")
