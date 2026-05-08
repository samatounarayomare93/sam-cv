import sys
import io
# Force UTF-8 encoding on Windows to prevent UnicodeEncodeError for emojis
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

import asyncio
import gc
import logging
from logging.handlers import RotatingFileHandler
import os
import shutil
import traceback
import time

# Monkeypatch curl_cffi to prevent Event Loop Closed crashes during GC
try:
    import curl_cffi.aio
    original_del = getattr(curl_cffi.aio.AsyncSession, '__del__', None)
    if original_del:
        def safe_del(self):
            try:
                original_del(self)
            except Exception:
                pass
        curl_cffi.aio.AsyncSession.__del__ = safe_del
except Exception:
    pass

from core.keep_alive import keep_alive
from core.main_bot import AlphaOrchestrator
from core.telegram_dashboard import SovereignDashboard
from core.auto_queue_refill import auto_refill_loop

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)
os.makedirs("pdf_cache", exist_ok=True)
os.makedirs("core/pdf_cache", exist_ok=True)
os.makedirs("core/temp_cvs", exist_ok=True)

# Use RotatingFileHandler (max 5MB per file, keep 2 backups) instead of TimedRotating
# This guarantees disk never fills up from logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [SWARM] %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler(
            "logs/orchestrator.log",
            maxBytes=5 * 1024 * 1024,   # 5MB max
            backupCount=2,               # Keep 2 backups = max 15MB total
            encoding="utf-8"
        ),
        logging.StreamHandler(sys.stdout)
    ]
)

