#!/usr/bin/env python3
"""Final verification before deployment"""
import sys
import os

print("=" * 70)
print("🔍 FINAL VERIFICATION - ULTRA-MAXIMUM MODE")
print("=" * 70)

errors = []
warnings = []
passed = []

# Test 1: Import all core modules
print("\n📦 Testing Core Modules...")
try:
    from core.db_client import RealityShapingDB
    passed.append("✅ db_client")
except Exception as e:
    errors.append(f"❌ db_client: {e}")

try:
    from core.ai_agent import OmniIntelligence
    passed.append("✅ ai_agent")
except Exception as e:
    errors.append(f"❌ ai_agent: {e}")

try:
    from core.smtp_engine import send_strike
    passed.append("✅ smtp_engine")
except Exception as e:
    errors.append(f"❌ smtp_engine: {e}")

try:
    from core.email_rotator import get_rotator
    passed.append("✅ email_rotator")
except Exception as e:
    errors.append(f"❌ email_rotator: {e}")

try:
    from core.main_bot import AlphaOrchestrator
    passed.append("✅ main_bot")
except Exception as e:
    errors.append(f"❌ main_bot: {e}")

try:
    from core.error_recovery import SmartRetry
    passed.append("✅ error_recovery")
except Exception as e:
    errors.append(f"❌ error_recovery: {e}")

# Test 2: Check .env configuration
print("\n⚙️  Testing Configuration...")
from dotenv import load_dotenv
load_dotenv()

required_vars = [
    'SUPABASE_URL', 'SUPABASE_KEY',
    'GROQ_API_KEY', 'GEMINI_API_KEY',
    'GMAIL_SMTP_USER', 'GMAIL_APP_PASSWORD',
    'ZOHO_SMTP_USER', 'ZOHO_APP_PASSWORD',
    'ZOHO_SMTP_USER_2', 'ZOHO_APP_PASSWORD_2',
    'BREVO_API_KEY',
    'TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID'
]

for var in required_vars:
    if os.getenv(var):
        passed.append(f"✅ {var}")
    else:
        warnings.append(f"⚠️  {var} not set")

# Test 3: Verify ULTRA-MAXIMUM settings
print("\n🔥 Verifying ULTRA-MAXIMUM Settings...")
ultra_settings = {
    'MAX_APPLICATIONS_PER_DAY': '1500',
    'MAX_APPLICATIONS_PER_HOUR': '120',
    'MIN_MATCH_SCORE': '55',
    'QUALITY_THRESHOLD': '55',
    'BUSINESS_HOURS_START': '5',
    'BUSINESS_HOURS_END': '23',
    'MAX_PARALLEL_STRIKES': '15',
    'BATCH_SIZE': '75',
    'MAX_PARALLEL_SCRAPERS': '7',
    'SCRAPE_INTERVAL_MINUTES': '90',
    'NATURAL_BREAK_PROBABILITY': '0.05',
    'GC_INTERVAL': '90',
}

for key, expected in ultra_settings.items():
    actual = os.getenv(key)
    if actual == expected:
        passed.append(f"✅ {key}={expected}")
    else:
        errors.append(f"❌ {key}: expected {expected}, got {actual}")

# Test 4: Check email capacity
print("\n📧 Calculating Email Capacity...")
capacity = 0
if os.getenv('GMAIL_SMTP_USER'):
    capacity += 500
if os.getenv('ZOHO_SMTP_USER'):
    capacity += 500
if os.getenv('ZOHO_SMTP_USER_2'):
    capacity += 500
if os.getenv('BREVO_API_KEY'):
    capacity += 300
if os.getenv('RESEND_API_KEY'):
    capacity += 100

if capacity >= 1900:
    passed.append(f"✅ Email capacity: {capacity}/day")
else:
    errors.append(f"❌ Email capacity: {capacity}/day (need 1900)")

# Test 5: Check file structure
print("\n📁 Checking File Structure...")
required_files = [
    'run.py',
    'core/main_bot.py',
    'core/db_client.py',
    'core/ai_agent.py',
    'core/smtp_engine.py',
    'core/email_rotator.py',
    '.env',
    'requirements.txt'
]

for file in required_files:
    if os.path.exists(file):
        passed.append(f"✅ {file}")
    else:
        errors.append(f"❌ Missing: {file}")

# Print results
print("\n" + "=" * 70)
print(f"📊 RESULTS:")
print(f"  ✅ Passed: {len(passed)}")
print(f"  ⚠️  Warnings: {len(warnings)}")
print(f"  ❌ Errors: {len(errors)}")
print("=" * 70)

if errors:
    print("\n❌ ERRORS FOUND:")
    for err in errors[:10]:  # Show first 10 errors
        print(f"  {err}")
    if len(errors) > 10:
        print(f"  ... and {len(errors) - 10} more")

if warnings:
    print("\n⚠️  WARNINGS:")
    for warn in warnings[:5]:  # Show first 5 warnings
        print(f"  {warn}")
    if len(warnings) > 5:
        print(f"  ... and {len(warnings) - 5} more")

print("\n" + "=" * 70)

if not errors:
    print("✅ ALL CRITICAL CHECKS PASSED!")
    print("\n🔥 ULTRA-MAXIMUM MODE VERIFIED!")
    print("\nExpected Performance:")
    print("  • 1,500 applications/day")
    print("  • 45,000 applications/month")
    print("  • 1,200-1,275 successful/day")
    print("  • 36,000-38,250 successful/month")
    print("  • 78.9% email capacity usage")
    print("  • 18 hours/day operation (5 AM - 11 PM)")
    print("\n🚀 READY TO DEPLOY!")
    print("\nNext steps:")
    print("  1. git add .")
    print("  2. git commit -m 'ULTRA-MAXIMUM: 1500 apps/day'")
    print("  3. git push")
    print("  4. Monitor on Telegram: /status")
    sys.exit(0)
else:
    print("❌ CRITICAL ERRORS FOUND - FIX BEFORE DEPLOYING")
    sys.exit(1)

print("=" * 70)
