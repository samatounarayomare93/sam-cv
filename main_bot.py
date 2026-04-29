#!/usr/bin/env python3
"""
🚀 SAM CV BOT - CLOUD ENTRY POINT
Main entry point for cloud deployment (Render, Railway, etc.)
"""

import sys
import os

# Add core directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

# Import and run the main bot
from core.main_bot import run_orchestrator
import asyncio

if __name__ == "__main__":
    print("🚀 Starting Sam CV Bot on Cloud...")
    print(f"📍 Python: {sys.version}")
    print(f"📂 Working Directory: {os.getcwd()}")
    print(f"☁️ Cloud Mode: {os.getenv('RENDER') or os.getenv('RAILWAY') or 'Local'}")
    
    try:
        asyncio.run(run_orchestrator())
    except KeyboardInterrupt:
        print("\n⚠️ Bot stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
