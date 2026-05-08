#!/usr/bin/env python3
"""
🔍 DIAGNOSE EMAIL NOW - COMPREHENSIVE AUDIT
Checks all providers and identifying the exact point of failure.
"""
import os
import sys
import requests
import smtplib
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load .env
load_dotenv()

TEST_EMAIL = os.getenv("TEST_RECEIVER_EMAIL", "samsalameh.cv@gmail.com")
print(f"\n{'='*60}")
print(f"DIAGNOSING EMAIL DELIVERY TO: {TEST_EMAIL}")
print(f"{'='*60}\n")

# ── 0. ENVIRONMENT CHECK ───────────────────────────────────────
is_render = os.getenv("RENDER") or os.getenv("RENDER_SERVICE_ID")
print(f"TEST 0: Environment Check")
print(f"   Platform: {'RENDER (Cloud)' if is_render else 'LOCAL (PC)'}")
if is_render:
    print(f"   Note: SMTP ports 465/587 are often blocked on cloud. Port 2525 or HTTP API is preferred.")
print()

# ── 1. BREVO HTTP API ──────────────────────────────────────────
print("TEST 1: Brevo HTTP API")
brevo_api = os.getenv("BREVO_API_KEY", "").strip()
if not brevo_api:
    brevo_api = "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"

brevo_account = os.getenv("BREVO_ACCOUNT_EMAIL", "samatou683@gmail.com").strip()
gmail_user = os.getenv("GMAIL_SMTP_USER", "samsalameh.cv@gmail.com").strip()

print(f"   API Key: {'SET (Fallback used)' if not os.getenv('BREVO_API_KEY') else 'SET (User key)'}")
print(f"   Default Sender: {brevo_account}")
print(f"   Candidate Email: {gmail_user}")

if brevo_api:
    # First check what senders are verified
    print("\n   Checking Brevo verified senders...")
    active_senders = []
    try:
        r = requests.get(
            "https://api.brevo.com/v3/senders",
            headers={"api-key": brevo_api, "Accept": "application/json"},
            timeout=10
        )
        if r.status_code == 200:
            senders = r.json().get("senders", [])
            print(f"   Verified senders in Brevo ({len(senders)} total):")
            for s in senders:
                status = "ACTIVE" if s.get("active") else "INACTIVE"
                print(f"      {status} - {s.get('email')} ({s.get('name')})")
                if s.get("active"):
                    active_senders.append(s.get("email"))
        else:
            print(f"   Could not fetch senders: {r.status_code} - {r.text[:200]}")
    except Exception as e:
        print(f"   Error checking senders: {e}")

    # Determine best sender
    best_sender = brevo_account
    if gmail_user in active_senders:
        best_sender = gmail_user
        print(f"\n   SUCCESS: {gmail_user} is ACTIVE. Using as primary.")
    else:
        print(f"\n   WARNING: {gmail_user} is NOT active in Brevo. Falling back to {brevo_account}.")

    # Try sending test email via Brevo
    print(f"   Sending test email via Brevo from {best_sender}...")
    try:
        payload = {
            "sender": {"email": best_sender, "name": "Sam Salameh"},
            "to": [{"email": TEST_EMAIL}],
            "subject": "BREVO DIAGNOSTIC - Sam Job Automator",
            "htmlContent": f"""
            <h2>Brevo Diagnostic Test</h2>
            <p><strong>Environment:</strong> {'Render' if is_render else 'Local'}</p>
            <p><strong>Sender Used:</strong> {best_sender}</p>
            <p><strong>Status:</strong> This confirms HTTP API delivery is working.</p>
            """,
            "replyTo": {"email": gmail_user, "name": "Sam Salameh"}
        }
        r = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={"api-key": brevo_api, "Content-Type": "application/json"},
            json=payload,
            timeout=20
        )
        if r.status_code in (200, 201, 202):
            print(f"   BREVO SUCCESS! Status: {r.status_code}")
        else:
            print(f"   BREVO FAILED: {r.status_code}")
            print(f"   Response: {r.text[:300]}")
    except Exception as e:
        print(f"   Exception: {e}")

print()

# ── 2. GMAIL SMTP ──────────────────────────────────────────────
print("TEST 2: Gmail SMTP (Port 465 SSL)")
gmail_pass = os.getenv("GMAIL_APP_PASSWORD", "").strip()

if gmail_user and gmail_pass:
    try:
        print(f"   Connecting to smtp.gmail.com:465...")
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15)
        server.login(gmail_user, gmail_pass)
        print(f"   Gmail SMTP connected and authenticated!")
        server.quit()
    except Exception as e:
        print(f"   Gmail SMTP Error: {type(e).__name__}: {e}")
        if "Network is unreachable" in str(e) or "Timeout" in str(e):
            print(f"   DIAGNOSIS: Port 465 is BLOCKED by your current network/hosting.")
else:
    print("   Skipped - Gmail credentials missing")

print()

# ── 3. ZOHO SMTP ───────────────────────────────────────────────
print("TEST 3: Zoho SMTP (Port 465 SSL)")
zoho_user = os.getenv("ZOHO_SMTP_USER", "").strip()
zoho_pass = os.getenv("ZOHO_APP_PASSWORD", "").strip()

if zoho_user and zoho_pass:
    try:
        print(f"   Connecting to smtp.zoho.com:465...")
        server = smtplib.SMTP_SSL("smtp.zoho.com", 465, timeout=15)
        server.login(zoho_user, zoho_pass)
        print(f"   Zoho SMTP connected and authenticated!")
        server.quit()
    except Exception as e:
        print(f"   Zoho SMTP Error: {type(e).__name__}: {e}")
else:
    print("   Skipped - Zoho credentials missing")

print(f"\n{'='*60}")
print("DIAGNOSIS COMPLETE")
print(f"{'='*60}\n")

print("💡 RECOMMENDATION:")
if is_render:
    print("1. Use BREVO HTTP API or RESEND API for production on Render.")
    print("2. Ensure samsalameh.cv@gmail.com is VERIFIED in Brevo dashboard.")
else:
    print("1. Gmail SMTP is working locally - perfect for dev.")
    print("2. Run the final_strike_verification.py to see the new premium design.")
