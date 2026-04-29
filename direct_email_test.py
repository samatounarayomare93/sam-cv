#!/usr/bin/env python3
"""
🚀 DIRECT EMAIL TEST
Sends email directly using multiple methods to diagnose the issue
"""

import os
import sys
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("🚀 DIRECT EMAIL DELIVERY TEST")
print("=" * 70)

recipient = "rita.cordahi@outlook.com"
print(f"\n📬 Target: {recipient}")
print("-" * 70)

# Test 1: Brevo HTTP API
print("\n[TEST 1] Brevo HTTP API (Port 443)")
print("-" * 70)

api_key = os.getenv('BREVO_API_KEY')
if api_key:
    try:
        payload = {
            "sender": {
                "email": "a974ef001@smtp-brevo.com",
                "name": "Sam Salameh"
            },
            "to": [{"email": recipient}],
            "subject": "🧪 Test Email #1 - Brevo HTTP API",
            "htmlContent": """
            <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2 style="color: #06b6d4;">✅ Email Delivery Test</h2>
                <p>This is a <strong>direct test</strong> from Sam's CV Bot.</p>
                <p><strong>Method:</strong> Brevo HTTP API (Port 443)</p>
                <p><strong>Time:</strong> """ + str(__import__('datetime').datetime.now()) + """</p>
                <hr>
                <p style="color: #666; font-size: 12px;">
                    If you received this email, the delivery system is working correctly!
                </p>
            </body>
            </html>
            """,
            "replyTo": {
                "email": "samsalameh.cv@zohomail.com",
                "name": "Sam Salameh"
            }
        }
        
        response = requests.post(
            'https://api.brevo.com/v3/smtp/email',
            headers={
                'api-key': api_key,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            json=payload,
            timeout=20
        )
        
        if response.status_code in [200, 201, 202]:
            print(f"  ✅ SUCCESS! Status: {response.status_code}")
            print(f"  📧 Message ID: {response.json().get('messageId', 'N/A')}")
            print(f"  📬 Email sent to: {recipient}")
        else:
            print(f"  ❌ FAILED! Status: {response.status_code}")
            print(f"  📄 Response: {response.text}")
            
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
else:
    print("  ⚠️ Brevo API key not set")

# Test 2: Alternative recipient (Gmail) to verify Brevo works
print("\n[TEST 2] Brevo HTTP API to Gmail (Verification)")
print("-" * 70)

gmail_test = "sam.dev1@gmail.com"  # Change this to your Gmail
if api_key:
    try:
        payload = {
            "sender": {
                "email": "a974ef001@smtp-brevo.com",
                "name": "Sam Salameh"
            },
            "to": [{"email": gmail_test}],
            "subject": "🧪 Test Email #2 - Gmail Verification",
            "htmlContent": """
            <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2 style="color: #06b6d4;">✅ Gmail Delivery Test</h2>
                <p>This email is sent to <strong>Gmail</strong> to verify Brevo API works.</p>
                <p>If this arrives but Outlook doesn't, it means <strong>Outlook is blocking Brevo</strong>.</p>
                <hr>
                <p style="color: #666; font-size: 12px;">
                    Test from Sam's CV Bot
                </p>
            </body>
            </html>
            """
        }
        
        response = requests.post(
            'https://api.brevo.com/v3/smtp/email',
            headers={
                'api-key': api_key,
                'Content-Type': 'application/json'
            },
            json=payload,
            timeout=20
        )
        
        if response.status_code in [200, 201, 202]:
            print(f"  ✅ SUCCESS! Status: {response.status_code}")
            print(f"  📧 Message ID: {response.json().get('messageId', 'N/A')}")
            print(f"  📬 Email sent to: {gmail_test}")
        else:
            print(f"  ❌ FAILED! Status: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ ERROR: {e}")

# Test 3: Check Brevo account status
print("\n[TEST 3] Brevo Account Status")
print("-" * 70)

if api_key:
    try:
        response = requests.get(
            'https://api.brevo.com/v3/account',
            headers={'api-key': api_key},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Account active")
            print(f"  📧 Email: {data.get('email', 'N/A')}")
            
            # Check plan limits
            plan = data.get('plan', [{}])[0] if data.get('plan') else {}
            print(f"  📊 Plan: {plan.get('type', 'N/A')}")
            
            # Check relay data
            relay = data.get('relay', {})
            if relay:
                print(f"  📮 Relay enabled: {relay.get('enabled', False)}")
        else:
            print(f"  ❌ Failed to get account info: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ ERROR: {e}")

print("\n" + "=" * 70)
print("📊 DIAGNOSIS")
print("=" * 70)
print("""
If Test #1 shows SUCCESS but email doesn't arrive:
  → Outlook is likely blocking/filtering Brevo emails
  → Check Outlook's Junk/Spam folder
  → Check Outlook's "Focused" vs "Other" inbox tabs
  
If Test #2 (Gmail) works but Test #1 doesn't:
  → Confirms Outlook is blocking Brevo
  → Solution: Use Gmail API or different email provider

If both tests fail:
  → Brevo account issue
  → Check Brevo dashboard for sending limits
  → Verify API key is valid

NEXT STEPS:
1. Check rita.cordahi@outlook.com inbox (all folders)
2. Check {gmail_test} inbox
3. If Gmail works but Outlook doesn't → Outlook is blocking
""")
print("=" * 70)
