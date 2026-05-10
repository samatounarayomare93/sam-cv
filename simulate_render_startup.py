"""
Simulate Render startup environment to find the crash.
Sets RENDER=true and tries to import everything run.py imports.
"""
import os
import sys

# Simulate Render environment
os.environ['RENDER'] = 'true'
os.environ['RENDER_EXTERNAL_URL'] = 'https://sam-job-automator.onrender.com'
os.environ['PORT'] = '10000'

print("Simulating Render startup...")
print("="*60)

errors = []

# Test 1: email_rotator with RENDER=true
print("\n[1] Testing email_rotator with RENDER=true...")
try:
    import importlib
    import core.email_rotator
    importlib.reload(core.email_rotator)  # Reload with RENDER=true
    r = core.email_rotator.get_rotator()
    print(f"  OK: usage_file = {r.usage_file}")
    print(f"  OK: current_provider = {r.get_current_provider()}")
except Exception as e:
    print(f"  FAIL: {e}")
    import traceback
    traceback.print_exc()
    errors.append(f"email_rotator: {e}")

# Test 2: run.py imports
print("\n[2] Testing run.py imports...")
try:
    from core.keep_alive import keep_alive
    print("  OK: keep_alive")
except Exception as e:
    print(f"  FAIL keep_alive: {e}")
    errors.append(f"keep_alive: {e}")

try:
    from core.main_bot import AlphaOrchestrator
    print("  OK: AlphaOrchestrator")
except Exception as e:
    print(f"  FAIL AlphaOrchestrator: {e}")
    errors.append(f"AlphaOrchestrator: {e}")

try:
    from core.telegram_dashboard import SovereignDashboard
    print("  OK: SovereignDashboard")
except Exception as e:
    print(f"  FAIL SovereignDashboard: {e}")
    errors.append(f"SovereignDashboard: {e}")

try:
    from core.auto_queue_refill import auto_refill_loop
    print("  OK: auto_refill_loop")
except Exception as e:
    print(f"  FAIL auto_refill_loop: {e}")
    errors.append(f"auto_refill_loop: {e}")

# Test 3: AlphaOrchestrator instantiation
print("\n[3] Testing AlphaOrchestrator instantiation...")
try:
    from core.db_client import RealityShapingDB
    from core.ai_agent import OmniIntelligence
    db = RealityShapingDB()
    ai = OmniIntelligence()
    engine = AlphaOrchestrator(db=db, ai=ai)
    print(f"  OK: engine created")
except Exception as e:
    print(f"  FAIL: {e}")
    import traceback
    traceback.print_exc()
    errors.append(f"AlphaOrchestrator init: {e}")

print(f"\n{'='*60}")
print(f"RESULT: {len(errors)} errors found")
for e in errors:
    print(f"  - {e}")
