#!/usr/bin/env python3
"""URGENT: Test Gmail SMTP now"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

gmail_user = os.getenv('GMAIL_SMTP_USER')
gmail_password = os.getenv('GMAIL_APP_PASSWORD')
gmail_recipient = os.getenv('GMAIL_TEST_RECIPIENT', gmail_user)

print('=' * 70)
print('🧪 URGENT TEST - Gmail SMTP')
print('=' * 70)
print(f'From: {gmail_user}')
print(f'To: {gmail_recipient}')
print(f'Password: {"*" * 8 if gmail_password else "NOT SET"}')

if not gmail_user or not gmail_password:
    print('\n❌ ERROR: Gmail credentials not set!')
    raise SystemExit(1)

if not gmail_recipient:
    print('\n❌ ERROR: No recipient configured! Set GMAIL_TEST_RECIPIENT or GMAIL_SMTP_USER.')
    raise SystemExit(1)

try:
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = gmail_recipient
    msg['Subject'] = 'URGENT TEST - Check if this arrives!'
    
    body = f'''
URGENT TEST EMAIL

If you receive this, Gmail SMTP is working!

Time: Now
From: Gmail SMTP Direct
Test: urgent_test_email.py
Recipient: {gmail_recipient}

---
Sam Salameh CV Bot
    '''
    
    msg.attach(MIMEText(body, 'plain'))
    
    print('\n🔌 Connecting to Gmail SMTP...')
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    
    print('🔐 Logging in...')
    server.login(gmail_user, gmail_password)
    
    print('📧 Sending email...')
    server.send_message(msg)
    server.quit()
    
    print('\n' + '=' * 70)
    print('✅ EMAIL SENT SUCCESSFULLY!')
    print('=' * 70)
    print(f'\n📧 Check your inbox: {gmail_recipient}')
    print('⏰ Email should arrive within 10 seconds!')
    print('\n💡 Search Gmail for: "URGENT TEST"')
    print('=' * 70)
    
except smtplib.SMTPAuthenticationError as e:
    print('\n' + '=' * 70)
    print('❌ AUTHENTICATION ERROR')
    print('=' * 70)
    print(f'Error: {e}')
    print('\nThe App Password might be wrong!')
    print('Current password:', gmail_password)
    
except Exception as e:
    print('\n' + '=' * 70)
    print('❌ ERROR')
    print('=' * 70)
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
