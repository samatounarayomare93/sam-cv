#!/usr/bin/env python3
"""
Quick test to send email with HTML CV attachment
"""
import sys
import os
sys.path.insert(0, 'core')

from dotenv import load_dotenv
load_dotenv()

from core.smtp_engine import send_test_email

print("=" * 70)
print("📧 TESTING EMAIL WITH HTML CV ATTACHMENT")
print("=" * 70)

# Test email
recipient = os.getenv('TEST_RECEIVER_EMAIL', 'samsalameh.cv@gmail.com')
print(f"\n📬 Sending test email to: {recipient}")
print(f"📎 Attachment: Sam_Salameh_CV.html (~12KB)")
print(f"✉️  Subject: Lead Automation Engineer Application - Sam Salameh")
print(f"🎨 Template: Clean professional white design")
print("\n" + "=" * 70)

result = send_test_email(recipient_email=recipient)

print("=" * 70)
if result:
    print("✅ EMAIL SENT SUCCESSFULLY!")
    print(f"📬 Check inbox: {recipient}")
    print("📎 Attachment: Sam_Salameh_CV.html")
else:
    print("❌ EMAIL FAILED TO SEND")
    print("Check logs above for details")
print("=" * 70)
