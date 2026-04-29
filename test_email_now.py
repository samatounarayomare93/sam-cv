#!/usr/bin/env python3
"""
🧪 QUICK EMAIL TEST
Tests email sending with current configuration
"""

import sys
import os

# Add core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("🧪 EMAIL TEST - CHECKING CONFIGURATION")
print("=" * 60)

# Check environment variables
print("\n📧 EMAIL CONFIGURATION:")
print(f"  ZOHO_SMTP_USER: {os.getenv('ZOHO_SMTP_USER', 'NOT SET')}")
print(f"  ZOHO_APP_PASSWORD: {'SET ✅' if os.getenv('ZOHO_APP_PASSWORD') else 'NOT SET ❌'}")
print(f"  BREVO_SMTP_LOGIN: {os.getenv('BREVO_SMTP_LOGIN', 'NOT SET')}")
print(f"  BREVO_SMTP_PASSWORD: {'SET ✅' if os.getenv('BREVO_SMTP_PASSWORD') else 'NOT SET ❌'}")
print(f"  SENDER_EMAIL: {os.getenv('SENDER_EMAIL', 'NOT SET')}")
print(f"  TEST_RECEIVER_EMAIL: {os.getenv('TEST_RECEIVER_EMAIL', 'NOT SET')}")

# Test email sending
print("\n🚀 SENDING TEST EMAIL...")
print("-" * 60)

try:
    from core.smtp_engine import send_test_email
    
    recipient = os.getenv('TEST_RECEIVER_EMAIL', 'rita.cordahi@outlook.com')
    print(f"📬 Sending to: {recipient}")
    
    result = send_test_email(recipient_email=recipient)
    
    if result:
        print("\n✅ SUCCESS! Email sent successfully!")
        print(f"📬 Check inbox: {recipient}")
        print("📁 Also check spam/junk folder")
    else:
        print("\n❌ FAILED! Email could not be sent")
        print("\n🔍 TROUBLESHOOTING:")
        print("  1. Check if ZOHO_SMTP_USER and ZOHO_APP_PASSWORD are set correctly")
        print("  2. Verify Zoho app password is valid (accounts.zoho.com → Security → App Passwords)")
        print("  3. Check if Brevo credentials are correct")
        print("  4. Look at logs above for specific error messages")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