# ─────────────────────────────────────────────────────────────────────────────
# DISK JANITOR: Runs every 30 minutes, keeps disk clean forever
# ─────────────────────────────────────────────────────────────────────────────
async def disk_janitor():
    """Permanently keeps disk clean. Runs every 30 minutes."""
    while True:
        try:
            await asyncio.sleep(1800)  # Every 30 minutes

            cleaned = 0

            # 1. Clean PDF cache directories (keep only last 50 files)
            for cache_dir in ["pdf_cache", "core/pdf_cache", "core/temp_cvs"]:
                if os.path.exists(cache_dir):
                    files = sorted(
                        [os.path.join(cache_dir, f) for f in os.listdir(cache_dir)
                         if os.path.isfile(os.path.join(cache_dir, f))],
                        key=os.path.getmtime
                    )
                    # Delete all but the 10 newest
                    for f in files[:-10]:
                        try:
                            os.remove(f)
                            cleaned += 1
                        except Exception:
                            pass

            # 2. Clean cover_letters directory
            if os.path.exists("cover_letters"):
                files = sorted(
                    [os.path.join("cover_letters", f) for f in os.listdir("cover_letters")
                     if os.path.isfile(os.path.join("cover_letters", f))],
                    key=os.path.getmtime
                )
                for f in files[:-5]:
                    try:
                        os.remove(f)
                        cleaned += 1
                    except Exception:
                        pass

            # 3. Clean temp directory
            if os.path.exists("temp_mirror"):
                try:
                    shutil.rmtree("temp_mirror", ignore_errors=True)
                    os.makedirs("temp_mirror", exist_ok=True)
                    cleaned += 1
                except Exception:
                    pass

            # 4. Truncate log file if > 4MB (safety net on top of RotatingFileHandler)
            log_file = "logs/orchestrator.log"
            if os.path.exists(log_file) and os.path.getsize(log_file) > 4 * 1024 * 1024:
                with open(log_file, "w", encoding="utf-8") as f:
                    f.write(f"[JANITOR] Log truncated at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                cleaned += 1

            # 5. Clean SQLite DB system_logs table (keep last 1000 rows)
            try:
                import sqlite3
                db_path = "sam_ultimate.db"
                if os.path.exists(db_path):
                    conn = sqlite3.connect(db_path)
                    conn.execute(
                        "DELETE FROM system_logs WHERE id NOT IN "
                        "(SELECT id FROM system_logs ORDER BY id DESC LIMIT 1000)"
                    )
                    conn.execute("VACUUM")
                    conn.commit()
                    conn.close()
                    cleaned += 1
            except Exception:
                pass

            if cleaned > 0:
                logging.info(f"🧹 [JANITOR] Cleaned {cleaned} items. Disk healthy.")

        except asyncio.CancelledError:
            break
        except Exception as e:
            logging.warning(f"⚠️ [JANITOR] Error: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# RESOURCE WATCHDOG: Memory monitor
# ─────────────────────────────────────────────────────────────────────────────
async def resource_watchdog():
    """Monitor memory and pressure-clean the system."""
    while True:
        try:
            await asyncio.sleep(120)
            gc.collect()
            try:
                import psutil
                process = psutil.Process()
                mem_mb = process.memory_info().rss / (1024 * 1024)
                if mem_mb > 420:
                    logging.warning(f"⚠️ [WATCHDOG] HIGH MEMORY: {mem_mb:.0f}MB! Forcing cleanup...")
                    gc.collect(2)
                    gc.collect()
                else:
                    logging.info(f"💚 [WATCHDOG] Memory: {mem_mb:.0f}MB OK")
            except ImportError:
                gc.collect()
                logging.info("💚 [WATCHDOG] GC complete")
        except asyncio.CancelledError:
            break
        except Exception as e:
            logging.warning(f"⚠️ [WATCHDOG] Error: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# HEALTH MONITOR: Watches tasks and restarts dead ones
# ─────────────────────────────────────────────────────────────────────────────
async def health_monitor():
    """Monitor system health every minute."""
    while True:
        try:
            await asyncio.sleep(60)
            current_tasks = [t for t in asyncio.all_tasks() if not t.done()]
            logging.info(f"💓 [HEALTH] System alive. Active tasks: {len(current_tasks)}")
        except asyncio.CancelledError:
            break
        except Exception as e:
            logging.warning(f"⚠️ [HEALTH] Error: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# CONTINUOUS SCRAPERS: Feed leads to queue forever
# ─────────────────────────────────────────────────────────────────────────────
async def continuous_scraper_background(engine, interval_seconds: int = 300, scraper_name: str = "Generic"):
    """Continuous background scraper that NEVER stops."""
    logging.info(f"🏭 [SCRAPER-{scraper_name}] Started. Interval: {interval_seconds}s")

    while True:
        try:
            await asyncio.sleep(interval_seconds)

            if not engine or not engine.is_running:
                break

            raw_leads = []
            try:
                from core.scrapers import scraper as main_scraper
                from core.scrapers.omni_crawler import OmniCrawler
                from core.scrapers.daleel_parallel import daleel_parallel_scan

                if scraper_name == "MAIN" and main_scraper:
                    leads = await asyncio.wait_for(
                        asyncio.to_thread(main_scraper.get_latest_jobs), timeout=120
                    )
                    if isinstance(leads, list):
                        raw_leads.extend(leads)

                elif scraper_name == "DALEEL" and engine.db:
                    leads = await asyncio.wait_for(
                        daleel_parallel_scan(engine.db, pages=3), timeout=120
                    )
                    if isinstance(leads, list):
                        raw_leads.extend(leads)

                elif scraper_name == "OMNI" and engine.omni_crawler:
                    leads = await asyncio.wait_for(
                        engine.omni_crawler.hunt_the_web(), timeout=180
                    )
                    if isinstance(leads, list):
                        raw_leads.extend(leads)

                elif scraper_name == "PLATFORMS" and engine.omni_crawler:
                    leads = await asyncio.wait_for(
                        engine.omni_crawler.hunt_registered_platforms(), timeout=120
                    )
                    if isinstance(leads, list):
                        raw_leads.extend(leads)

                elif scraper_name == "ELITE":
                    try:
                        from core.scrapers.elite_companies_scraper import run_elite_scan
                        leads = await asyncio.wait_for(run_elite_scan(engine.db), timeout=180)
                        if isinstance(leads, list):
                            raw_leads.extend(leads)
                    except Exception as e:
                        logging.debug(f"Elite scraper: {e}")

            except asyncio.TimeoutError:
                logging.warning(f"⏱️ [SCRAPER-{scraper_name}] Timeout — skipping cycle")
            except Exception as e:
                logging.warning(f"⚠️ [SCRAPER-{scraper_name}] Error: {e}")

            # Save clean leads to queue
            if raw_leads and engine.db:
                JUNK = {
                    'target node', 'none', 'null', 'unknown', 'automatic target',
                    'oracle lead', 'linkedin', 'indeed', 'glassdoor', 'bayt',
                    'naukrigulf', 'gulftalent', 'test', 'example', 'sample'
                }
                clean = [
                    l for l in raw_leads
                    if l.get('company_name', '').lower().strip() not in JUNK
                    and len(l.get('company_name', '').strip()) >= 3
                ]
                if clean:
                    logging.info(f"🏭 [SCRAPER-{scraper_name}] Feeding {len(clean)} leads to queue...")
                    save_tasks = [
                        engine.db.save_potential_lead(l, score=l.get('priority_score', 75))
                        for l in clean
                    ]
                    await asyncio.gather(*save_tasks, return_exceptions=True)

        except asyncio.CancelledError:
            logging.info(f"🛑 [SCRAPER-{scraper_name}] Stopped.")
            break
        except Exception as e:
            logging.error(f"❌ [SCRAPER-{scraper_name}] Fatal: {e}")
            await asyncio.sleep(60)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN: Immortal restart loop
# ─────────────────────────────────────────────────────────────────────────────
async def main():
    logging.info("=" * 70)
    logging.info("PROJECT CHRONOS: OMEGA-SOVEREIGNTY — IMMORTAL MODE ACTIVE")
    logging.info("=" * 70)

    # Start Keep-Alive (port binding for Render)
    keep_alive()

    restart_count = 0

    while True:  # Infinite restart loop — NEVER gives up
        try:
            from core.db_client import RealityShapingDB
            from core.ai_agent import OmniIntelligence

            shared_db = RealityShapingDB()
            shared_ai = OmniIntelligence()

            engine = AlphaOrchestrator(db=shared_db, ai=shared_ai)
            dashboard = SovereignDashboard(db=shared_db, ai=shared_ai)

            logging.info(f"🚀 [SYSTEM] Launching all tasks (restart #{restart_count})...")

            # Critical tasks — if any of these die, restart everything
            critical_tasks = [
                asyncio.create_task(engine.execute_divine_loop(), name="Engine"),
                asyncio.create_task(resource_watchdog(),          name="Watchdog"),
                asyncio.create_task(health_monitor(),             name="HealthMonitor"),
                asyncio.create_task(disk_janitor(),               name="DiskJanitor"),
                asyncio.create_task(auto_refill_loop(),           name="AutoQueueRefill"),
                asyncio.create_task(
                    continuous_scraper_background(engine, 300,  "MAIN"),     name="Scraper-Main"),
                asyncio.create_task(
                    continuous_scraper_background(engine, 420,  "DALEEL"),   name="Scraper-Daleel"),
                asyncio.create_task(
                    continuous_scraper_background(engine, 600,  "PLATFORMS"),name="Scraper-Platforms"),
                asyncio.create_task(
                    continuous_scraper_background(engine, 900,  "OMNI"),     name="Scraper-Omni"),
                asyncio.create_task(
                    continuous_scraper_background(engine, 1800, "ELITE"),    name="Scraper-Elite"),
            ]

            # Dashboard is NON-CRITICAL — runs independently, auto-restarts if it dies
            async def dashboard_immortal():
                """Dashboard wrapper — restarts itself if it crashes, never kills the swarm."""
                while True:
                    try:
                        await dashboard.run_headless()
                    except asyncio.CancelledError:
                        break
                    except Exception as e:
                        logging.warning(f"⚠️ [DASHBOARD] Crashed: {e} — restarting in 30s...")
                        await asyncio.sleep(30)

            dashboard_task = asyncio.create_task(dashboard_immortal(), name="Dashboard")

            swarm_tasks = critical_tasks + [dashboard_task]

            done, pending = await asyncio.wait(
                critical_tasks,  # Only wait on CRITICAL tasks
                return_when=asyncio.FIRST_EXCEPTION
            )

            # Cancel all tasks cleanly
            for task in swarm_tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*swarm_tasks, return_exceptions=True)

            # Log which task died
            for task in done:
                if task.exception():
                    logging.error(f"💀 Task '{task.get_name()}' died: {task.exception()}")

            logging.warning(f"⚠️ [SYSTEM] Swarm collapsed. Restarting in 15s... (#{restart_count})")
            await asyncio.sleep(15)
            restart_count += 1

        except KeyboardInterrupt:
            logging.info("[SHUTDOWN] Graceful shutdown.")
            break
        except Exception as e:
            logging.error(f"❌ [FATAL] {e}\n{traceback.format_exc()}")
            restart_count += 1
            wait = min(30 * restart_count, 300)  # Max 5 min wait
            logging.info(f"🔄 Restarting in {wait}s... (#{restart_count})")
            await asyncio.sleep(wait)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
