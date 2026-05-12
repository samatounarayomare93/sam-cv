"""
After creating a new Render account and service, run this script
with the new service ID to sync all env vars automatically.

Usage:
  .sovereign_runtime\python.exe setup_new_render_account.py NEW_SERVICE_ID NEW_API_KEY
"""
import os, sys, requests
from dotenv import load_dotenv
load_dotenv()

if len(sys.argv) < 3:
    print("""
HOW TO GET A NEW FREE RENDER ACCOUNT:
======================================

1. Open: render.com
2. Click "Sign Up" with a DIFFERENT Google/GitHub account
   (not samatou683@gmail.com)

3. After login, click "New +" → "Web Service"

4. Connect GitHub:
   - Click "Connect GitHub"
   - Authorize Render
   - Search for: sam-cv
   - Select: samatounarayomare93/sam-cv

5. Configure:
   Name:          sam-bot-new
   Region:        Frankfurt (EU)
   Branch:        main
   Build Command: pip install -r requirements.txt
   Start Command: python run.py
   Plan:          Free

6. Click "Create Web Service"

7. Wait for it to start building (2-3 minutes)

8. Go to: dashboard.render.com
   Click your service → Settings → Copy the Service ID (starts with srv-)

9. Go to: dashboard.render.com/u/settings/api-keys
   Create new API key → Copy it

10. Run this script:
    .sovereign_runtime\\python.exe setup_new_render_account.py srv-XXXXXXXX rnd_XXXXXXXX

That's it! All env vars will be synced automatically.
""")
    sys.exit(0)

new_service_id = sys.argv[1]
new_api_key = sys.argv[2]

print(f"Setting up new Render service: {new_service_id}")

headers = {
    'Authorization': f'Bearer {new_api_key}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Verify service exists
r = requests.get(f'https://api.render.com/v1/services/{new_service_id}', headers=headers, timeout=15)
if r.status_code != 200:
    print(f"ERROR: Service not found. Status: {r.status_code}")
    print(r.text[:200])
    sys.exit(1)

svc = r.json()
print(f"Service found: {svc.get('name')} | {svc.get('serviceDetails',{}).get('url','?')}")

# Sync all env vars
env_vars = []
keys_to_sync = {
    'GROQ_API_KEY':           os.getenv('GROQ_API_KEY',''),
    'GEMINI_API_KEY':         os.getenv('GEMINI_API_KEY',''),
    'OPENROUTER_API_KEY':     os.getenv('OPENROUTER_API_KEY',''),
    'HUGGINGFACE_API_KEY':    os.getenv('HUGGINGFACE_API_KEY',''),
    'DEEPSEEK_API_KEY':       os.getenv('DEEPSEEK_API_KEY',''),
    'RESEND_API_KEY':         os.getenv('RESEND_API_KEY',''),
    'BREVO_API_KEY':          os.getenv('BREVO_API_KEY',''),
    'GMAIL_SMTP_USER':        os.getenv('GMAIL_SMTP_USER',''),
    'GMAIL_APP_PASSWORD':     os.getenv('GMAIL_APP_PASSWORD',''),
    'ZOHO_SMTP_USER':         os.getenv('ZOHO_SMTP_USER',''),
    'ZOHO_APP_PASSWORD':      os.getenv('ZOHO_APP_PASSWORD',''),
    'ZOHO_SMTP_USER_2':       os.getenv('ZOHO_SMTP_USER_2',''),
    'ZOHO_APP_PASSWORD_2':    os.getenv('ZOHO_APP_PASSWORD_2',''),
    'SUPABASE_URL':           os.getenv('SUPABASE_URL',''),
    'SUPABASE_KEY':           os.getenv('SUPABASE_KEY',''),
    'SUPABASE_SERVICE_ROLE_KEY': os.getenv('SUPABASE_SERVICE_ROLE_KEY',''),
    'TELEGRAM_BOT_TOKEN':     os.getenv('TELEGRAM_BOT_TOKEN',''),
    'TELEGRAM_CHAT_ID':       os.getenv('TELEGRAM_CHAT_ID',''),
    'TELEGRAM_API_ID':        os.getenv('TELEGRAM_API_ID',''),
    'TELEGRAM_API_HASH':      os.getenv('TELEGRAM_API_HASH',''),
    'TELEGRAM_SESSION_STRING': os.getenv('TELEGRAM_SESSION_STRING',''),
    'GITHUB_PAT':             os.getenv('GITHUB_PAT',''),
    'RENDER_API_KEY':         new_api_key,
    'RENDER_SERVICE_ID':      new_service_id,
    'RENDER_EXTERNAL_URL':    svc.get('serviceDetails',{}).get('url',''),
    'RENDER':                 'true',
    'KILL_SWITCH_ACTIVE':     'false',
    'SENDER_NAME':            os.getenv('SENDER_NAME','Sam Salameh'),
    'SENDER_EMAIL':           os.getenv('SENDER_EMAIL',''),
    'CANDIDATE_NAME':         os.getenv('CANDIDATE_NAME','Sam Salameh'),
    'CANDIDATE_PHONE':        os.getenv('CANDIDATE_PHONE',''),
    'LINKEDIN_URL':           os.getenv('LINKEDIN_URL',''),
    'TEST_RECEIVER_EMAIL':    os.getenv('TEST_RECEIVER_EMAIL',''),
    'BREVO_SMTP_LOGIN':       os.getenv('BREVO_SMTP_LOGIN',''),
    'BREVO_SMTP_PASSWORD':    os.getenv('BREVO_SMTP_PASSWORD',''),
    'BREVO_ACCOUNT_EMAIL':    os.getenv('BREVO_ACCOUNT_EMAIL',''),
    'BREVO_SENDER_EMAIL':     os.getenv('BREVO_SENDER_EMAIL',''),
    'DIVINE_LOG_LEVEL':       'INFO',
    'MAX_PARALLEL_STRIKES':   '5',
    'MAX_EMAILS_PER_DAY':     '1900',
}

for k, v in keys_to_sync.items():
    if v:
        env_vars.append({'key': k, 'value': v})

print(f"\nSyncing {len(env_vars)} env vars...")
r2 = requests.put(
    f'https://api.render.com/v1/services/{new_service_id}/env-vars',
    headers=headers,
    json=env_vars,
    timeout=30
)
print(f"Sync status: {r2.status_code}")
if r2.status_code in (200, 201):
    print("SUCCESS! All env vars synced.")
    
    # Update local .env
    env_path = '.env'
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    import re
    content = re.sub(r'^RENDER_SERVICE_ID=.*$', f'RENDER_SERVICE_ID={new_service_id}', content, flags=re.MULTILINE)
    content = re.sub(r'^RENDER_API_KEY=.*$', f'RENDER_API_KEY={new_api_key}', content, flags=re.MULTILINE)
    
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Local .env updated!")
    
    # Trigger deploy
    print("\nTriggering deploy...")
    r3 = requests.post(
        f'https://api.render.com/v1/services/{new_service_id}/deploys',
        headers=headers,
        json={'clearCache': 'do_not_clear'},
        timeout=15
    )
    if r3.status_code in (200, 201):
        dep = r3.json().get('deploy', r3.json())
        print(f"Deploy triggered! ID: {dep.get('id')}")
        print(f"\nWait 3-5 minutes then test: {svc.get('serviceDetails',{}).get('url','')}")
    else:
        print(f"Deploy trigger: {r3.status_code} - {r3.text[:100]}")
else:
    print(f"Error: {r2.text[:200]}")
