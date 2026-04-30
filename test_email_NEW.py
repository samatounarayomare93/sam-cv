#!/usr/bin/env python3
"""
🧪 NEW TEST: Email with correct subject format and clean CV filename
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from core.smtp_engine import send_test_email

print("=" * 70)
print("📧 TESTING EMAIL WITH NEW FORMAT")
print("=" * 70)

# Test email
recipient = os.getenv('TEST_RECEIVER_EMAIL', 'samsalameh.cv@gmail.com')

print(f"\n📬 Sending test email to: {recipient}")
print(f"\n✅ NEW FORMAT:")
print(f"   Subject: Application: Lead Automation Engineer - Future Tech Industries [STRIKE-2771]")
print(f"   CV Attachment: Sam_Salameh_CV.pdf")
print(f"   Cover Letter: Sam_Salameh_Cover_Letter.pdf")
print(f"\n🎨 Professional template with clean formatting")
print("\n" + "=" * 70)
print("⏳ Sending...")

result = send_test_email(recipient_email=recipient)

print("=" * 70)
if result:
    print("✅ EMAIL SENT SUCCESSFULLY!")
    print(f"\n📱 CHECK YOUR INBOX: {recipient}")
    print("\n🔍 VERIFY:")
    print("   1. Subject: Application: Lead Automation Engineer - Future Tech Industries [STRIKE-2771]")
    print("   2. Attachment: Sam_Salameh_CV.pdf (clean filename)")
    print("   3. Location: Inbox (not spam)")
    print("   4. From: Sam Salameh")
else:
    print("❌ EMAIL FAILED TO SEND")
    print("Check logs above for details")
print("=" * 70)
