#!/usr/bin/env python3
"""
Check Brevo account status and recent email deliveries
"""
import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

api_key = os.getenv('BREVO_API_KEY')

if not api_key:
    print("❌ BREVO_API_KEY not found in .env")
    exit(1)

headers = {
    "api-key": api_key,
    "Content-Type": "application/json"
}

print("=" * 80)
print("🔍 CHECKING BREVO ACCOUNT STATUS")
print("=" * 80)

# 1. Check account info
print("\n📊 Account Information:")
try:
    response = requests.get("https://api.brevo.com/v3/account", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Email: {data.get('email', 'N/A')}")
        print(f"✅ Plan: {data.get('plan', [{}])[0].get('type', 'N/A')}")
        print(f"✅ Credits: {data.get('plan', [{}])[0].get('credits', 'N/A')}")
    else:
        print(f"❌ Failed to get account info: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"❌ Error: {e}")

# 2. Check email events (last 24 hours)
print("\n📧 Recent Email Events (Last 24 hours):")
try:
    # Get events from last 24 hours
    end_date = datetime.now()
    start_date = end_date - timedelta(hours=24)
    
    params = {
        "limit": 50,
        "offset": 0,
        "startDate": start_date.strftime("%Y-%m-%d"),
        "endDate": end_date.strftime("%Y-%m-%d"),
        "email": "samsalameh.cv@gmail.com"  # Filter by recipient
    }
    
    response = requests.get(
        "https://api.brevo.com/v3/smtp/statistics/events",
        headers=headers,
        params=params
    )
    
    if response.status_code == 200:
        data = response.json()
        events = data.get('events', [])
        
        if events:
            print(f"✅ Found {len(events)} events:")
            for event in events[:10]:  # Show last 10
                event_type = event.get('event', 'unknown')
                email = event.get('email', 'N/A')
                date = event.get('date', 'N/A')
                subject = event.get('subject', 'N/A')
                message_id = event.get('message-id', 'N/A')
                
                print(f"\n  📨 Event: {event_type}")
                print(f"     To: {email}")
                print(f"     Subject: {subject[:50]}...")
                print(f"     Date: {date}")
                print(f"     Message ID: {message_id}")
                
                # Check for bounces or blocks
                if event_type in ['hard_bounce', 'soft_bounce', 'blocked', 'invalid_email']:
                    print(f"     ⚠️ REASON: {event.get('reason', 'N/A')}")
        else:
            print("⚠️ No events found in last 24 hours")
    else:
        print(f"❌ Failed to get events: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"❌ Error: {e}")

# 3. Check senders
print("\n📤 Configured Senders:")
try:
    response = requests.get("https://api.brevo.com/v3/senders", headers=headers)
    if response.status_code == 200:
        data = response.json()
        senders = data.get('senders', [])
        if senders:
            for sender in senders:
                email = sender.get('email', 'N/A')
                name = sender.get('name', 'N/A')
                active = sender.get('active', False)
                print(f"  {'✅' if active else '❌'} {name} <{email}>")
        else:
            print("  ⚠️ No senders configured")
    else:
        print(f"❌ Failed to get senders: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("🔍 DIAGNOSIS:")
print("=" * 80)
print("""
If you see 'blocked' or 'hard_bounce' events:
  → Brevo is blocking emails to Gmail
  → Solution: Use a different sender address (not Gmail)

If you see 'delivered' events but no email:
  → Gmail is silently dropping emails
  → Solution: Add SPF/DKIM records or use Gmail API

If you see no events at all:
  → Emails are not being sent to Brevo
  → Check the bot logs for errors
""")
