"""
╔══════════════════════════════════════════════════════════════════════════════╗
║          PROJECT CHRONOS - IMMORTAL WATCHDOG v3.0                          ║
║          Runs FOREVER. Never stops. Never crashes permanently.              ║
║          Auto-cleans logs. Auto-heals. Auto-restarts.                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
import sys
import os
import time
import traceback
import logging
import gc
import shutil
from datetime import datetime
from logging.handlers import RotatingFileHandler

# ─── Ensure logs directory exists ────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)

# ─── Rotating log handler: max 5MB per file, keep 2 backups ──────────────────
# This ensures logs NEVER fill the disk — auto-rotates and deletes old logs
_log_handler = RotatingFileHandler(
    f"logs/immortal_{datetime.now().strftime('%Y%m%d')}.log",
    maxBytes=5 * 1024 * 1024,   # 5 MB max per file
    backupCount=2,               # Keep only 2 backup files
    encoding="utf-8"
)
_log_handler.setFormatter(logging.Formatter("%(asctime)s - [IMMORTAL] %(levelname)s - %(message)s"))

_console_handler = logging.StreamHandler(sys.stdout)
_console_handler.setFormatter(logging.Formatter("%(asctime)s - [IMMORTAL] %(levelname)s - %(message)s"))

logging.basicConfig(
    level=logging.INFO,
    handlers=[_log_handler, _console_handler]
)

# ─── Constants ────────────────────────────────────────────────────────────────
MAX_LOG_SIZE_MB = 50          # Total logs folder max size before aggressive cleanup
LOG_CLEANUP_INTERVAL = 3600   # Check log sizes every hour
MAX_RESTARTS = 999_999        # Effectively infinite
BACKOFF_BASE = 2              # Exponential backoff base (seconds)
BACKOFF_MAX = 300             # Max wait between restarts: 5 minutes (not 1 hour!)
MODULES_TO_RELOAD = [
    'run',
    'core.main_bot', 'core.db_client', 'core.ai_agent',
    'core.smtp_engine', 'core.telegram_dashboard',
    'core.scrapers.scraper', 'core.keep_alive',
    'core.orchestrator', 'core.scheduler',
    'core.lead_processor', 'core.scrape_service',
]


def _clean_old_logs():
    """
    Auto-cleanup: Remove old log files if logs/ folder exceeds MAX_LOG_SIZE_MB.
    Keeps the most recent log files only.
    """
    try:
        logs_dir = "logs"
        if not os.path.exists(logs_dir):
            return

        # Calculate total size
        total_mb = sum(
            os.path.getsize(os.path.join(logs_dir, f))
            for f in os.listdir(logs_dir)
            if os.path.isfile(os.path.join(logs_dir, f))
        ) / (1024 * 1024)

        if total_mb > MAX_LOG_SIZE_MB:
            logging.info(f"🧹 [IMMORTAL] Logs folder is {total_mb:.1f}MB > {MAX_LOG_SIZE_MB}MB. Cleaning...")
            # Get all log files sorted by modification time (oldest first)
            log_files = sorted(
                [os.path.join(logs_dir, f) for f in os.listdir(logs_dir)
                 if os.path.isfile(os.path.join(logs_dir, f))],
                key=os.path.getmtime
            )
            # Delete oldest files until we're under the limit
            for log_file in log_files[:-3]:  # Always keep the 3 most recent
                try:
                    size_mb = os.path.getsize(log_file) / (1024 * 1024)
                    os.remove(log_file)
                    total_mb -= size_mb
                    logging.info(f"🗑️ [IMMORTAL] Deleted old log: {os.path.basename(log_file)} ({size_mb:.1f}MB)")
                    if total_mb <= MAX_LOG_SIZE_MB * 0.7:  # Stop at 70% of limit
                        break
                except Exception as e:
                    logging.warning(f"⚠️ [IMMORTAL] Could not delete {log_file}: {e}")

        # Also truncate any single log file > 10MB
        for f in os.listdir(logs_dir):
            fp = os.path.join(logs_dir, f)
            if os.path.isfile(fp) and os.path.getsize(fp) > 10 * 1024 * 1024:
                try:
                    with open(fp, 'w', encoding='utf-8') as fh:
                        fh.truncate(0)
                    logging.info(f"✂️ [IMMORTAL] Truncated oversized log: {f}")
                except Exception as e:
                    logging.warning(f"⚠️ [IMMORTAL] Could not truncate {f}: {e}")

    except Exception as e:
        logging.warning(f"⚠️ [IMMORTAL] Log cleanup error: {e}")


def _clean_temp_files():
    """Remove temp files that accumulate over time."""
    try:
        # Clean temp CV files
        for temp_dir in ["core/temp_cvs", "temp_mirror"]:
            if os.path.exists(temp_dir):
                for f in os.listdir(temp_dir):
                    fp = os.path.join(temp_dir, f)
                    try:
                        if os.path.isfile(fp):
                            age_hours = (time.time() - os.path.getmtime(fp)) / 3600
                            if age_hours > 24:  # Delete files older than 24 hours
                                os.remove(fp)
                    except Exception:
                        pass

        # Clean cache directory (keep only last 1000 entries)
        cache_dir = "cache"
        if os.path.exists(cache_dir):
            cache_files = sorted(
                [os.path.join(cache_dir, f) for f in os.listdir(cache_dir)
                 if os.path.isfile(os.path.join(cache_dir, f))],
                key=os.path.getmtime
            )
            if len(cache_files) > 1000:
                for old_file in cache_files[:-1000]:
                    try:
                        os.remove(old_file)
                    except Exception:
                        pass
                logging.info(f"🧹 [IMMORTAL] Cleaned {len(cache_files) - 1000} old cache files")

    except Exception as e:
        logging.warning(f"⚠️ [IMMORTAL] Temp cleanup error: {e}")


def _reload_modules():
    """Force reload of all core modules to clear corrupted state."""
    reloaded = 0
    for mod in MODULES_TO_RELOAD:
        if mod in sys.modules:
            del sys.modules[mod]
            reloaded += 1
    if reloaded:
        logging.info(f"♻️ [IMMORTAL] Reloaded {reloaded} modules to clear state")


def immortal_wrapper():
    """
    IMMORTAL MODE v3.0: Runs the bot FOREVER with maximum error recovery.
    
    Features:
    - Infinite restart loop (999,999 attempts)
    - Smart exponential backoff (max 5 min, not 1 hour)
    - Auto log rotation and cleanup
    - Auto temp file cleanup
    - Module state reset on crash
    - Memory garbage collection
    - Detailed crash logging
    """
    restart_count = 0
    last_cleanup_time = time.time()
    consecutive_fast_crashes = 0  # Track crashes that happen within 60 seconds
    last_crash_time = 0

    logging.info("=" * 60)
    logging.info("CHRONOS IMMORTAL WATCHDOG STARTED")
    logging.info("=" * 60)

    # Initial cleanup
    _clean_old_logs()
    _clean_temp_files()

    while restart_count < MAX_RESTARTS:
        try:
            restart_count += 1
            logging.info(f"🔄 IMMORTAL BOOT (Attempt #{restart_count})")

            # Periodic maintenance (every hour)
            now = time.time()
            if now - last_cleanup_time > LOG_CLEANUP_INTERVAL:
                _clean_old_logs()
                _clean_temp_files()
                last_cleanup_time = now

            # Run the main bot
            import run  # noqa: F401 — run.py contains asyncio.run(main())

            # If run.py exits normally (shouldn't happen), restart anyway
            logging.warning("⚠️ Main process exited normally. Restarting in 5 seconds...")
            time.sleep(5)

        except KeyboardInterrupt:
            logging.info("🛑 Graceful shutdown requested by user. Goodbye.")
            break

        except SystemExit as e:
            if e.code == 0:
                logging.info("✅ Clean exit requested. Stopping.")
                break
            else:
                logging.error(f"💀 SystemExit with code {e.code}. Restarting...")
                time.sleep(10)

        except Exception as e:
            crash_time = time.time()
            time_since_last_crash = crash_time - last_crash_time
            last_crash_time = crash_time

            # Track fast consecutive crashes (crash within 60s of last crash)
            if time_since_last_crash < 60:
                consecutive_fast_crashes += 1
            else:
                consecutive_fast_crashes = 0

            logging.critical(f"💀 FATAL ERROR (Restart #{restart_count}): {type(e).__name__}: {e}")
            logging.critical(f"Traceback:\n{traceback.format_exc()}")

            # Smart backoff: faster recovery for isolated crashes, slower for crash loops
            if consecutive_fast_crashes > 5:
                # Crash loop detected — wait longer
                wait_time = min(BACKOFF_BASE ** min(consecutive_fast_crashes, 8), BACKOFF_MAX)
                logging.warning(f"⚠️ [IMMORTAL] Crash loop detected ({consecutive_fast_crashes} fast crashes). Waiting {wait_time}s...")
            else:
                # Isolated crash — restart quickly
                wait_time = min(BACKOFF_BASE ** min(restart_count - 1, 6), 60)

            logging.info(f"⏳ Restarting in {wait_time:.0f} seconds... (Attempt {restart_count}/{MAX_RESTARTS})")
            time.sleep(wait_time)

            # Cleanup before restart
            gc.collect()
            _reload_modules()

    logging.info("🏁 [IMMORTAL] Max restarts reached or shutdown requested. Exiting.")


if __name__ == "__main__":
    immortal_wrapper()
