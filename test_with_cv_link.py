#!/usr/bin/env python3
"""
Test email with CV link
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

print("\n" + "="*70)
print("📧 SENDING TEST EMAIL WITH CV LINK")
print("="*70)

from core.smtp_engine import send_test_email

recipient = 'samsalameh.cv@gmail.com'
print(f"\n📬 To: {recipient}")
print(f"📧 Subject: Application: Lead Automation Engineer - Future Tech Industries [STRIKE-2771]")
print(f"📎 Attachment: Sam_Salameh_CV.pdf")
print(f"🔗 CV Link: https://samatounarayomare93.github.io/sam-cv/Sam_Salameh_CV.html")
print(f"🎨 Email Body: Dark mode with VIEW CV button")
print(f"\n⏳ Sending...\n")

result = send_test_email(recipient_email=recipient)

print("\n" + "="*70)
if result:
    print("✅ SUCCESS! Email sent!")
    print(f"\n📱 CHECK YOUR INBOX: {recipient}")
    print("\n🔍 You should see:")
    print("   • Subject with company and STRIKE-ID")
    print("   • PDF attachment")
    print("   • Button to view CV online")
else:
    print("❌ FAILED! Check the error above")
print("="*70 + "\n")
