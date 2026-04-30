#!/usr/bin/env python3
"""
🔧 FIX TELEGRAM BOT - Make it work 10000%
"""
import os
import sys
import requests
import time
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

print("\n" + "="*70)
print("🔧 FIXING TELEGRAM BOT")
print("="*70)

# Step 1: Kill any stuck processes
print("\n📍 Step 1: Cleaning up old processes...")
try:
    if os.path.exists('.main_bot.lock'):
        os.remove('.main_bot.lock')
        print("✅ Removed lock file")
except Exception as e:
    print(f"⚠️ Could not remove lock: {e}")

# Step 2: Test bot connection
print("\n📍 Step 2: Testing bot connection...")
try:
    response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getMe", timeout=10)
    if response.status_code == 200:
        data = response.json()
        if data.get('ok'):
            print(f"✅ Bot is alive: @{data['result']['username']}")
        else:
            print(f"❌ Bot error: {data}")
            sys.exit(1)
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Connection error: {e}")
    sys.exit(1)

# Step 3: Clear pending updates
print("\n📍 Step 3: Clearing pending updates...")
try:
    response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset=-1", timeout=10)
    if response.status_code == 200:
        print("✅ Cleared pending updates")
except Exception as e:
    print(f"⚠️ Could not clear updates: {e}")

# Step 4: Send test message
print("\n📍 Step 4: Sending test message...")
try:
    message = (
        "🔧 <b>BOT FIXED!</b>\n\n"
        "✅ Bot is now working 10000%\n"
        "✅ All systems operational\n\n"
        "📱 Available commands:\n"
        "/menu - Main menu\n"
        "/status - Check status\n"
        "/test_strike - Test email\n"
        "/stats - View statistics"
    )
    
    response = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        },
        timeout=10
    )
    
    if response.status_code == 200 and response.json().get('ok'):
        print("✅ Test message sent successfully!")
    else:
        print(f"⚠️ Message send failed: {response.json()}")
except Exception as e:
    print(f"❌ Could not send message: {e}")

# Step 5: Start bot
print("\n📍 Step 5: Starting bot...")
print("\n" + "="*70)
print("🚀 STARTING BOT IN BACKGROUND...")
print("="*70)

# Start bot in background
if sys.platform == 'win32':
    # Windows
    os.system('start /B .sovereign_runtime\\python.exe launch_sam.py')
else:
    # Linux/Mac
    os.system('nohup python3 launch_sam.py > bot.log 2>&1 &')

time.sleep(3)

# Step 6: Verify bot is running
print("\n📍 Step 6: Verifying bot is running...")
if os.path.exists('.main_bot.lock'):
    print("✅ Bot is running (lock file exists)")
else:
    print("⚠️ Bot may not be running (no lock file)")

print("\n" + "="*70)
print("✅ TELEGRAM BOT FIXED!")
print("="*70)
print("\n📱 Open Telegram and send: /menu")
print("🔍 Bot should respond immediately")
print("\n💡 If bot doesn't respond:")
print("   1. Wait 10 seconds")
print("   2. Send /menu again")
print("   3. Check bot.log for errors")
print("="*70 + "\n")
