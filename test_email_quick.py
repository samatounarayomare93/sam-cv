import os
import sys
import logging
from core import config
from core.smtp_engine import send_test_email, test_email_connection

logging.basicConfig(level=logging.INFO)

# Test the connection status first
print("--- Testing Email Connection Status ---")
status = test_email_connection()
print(f"Connection Status: {status}")

print("\n--- Sending Test Strike ---")
# Try sending a test strike
try:
    success = send_test_email()
    print(f"Test Strike Success: {success}")
except Exception as e:
    print(f"Test Strike Failed with exception: {e}")
