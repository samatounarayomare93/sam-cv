import sys
import os
import logging
import asyncio

# [🛡️ WINDOWS UTF-8 FIX]
if sys.platform == 'win32':
    import io
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from core import smtp_engine
from core import config

# Force logging to be very verbose
logging.basicConfig(level=logging.DEBUG)

async def deep_diagnostic():
    target = "samsalameh.cv@gmail.com"
    print(f"Starting deep diagnostic for: {target}")
    print("-" * 50)
    
    # 1. Test Gmail SMTP (Direct)
    print("\n[STEP 1] Testing Gmail SMTP (Port 465 SSL)...")
    try:
        import smtplib
        import ssl
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=15) as server:
            server.login(config.GMAIL_SMTP_USER, config.GMAIL_APP_PASSWORD)
            print("[OK] Gmail SMTP Login Success!")
    except Exception as e:
        print(f"[FAIL] Gmail SMTP Login Failed: {e}")

    # 2. Test Brevo HTTP API (Direct)
    print("\n[STEP 2] Testing Brevo HTTP API...")
    try:
        import requests
        headers = {
            "api-key": config.BREVO_API_KEY,
            "content-type": "application/json",
            "accept": "application/json"
        }
        test_payload = {
            "sender": {"name": config.SENDER_NAME, "email": config.SENDER_EMAIL},
            "to": [{"email": target}],
            "subject": "Brevo API Diagnostic",
            "htmlContent": "<html><body>Diagnostic check</body></html>"
        }
        r = requests.post("https://api.brevo.com/v3/smtp/email", headers=headers, json=test_payload, timeout=15)
        if r.status_code in (200, 201, 202):
            print(f"[OK] Brevo API Success! (Status: {r.status_code})")
            print(f"   Response: {r.text}")
        else:
            print(f"[FAIL] Brevo API Failed: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"[ERROR] Brevo API Error: {e}")

    # 3. Test SMTP Engine (End-to-End)
    print("\n[STEP 3] Testing Full SMTP Engine (End-to-End)...")
    try:
        # We use a thread since send_test_email might be blocking
        success = await asyncio.to_thread(smtp_engine.send_test_email, target)
        if success:
            print("[OK] SMTP Engine reported SUCCESS!")
        else:
            print("[FAIL] SMTP Engine reported FAILURE!")
    except Exception as e:
        print(f"[ERROR] SMTP Engine Error: {e}")

if __name__ == "__main__":
    asyncio.run(deep_diagnostic())
