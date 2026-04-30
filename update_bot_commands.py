#!/usr/bin/env python3
"""
Update bot commands
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

print("🔄 Updating bot commands...")

commands = [
    {"command": "start", "description": "🚀 Start bot"},
    {"command": "menu", "description": "📱 Main menu"},
    {"command": "stats", "description": "📊 Statistics"},
    {"command": "status", "description": "🖥️ System status"},
    {"command": "scrape", "description": "🔍 Scrape jobs"},
    {"command": "qualify", "description": "✅ Qualify leads"},
    {"command": "strike", "description": "🚀 Send applications"},
    {"command": "test_email", "description": "📧 Test email"},
    {"command": "kill", "description": "🛑 Kill switch"},
    {"command": "resume", "description": "🟢 Resume operations"},
    {"command": "ignite", "description": "🔥 Full ignition"},
    {"command": "leads", "description": "📋 View leads"},
    {"command": "audit", "description": "👁️ System audit"}
]

response = requests.post(
    f"https://api.telegram.org/bot{TOKEN}/setMyCommands",
    json={"commands": commands}
)

if response.status_code == 200:
    print("✅ Commands updated successfully!")
    print(f"\n📋 {len(commands)} commands set:")
    for cmd in commands:
        print(f"   /{cmd['command']} - {cmd['description']}")
else:
    print(f"❌ Failed: {response.text}")
