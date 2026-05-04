"""Test SendPulse API connection and email sending"""
import requests
import os
import sys
from dotenv import load_dotenv
load_dotenv()

def test_sendpulse(client_id, client_secret):
    print(f"Testing SendPulse...")
    print(f"Client ID: {client_id[:10]}...")
    
    # Step 1: Get token
    print("\n1. Getting access token...")
    r = requests.post(
        "https://api.sendpulse.com/oauth/access_token",
        json={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        },
        timeout=15
    )
    print(f"   Status: {r.status_code}")
    if r.status_code != 200:
        print(f"   ERROR: {r.text}")
        return False
    
    token = r.json().get("access_token")
    print(f"   Token: {token[:20]}...")
    
    # Step 2: Check account info
    print("\n2. Checking account info...")
    headers = {"Authorization": f"Bearer {token}"}
    r2 = requests.get("https://api.sendpulse.com/user/balance", headers=headers, timeout=10)
    print(f"   Status: {r2.status_code}")
    if r2.status_code == 200:
        data = r2.json()
        print(f"   Balance: {data}")
    
    # Step 3: Send test email
    print("\n3. Sending test email...")
    payload = {
        "email": {
            "html": "<h2>SendPulse Test!</h2><p>SendPulse is working! 400 emails/day unlocked!</p>",
            "text": "SendPulse is working!",
            "subject": "SendPulse Test - Working!",
            "from": {"name": "Sam Salameh", "email": "samsalameh.cv@gmail.com"},
            "to": [{"name": "Sam", "email": "samsalameh.cv@gmail.com"}]
        }
    }
    r3 = requests.post(
        "https://api.sendpulse.com/smtp/emails",
        headers={**headers, "Content-Type": "application/json"},
        json=payload,
        timeout=20
    )
    print(f"   Status: {r3.status_code}")
    print(f"   Response: {r3.text[:300]}")
    
    if r3.status_code in (200, 201, 202):
        print("\n✅ SENDPULSE WORKS! Email sent!")
        return True
    else:
        print("\n❌ SendPulse email failed")
        return False

# Get from command line args or env
if len(sys.argv) == 3:
    client_id = sys.argv[1]
    client_secret = sys.argv[2]
elif os.getenv("SENDPULSE_CLIENT_ID"):
    client_id = os.getenv("SENDPULSE_CLIENT_ID")
    client_secret = os.getenv("SENDPULSE_CLIENT_SECRET")
else:
    print("Usage: python test_sendpulse.py CLIENT_ID CLIENT_SECRET")
    print("Or set SENDPULSE_CLIENT_ID and SENDPULSE_CLIENT_SECRET in .env")
    sys.exit(1)

test_sendpulse(client_id, client_secret)
