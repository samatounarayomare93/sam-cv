#!/usr/bin/env python3
"""
🧪 TELEGRAM BOT TEST
Quick script to verify the bot is responding
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

print("=" * 70)
print("🧪 TESTING TELEGRAM BOT")
print("=" * 70)

# Test 1: Check bot info
print("\n📡 Test 1: Checking bot info...")
try:
    response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getMe")
    if response.status_code == 200:
        data = response.json()
        if data['ok']:
            bot_info = data['result']
            print(f"✅ Bot is alive!")
            print(f"   - Bot ID: {bot_info['id']}")
            print(f"   - Username: @{bot_info['username']}")
            print(f"   - Name: {bot_info['first_name']}")
        else:
            print(f"❌ Bot API error: {data}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
except Exception as e:
    print(f"❌ Connection error: {e}")

# Test 2: Send test message
print("\n📤 Test 2: Sending test message...")
try:
    message = (
        "🧪 <b>TELEGRAM BOT TEST</b>\n"
        "━━━━━━━━━━━━━━━\n"
        "✅ Bot is <b>ONLINE</b> and responding!\n"
        "✅ Connection successful!\n"
        "✅ Ready to receive commands!\n"
        "━━━━━━━━━━━━━━━\n\n"
        "Try these commands:\n"
        "• /menu - Main menu\n"
        "• /status - System status\n"
        "• /test_strike - Test email\n"
        "• /stats - Statistics\n\n"
        "<i>Test completed at: {}</i>"
    )
    
    from datetime import datetime
    message = message.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    response = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        if data['ok']:
            print(f"✅ Test message sent successfully!")
            print(f"   - Message ID: {data['result']['message_id']}")
            print(f"   - Chat ID: {data['result']['chat']['id']}")
        else:
            print(f"❌ Send error: {data}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
except Exception as e:
    print(f"❌ Send error: {e}")

# Test 3: Check for updates (recent messages)
print("\n📥 Test 3: Checking for recent messages...")
try:
    response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates?limit=5")
    if response.status_code == 200:
        data = response.json()
        if data['ok']:
            updates = data['result']
            if updates:
                print(f"✅ Found {len(updates)} recent updates")
                latest = updates[-1]
                if 'message' in latest:
                    msg = latest['message']
                    print(f"   - Latest message: {msg.get('text', 'N/A')[:50]}")
                    print(f"   - From: {msg.get('from', {}).get('first_name', 'Unknown')}")
                    print(f"   - Date: {msg.get('date', 'Unknown')}")
            else:
                print("⚠️  No recent messages found")
        else:
            print(f"❌ Updates error: {data}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
except Exception as e:
    print(f"❌ Updates error: {e}")

print("\n" + "=" * 70)
print("🎯 TEST COMPLETE")
print("=" * 70)
print("\n📱 Now open Telegram and:")
print("   1. Check if you received the test message")
print("   2. Send: /menu")
print("   3. Send: /test_strike")
print("\n✅ If you see responses, the bot is working perfectly!")
print("=" * 70)
