#!/usr/bin/env python3
"""
🔧 ACTIVATE BREVO SENDER - تفعيل samsalameh.cv@gmail.com في Brevo
يضيف Sam's real Gmail كـ verified sender في Brevo
"""
import os
import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

from dotenv import load_dotenv
load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY", "").strip()
GMAIL_USER = os.getenv("GMAIL_SMTP_USER", "samsalameh.cv@gmail.com").strip()

print(f"\n{'='*60}")
print(f"🔧 ACTIVATING BREVO SENDER: {GMAIL_USER}")
print(f"{'='*60}\n")

if not BREVO_API_KEY:
    print("❌ BREVO_API_KEY not found in .env!")
    exit(1)

headers = {
    "api-key": BREVO_API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Step 1: Check current senders
print("📋 Current verified senders:")
r = requests.get("https://api.brevo.com/v3/senders", headers=headers, timeout=10)
if r.status_code == 200:
    senders = r.json().get("senders", [])
    gmail_sender = None
    for s in senders:
        active = "🟢 ACTIVE" if s.get("active") else "🔴 INACTIVE"
        print(f"   {active} - {s.get('email')} (id: {s.get('id')})")
        if s.get("email") == GMAIL_USER:
            gmail_sender = s
else:
    print(f"❌ Could not fetch senders: {r.status_code}")
    exit(1)

print()

# Step 2: If samsalameh.cv@gmail.com exists but inactive, try to resend verification
if gmail_sender:
    sender_id = gmail_sender.get("id")
    is_active = gmail_sender.get("active", False)
    
    if is_active:
        print(f"✅ {GMAIL_USER} is already ACTIVE in Brevo!")
        print("   Update .env: BREVO_PRIMARY_SENDER=samsalameh.cv@gmail.com")
    else:
        print(f"⚠️  {GMAIL_USER} exists but is INACTIVE")
        print(f"   Attempting to resend verification email...")
        
        # Try to resend verification
        r2 = requests.put(
            f"https://api.brevo.com/v3/senders/{sender_id}/validate",
            headers=headers,
            timeout=10
        )
        if r2.status_code in (200, 201, 204):
            print(f"✅ Verification email resent to {GMAIL_USER}!")
            print(f"   📧 Check {GMAIL_USER} inbox and click the verification link!")
        else:
            print(f"   Response: {r2.status_code} - {r2.text[:200]}")
            print(f"\n   💡 Manual fix: Go to https://app.brevo.com/senders")
            print(f"   Find {GMAIL_USER} and click 'Activate' or 'Resend verification'")
else:
    print(f"➕ {GMAIL_USER} not found in Brevo. Creating new sender...")
    
    payload = {
        "name": "Sam Salameh",
        "email": GMAIL_USER
    }
    r2 = requests.post(
        "https://api.brevo.com/v3/senders",
        headers=headers,
        json=payload,
        timeout=10
    )
    if r2.status_code in (200, 201):
        data = r2.json()
        print(f"✅ Sender created! ID: {data.get('id')}")
        print(f"   📧 Check {GMAIL_USER} inbox for verification email from Brevo!")
        print(f"   Click the link to activate the sender.")
    else:
        print(f"❌ Failed to create sender: {r2.status_code} - {r2.text[:300]}")

print(f"\n{'='*60}")
print("📋 WHAT TO DO NEXT:")
print(f"{'='*60}")
print(f"1. Check {GMAIL_USER} inbox for a verification email from Brevo")
print(f"2. Click the verification link in that email")
print(f"3. Run this script again to confirm it's ACTIVE")
print(f"4. Add to .env: BREVO_PRIMARY_SENDER={GMAIL_USER}")
print(f"\nOR: Go directly to https://app.brevo.com/senders")
print(f"    Find {GMAIL_USER} and click Activate")
