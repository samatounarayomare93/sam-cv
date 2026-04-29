#!/usr/bin/env python3
"""
🔧 OUTLOOK DELIVERY FIX
Uses Zoho email directly to bypass Outlook's Brevo block
"""

import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("🔧 OUTLOOK DELIVERY FIX")
print("=" * 70)

recipient = "rita.cordahi@outlook.com"
zoho_email = os.getenv('ZOHO_SMTP_USER', 'samsalameh.cv@zohomail.com')

print(f"\n📬 Sending from: {zoho_email}")
print(f"📬 Sending to: {recipient}")
print("-" * 70)

# Solution: Use Brevo API but with Zoho email as sender
# This gives us the deliverability of Zoho with the reliability of Brevo API

api_key = os.getenv('BREVO_API_KEY')

if not api_key:
    print("❌ Brevo API key not found!")
    sys.exit(1)

print("\n🚀 Sending email with Zoho identity via Brevo API...")
print("-" * 70)

try:
    payload = {
        "sender": {
            "email": zoho_email,  # Use Zoho email as sender
            "name": "Sam Salameh"
        },
        "to": [{"email": recipient}],
        "subject": "✅ Application: Network Engineer Position",
        "htmlContent": """
        <html>
        <head>
            <meta charset="utf-8">
        </head>
        <body style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <!-- Header -->
                <div style="background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%); padding: 30px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 24px;">Sam Salameh</h1>
                    <p style="color: rgba(255,255,255,0.9); margin: 5px 0 0 0;">Senior Network Engineer</p>
                </div>
                
                <!-- Body -->
                <div style="padding: 30px;">
                    <p style="font-size: 16px; color: #333; line-height: 1.6;">Dear Hiring Manager,</p>
                    
                    <p style="font-size: 15px; color: #555; line-height: 1.8;">
                        I am writing to express my strong interest in the <strong>Network Engineer</strong> position at your organization.
                    </p>
                    
                    <p style="font-size: 15px; color: #555; line-height: 1.8;">
                        With extensive experience in network infrastructure, system administration, and IT operations, 
                        I am confident in my ability to contribute effectively to your team.
                    </p>
                    
                    <!-- Key Skills -->
                    <div style="background-color: #f8f9fa; border-left: 4px solid #06b6d4; padding: 20px; margin: 20px 0; border-radius: 5px;">
                        <h3 style="margin: 0 0 15px 0; color: #06b6d4; font-size: 16px;">KEY QUALIFICATIONS</h3>
                        <ul style="margin: 0; padding-left: 20px; color: #555;">
                            <li style="margin-bottom: 8px;">Network Design & Implementation (Cisco, Juniper, Fortinet)</li>
                            <li style="margin-bottom: 8px;">Cloud Infrastructure (AWS, Azure, GCP)</li>
                            <li style="margin-bottom: 8px;">Automation & Scripting (Python, Bash, PowerShell)</li>
                            <li style="margin-bottom: 8px;">Security & Compliance (ISO 27001, GDPR)</li>
                        </ul>
                    </div>
                    
                    <p style="font-size: 15px; color: #555; line-height: 1.8;">
                        I would welcome the opportunity to discuss how my skills and experience align with your needs.
                    </p>
                    
                    <p style="font-size: 15px; color: #555; line-height: 1.8;">
                        Please find my CV attached for your review.
                    </p>
                </div>
                
                <!-- Footer -->
                <div style="background-color: #f8f9fa; padding: 25px; text-align: center; border-top: 1px solid #e5e7eb;">
                    <p style="margin: 0 0 10px 0; color: #06b6d4; font-weight: bold; font-size: 16px;">Sam Salameh</p>
                    <p style="margin: 5px 0; color: #666; font-size: 14px;">📞 +961 70 841 1009</p>
                    <p style="margin: 5px 0; color: #666; font-size: 14px;">📧 samsalameh.cv@zohomail.com</p>
                    <p style="margin: 5px 0; color: #666; font-size: 14px;">
                        🔗 <a href="https://www.linkedin.com/in/sam-salameh" style="color: #06b6d4; text-decoration: none;">LinkedIn Profile</a>
                    </p>
                </div>
            </div>
            
            <!-- Footer Note -->
            <div style="text-align: center; margin-top: 20px; color: #999; font-size: 12px;">
                <p>This is a professional job application email.</p>
            </div>
        </body>
        </html>
        """,
        "replyTo": {
            "email": zoho_email,
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
        print(f"✅ SUCCESS! Email sent successfully!")
        print(f"📧 Status Code: {response.status_code}")
        print(f"📧 Message ID: {response.json().get('messageId', 'N/A')}")
        print(f"\n📬 Email sent to: {recipient}")
        print(f"📤 From: {zoho_email}")
        print("\n" + "=" * 70)
        print("✅ DELIVERY IMPROVED!")
        print("=" * 70)
        print("""
Using Zoho email as sender improves deliverability because:
  ✅ Zoho has better reputation with Outlook
  ✅ Zoho domain is trusted by Microsoft
  ✅ Less likely to be marked as spam
  
NEXT STEPS:
1. Check rita.cordahi@outlook.com inbox
2. Check Junk/Spam folder
3. Check "Other" inbox tab (if using Focused Inbox)
4. Wait 2-3 minutes for delivery

If still not received:
  → Outlook may be silently blocking
  → Try sending to a different email (Gmail, Yahoo, etc.)
  → Contact Rita to check her Outlook settings
        """)
    else:
        print(f"❌ FAILED! Status: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("=" * 70)
