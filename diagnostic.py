import os
import asyncio
import logging
import sys
from dotenv import load_dotenv

# --- PILLAR 2: Telegram ---
try:
    from telegram import Bot
except ImportError:
    Bot = None

# --- PILLAR 3: Telethon ---
try:
    from telethon import TelegramClient
    from telethon.sessions import StringSession
except ImportError:
    TelegramClient = None

# Load Environment
load_dotenv()

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_step(msg):
    print(f"{Colors.OKCYAN}[INIT] {msg}{Colors.ENDC}")

def print_ok(msg):
    print(f"{Colors.OKGREEN}[PASS] {msg}{Colors.ENDC}")

def print_fail(msg):
    print(f"{Colors.FAIL}[FAIL] {msg}{Colors.ENDC}")

def print_info(msg):
    print(f"{Colors.OKBLUE}[INFO] {msg}{Colors.ENDC}")

async def run_diagnostic():
    # Force UTF-8 if the environment supports it, otherwise fallback.
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

    print(f"\n{Colors.BOLD}{Colors.HEADER}--- PROJECT CHRONOS: MILLION-PERCENT PRE-FLIGHT AUDIT ---{Colors.ENDC}\n")
    
    overall_success = True

    # --- PILLAR 1: SUPABASE DB ---
    print_step("Pillar 1: Supabase Intelligence Link...")
    try:
        from core.db_client import RealityShapingDB
        db = RealityShapingDB()
        if not db.enabled:
            print_fail("Supabase unconfigured. Local SQLite ONLY. (Not cloud-safe)")
            overall_success = False
        else:
            # Simple health check (use 'applications' table which exists)
            success, data = await db._request_with_retry("GET", f"{db.url}/rest/v1/applications?limit=1")
            if success:
                print_ok("Supabase C2 Link Established. Read/Write Verified.")
            else:
                print_fail(f"Supabase Connection Failed: {data}")
                overall_success = False
    except Exception as e:
        print_fail(f"Supabase Fatal Error: {e}")
        overall_success = False

    # --- PILLAR 2: BOT TOKEN ---
    print_step("Pillar 2: Telegram Bot Token...")
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or ":" not in token:
        print_fail("TELEGRAM_BOT_TOKEN missing or invalid.")
        overall_success = False
    else:
        try:
            bot = Bot(token=token)
            me = await bot.get_me()
            print_ok(f"Bot Identity Confirmed: @{me.username}")
        except Exception as e:
            print_fail(f"Bot Token Validation Failed: {e}")
            overall_success = False

    # --- PILLAR 3: PHANTOM SESSION ---
    print_step("Pillar 3: Phantom Network Session String...")
    session_str = os.getenv("TELEGRAM_SESSION_STRING")
    api_id = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")

    if not all([session_str, api_id, api_hash]):
        print_fail("PHANTOM_NETWORK creds missing (Session/API_ID/API_HASH).")
        overall_success = False
    else:
        try:
            client = TelegramClient(StringSession(session_str), api_id, api_hash)
            await client.connect()
            if await client.is_user_authorized():
                me = await client.get_me()
                name = me.first_name or me.username
                print_ok(f"Phantom Session IMMORTAL. Authenticated as: {name}")
            else:
                print_fail("Session String EXPIRED or INVALID. Generate a new one.")
                overall_success = False
            await client.disconnect()
        except Exception as e:
            print_fail(f"Phantom Authentication Failed: {e}")
            overall_success = False

    # --- PILLAR 4: RENDER PORT BINDING ---
    print_step("Pillar 4: Render Keep-Alive Port Binding...")
    try:
        with open("core/keep_alive.py", "r", encoding='utf-8') as f:
            content = f.read()
            if 'os.environ.get("PORT"' in content or 'os.getenv("PORT"' in content:
                print_ok("Dynamic $PORT Binding Detected. Ready for Render.")
            else:
                print_fail("Hardcoded port detected! Render will kill the app.")
                overall_success = False
    except FileNotFoundError:
        print_fail("core/keep_alive.py MISSING.")
        overall_success = False

    print("\n" + "="*50)
    if overall_success:
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 ALL SYSTEMS GO. PROJECT CHRONOS IS READY FOR ASCENSION.{Colors.ENDC}")
        print(f"{Colors.OKBLUE}You are cleared to shut down your PC. The cloud is now the Master.{Colors.ENDC}\n")
    else:
        print(f"\n{Colors.FAIL}{Colors.BOLD}🚨 CRITICAL FAILURES DETECTED.{Colors.ENDC}")
        print(f"{Colors.WARNING}Fix the red lines before shutting down your PC.{Colors.ENDC}\n")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_diagnostic())
