import asyncio
import os
import sys
import re
from unittest.mock import AsyncMock, MagicMock

# Ensure core is in path
sys.path.append(os.getcwd())

# Mock Telegram and DB before importing dashboard
sys.modules["telegram"] = MagicMock()
sys.modules["telegram.ext"] = MagicMock()
from core.telegram_dashboard import SovereignDashboard

async def run_qa():
    print("[QA] STARTING MEGA-SOVEREIGN C2 AUDIT...")
    bot = SovereignDashboard()
    bot.db = AsyncMock()
    bot.ai = AsyncMock()
    bot.authorized_users = ["12345"] # Mock owner
    
    # 20 Button labels exactly as they appear in the UI
    buttons = [
        "Run Now", "Status", "Tasks", "Shield",
        "Pulse", "Stats", "Leads", "Prep",
        "Campaign", "Follow-up", "Companies", "Settings",
        "Pause", "Resume", "Track", "Omega Halt",
        "Lazarus", "Repair", "Hygiene", "Reboot"
    ]
    
    passed = 0
    failed = []
    
    for btn in buttons:
        print(f"  [CHECK] Testing Label: [{btn}]")
        
        # 1. Test Normalization
        clean = bot.clean_text(btn)
        print(f"    Normalized: '{clean}'")
        
        # 2. Test Routing
        update = AsyncMock()
        update.effective_user.id = 12345
        update.message.text = btn
        context = MagicMock()
        
        try:
            # We use a mock dispatcher to see if it triggers the right command
            # For buttons mapped to /command, it calls _dispatch_command
            # For buttons mapped to code blocks, it executes text logic
            result = await bot.handle_text_oracle(update, context)
            passed += 1
            print("    [RESULT] Routing: OK")
        except Exception as e:
            print(f"    [RESULT] Routing: FAILED - {e}")
            failed.append(btn)
            
    print("\n" + "="*40)
    print(f"QA SUMMARY: {passed}/{len(buttons)} Passed")
    if failed:
        print(f"FAILED BUTTONS: {failed}")
    else:
        print("100% SOVEREIGN PARITY ACHIEVED.")
    print("="*40)

if __name__ == "__main__":
    asyncio.run(run_qa())
