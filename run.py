import asyncio
import gc
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys
import traceback

# [🛡️ FIX]: Monkeypatch curl_cffi to prevent Event Loop Closed crashes during GC
try:
    import curl_cffi.aio
    original_del = getattr(curl_cffi.aio.AsyncSession, '__del__', None)
    if original_del:
        def safe_del(self):
            try:
                original_del(self)
            except RuntimeError as e:
                if "Event loop is closed" not in str(e):
                    pass
            except Exception:
                pass
        curl_cffi.aio.AsyncSession.__del__ = safe_del
except Exception:
    pass

from core.keep_alive import keep_alive
from core.main_bot import AlphaOrchestrator
from core.telegram_dashboard import SovereignDashboard

# [💎 CLOUD-PERFECTION]: Unified Swarm Orchestrator (Single-Process)
# This prevents the 512MB OOM crash on Render by sharing memory between components.

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - [UNIFIED-SWARM] %(levelname)s - %(message)s",
    handlers=[
        TimedRotatingFileHandler("logs/orchestrator.log", when="D", interval=1, backupCount=1, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

async def resource_watchdog():
    """Monitor memory and pressure-clean the system."""
    while True:
        await asyncio.sleep(300) # Every 5 minutes
        gc.collect()
        logging.info("🧹 [RESOURCE-WATCHDOG]: Memory cleared. Swarm health optimized.")

async def main():
    print("""
    ================================================================================
    PROJECT CHRONOS: OMEGA-SOVEREIGNTY UNIFIED SWARM
    🛡️ BULLETPROOF MODE: IMMORTAL OPERATION ACTIVE
    --------------------------------------------------------------------------------
    Status: CONSOLIDATING INTELLIGENCE...
    Memory Mode: SLIM-PROCESS (OOM Protection Active)
    Self-Healing: ENABLED
    Auto-Recovery: ENABLED
    ================================================================================
    """)

    # 1. Start Keep-Alive (Immediate Port Binding for Render)
    logging.info("[SYSTEM] Activating Cloud Heartbeat (Port Binding)...")
    keep_alive()

    # 2. Initialize Shared Swarm Intelligence (Saves massive RAM)
    logging.info("[SYSTEM] Initializing Shared Swarm Intelligence...")
    try:
        from core.db_client import RealityShapingDB
        from core.ai_agent import OmniIntelligence
        from core.bulletproof_system import get_bulletproof_system
        
        shared_db = RealityShapingDB()
        shared_ai = OmniIntelligence()
        
        # 🛡️ Initialize Bulletproof System
        logging.info("[BULLETPROOF] Initializing immortal operation system...")
        bulletproof = get_bulletproof_system(db=shared_db, ai=shared_ai)
        await bulletproof.start_monitoring()
        
        engine = AlphaOrchestrator(db=shared_db, ai=shared_ai)
        dashboard = SovereignDashboard(db=shared_db, ai=shared_ai)

        logging.info("[SYSTEM] Launching Unified Swarm Tasks...")
        
        # 🛡️ Run main tasks with immortal loop protection
        async def run_engine_immortal():
            """Engine with immortal loop protection"""
            await bulletproof.immortal_loop.run_forever(engine.execute_divine_loop)
        
        async def run_dashboard_immortal():
            """Dashboard with immortal loop protection"""
            await bulletproof.immortal_loop.run_forever(dashboard.run_headless)
        
        # We run them as concurrent tasks in the SAME python process
        swarm_tasks = [
            asyncio.create_task(run_engine_immortal()),
            asyncio.create_task(run_dashboard_immortal()),
            asyncio.create_task(resource_watchdog())
        ]

        # Wait for all systems to finish (or run forever)
        await asyncio.gather(*swarm_tasks)

    except KeyboardInterrupt:
        logging.info("[SHUTDOWN] Safely anchoring the Swarm...")
    except Exception as e:
        logging.error(f"⚠️ [FATAL] Swarm Collapse: {e}")
        logging.error(f"Stack trace: {traceback.format_exc()}")
        # Emergency restart logic (optional for Render since it restarts the dyno)
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
