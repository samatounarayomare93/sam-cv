import sys
import os
import logging

# Add core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from core.smtp_engine import send_test_email
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

print("=" * 70)
print("TESTING PREMIUM EMAIL ENGINE")
print("=" * 70)

target = "samsalameh.cv@gmail.com"
print(f"Target: {target}")

try:
    result = send_test_email(target)
    if result:
        print("\n[OK] SUCCESS: Email sent!")
    else:
        print("\n[FAIL] FAILED: Email could not be sent. Check logs.")
except Exception as e:
    print(f"\n[ERROR] ERROR: {e}")
    import traceback
    traceback.print_exc()

print("=" * 70)
