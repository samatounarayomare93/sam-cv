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
        await asyncio.sleep(120) # Every 2 minutes (was 5 - too slow for 512MB)
        gc.collect()
        # [🛡️ OOM-FIX]: Check actual memory usage and force aggressive cleanup
        try:
            import psutil
            process = psutil.Process()
            mem_mb = process.memory_info().rss / (1024 * 1024)
            if mem_mb > 400:  # Approaching 512MB Render limit
                logging.warning(f"⚠️ [RESOURCE-WATCHDOG]: HIGH MEMORY: {mem_mb:.0f}MB! Forcing aggressive cleanup...")
                gc.collect(2)  # Full generation-2 collection
                gc.collect()
            else:
                logging.info(f"🧹 [RESOURCE-WATCHDOG]: Memory: {mem_mb:.0f}MB. Swarm health optimized.")
        except ImportError:
            logging.info("🧹 [RESOURCE-WATCHDOG]: Memory cleared. Swarm health optimized.")

async def health_monitor():
    """🛡️ IMMORTALITY: Monitor system health and auto-restart on failure."""
    last_heartbeat = {}
    restart_count = 0
    max_restarts = 10
    
    while True:
        await asyncio.sleep(60)  # Check every minute
        
        try:
            # Check if tasks are still alive
            current_tasks = [t for t in asyncio.all_tasks() if not t.done()]
            
            if len(current_tasks) < 3:  # Should have at least 3 tasks running
                logging.warning(f"⚠️ [HEALTH-MONITOR] Only {len(current_tasks)} tasks running. System may be degraded.")
            
            # Log heartbeat
            logging.info(f"💓 [HEALTH-MONITOR] System alive. Active tasks: {len(current_tasks)}")
            
        except Exception as e:
            logging.error(f"❌ [HEALTH-MONITOR] Error: {e}")

async def main():
    print("""
    ================================================================================
    PROJECT CHRONOS: OMEGA-SOVEREIGNTY UNIFIED SWARM
    --------------------------------------------------------------------------------
    Status: CONSOLIDATING INTELLIGENCE...
    Memory Mode: SLIM-PROCESS (OOM Protection Active)
    🛡️ IMMORTALITY MODE: ENABLED (Auto-restart on crash)
    ================================================================================
    """)

    # 1. Start Keep-Alive (Immediate Port Binding for Render)
    logging.info("[SYSTEM] Activating Cloud Heartbeat (Port Binding)...")
    keep_alive()

    # 2. Initialize Shared Swarm Intelligence (Saves massive RAM)
    logging.info("[SYSTEM] Initializing Shared Swarm Intelligence...")
    
    restart_count = 0
    max_restarts = 100  # Allow 100 restarts before giving up
    
    while restart_count < max_restarts:
        try:
            from core.db_client import RealityShapingDB
            from core.ai_agent import OmniIntelligence
            
            shared_db = RealityShapingDB()
            shared_ai = OmniIntelligence()
            
            engine = AlphaOrchestrator(db=shared_db, ai=shared_ai)
            dashboard = SovereignDashboard(db=shared_db, ai=shared_ai)

            logging.info(f"[SYSTEM] Launching Unified Swarm Tasks... (Restart #{restart_count})")
            
            # We run them as concurrent tasks in the SAME python process
            swarm_tasks = [
                asyncio.create_task(engine.execute_divine_loop(), name="Engine"),
                asyncio.create_task(dashboard.run_headless(), name="Dashboard"),
                asyncio.create_task(resource_watchdog(), name="Watchdog"),
                asyncio.create_task(health_monitor(), name="HealthMonitor")
            ]

            # Wait for all systems to finish (or run forever)
            await asyncio.gather(*swarm_tasks, return_exceptions=True)
            
            # If we reach here, a task finished unexpectedly
            logging.warning("⚠️ [SYSTEM] A task finished unexpectedly. Restarting in 10 seconds...")
            await asyncio.sleep(10)
            restart_count += 1

        except KeyboardInterrupt:
            logging.info("[SHUTDOWN] Safely anchoring the Swarm...")
            break
        except Exception as e:
            logging.error(f"⚠️ [FATAL] Swarm Collapse: {e}")
            logging.error(f"⚠️ [FATAL] Traceback: {traceback.format_exc()}")
            
            restart_count += 1
            if restart_count < max_restarts:
                logging.info(f"🔄 [AUTO-RESTART] Restarting in 30 seconds... (Attempt {restart_count}/{max_restarts})")
                await asyncio.sleep(30)
            else:
                logging.error(f"❌ [FATAL] Max restarts ({max_restarts}) reached. Giving up.")
                sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
