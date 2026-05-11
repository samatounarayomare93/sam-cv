"""
Setup new Render account and create service automatically.
"""
import os, sys, requests, json, time
from dotenv import load_dotenv
load_dotenv()

NEW_API_KEY = 'rnd_m4ozEoc4nQYOT16Omj0U9QGd3pra'
headers = {'Authorization': f'Bearer {NEW_API_KEY}', 'Content-Type': 'application/json', 'Accept': 'application/json'}

print("="*60)
print("STEP 1: Verify new API key")
print("="*60)

r = requests.get('https://api.render.com/v1/owners', headers=headers, timeout=15)
print(f"Status: {r.status_code}")
if r.status_code != 200:
    print(f"Error: {r.text[:200]}")
    sys.exit(1)

owners = r.json()
owner = owners[0].get('owner', owners[0]) if owners else {}
owner_id = owner.get('id', '')
owner_email = owner.get('email', '')
print(f"Account: {owner_email}")
print(f"Owner ID: {owner_id}")

print("\n" + "="*60)
print("STEP 2: Create new web service")
print("="*60)

# First check if any services already exist on this account
r_list = requests.get('https://api.render.com/v1/services?limit=10', headers=headers, timeout=15)
existing = r_list.json() if r_list.status_code == 200 else []

if existing:
    print(f"Found {len(existing)} existing service(s) on this account:")
    for svc_item in existing:
        s = svc_item.get('service', svc_item)
        print(f"  {s.get('name')} | {s.get('id')} | {s.get('serviceDetails',{}).get('url','?')}")
    svc = existing[0].get('service', existing[0])
    new_service_id = svc.get('id', '')
    new_url = svc.get('serviceDetails', {}).get('url', '')
    print(f"\nUsing service: {new_service_id} | {new_url}")
else:
    # Try to create service (repo is now public)
    service_payload = {
        "type": "web_service",
        "name": "sam-bot-v2",
        "ownerId": owner_id,
        "repo": "https://github.com/samatounarayomare93/sam-cv",
        "branch": "main",
        "autoDeploy": "yes",
        "serviceDetails": {
            "env": "python",
            "envSpecificDetails": {
                "buildCommand": "pip install -r requirements.txt",
                "startCommand": "python run.py"
            },
            "plan": "free",
            "region": "frankfurt",
            "numInstances": 1,
        }
    }
    r2 = requests.post('https://api.render.com/v1/services', headers=headers, json=service_payload, timeout=30)
    print(f"Create status: {r2.status_code}")
    if r2.status_code in (200, 201):
        svc = r2.json().get('service', r2.json())
        new_service_id = svc.get('id', '')
        new_url = svc.get('serviceDetails', {}).get('url', '')
        print(f"Service created: {new_service_id} | {new_url}")
    else:
        print(f"Error: {r2.text[:300]}")
        sys.exit(1)

print("\n" + "="*60)
print("STEP 3: Sync all env vars")
print("="*60)

