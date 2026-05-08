#!/usr/bin/env python3
"""
🚀 SYNC ALL ENV VARS TO RENDER
يرفع كل الـ credentials من .env إلى Render dashboard
"""
import requests, os, time
from dotenv import load_dotenv
load_dotenv()

RENDER_API_KEY = os.getenv('RENDER_API_KEY')
SERVICE_ID = os.getenv('RENDER_SERVICE_ID')
headers = {'Authorization': f'Bearer {RENDER_API_KEY}', 'Accept': 'application/json', 'Content-Type': 'application/json'}

# All critical env vars to sync to Render
ENV_VARS_TO_SYNC = {
    # Email - Gmail (PRIMARY - best deliverability)
    'GMAIL_SMTP_USER': os.getenv('GMAIL_SMTP_USER', ''),
    'GMAIL_APP_PASSWORD': os.getenv('GMAIL_APP_PASSWORD', ''),
    
    # Email - Zoho (SECONDARY)
    'ZOHO_SMTP_USER': os.getenv('ZOHO_SMTP_USER', ''),
    'ZOHO_APP_PASSWORD': os.getenv('ZOHO_APP_PASSWORD', ''),
    'ZOHO_SMTP_USER_2': os.getenv('ZOHO_SMTP_USER_2', ''),
    'ZOHO_APP_PASSWORD_2': os.getenv('ZOHO_APP_PASSWORD_2', ''),
    
    # Email - Brevo (FALLBACK)
    'BREVO_API_KEY': os.getenv('BREVO_API_KEY', ''),
    'BREVO_SMTP_LOGIN': os.getenv('BREVO_SMTP_LOGIN', ''),
    'BREVO_SMTP_PASSWORD': os.getenv('BREVO_SMTP_PASSWORD', ''),
    'BREVO_ACCOUNT_EMAIL': os.getenv('BREVO_ACCOUNT_EMAIL', ''),
    'BREVO_SENDER_EMAIL': os.getenv('BREVO_SENDER_EMAIL', ''),
    'BREVO_PRIMARY_SENDER': os.getenv('BREVO_PRIMARY_SENDER', 'samatou683@gmail.com'),
    
    # Telegram
    'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN', ''),
    'TELEGRAM_CHAT_ID': os.getenv('TELEGRAM_CHAT_ID', ''),
    'TELEGRAM_API_ID': os.getenv('TELEGRAM_API_ID', ''),
    'TELEGRAM_API_HASH': os.getenv('TELEGRAM_API_HASH', ''),
    'TELEGRAM_SESSION_STRING': os.getenv('TELEGRAM_SESSION_STRING', ''),
    
    # Supabase
    'SUPABASE_URL': os.getenv('SUPABASE_URL', ''),
    'SUPABASE_KEY': os.getenv('SUPABASE_KEY', ''),
    'SUPABASE_SERVICE_ROLE_KEY': os.getenv('SUPABASE_SERVICE_ROLE_KEY', ''),
    
    # AI
    'GROQ_API_KEY': os.getenv('GROQ_API_KEY', ''),
    'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY', ''),
    
    # Resend
    'RESEND_API_KEY': os.getenv('RESEND_API_KEY', ''),
    'RESEND_FROM_EMAIL': os.getenv('RESEND_FROM_EMAIL', ''),
    
    # Identity
    'SENDER_NAME': os.getenv('SENDER_NAME', 'Sam Salameh'),
    'SENDER_EMAIL': os.getenv('SENDER_EMAIL', ''),
    'CANDIDATE_NAME': os.getenv('CANDIDATE_NAME', 'Sam Salameh'),
    'CANDIDATE_PHONE': os.getenv('CANDIDATE_PHONE', ''),
    'LINKEDIN_URL': os.getenv('LINKEDIN_URL', ''),
    'CANDIDATE_PROFESSION': os.getenv('CANDIDATE_PROFESSION', 'Senior Network Engineer'),
    
    # Test
    'TEST_RECEIVER_EMAIL': os.getenv('TEST_RECEIVER_EMAIL', ''),
    
    # System
    'KILL_SWITCH_ACTIVE': 'false',
    'DIVINE_LOG_LEVEL': 'INFO',
    'MAX_PARALLEL_STRIKES': os.getenv('MAX_PARALLEL_STRIKES', '5'),
    'MAX_EMAILS_PER_DAY': os.getenv('MAX_EMAILS_PER_DAY', '1900'),
    'GITHUB_PAT': os.getenv('GITHUB_PAT', ''),
    'RENDER_API_KEY': os.getenv('RENDER_API_KEY', ''),
    'RENDER_SERVICE_ID': os.getenv('RENDER_SERVICE_ID', ''),
}

# Filter out empty values
env_vars_to_set = {k: v for k, v in ENV_VARS_TO_SYNC.items() if v}

print(f"🚀 Syncing {len(env_vars_to_set)} env vars to Render service {SERVICE_ID}...\n")

# Build the payload for bulk update
env_var_list = [{"key": k, "value": v} for k, v in env_vars_to_set.items()]

# Render API: PUT /services/{id}/env-vars (bulk update)
r = requests.put(
    f'https://api.render.com/v1/services/{SERVICE_ID}/env-vars',
    headers=headers,
    json=env_var_list,
    timeout=30
)

if r.status_code in (200, 201):
    result = r.json()
    print(f"✅ SUCCESS! {len(env_var_list)} env vars synced to Render!")
    print("\nSynced variables:")
    for item in env_var_list:
        key = item['key']
        val = item['value']
        display = val[:4] + '...' + val[-4:] if len(val) > 8 else '***'
        print(f"  ✅ {key} = {display}")
    
    print("\n🔄 Render will auto-redeploy with new env vars...")
    print("⏳ Wait 2-3 minutes then test the bot again via Telegram")
    
elif r.status_code == 400:
    print(f"⚠️ Bulk update failed ({r.status_code}), trying one by one...")
    print(f"Error: {r.text[:300]}")
    
    # Try one by one
    success_count = 0
    fail_count = 0
    for key, value in env_vars_to_set.items():
        r2 = requests.put(
            f'https://api.render.com/v1/services/{SERVICE_ID}/env-vars',
            headers=headers,
            json=[{"key": key, "value": value}],
            timeout=15
        )
        if r2.status_code in (200, 201):
            success_count += 1
            display = value[:4] + '...' + value[-4:] if len(value) > 8 else '***'
            print(f"  ✅ {key} = {display}")
        else:
            fail_count += 1
            print(f"  ❌ {key} failed: {r2.status_code} - {r2.text[:100]}")
        time.sleep(0.2)
    
    print(f"\n✅ {success_count} synced, ❌ {fail_count} failed")
else:
    print(f"❌ Failed: {r.status_code} - {r.text[:500]}")
