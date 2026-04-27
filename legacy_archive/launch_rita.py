"""
SAM JOB EMPIRE - UNIFIED LAUNCHER v2
=====================================
The single entry point for the entire system
"""

import sys
import os
import time
import logging
from datetime import datetime

# Setup paths
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [SAM] %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('sam.log', encoding='utf-8')
    ]
)

def check_dependencies():
    """Verify all required packages are installed"""
    required = {
        'requests': 'requests',
        'bs4': 'beautifulsoup4',
        'dotenv': 'python-dotenv',
        'telegram': 'python-telegram-bot',
        'groq': 'groq',
        'fpdf': 'fpdf2',
        'psutil': 'psutil'
    }
    missing = []
    for module_name, package_name in required.items():
        try:
            if module_name == 'telegram':
                import telegram.ext
            else:
                __import__(module_name)
        except ImportError:
            missing.append(package_name)
    
    if missing:
        logging.error(f"❌ Missing packages: {missing}")
        logging.info("💡 Run: pip install -r requirements.txt")
        return False
    return True

def check_env():
    """Check critical environment variables"""
    from dotenv import load_dotenv
    load_dotenv()
    
    critical = ['TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID']
    missing = [v for v in critical if not os.getenv(v) or os.getenv(v) == f'your-{v.lower()}-here']
    
    if missing:
        logging.warning(f"⚠️  Missing env vars: {missing}")
        logging.info("💡 Edit .env file and add your Telegram bot token and chat ID")
        return False
    return True

def check_directories():
    """Ensure required directories exist"""
    dirs = ['data', 'pdfs', 'logs', 'cache']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    return True

def main():
    """Main entry point - orchestrates the entire system"""
    # Fix stdout console encoding to prevent charmap crashes
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    
    print("🚀 SAM JOB EMPIRE - AUTONOMOUS APPLICATION ENGINE v2")
    
    logging.info("🚀 SAM JOB EMPIRE STARTING...")
    logging.info(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Pre-flight checks
    logging.info("🔍 Running pre-flight checks...")
    
    if not check_directories():
        sys.exit(1)
    
    if not check_dependencies():
        logging.critical("❌ Dependency check failed!")
        sys.exit(1)
    
    env_ok = check_env()
    if not env_ok:
        logging.info("⚠️  Continuing with limited functionality...")
    
    # Check for kill switch
    from dotenv import load_dotenv
    load_dotenv()
    
    if os.getenv('KILL_SWITCH', '').lower() == 'true':
        logging.critical("🛑 KILL SWITCH ACTIVE! Exiting.")
        sys.exit(0)
    
    # Choose mode
    mode = os.getenv('ZERO_INVESTMENT_MODE', 'true').lower()
    use_ai = os.getenv('USE_AI_ANALYSIS', 'false').lower() == 'true'
    
    logging.info(f"📊 Mode: {'ZERO COST' if mode == 'true' else 'PREMIUM'}")
    logging.info(f"🤖 AI Analysis: {'ENABLED' if use_ai else 'DISABLED'}")
    
    try:
        # Import and run Telegram bot (main control interface)
        logging.info("📱 Starting Telegram Dashboard...")
        from core.telegram_dashboard import SovereignDashboard
        
        logging.info("✅ All systems initialized!")
        logging.info("📍 Control via Telegram bot commands")
        logging.info("🛑 Press Ctrl+C to stop\n")
        
        # Start the bot
        bot = SovereignDashboard()
        bot.ignite()
        
    except KeyboardInterrupt:
        logging.info("\n👋 SAM shutting down gracefully...")
    except Exception as e:
        logging.critical(f"💥 FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
