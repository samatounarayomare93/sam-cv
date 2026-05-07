import sys
import io
# [🛡️ FIX]: Force UTF-8 encoding on Windows to prevent UnicodeEncodeError for emojis
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

import asyncio
import gc
import logging
from logging.handlers import TimedRotatingFileHandler
import os
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
from core.auto_queue_refill import auto_refill_loop

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


async def continuous_scraper_background(engine, interval_seconds: int = 300, scraper_name: str = "Generic"):
    """
    [🔥 REVOLUTIONARY]: Continuous background scraper that NEVER stops.
    Runs independently from the main loop - feeds leads to queue continuously.
    This is the FACTORY ASSEMBLY LINE approach:
    - Main loop = workers processing leads
    - This task = conveyor belt feeding new leads
    Queue NEVER runs dry!
    """
    import asyncio
    logging.info(f"🏭 [CONTINUOUS-SCRAPER-{scraper_name}]: Background scraper started. Interval: {interval_seconds}s")
    
    while True:
        try:
            await asyncio.sleep(interval_seconds)
            
            if not engine or not engine.is_running:
                break
                
            logging.info(f"🔄 [CONTINUOUS-SCRAPER-{scraper_name}]: Running background discovery cycle...")
            raw_leads = []
            
            try:
                from core.scrapers import scraper as main_scraper
                from core.scrapers.omni_crawler import OmniCrawler
                from core.scrapers.daleel_parallel import daleel_parallel_scan
                from core.ai_agent import OmniIntelligence
                
                if scraper_name == "MAIN" and main_scraper:
                    leads = await asyncio.to_thread(main_scraper.get_latest_jobs)
                    if isinstance(leads, list):
                        raw_leads.extend(leads)
                        
                elif scraper_name == "DALEEL" and engine.db:
                    leads = await daleel_parallel_scan(engine.db, pages=3)
                    if isinstance(leads, list):
                        raw_leads.extend(leads)
                        
                elif scraper_name == "OMNI" and engine.omni_crawler:
                    leads = await engine.omni_crawler.hunt_the_web()
                    if isinstance(leads, list):
                        raw_leads.extend(leads)
                        
                elif scraper_name == "PLATFORMS" and engine.omni_crawler:
                    leads = await engine.omni_crawler.hunt_registered_platforms()
                    if isinstance(leads, list):
                        raw_leads.extend(leads)
                        
                elif scraper_name == "ELITE":
                    # 🏆 ELITE COMPANIES: Direct career page scraping
                    # This is the BEST source - jobs before they hit job boards!
                    try:
                        from core.scrapers.elite_companies_scraper import run_elite_scan
                        leads = await run_elite_scan(engine.db)
                        if isinstance(leads, list):
                            raw_leads.extend(leads)
                            logging.info(f"🏆 ELITE SCRAPER: Found {len(leads)} exclusive jobs from top companies!")
                    except Exception as e:
                        logging.warning(f"⚠️ Elite scraper error: {e}")
                        
            except Exception as e:
                logging.warning(f"⚠️ [CONTINUOUS-SCRAPER-{scraper_name}]: Scrape error: {e}")
            
            # Save all discovered leads to queue
            if raw_leads and engine.db:
                JUNK = {'target node', 'none', 'null', 'unknown', 'automatic target', 'oracle lead',
                        'linkedin', 'indeed', 'glassdoor', 'bayt', 'naukrigulf', 'gulftalent'}
                clean = [l for l in raw_leads 
                         if l.get('company_name', '').lower().strip() not in JUNK
                         and len(l.get('company_name', '').strip()) >= 3]
                
                if clean:
                    logging.info(f"🏭 [CONTINUOUS-SCRAPER-{scraper_name}]: Feeding {len(clean)} fresh leads to queue...")
                    save_tasks = [engine.db.save_potential_lead(l, score=l.get('priority_score', 75)) for l in clean]
                    await asyncio.gather(*save_tasks, return_exceptions=True)
                    
        except asyncio.CancelledError:
            logging.info(f"🛑 [CONTINUOUS-SCRAPER-{scraper_name}]: Stopped.")
            break
        except Exception as e:
            logging.error(f"❌ [CONTINUOUS-SCRAPER-{scraper_name}]: Fatal error: {e}")
            await asyncio.sleep(60)  # Wait 1 min before retry

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
            
            # [🧹 HYGIENE]: Truncate logs and clear cache if too big
            try:
                log_file = "logs/orchestrator.log"
                if os.path.exists(log_file) and os.path.getsize(log_file) > 10 * 1024 * 1024: # 10MB
                    with open(log_file, "w") as f: f.truncate(0)
                    logging.info("🧹 [HYGIENE]: Truncated massive log file.")
            except: pass

            # We run them as concurrent tasks in the SAME python process
            swarm_tasks = [
                asyncio.create_task(engine.execute_divine_loop(), name="Engine"),
                asyncio.create_task(dashboard.run_headless(), name="Dashboard"),
                asyncio.create_task(resource_watchdog(), name="Watchdog"),
                asyncio.create_task(health_monitor(), name="HealthMonitor"),
                # [🔄 AUTO-REFILL]: Keeps queue ALWAYS full - never runs dry!
                asyncio.create_task(auto_refill_loop(), name="AutoQueueRefill"),
                # [🔥 REVOLUTIONARY]: Continuous background scrapers - NEVER stop feeding leads!
                # Each runs independently so queue is ALWAYS full
                asyncio.create_task(continuous_scraper_background(engine, interval_seconds=300, scraper_name="MAIN"), name="Scraper-Main"),
                asyncio.create_task(continuous_scraper_background(engine, interval_seconds=420, scraper_name="DALEEL"), name="Scraper-Daleel"),
                asyncio.create_task(continuous_scraper_background(engine, interval_seconds=600, scraper_name="PLATFORMS"), name="Scraper-Platforms"),
                asyncio.create_task(continuous_scraper_background(engine, interval_seconds=900, scraper_name="OMNI"), name="Scraper-Omni"),
                asyncio.create_task(continuous_scraper_background(engine, interval_seconds=1800, scraper_name="ELITE"), name="Scraper-Elite"),
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
