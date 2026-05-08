#!/usr/bin/env python3
"""
🔍 Simulate EXACTLY what Render does when sending email
Same code path, same env vars, but force is_render=True
"""
import os, sys, logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

# Force Render mode
os.environ['RENDER'] = 'true'

TEST_EMAIL = os.getenv('TEST_RECEIVER_EMAIL', 'samsalameh.cv@gmail.com')
print(f"\n{'='*60}")
print(f"🔍 SIMULATING RENDER EMAIL SEND TO: {TEST_EMAIL}")
print(f"{'='*60}\n")

# Check what's available
print("📋 Credentials check:")
print(f"  GMAIL_SMTP_USER: {os.getenv('GMAIL_SMTP_USER','❌ MISSING')}")
print(f"  GMAIL_APP_PASSWORD: {'✅ SET' if os.getenv('GMAIL_APP_PASSWORD') else '❌ MISSING'}")
print(f"  ZOHO_SMTP_USER: {os.getenv('ZOHO_SMTP_USER','❌ MISSING')}")
print(f"  ZOHO_APP_PASSWORD: {'✅ SET' if os.getenv('ZOHO_APP_PASSWORD') else '❌ MISSING'}")
print(f"  BREVO_API_KEY: {'✅ SET' if os.getenv('BREVO_API_KEY') else '❌ MISSING'}")
print()

from core import smtp_engine

print(f"🚀 Calling send_email() with RENDER=true...\n")
result = smtp_engine.send_email(
    to_email=TEST_EMAIL,
    company_name="Test Company",
    job_title="Network Engineer",
    custom_body="<p>This is a test from Render simulation.</p>",
    platform="test",
    mission_type="test",
    attachment_paths=[],
    sender_name="Sam Salameh"
)

print(f"\n{'='*60}")
print(f"RESULT: {'✅ SUCCESS - Email sent!' if result else '❌ FAILED - Email NOT sent'}")
print(f"{'='*60}")
