#!/usr/bin/env python3
"""
🔧 FIX BREVO SENDER NAME - تصليح اسم المرسل في Brevo
يغير اسم samatou683@gmail.com من "Aurora" إلى "Sam Salameh"
"""
import os
import requests

from dotenv import load_dotenv
load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY", "").strip()

headers = {
    "api-key": BREVO_API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

print("🔧 Fixing Brevo sender names...\n")

# Get all senders
r = requests.get("https://api.brevo.com/v3/senders", headers=headers, timeout=10)
senders = r.json().get("senders", [])

for sender in senders:
    sender_id = sender.get("id")
    email = sender.get("email")
    name = sender.get("name")
    active = sender.get("active")
    
    print(f"Sender ID {sender_id}: {email} (name: '{name}', active: {active})")
    
    # Fix the name if it's wrong
    if email == "samatou683@gmail.com" and name != "Sam Salameh":
        print(f"  → Updating name from '{name}' to 'Sam Salameh'...")
        r2 = requests.put(
            f"https://api.brevo.com/v3/senders/{sender_id}",
            headers=headers,
            json={"name": "Sam Salameh", "email": email},
            timeout=10
        )
        if r2.status_code in (200, 201, 204):
            print(f"  ✅ Name updated to 'Sam Salameh'!")
        else:
            print(f"  ❌ Failed: {r2.status_code} - {r2.text[:200]}")
    elif email == "samatou683@gmail.com" and name == "Sam Salameh":
        print(f"  ✅ Name already correct!")

print("\n✅ Done!")
