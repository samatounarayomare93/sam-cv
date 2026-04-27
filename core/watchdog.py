import subprocess
import time
import logging
import sys
import os

# ==========================================
# [🕵️ PHASE GHOST: ETERNAL WATCHDOG]
# ==========================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [WATCHDOG] %(levelname)s - %(message)s"
)

def start_hive():
    """Launches the Project Chronos Main Bot Hive."""
    script_path = os.path.join(os.path.dirname(__file__), "main_bot.py")
    logging.info(f"🚀 WATCHDOG: Launching Hive Swarm node: {script_path}")
    return subprocess.Popen([sys.executable, script_path])

def main():
    logging.info("👻 WATCHDOG: Initializing Eternal Monitoring Protocol...")
    
    process = start_hive()
    
    while True:
        try:
            # Check if process is still running
            status = process.poll()
            
            if status is not None:
                logging.warning(f"⚠️ WATCHDOG: Swarm node terminated (Exit Code: {status}).")
                logging.info("👻 WATCHDOG: Commencing Resurrection Protocol...")
                time.sleep(5)
                process = start_hive()
            
            # Mission Pulse
            time.sleep(30)
            
        except KeyboardInterrupt:
            logging.info("🛑 WATCHDOG: Monitoring suspended by user.")
            process.terminate()
            break
        except Exception as e:
            logging.error(f"❌ WATCHDOG: Monitoring Failure - {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
