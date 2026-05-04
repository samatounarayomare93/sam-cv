#!/usr/bin/env python3
"""Direct email test with full logging"""
import logging
import sys

# Setup logging to see everything
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

from core import smtp_engine

print("=" * 80)
print("🧪 TESTING EMAIL DELIVERY NOW...")
print("=" * 80)

result = smtp_engine.send_test_email('samsalameh.cv@gmail.com')

print("=" * 80)
if result:
    print("✅ Email sent successfully!")
    print("📬 Check your inbox at: samsalameh.cv@gmail.com")
else:
    print("❌ Email failed to send!")
    print("Check the logs above to see which provider failed and why")
print("=" * 80)
