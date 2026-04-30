#!/usr/bin/env python3
"""
🧪 TEST GMAIL SMTP DIRECTLY
Test if Gmail SMTP works with the new App Password
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("🧪 TESTING GMAIL SMTP")
print("=" * 70)

gmail_user = os.getenv('GMAIL_SMTP_USER')
gmail_password = os.getenv('GMAIL_APP_PASSWORD')
test_email = os.getenv('TEST_RECEIVER_EMAIL')

print(f"\n📧 Configuration:")
print(f"   From: {gmail_user}")
print(f"   To: {test_email}")
print(f"   Password: {'*' * len(gmail_password) if gmail_password else 'NOT SET'}")

if not gmail_user or not gmail_password:
    print("\n❌ ERROR: Gmail credentials not set in .env!")
    exit(1)

print("\n🔌 Connecting to Gmail SMTP...")

try:
    # Create message
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = test_email
    msg['Subject'] = '✅ TEST EMAIL - Gmail SMTP Working!'
    
    body = """
    🎉 SUCCESS! Gmail SMTP is working!
    
    This email was sent directly from your Gmail account using SMTP.
    
    ✅ Gmail App Password: Working
    ✅ SMTP Connection: Successful
    ✅ Email Delivery: 100%
    
    From now on, all emails will be sent from your Gmail directly!
    
    ---
    Sam Salameh CV Bot
    Powered by Gmail SMTP
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Connect to Gmail SMTP
    print("   Connecting to smtp.gmail.com:587...")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    
    print("   Logging in...")
    server.login(gmail_user, gmail_password)
    
    print("   Sending email...")
    server.send_message(msg)
    server.quit()
    
    print("\n" + "=" * 70)
    print("✅ SUCCESS! Email sent via Gmail SMTP!")
    print("=" * 70)
    print(f"\n📧 Check your inbox: {test_email}")
    print("   The email should arrive within 10 seconds!")
    print("\n🎉 Gmail SMTP is now working 100%!")
    print("=" * 70)
    
except smtplib.SMTPAuthenticationError as e:
    print("\n" + "=" * 70)
    print("❌ AUTHENTICATION ERROR")
    print("=" * 70)
    print(f"Error: {e}")
    print("\nPossible causes:")
    print("1. App Password is incorrect")
    print("2. 2-Step Verification not enabled")
    print("3. App Password was revoked")
    print("\nSolution:")
    print("1. Go to: https://myaccount.google.com/apppasswords")
    print("2. Generate a new App Password")
    print("3. Update .env with new password")
    
except Exception as e:
    print("\n" + "=" * 70)
    print("❌ ERROR")
    print("=" * 70)
    print(f"Error: {e}")
    print("\nCheck:")
    print("1. Internet connection")
    print("2. Gmail credentials in .env")
    print("3. Firewall settings")
