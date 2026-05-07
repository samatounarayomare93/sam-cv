#!/usr/bin/env python3
"""
System health check - tests all critical components
"""
import asyncio
import logging
import os
import sys

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.WARNING, format="%(levelname)s - %(message)s")

results = {}

async def test_db():
    try:
        from core.db_client import RealityShapingDB
        db = RealityShapingDB()
        backend = getattr(db, 'backend', 'unknown')
        leads = await db.get_pending_leads(limit=3)
        results['db'] = f"OK ({backend}, {len(leads)} pending leads)"
    except Exception as e:
        results['db'] = f"ERROR: {e}"

async def test_ai():
    try:
        from core.ai_agent import OmniIntelligence
        ai = OmniIntelligence()
        results['ai'] = f"OK ({type(ai).__name__})"
    except Exception as e:
        results['ai'] = f"ERROR: {e}"

async def test_email():
    try:
        from core.smtp_engine import send_strike
        results['email'] = "OK (send_strike importable)"
    except Exception as e:
        results['email'] = f"ERROR: {e}"

async def test_pdf():
    try:
        from core.pdf_generator import create_personalized_pdf, generate_triple_package
        results['pdf'] = "OK (create_personalized_pdf + generate_triple_package importable)"
    except Exception as e:
        results['pdf'] = f"ERROR: {e}"

async def test_telegram():
    try:
        from core.telegram_dashboard import SovereignDashboard
        results['telegram'] = "OK (SovereignDashboard importable)"
    except Exception as e:
        results['telegram'] = f"ERROR: {e}"

async def test_scrapers():
    try:
        from core.scrapers.omni_crawler import OmniCrawler
        results['scrapers'] = "OK (OmniCrawler importable)"
    except Exception as e:
        results['scrapers'] = f"ERROR: {e}"

async def test_engine():
    try:
        from core.db_client import RealityShapingDB
        from core.ai_agent import OmniIntelligence
        from core.main_bot import AlphaOrchestrator
        db = RealityShapingDB()
        ai = OmniIntelligence()
        engine = AlphaOrchestrator(db=db, ai=ai)
        await engine.close()
        results['engine'] = f"OK (concurrency={engine.concurrency_limit})"
    except Exception as e:
        results['engine'] = f"ERROR: {e}"

async def test_env():
    required = [
        'TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID',
        'GEMINI_API_KEY',
        'SUPABASE_URL', 'SUPABASE_KEY',
    ]
    missing = [k for k in required if not os.getenv(k)]
    optional_email = [k for k in ['GMAIL_USER', 'BREVO_API_KEY', 'ZOHO_USER', 'RESEND_API_KEY'] if os.getenv(k)]
    if missing:
        results['env'] = f"MISSING: {missing}"
    else:
        results['env'] = f"OK (all required vars set, email providers: {optional_email})"

async def main():
    print("\n" + "="*60)
    print("  SYSTEM HEALTH CHECK")
    print("="*60)

    await asyncio.gather(
        test_db(),
        test_ai(),
        test_email(),
        test_pdf(),
        test_telegram(),
        test_scrapers(),
        test_engine(),
        test_env(),
        return_exceptions=True
    )

    for component, status in results.items():
        icon = "✅" if status.startswith("OK") else "❌"
        print(f"  {icon} {component:12s}: {status}")

    print("="*60)
    errors = [k for k, v in results.items() if not v.startswith("OK")]
    if errors:
        print(f"\n  ⚠️  {len(errors)} issue(s) found: {errors}")
    else:
        print("\n  🚀 All systems GO. Ready to run.")
    print()

if __name__ == "__main__":
    asyncio.run(main())
