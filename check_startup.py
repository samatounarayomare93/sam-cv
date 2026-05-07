#!/usr/bin/env python3
"""Quick startup verification script."""
import sys, os, json, asyncio
sys.path.insert(0, '.')
sys.path.insert(0, 'core')

from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("PROJECT CHRONOS - STARTUP VERIFICATION")
print("=" * 60)

# 1. Check Telegram
import urllib.request
token = os.getenv('TELEGRAM_BOT_TOKEN', '')
try:
    url = f'https://api.telegram.org/bot{token}/getMe'
    with urllib.request.urlopen(url, timeout=10) as r:
        data = json.loads(r.read())
    if data.get('ok'):
        bot = data['result']
        uname = bot.get('username', '?')
        fname = bot.get('first_name', '?')
        print(f'[OK] Telegram bot: @{uname} ({fname})')
    else:
        print(f'[FAIL] Telegram API: {data}')
except Exception as e:
    print(f'[FAIL] Telegram: {e}')

# 2. Check DB import
try:
    from core.db_client import RealityShapingDB
    db = RealityShapingDB()
    print('[OK] DB client initialized')
except Exception as e:
    print(f'[FAIL] DB client: {e}')

# 3. Check AI agent
try:
    from core.ai_agent import OmniIntelligence
    ai = OmniIntelligence()
    print('[OK] AI agent initialized')
except Exception as e:
    print(f'[FAIL] AI agent: {e}')

# 4. Check SMTP engine
try:
    from core.smtp_engine import send_strike
    print('[OK] SMTP engine imported')
except Exception as e:
    print(f'[FAIL] SMTP engine: {e}')

# 5. Check PDF generator
try:
    from core.pdf_generator import create_personalized_pdf, generate_triple_package
    print('[OK] PDF generator imported')
except Exception as e:
    print(f'[FAIL] PDF generator: {e}')

# 6. Check orchestrator
try:
    from core.main_bot import AlphaOrchestrator
    engine = AlphaOrchestrator(db=db, ai=ai)
    print('[OK] AlphaOrchestrator initialized')
except Exception as e:
    print(f'[FAIL] AlphaOrchestrator: {e}')

# 7. Check Telegram dashboard
try:
    from core.telegram_dashboard import SovereignDashboard
    dashboard = SovereignDashboard(db=db, ai=ai)
    print('[OK] SovereignDashboard initialized')
except Exception as e:
    print(f'[FAIL] SovereignDashboard: {e}')

# 8. Check scrapers
try:
    from core.scrapers import scraper
    from core.scrapers.omni_crawler import OmniCrawler
    from core.scrapers.daleel_parallel import daleel_parallel_scan
    print('[OK] Scrapers imported')
except Exception as e:
    print(f'[FAIL] Scrapers: {e}')

print("=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
