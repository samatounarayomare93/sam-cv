#!/usr/bin/env python3
"""
🚀 SAM CV BOT - CLOUD ENTRY POINT
Main entry point for cloud deployment (Render, Railway, etc.)
"""

import sys
import os
import logging

# Setup logging first
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [CLOUD] %(levelname)s - %(message)s"
)

# Add core directory to path
BASE_DIR = os.path.dirname(__file__)
CORE_DIR = os.path.join(BASE_DIR, 'core')
if CORE_DIR not in sys.path:
    sys.path.insert(0, CORE_DIR)

# Import and run the main bot
from core.main_bot import run_orchestrator
import asyncio


def is_cloud_environment() -> bool:
    return any(os.getenv(name) for name in ('RENDER', 'RAILWAY', 'HEROKU', 'VERCEL', 'FLY_IO'))


if __name__ == "__main__":
    logging.info("🚀 Starting Sam CV Bot...")
    logging.info(f"📍 Python: {sys.version}")
    logging.info(f"📂 Working Directory: {os.getcwd()}")
    
    # Detect cloud environment
    cloud_env = 'Cloud' if is_cloud_environment() else 'Local'
    logging.info(f"☁️ Cloud Mode: {cloud_env}")
    
    # Start keep-alive server if on cloud
    if cloud_env == 'Cloud':
        try:
            from core.keep_alive import keep_alive
            keep_alive()
            logging.info("🛡️ Keep-Alive system activated for 24/7 operation")
        except Exception as e:
            logging.warning(f"⚠️ Keep-Alive failed to start: {e}")
    
    try:
        asyncio.run(run_orchestrator())
    except KeyboardInterrupt:
        logging.info("\n⚠️ Bot stopped by user")
    except Exception as e:
        logging.critical(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
