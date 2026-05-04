#!/usr/bin/env python3
"""
🧪 GMAIL SMTP TEST SCRIPT
========================
Tests Gmail SMTP connection directly to diagnose email delivery issues.
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def test_gmail_smtp():
    """Test Gmail SMTP connection and send a test email."""
    
    print("=" * 60)
    print("🧪 GMAIL SMTP CONNECTION TEST")
    print("=" * 60)
    
    # Get credentials from .env
    gmail_user = os.getenv('GMAIL_SMTP_USER', '').strip()
    gmail_pass = os.getenv('GMAIL_APP_PASSWORD', '').strip()
    test_recipient = os.getenv('TEST_RECEIVER_EMAIL', gmail_user).strip()
    
    print(f"\n📧 Gmail User: {gmail_user}")
    print(f"🔑 App Password: {'✅ SET' if gmail_pass else '❌ MISSING'} ({len(gmail_pass)} chars)")
    print(f"📬 Test Recipient: {test_recipient}")
    
    if not gmail_user or not gmail_pass:
        print("\n❌ ERROR: Gmail credentials not configured in .env file!")
        print("   Please set GMAIL_SMTP_USER and GMAIL_APP_PASSWORD")
        return False
    
    # Create test message
    msg = MIMEMultipart()
    msg['From'] = f"Sam Salameh <{gmail_user}>"
    msg['To'] = test_recipient
    msg['Subject'] = "🧪 Gmail SMTP Test - Sam Job Bot"
    
    body = """
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #00b4d8;">✅ Gmail SMTP Test Successful!</h2>
        <p>This email was sent directly via Gmail SMTP (Port 465 SSL).</p>
        <p><strong>Sender:</strong> {}</p>
        <p><strong>Time:</strong> {}</p>
        <hr>
        <p style="color: #666; font-size: 12px;">
            If you received this email in your INBOX (not spam), Gmail SMTP is working perfectly! 🎉
        </p>
    </body>
    </html>
    """.format(gmail_user, __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    msg.attach(MIMEText(body, 'html'))
    
    # Test connection
    print("\n" + "=" * 60)
    print("🔌 TESTING CONNECTION...")
    print("=" * 60)
    
    try:
        print("\n1️⃣ Connecting to smtp.gmail.com:465 (SSL)...")
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=15)
        print("   ✅ SSL connection established!")
        
        print("\n2️⃣ Authenticating...")
        server.login(gmail_user, gmail_pass)
        print("   ✅ Authentication successful!")
        
        print("\n3️⃣ Sending test email...")
        server.send_message(msg)
        print("   ✅ Email sent successfully!")
        
        server.quit()
        
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Gmail SMTP is working perfectly!")
        print("=" * 60)
        print(f"\n📬 Check your inbox at: {test_recipient}")
        print("   (If it's in spam, mark it as 'Not Spam' to train Gmail)")
        print("\n✅ Your bot should now send emails via Gmail SMTP!")
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ AUTHENTICATION FAILED: {e}")
        print("\n🔧 TROUBLESHOOTING:")
        print("   1. Make sure you're using an App Password, not your regular Gmail password")
        print("   2. Generate App Password at: https://myaccount.google.com/apppasswords")
        print("   3. Make sure 2-Step Verification is enabled on your Google account")
        print("   4. Copy the 16-character app password (no spaces) to .env file")
        return False
        
    except smtplib.SMTPConnectError as e:
        print(f"\n❌ CONNECTION FAILED: {e}")
        print("\n🔧 TROUBLESHOOTING:")
        print("   1. Port 465 may be blocked by your firewall/ISP")
        print("   2. Try running this test from a different network")
        print("   3. Check if your antivirus is blocking SMTP connections")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {e}")
        import traceback
        print("\n📋 Full traceback:")
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    test_gmail_smtp()
