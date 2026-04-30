#!/usr/bin/env python3
"""
🧪 SIMPLE TEST: Send email exactly as you want it
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

print("\n" + "="*70)
print("📧 SENDING TEST EMAIL")
print("="*70)

from core.smtp_engine import send_test_email

# Send test email
recipient = 'samsalameh.cv@gmail.com'
print(f"\n📬 To: {recipient}")
print(f"📧 Subject: Application: Lead Automation Engineer - Future Tech Industries [STRIKE-2771]")
print(f"📎 Attachments:")
print(f"   1. Sam_Salameh_CV.html (Complete HTML - needs Chrome to open)")
print(f"   2. Sam_Salameh_CV.pdf (PDF version)")
print(f"🎨 Email Body: Dark mode professional design")
print(f"\n⏳ Generating and sending...\n")

result = send_test_email(recipient_email=recipient)

print("\n" + "="*70)
if result:
    print("✅ SUCCESS! Email sent!")
    print(f"\n📱 CHECK YOUR INBOX: {recipient}")
    print("\n🔍 You should see:")
    print("   • Subject: Application: Lead Automation Engineer - Future Tech Industries [STRIKE-2771]")
    print("   • Attachments: Sam_Salameh_CV.html + Sam_Salameh_CV.pdf")
    print("   • Dark mode professional email body")
    print("   • Try both attachments and tell me which one is better!")
else:
    print("❌ FAILED! Check the error above")
print("="*70 + "\n")
