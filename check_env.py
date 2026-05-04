#!/usr/bin/env python3
"""
🔍 Environment Variables Checker
Verifies all required credentials are configured
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 80)
print("🔍 CHECKING ENVIRONMENT VARIABLES")
print("=" * 80)

# Check if running on Render
is_render = os.getenv("RENDER") is not None
print(f"\n📍 Environment: {'☁️ RENDER CLOUD' if is_render else '💻 LOCAL'}")

# Required variables
required_vars = {
    "GMAIL_SMTP_USER": "Gmail email address",
    "GMAIL_APP_PASSWORD": "Gmail app password (16 chars)",
    "TELEGRAM_BOT_TOKEN": "Telegram bot token",
    "TELEGRAM_CHAT_ID": "Telegram chat ID",
    "SUPABASE_URL": "Supabase database URL",
    "SUPABASE_KEY": "Supabase API key",
}

# Optional but recommended
optional_vars = {
    "BREVO_API_KEY": "Brevo API key (backup email)",
    "BREVO_SMTP_LOGIN": "Brevo SMTP login",
    "BREVO_SMTP_PASSWORD": "Brevo SMTP password",
    "ZOHO_SMTP_USER": "Zoho email (backup)",
    "ZOHO_APP_PASSWORD": "Zoho app password",
}

print("\n" + "=" * 80)
print("📋 REQUIRED VARIABLES")
print("=" * 80)

all_good = True
for var, desc in required_vars.items():
    value = os.getenv(var, "").strip()
    if value:
        # Mask sensitive values
        if "PASSWORD" in var or "TOKEN" in var or "KEY" in var:
            display = f"{value[:4]}...{value[-4:]}" if len(value) > 8 else "***"
        else:
            display = value[:30] + "..." if len(value) > 30 else value
        print(f"✅ {var:25} = {display}")
    else:
        print(f"❌ {var:25} = MISSING!")
        all_good = False

print("\n" + "=" * 80)
print("📋 OPTIONAL VARIABLES (Backups)")
print("=" * 80)

for var, desc in optional_vars.items():
    value = os.getenv(var, "").strip()
    if value:
        if "PASSWORD" in var or "TOKEN" in var or "KEY" in var:
            display = f"{value[:4]}...{value[-4:]}" if len(value) > 8 else "***"
        else:
            display = value[:30] + "..." if len(value) > 30 else value
        print(f"✅ {var:25} = {display}")
    else:
        print(f"⚠️  {var:25} = Not set (optional)")

print("\n" + "=" * 80)
if all_good:
    print("🎉 ALL REQUIRED VARIABLES ARE SET!")
    print("=" * 80)
    print("\n✅ Your bot should work correctly.")
    if is_render:
        print("☁️  Running on Render - credentials are configured!")
else:
    print("❌ SOME REQUIRED VARIABLES ARE MISSING!")
    print("=" * 80)
    if is_render:
        print("\n🔧 FIX ON RENDER:")
        print("   1. Go to: https://dashboard.render.com")
        print("   2. Select your service")
        print("   3. Go to 'Environment' tab")
        print("   4. Add the missing variables")
        print("   5. Save and wait for redeploy")
    else:
        print("\n🔧 FIX LOCALLY:")
        print("   1. Edit your .env file")
        print("   2. Add the missing variables")
        print("   3. Save and restart the bot")

print("\n" + "=" * 80)
