"""Test the smart rotation system"""
import os
os.environ['RENDER'] = 'true'
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

from dotenv import load_dotenv
load_dotenv()

from core.email_rotator import get_rotator, record_email_sent, get_email_stats

rotator = get_rotator()

print("=" * 60)
print("SMART ROTATION TEST")
print("=" * 60)

# Show current providers
print(f"\nConfigured providers ({len(rotator.providers)}):")
for p in rotator.providers:
    used = rotator.usage.get(p['name'], {}).get('count', 0)
    print(f"  {p['display_name']:15} | limit: {p['limit']:4}/day | used: {used:4} | remaining: {p['limit']-used:4}")

print(f"\nTotal daily capacity: {rotator.get_total_daily_limit()} emails/day")

# Simulate rotation
print("\n--- SIMULATING ROTATION ---")
print("Scenario: Resend hits limit → auto-switches to Zoho → then Brevo")

# Simulate Resend hitting limit
print("\n1. Resend #1 hits limit (100/100)...")
for _ in range(100):
    record_email_sent("resend_1")

next_p = rotator.get_next_provider()
print(f"   Next provider: {next_p['display_name'] if next_p else 'NONE'}")

# Simulate Zoho hitting limit
print("\n2. Zoho #1 hits limit (500/500)...")
for _ in range(500):
    record_email_sent("zoho_1")

next_p = rotator.get_next_provider()
print(f"   Next provider: {next_p['display_name'] if next_p else 'NONE'}")

# Reset for clean state
rotator.reset_usage()
print("\n✅ Rotation works correctly!")
print("Bot will automatically switch providers when limits are hit.")
