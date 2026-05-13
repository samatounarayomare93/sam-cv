import asyncio
import os
import sys
from unittest.mock import MagicMock

# Mocking the environment for testing
os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
os.environ["TELEGRAM_CHAT_ID"] = "6639482672"

# Mocking the dependencies to avoid network calls
sys.modules["telegram"] = MagicMock()
sys.modules["telegram.ext"] = MagicMock()

from core.telegram_dashboard import SovereignDashboard

async def verify_mappings():
    print("[AUDIT] SOVEREIGN MAPPING AUDIT...")
    bot = SovereignDashboard()
    bot.db = MagicMock()
    bot.ai = MagicMock()
    
    # Test cases for the 20 buttons
    test_buttons = [
        "Run Now", "Status", "Tasks", "Shield",
        "Pulse", "Stats", "Leads", "Prep",
        "Campaign", "Follow-up", "Companies", "Settings",
        "Pause", "Resume", "Track", "Omega Halt",
        "Lazarus", "Repair", "Hygiene", "Reboot"
    ]
    
    for btn in test_buttons:
        update = MagicMock()
        update.effective_user.id = 6639482672
        update.message.text = btn
        context = MagicMock()
        
        print(f"Testing: [{btn}]...", end=" ")
        try:
            # We just want to see if it reaches a logical branch without crashing
            await bot.handle_text_oracle(update, context)
            print("✅ PASS")
        except Exception as e:
            print(f"❌ FAIL: {e}")

if __name__ == "__main__":
    asyncio.run(verify_mappings())
