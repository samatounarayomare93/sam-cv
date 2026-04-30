#!/usr/bin/env python3
"""
🔧 SETUP GMAIL API - FRESH START
This will help you set up Gmail API properly
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("🔧 GMAIL API SETUP GUIDE")
print("=" * 70)

print("\n📋 CURRENT CONFIGURATION:")
print(f"   Gemini API Key: {os.getenv('GEMINI_API_KEY', 'NOT SET')[:20]}...")
print(f"   Sender Email: {os.getenv('SENDER_EMAIL', 'NOT SET')}")
print(f"   Test Email: {os.getenv('TEST_RECEIVER_EMAIL', 'NOT SET')}")

print("\n" + "=" * 70)
print("⚠️  PROBLEM IDENTIFIED:")
print("=" * 70)
print("• Zoho SMTP: BLOCKED (unusual activity)")
print("• Brevo SMTP: Emails sent but Gmail marks as SPAM")
print("• Gmail API: Token expired")

print("\n" + "=" * 70)
print("✅ SOLUTION: Use Brevo HTTP API (Port 443)")
print("=" * 70)
print("Brevo HTTP API works better than SMTP because:")
print("• Uses HTTPS (Port 443) - never blocked")
print("• Better deliverability")
print("• No SMTP port issues")

print("\n" + "=" * 70)
print("🔍 CHECKING WHY EMAILS NOT ARRIVING:")
print("=" * 70)

reasons = [
    "1. Gmail is marking Brevo emails as SPAM",
    "2. Gmail 'Focused Inbox' is hiding emails in 'Other' tab",
    "3. Gmail filters are auto-archiving emails",
    "4. Brevo sender reputation is low for new accounts"
]

for reason in reasons:
    print(f"   {reason}")

print("\n" + "=" * 70)
print("📱 WHAT TO DO NOW:")
print("=" * 70)
print("\n1. CHECK SPAM FOLDER:")
print("   • Open Gmail")
print("   • Click 'Spam' on left sidebar")
print("   • Search for 'Sam Salameh' or 'Lead Automation'")

print("\n2. CHECK ALL MAIL:")
print("   • Click 'All Mail' in Gmail")
print("   • Search for: from:@sendinblue.com")

print("\n3. CHECK PROMOTIONS TAB:")
print("   • Gmail might put it in 'Promotions' or 'Updates'")

print("\n4. ADD BREVO TO SAFE SENDERS:")
print("   • If you find email in spam, click 'Not Spam'")
print("   • Add noreply@sendinblue.com to contacts")

print("\n" + "=" * 70)
print("🚀 ALTERNATIVE: Use Direct Gmail Sending")
print("=" * 70)
print("\nTo send FROM your Gmail directly (best deliverability):")
print("1. Go to: https://myaccount.google.com/apppasswords")
print("2. Create 'App Password' for 'Mail'")
print("3. Copy the 16-character password")
print("4. Add to .env:")
print("   GMAIL_SMTP_USER=samsalameh.cv@gmail.com")
print("   GMAIL_APP_PASSWORD=<your-16-char-password>")

print("\n" + "=" * 70)
