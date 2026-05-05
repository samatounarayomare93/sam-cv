"""
Automatically update ALL Render environment variables
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

RENDER_API_KEY = 'rnd_X4vP0V0M4LOJEGbFiKs2TM72NgTg'
HEADERS = {
    'Authorization': f'Bearer {RENDER_API_KEY}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# Step 1: Get all services
print("Getting Render services...")
r = requests.get('https://api.render.com/v1/services?limit=20', headers=HEADERS, timeout=15)
print(f"Status: {r.status_code}")

if r.status_code != 200:
    print(f"Error: {r.text}")
    exit(1)

services = r.json()
print(f"Found {len(services)} services:")
for s in services:
    svc = s.get('service', {})
    print(f"  - {svc.get('name')} | ID: {svc.get('id')} | URL: {svc.get('serviceDetails', {}).get('url', 'N/A')}")

# Find the bot service
service_id = None
for s in services:
    svc = s.get('service', {})
    name = svc.get('name', '').lower()
    if 'sam' in name or 'job' in name or 'bot' in name or 'cv' in name:
        service_id = svc.get('id')
        print(f"\nFound bot service: {svc.get('name')} (ID: {service_id})")
        break

if not service_id:
    # Use first service
    service_id = services[0].get('service', {}).get('id')
    print(f"\nUsing first service: {services[0].get('service', {}).get('name')} (ID: {service_id})")

# Step 2: Get current env vars
print(f"\nGetting current env vars for service {service_id}...")
r2 = requests.get(
    f'https://api.render.com/v1/services/{service_id}/env-vars',
    headers=HEADERS, timeout=15
)
print(f"Status: {r2.status_code}")

current_vars = {}
if r2.status_code == 200:
    for item in r2.json():
        current_vars[item.get('envVar', {}).get('key')] = item.get('envVar', {}).get('value', '')
    print(f"Current env vars: {len(current_vars)}")

# Step 3: Define ALL vars to set
new_vars = {
    # Zoho Account #2 (NEW)
    'ZOHO_SMTP_USER_2': 'samsalameh@zohomail.com',
    'ZOHO_APP_PASSWORD_2': 'EGDUw41ADNmM',
    
    # Resend API
    'RESEND_API_KEY': os.getenv('RESEND_API_KEY', 're_9hviZvvj_NHBwnZarfmnYfKszJaP4bivu'),
    
    # Zoho Account #1
    'ZOHO_SMTP_USER': os.getenv('ZOHO_SMTP_USER', 'samsalameh.cv@zohomail.com'),
    'ZOHO_APP_PASSWORD': os.getenv('ZOHO_APP_PASSWORD', 'R0R6dqr5qL1g'),
    
    # Gmail
    'GMAIL_SMTP_USER': os.getenv('GMAIL_SMTP_USER', 'samsalameh.cv@gmail.com'),
    'GMAIL_APP_PASSWORD': os.getenv('GMAIL_APP_PASSWORD', 'oimuanudzzngklnf'),
    
    # Brevo
    'BREVO_API_KEY': os.getenv('BREVO_API_KEY', ''),
    'BREVO_SMTP_LOGIN': os.getenv('BREVO_SMTP_LOGIN', ''),
    'BREVO_SMTP_PASSWORD': os.getenv('BREVO_SMTP_PASSWORD', ''),
    
    # Telegram
    'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN', ''),
    'TELEGRAM_CHAT_ID': os.getenv('TELEGRAM_CHAT_ID', ''),
    
    # Supabase
    'SUPABASE_URL': os.getenv('SUPABASE_URL', ''),
    'SUPABASE_KEY': os.getenv('SUPABASE_KEY', ''),
    
    # AI
    'GROQ_API_KEY': os.getenv('GROQ_API_KEY', ''),
    'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY', ''),
    
    # Config
    'TEST_RECEIVER_EMAIL': 'samsalameh.cv@gmail.com',
    'SENDER_EMAIL': 'samsalameh.cv@gmail.com',
    'MAX_EMAILS_PER_DAY': '10000',
    'MAX_EMAILS_PER_HOUR': '500',
    'MAX_PARALLEL_STRIKES': '20',
    'BATCH_SIZE': '50',
}

# Filter out empty values
new_vars = {k: v for k, v in new_vars.items() if v}

print(f"\nVars to update: {len(new_vars)}")

# Step 4: Update env vars
print("\nUpdating env vars on Render...")

# Build the update payload
env_var_list = [{"key": k, "value": v} for k, v in new_vars.items()]

r3 = requests.put(
    f'https://api.render.com/v1/services/{service_id}/env-vars',
    headers=HEADERS,
    json=env_var_list,
    timeout=30
)

print(f"Update status: {r3.status_code}")
if r3.status_code in (200, 201):
    print("✅ ALL ENV VARS UPDATED SUCCESSFULLY!")
    print("\nUpdated vars:")
    for k, v in new_vars.items():
        masked = v[:4] + '...' + v[-4:] if len(v) > 8 else '***'
        print(f"  {k} = {masked}")
    print("\n⏳ Render will auto-redeploy in ~2 minutes...")
else:
    print(f"❌ Error: {r3.text[:500]}")
    
    # Try individual updates
    print("\nTrying individual updates...")
    success = 0
    for k, v in new_vars.items():
        r_ind = requests.put(
            f'https://api.render.com/v1/services/{service_id}/env-vars',
            headers=HEADERS,
            json=[{"key": k, "value": v}],
            timeout=15
        )
        if r_ind.status_code in (200, 201):
            success += 1
        else:
            print(f"  Failed: {k} - {r_ind.status_code}")
    print(f"Individual updates: {success}/{len(new_vars)} succeeded")
