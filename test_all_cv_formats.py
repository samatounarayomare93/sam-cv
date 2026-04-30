#!/usr/bin/env python3
"""
🧪 CV FORMAT TEST
Sends email with PDF CV attachment (professional 2-page layout)
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

print("\n" + "="*70)
print("📧 COMPREHENSIVE CV FORMAT TEST")
print("="*70)

from core.smtp_engine import send_test_email

# Send test email with ALL CV formats
recipient = 'samsalameh.cv@gmail.com'

print(f"\n📬 To: {recipient}")
print(f"📧 Subject: Application: Lead Automation Engineer - Future Tech Industries [STRIKE-2771]")
print(f"\n📎 CV FORMATS:")
print(f"   1. ✅ CV PDF (Sam_Salameh_CV.pdf)")
print(f"      - Professional enhanced design")
print(f"      - Modern gradients and icons")
print(f"      - Complete experience with bullet points")
print(f"\n   2. ✅ Cover Letter PDF (Cover_Letter_[Company].pdf)")
print(f"      - Personalized for the company")
print(f"      - Professional business letter format")
print(f"      - Matching CV design")
print(f"\n🎨 Email Body: Dark mode professional design")
print(f"🔗 LinkedIn Button: Included in email")
print(f"\n⏳ Generating and sending...\n")

# The send_test_email function already includes both HTML and PDF attachments
# Plus the email template already has the online CV link button
result = send_test_email(recipient_email=recipient)

print("\n" + "="*70)
if result:
    print("✅ SUCCESS! Email sent with CV and Cover Letter!")
    print(f"\n📱 CHECK YOUR INBOX: {recipient}")
    print("\n🔍 You should see:")
    print("   • Subject: Application: Lead Automation Engineer - Future Tech Industries [STRIKE-2771]")
    print("   • Attachment 1: Sam_Salameh_CV.pdf (enhanced professional design)")
    print("   • Attachment 2: Cover_Letter_Future_Tech_Industries.pdf")
    print("   • Email body: Dark mode with LINKEDIN PROFILE button")
    print("\n💡 Both PDFs have:")
    print("   • Modern gradient design")
    print("   • Professional layout")
    print("   • Matching color scheme")
    print("\n🚀 Complete application package ready!")
else:
    print("❌ FAILED! Check the error above")
print("="*70 + "\n")
