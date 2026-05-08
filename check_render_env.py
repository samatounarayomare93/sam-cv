#!/usr/bin/env python3
"""Check if critical env vars are set on Render."""
import requests, os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY')
service_id = os.getenv('RENDER_SERVICE_ID')
headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}

print("🔍 Checking Render environment variables...\n")

r = requests.get(
    f'https://api.render.com/v1/services/{service_id}/env-vars',
    headers=headers, timeout=15
)

if r.status_code == 200:
    env_vars = r.json()
    
    critical_vars = [
        'GMAIL_SMTP_USER', 'GMAIL_APP_PASSWORD',
        'ZOHO_SMTP_USER', 'ZOHO_APP_PASSWORD',
        'BREVO_API_KEY', 'BREVO_ACCOUNT_EMAIL',
        'TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID',
        'SUPABASE_URL', 'SUPABASE_KEY'
    ]
    
    # Build a dict of what's set
    set_vars = {}
    for item in env_vars:
        if isinstance(item, dict):
            key = item.get('envVar', {}).get('key', '') or item.get('key', '')
            val = item.get('envVar', {}).get('value', '') or item.get('value', '')
            if key:
                set_vars[key] = val
    
    print(f"Total env vars on Render: {len(set_vars)}\n")
    print("Critical variables status:")
    for var in critical_vars:
        if var in set_vars:
            val = set_vars[var]
            # Show partial value for security
            display = val[:4] + '...' + val[-4:] if len(val) > 8 else '***'
            print(f"  ✅ {var} = {display}")
        else:
            print(f"  ❌ {var} = NOT SET ← MISSING!")
    
    # Check for GMAIL_APP_PASSWORD specifically
    if 'GMAIL_APP_PASSWORD' not in set_vars:
        print("\n🚨 GMAIL_APP_PASSWORD is NOT set on Render!")
        print("   This is why Gmail SMTP fails on Render.")
        print("   Fix: Go to Render dashboard → Environment → Add GMAIL_APP_PASSWORD")
        local_pass = os.getenv('GMAIL_APP_PASSWORD', '')
        if local_pass:
            print(f"   Value to add: {local_pass}")
else:
    print(f"❌ Could not fetch env vars: {r.status_code} - {r.text[:300]}")
    
    # Try alternative endpoint
    r2 = requests.get(
        f'https://api.render.com/v1/services/{service_id}/env-groups',
        headers=headers, timeout=15
    )
    print(f"Alt endpoint: {r2.status_code} - {r2.text[:200]}")
