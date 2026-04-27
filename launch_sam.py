#!/usr/bin/env python
"""
launch_sam.py - Telegram Dashboard Launcher
Starts the Sovereign Dashboard (C2 control interface) for Project Chronos.
Called by: .github/workflows/24_7_telegram_bot.yml

[RENDER.COM COMPATIBLE] - Runs bot in background thread to avoid blocking startup.
"""

import sys
import os
import threading
import time
import signal

# Ensure we can import core modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.telegram_dashboard import SovereignDashboard
from core.keep_alive import run_keep_alive_server, _self_ping_loop

# Global bot instance
bot_instance = None
bot_thread = None
shutdown_event = threading.Event()


def run_bot():
    """Run bot in background thread."""
    global bot_instance
    try:
        bot_instance = SovereignDashboard()
        print(f"Dashboard initialized in background thread")
        print(f"Starting Telegram bot polling...")
        bot_instance.ignite()
    except Exception as e:
        print(f"Bot error: {e}")
        # On Render, we don't want to exit the main thread if the bot fails, 
        # as the web server must stay alive to prevent 502/restarts.
        print(f"Bot thread failed, but keeping web server alive for health checks.")


def handle_shutdown(signum, frame):
    """Handle graceful shutdown."""
    print("\nShutdown signal received. Stopping bot...")
    shutdown_event.set()
    sys.exit(0)


def main():
    """Start the Telegram dashboard in background and Web HUD in main thread."""
    global bot_thread
    
    print("PROJECT CHRONOS: TELEGRAM DASHBOARD LAUNCHER")
    print("-" * 50)
    print("RENDER.COM OPTIMIZED MODE (Main-thread Web HUD)")
    print("")
    
    # Register shutdown handlers
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)

    # 1. Start the self-ping loop in a daemon thread
    p = threading.Thread(target=_self_ping_loop, name="SelfPing", daemon=True)
    p.start()
    
    try:
        # 2. Start bot in background thread (daemon=True keeps process alive)
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        
        # Small delay to let bot initialize
        time.sleep(2)
        
        print("Bot thread launched")
        print("Starting Web HUD on main thread (Port Binding)...")
        print("")
        
        # 3. Start the Web HUD server on the MAIN THREAD (Blocking)
        run_keep_alive_server()
            
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received.")
        shutdown_event.set()
    except Exception as e:
        print(f"Fatal error: {e}")
        shutdown_event.set()
        sys.exit(1)


if __name__ == "__main__":
    main()
