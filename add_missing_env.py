import requests
import os
from dotenv import load_dotenv

load_dotenv()

RENDER_API_KEY = 'rnd_X4vP0V0M4LOJEGbFiKs2TM72NgTg'
SERVICE_ID = 'srv-d7s6rf6gvqtc73bt431g'

headers = {
    'Authorization': f'Bearer {RENDER_API_KEY}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# Get current env vars to see what's missing
r = requests.get(
    f'https://api.render.com/v1/services/{SERVICE_ID}/env-vars',
    headers=headers, timeout=15
)
current = {item['envVar']['key']: item['envVar']['value'] for item in r.json()}
print(f"Current vars: {len(current)}")
print("Keys:", list(current.keys()))

# Add ALL missing critical vars
missing_vars = []

# Check what's missing
critical_vars = {
    'SUPABASE_SERVICE_ROLE_KEY': os.getenv('SUPABASE_SERVICE_ROLE_KEY', ''),
    'SUPABASE_URL': os.getenv('SUPABASE_URL', ''),
    'SUPABASE_KEY': os.getenv('SUPABASE_KEY', ''),
    'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN', ''),
    'TELEGRAM_CHAT_ID': os.getenv('TELEGRAM_CHAT_ID', ''),
    'GROQ_API_KEY': os.getenv('GROQ_API_KEY', ''),
    'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY', ''),
    'BREVO_API_KEY': os.getenv('BREVO_API_KEY', ''),
    'RESEND_API_KEY': os.getenv('RESEND_API_KEY', ''),
    'ZOHO_SMTP_USER': os.getenv('ZOHO_SMTP_USER', ''),
    'ZOHO_APP_PASSWORD': os.getenv('ZOHO_APP_PASSWORD', ''),
    'ZOHO_SMTP_USER_2': os.getenv('ZOHO_SMTP_USER_2', ''),
    'ZOHO_APP_PASSWORD_2': os.getenv('ZOHO_APP_PASSWORD_2', ''),
    'GMAIL_SMTP_USER': os.getenv('GMAIL_SMTP_USER', ''),
    'GMAIL_APP_PASSWORD': os.getenv('GMAIL_APP_PASSWORD', ''),
    'BREVO_SMTP_LOGIN': os.getenv('BREVO_SMTP_LOGIN', ''),
    'BREVO_SMTP_PASSWORD': os.getenv('BREVO_SMTP_PASSWORD', ''),
}

for key, val in critical_vars.items():
    if key not in current and val:
        missing_vars.append({'key': key, 'value': val})
        print(f"MISSING: {key}")
    elif key in current:
        print(f"OK: {key}")

if missing_vars:
    print(f"\nAdding {len(missing_vars)} missing vars...")
    # Get all current vars + add missing
    all_vars = [{'key': k, 'value': v} for k, v in current.items()]
    all_vars.extend(missing_vars)
    
    r2 = requests.put(
        f'https://api.render.com/v1/services/{SERVICE_ID}/env-vars',
        headers=headers,
        json=all_vars,
        timeout=30
    )
    print(f"Update status: {r2.status_code}")
    if r2.status_code == 200:
        print("✅ All missing vars added!")
    else:
        print(f"Error: {r2.text[:300]}")
else:
    print("\nAll vars already set!")