env_vars = []
keys_to_sync = {
    'GROQ_API_KEY':              os.getenv('GROQ_API_KEY',''),
    'GEMINI_API_KEY':            os.getenv('GEMINI_API_KEY',''),
    'OPENROUTER_API_KEY':        os.getenv('OPENROUTER_API_KEY',''),
    'HUGGINGFACE_API_KEY':       os.getenv('HUGGINGFACE_API_KEY',''),
    'DEEPSEEK_API_KEY':          os.getenv('DEEPSEEK_API_KEY',''),
    'RESEND_API_KEY':            os.getenv('RESEND_API_KEY',''),
    'BREVO_API_KEY':             os.getenv('BREVO_API_KEY',''),
    'GMAIL_SMTP_USER':           os.getenv('GMAIL_SMTP_USER',''),
    'GMAIL_APP_PASSWORD':        os.getenv('GMAIL_APP_PASSWORD',''),
    'ZOHO_SMTP_USER':            os.getenv('ZOHO_SMTP_USER',''),
    'ZOHO_APP_PASSWORD':         os.getenv('ZOHO_APP_PASSWORD',''),
    'ZOHO_SMTP_USER_2':          os.getenv('ZOHO_SMTP_USER_2',''),
    'ZOHO_APP_PASSWORD_2':       os.getenv('ZOHO_APP_PASSWORD_2',''),
    'SUPABASE_URL':              os.getenv('SUPABASE_URL',''),
    'SUPABASE_KEY':              os.getenv('SUPABASE_KEY',''),
    'SUPABASE_SERVICE_ROLE_KEY': os.getenv('SUPABASE_SERVICE_ROLE_KEY',''),
    'TELEGRAM_BOT_TOKEN':        os.getenv('TELEGRAM_BOT_TOKEN',''),
    'TELEGRAM_CHAT_ID':          os.getenv('TELEGRAM_CHAT_ID',''),
    'TELEGRAM_API_ID':           os.getenv('TELEGRAM_API_ID',''),
    'TELEGRAM_API_HASH':         os.getenv('TELEGRAM_API_HASH',''),
    'TELEGRAM_SESSION_STRING':   os.getenv('TELEGRAM_SESSION_STRING',''),
    'GITHUB_PAT':                os.getenv('GITHUB_PAT',''),
    'RENDER_API_KEY':            NEW_API_KEY,
    'RENDER_SERVICE_ID':         new_service_id,
    'RENDER_EXTERNAL_URL':       new_url,
    'RENDER':                    'true',
    'KILL_SWITCH_ACTIVE':        'false',
    'SENDER_NAME':               os.getenv('SENDER_NAME','Sam Salameh'),
    'SENDER_EMAIL':              os.getenv('SENDER_EMAIL',''),
    'CANDIDATE_NAME':            os.getenv('CANDIDATE_NAME','Sam Salameh'),
    'CANDIDATE_PHONE':           os.getenv('CANDIDATE_PHONE',''),
    'LINKEDIN_URL':              os.getenv('LINKEDIN_URL',''),
    'TEST_RECEIVER_EMAIL':       os.getenv('TEST_RECEIVER_EMAIL',''),
    'BREVO_SMTP_LOGIN':          os.getenv('BREVO_SMTP_LOGIN',''),
    'BREVO_SMTP_PASSWORD':       os.getenv('BREVO_SMTP_PASSWORD',''),
    'BREVO_ACCOUNT_EMAIL':       os.getenv('BREVO_ACCOUNT_EMAIL',''),
    'BREVO_SENDER_EMAIL':        os.getenv('BREVO_SENDER_EMAIL',''),
    'DIVINE_LOG_LEVEL':          'INFO',
    'MAX_PARALLEL_STRIKES':      '5',
    'MAX_EMAILS_PER_DAY':        '1900',
    'MAX_APPLICATIONS_PER_DAY':  '1500',
    'MIN_MATCH_SCORE':           '45',
}

for k, v in keys_to_sync.items():
    if v:
        env_vars.append({'key': k, 'value': v})

r = requests.put(
    f'https://api.render.com/v1/services/{new_service_id}/env-vars',
    headers=headers, json=env_vars, timeout=30
)
print(f"Env sync: {r.status_code} — {len(env_vars)} vars")

print("\n" + "="*60)
print("STEP 4: Save to local .env")
print("="*60)

import re
env_path = '.env'
with open(env_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'^RENDER_SERVICE_ID=.*$', f'RENDER_SERVICE_ID={new_service_id}', content, flags=re.MULTILINE)
content = re.sub(r'^RENDER_API_KEY=.*$',    f'RENDER_API_KEY={NEW_API_KEY}',        content, flags=re.MULTILINE)

with open(env_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Local .env updated!")

print("\n" + "="*60)
print("RESULT")
print("="*60)
print(f"Account:    {owner_email}")
print(f"Service ID: {new_service_id}")
print(f"URL:        {new_url}")
print(f"API Key:    {NEW_API_KEY[:20]}...")
print(f"\nBuild will start automatically in ~1 minute.")
print(f"Check status: python check_render_status.py")
