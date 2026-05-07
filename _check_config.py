#!/usr/bin/env python3
"""Quick configuration check for ULTRA-MAXIMUM mode"""
from dotenv import load_dotenv
import os

load_dotenv()

print("=" * 70)
print("🔥 ULTRA-MAXIMUM MODE - CONFIGURATION CHECK")
print("=" * 70)

# Check critical settings
print("\n📊 APPLICATION SETTINGS:")
print(f"  MAX_APPLICATIONS_PER_DAY: {os.getenv('MAX_APPLICATIONS_PER_DAY', 'NOT SET')}")
print(f"  MAX_APPLICATIONS_PER_HOUR: {os.getenv('MAX_APPLICATIONS_PER_HOUR', 'NOT SET')}")
print(f"  MIN_MATCH_SCORE: {os.getenv('MIN_MATCH_SCORE', 'NOT SET')}")
print(f"  QUALITY_THRESHOLD: {os.getenv('QUALITY_THRESHOLD', 'NOT SET')}")

print("\n⏰ OPERATING HOURS:")
print(f"  START: {os.getenv('BUSINESS_HOURS_START', 'NOT SET')} AM")
print(f"  END: {os.getenv('BUSINESS_HOURS_END', 'NOT SET')} PM")
hours = int(os.getenv('BUSINESS_HOURS_END', 0)) - int(os.getenv('BUSINESS_HOURS_START', 0))
print(f"  TOTAL: {hours} hours/day")

print("\n📧 EMAIL PROVIDERS:")
providers = []
if os.getenv('GMAIL_SMTP_USER') and os.getenv('GMAIL_APP_PASSWORD'):
    providers.append("Gmail")
    print("  ✅ Gmail: CONFIGURED (500/day)")
else:
    print("  ❌ Gmail: NOT CONFIGURED")

if os.getenv('ZOHO_SMTP_USER') and os.getenv('ZOHO_APP_PASSWORD'):
    providers.append("Zoho1")
    print("  ✅ Zoho 1: CONFIGURED (500/day)")
else:
    print("  ❌ Zoho 1: NOT CONFIGURED")

if os.getenv('ZOHO_SMTP_USER_2') and os.getenv('ZOHO_APP_PASSWORD_2'):
    providers.append("Zoho2")
    print("  ✅ Zoho 2: CONFIGURED (500/day)")
else:
    print("  ❌ Zoho 2: NOT CONFIGURED")

if os.getenv('BREVO_API_KEY'):
    providers.append("Brevo")
    print("  ✅ Brevo: CONFIGURED (300/day)")
else:
    print("  ❌ Brevo: NOT CONFIGURED")

if os.getenv('RESEND_API_KEY'):
    providers.append("Resend")
    print("  ✅ Resend: CONFIGURED (100/day)")
else:
    print("  ❌ Resend: NOT CONFIGURED")

print(f"\n  TOTAL PROVIDERS: {len(providers)}/5")
print(f"  TOTAL CAPACITY: 1,900 emails/day")

print("\n🧠 AI PROVIDERS:")
if os.getenv('GROQ_API_KEY'):
    print("  ✅ Groq: CONFIGURED")
else:
    print("  ❌ Groq: NOT CONFIGURED")

if os.getenv('GEMINI_API_KEY'):
    print("  ✅ Gemini: CONFIGURED")
else:
    print("  ❌ Gemini: NOT CONFIGURED")

print("\n💾 DATABASE:")
if os.getenv('SUPABASE_URL') and os.getenv('SUPABASE_KEY'):
    print("  ✅ Supabase: CONFIGURED")
else:
    print("  ❌ Supabase: NOT CONFIGURED")

print("\n📱 TELEGRAM:")
if os.getenv('TELEGRAM_BOT_TOKEN') and os.getenv('TELEGRAM_CHAT_ID'):
    print("  ✅ Telegram: CONFIGURED")
else:
    print("  ❌ Telegram: NOT CONFIGURED")

print("\n⚡ PERFORMANCE SETTINGS:")
print(f"  MAX_PARALLEL_STRIKES: {os.getenv('MAX_PARALLEL_STRIKES', 'NOT SET')}")
print(f"  BATCH_SIZE: {os.getenv('BATCH_SIZE', 'NOT SET')}")
print(f"  MAX_PARALLEL_SCRAPERS: {os.getenv('MAX_PARALLEL_SCRAPERS', 'NOT SET')}")

print("\n" + "=" * 70)

# Verify ULTRA-MAXIMUM settings
errors = []
warnings = []

if os.getenv('MAX_APPLICATIONS_PER_DAY') != '1500':
    errors.append("MAX_APPLICATIONS_PER_DAY should be 1500")
if os.getenv('MAX_APPLICATIONS_PER_HOUR') != '120':
    errors.append("MAX_APPLICATIONS_PER_HOUR should be 120")
if os.getenv('MIN_MATCH_SCORE') != '55':
    warnings.append("MIN_MATCH_SCORE should be 55")
if len(providers) < 5:
    errors.append(f"Only {len(providers)} providers (need 5)")

if errors:
    print("❌ ERRORS:")
    for err in errors:
        print(f"  - {err}")
elif warnings:
    print("⚠️  WARNINGS:")
    for warn in warnings:
        print(f"  - {warn}")
    print("\n✅ READY TO DEPLOY (with warnings)")
else:
    print("✅ ALL CHECKS PASSED!")
    print("\n🚀 ULTRA-MAXIMUM MODE READY!")
    print("  • 1,500 apps/day")
    print("  • 45,000 apps/month")

print("=" * 70)
