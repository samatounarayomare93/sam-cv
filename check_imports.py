#!/usr/bin/env python3
"""Quick import checker for all critical modules."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from dotenv import load_dotenv
load_dotenv()

modules_to_check = [
    ('core.keep_alive', 'keep_alive'),
    ('core.db_client', 'RealityShapingDB'),
    ('core.ai_agent', 'OmniIntelligence'),
    ('core.runtime_helpers', 'HumanParityJitter'),
    ('core.follow_up_engine', 'FollowUpEngine'),
    ('core.linkedin_automator', 'NeuralLinkedIn'),
    ('core.error_recovery', 'SmartRetry'),
    ('core.anti_ban_protection', 'get_protection'),
    ('core.pdf_generator', 'generate_triple_package'),
    ('core.smtp_engine', 'send_strike'),
    ('core.telegram_dashboard', 'SovereignDashboard'),
    ('core.auto_queue_refill', 'auto_refill_loop'),
    ('core.main_bot', 'AlphaOrchestrator'),
    ('core.scrapers.omni_crawler', 'OmniCrawler'),
    ('core.scrapers.daleel_parallel', 'daleel_parallel_scan'),
]

errors = []
ok = []

for module_path, symbol in modules_to_check:
    try:
        mod = __import__(module_path, fromlist=[symbol])
        if not hasattr(mod, symbol):
            errors.append((module_path, f"Symbol '{symbol}' not found in module"))
        else:
            ok.append(module_path)
    except Exception as e:
        errors.append((module_path, str(e)))

print(f"\n{'='*60}")
print(f"IMPORT CHECK RESULTS: {len(ok)} OK, {len(errors)} ERRORS")
print(f"{'='*60}")

if ok:
    print(f"\n✅ OK ({len(ok)}):")
    for m in ok:
        print(f"   {m}")

if errors:
    print(f"\n❌ ERRORS ({len(errors)}):")
    for m, e in errors:
        print(f"   {m}: {e}")
else:
    print("\n🎉 ALL IMPORTS SUCCESSFUL!")
