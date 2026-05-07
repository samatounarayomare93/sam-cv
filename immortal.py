import sys
import os
import time
import traceback
import logging

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [IMMORTAL] %(levelname)s - %(message)s"
)

def immortal_wrapper():
    """
    IMMORTAL MODE: Runs the bot forever with maximum error recovery.
    Even if the main process crashes, this wrapper restarts it immediately.
    """
    restart_count = 0
    max_restarts = 999999  # Effectively infinite
    
    while restart_count < max_restarts:
        try:
            restart_count += 1
            logging.info(f"🔄 IMMORTAL BOOT (Attempt #{restart_count})")
            
            # Run the main bot
            import run
            
            # If run.py exits normally, restart anyway (shouldn't happen)
            logging.warning("⚠️ Main process exited. Restarting in 5 seconds...")
            time.sleep(5)
            
        except KeyboardInterrupt:
            logging.info("🛑 Graceful shutdown requested by user.")
            break
            
        except Exception as e:
            logging.critical(f"💀 FATAL ERROR: {e}")
            logging.critical(f"Traceback: {traceback.format_exc()}")
            
            # Wait before restart (exponential backoff up to 1 hour)
            wait_time = min(2 ** min(restart_count, 10), 3600)
            logging.info(f"⏳ Restarting in {wait_time} seconds...")
            time.sleep(wait_time)
            
            # Clear memory
            import gc
            gc.collect()
            
            # Force reload of modules to clear any corrupted state
            modules_to_reload = [
                'core.main_bot', 'core.db_client', 'core.ai_agent',
                'core.smtp_engine', 'core.telegram_dashboard',
                'core.scrapers.scraper', 'core.keep_alive'
            ]
            for mod in modules_to_reload:
                if mod in sys.modules:
                    del sys.modules[mod]

if __name__ == "__main__":
    immortal_wrapper()
