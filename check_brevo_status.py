#!/usr/bin/env python3
"""Check Brevo email delivery status"""
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

api_key = os.getenv('BREVO_API_KEY')

print("=" * 70)
print("📧 CHECKING BREVO EMAIL STATUS")
print("=" * 70)

# Get recent emails from Brevo
headers = {
    'accept': 'application/json',
    'api-key': api_key
}

# Get emails from last hour
params = {
    'limit': 10,
    'offset': 0,
    'sort': 'desc',
    'email': 'samsalameh.cv@gmail.com'
}

response = requests.get(
    'https://api.brevo.com/v3/smtp/emails',
    headers=headers,
    params=params
)

if response.status_code == 200:
    data = response.json()
    emails = data.get('transactionalEmails', [])
    
    print(f"\n📊 Recent Emails: {len(emails)}")
    print("=" * 70)
    
    for email in emails[:5]:  # Show last 5
        msg_id = email.get('messageId', 'N/A')
        to_email = email.get('email', 'N/A')
        subject = email.get('subject', 'N/A')[:40]
        date = email.get('date', 'N/A')
        status = email.get('event', 'N/A')
        
        print(f"\n📧 Email:")
        print(f"   To: {to_email}")
        print(f"   Subject: {subject}")
        print(f"   Status: {status}")
        print(f"   Date: {date}")
        print(f"   Message ID: {msg_id}")
        
        # Check if it's to samsalameh.cv@gmail.com
        if 'samsalameh.cv@gmail.com' in to_email:
            print(f"   ⭐ THIS IS YOUR TEST EMAIL!")
            
            # Get detailed status
            detail_response = requests.get(
                f'https://api.brevo.com/v3/smtp/emails/{msg_id}',
                headers=headers
            )
            
            if detail_response.status_code == 200:
                detail = detail_response.json()
                events = detail.get('events', [])
                print(f"\n   📊 Delivery Events:")
                for event in events:
                    print(f"      • {event.get('event')}: {event.get('time')}")
    
    print("\n" + "=" * 70)
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)

print("\n💡 TIP: If email shows 'sent' but not in inbox:")
print("   1. Check SPAM/Junk folder")
print("   2. Check 'Promotions' tab (Gmail)")
print("   3. Check 'Updates' tab (Gmail)")
print("   4. Search for 'Sam Salameh' in Gmail")
print("=" * 70)
