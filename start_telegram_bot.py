#!/usr/bin/env python3
"""
🚀 START TELEGRAM BOT
Quick script to start the Telegram bot
"""

import sys
import os
import asyncio
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [BOT] %(levelname)s - %(message)s"
)

# Add core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from dotenv import load_dotenv
load_dotenv()

print("=" * 70)
print("🚀 STARTING TELEGRAM BOT")
print("=" * 70)

# Check environment variables
token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

if not token:
    print("❌ TELEGRAM_BOT_TOKEN not found in .env!")
    sys.exit(1)

if not chat_id:
    print("❌ TELEGRAM_CHAT_ID not found in .env!")
    sys.exit(1)

print(f"\n✅ Token: {token[:20]}...")
print(f"✅ Chat ID: {chat_id}")

# Import and start bot
try:
    from core.telegram_dashboard import SovereignDashboard
    from core.db_client import RealityShapingDB
    from core.ai_agent import OmniIntelligence
    
    print("\n🔧 Initializing components...")
    db = RealityShapingDB()
    ai = OmniIntelligence()
    dashboard = SovereignDashboard(db=db, ai=ai)
    
    print("✅ Components initialized!")
    print("\n🚀 Starting Telegram bot...")
    print("=" * 70)
    print("✅ Bot is now running!")
    print("📱 Open Telegram and send: /menu")
    print("⚠️  Keep this window open!")
    print("=" * 70)
    print("\nPress Ctrl+C to stop the bot.")
    print("=" * 70)
    
    # Start the bot using run_headless
    asyncio.run(dashboard.run_headless())
    
except KeyboardInterrupt:
    print("\n\n⚠️ Bot stopped by user")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
