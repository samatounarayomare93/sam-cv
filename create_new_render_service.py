"""
Create a new Render service to get fresh build minutes.
"""
import os, requests, json, time
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY')
github_pat = os.getenv('GITHUB_PAT')
owner_id = 'tea-d6o873v5gffc73epjvt0'

headers_render = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json', 'Accept': 'application/json'}
headers_github = {'Authorization': f'token {github_pat}', 'Accept': 'application/vnd.github.v3+json'}

# Use original repo
repo_url = 'https://github.com/samatounarayomare93/sam-cv'

print("Creating new Render service 'sam-bot-v3'...")

service_payload = {
    "type": "web_service",
    "name": f"sam-bot-v3",
    "ownerId": owner_id,
    "repo": repo_url,
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

r = requests.post(
    'https://api.render.com/v1/services',
    headers=headers_render,
    json=service_payload,
    timeout=30
)
print(f"Status: {r.status_code}")
if r.status_code in (200, 201):
    svc_data = r.json()
    svc = svc_data.get('service', svc_data)
    new_id = svc.get('id', '')
    new_url = svc.get('serviceDetails', {}).get('url', '')
    print(f"SUCCESS!")
    print(f"New service ID: {new_id}")
    print(f"New URL: {new_url}")

    # Now sync all env vars to the new service
    print("\nSyncing env vars to new service...")
    env_vars = []
    important_keys = [
        'GROQ_API_KEY', 'GEMINI_API_KEY', 'OPENROUTER_API_KEY',
        'HUGGINGFACE_API_KEY', 'DEEPSEEK_API_KEY',
        'RESEND_API_KEY', 'BREVO_API_KEY',
        'GMAIL_SMTP_USER', 'GMAIL_APP_PASSWORD',
        'ZOHO_SMTP_USER', 'ZOHO_APP_PASSWORD',
        'ZOHO_SMTP_USER_2', 'ZOHO_APP_PASSWORD_2',
        'SUPABASE_URL', 'SUPABASE_KEY', 'SUPABASE_SERVICE_ROLE_KEY',
        'TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID',
        'TELEGRAM_API_ID', 'TELEGRAM_API_HASH', 'TELEGRAM_SESSION_STRING',
        'GITHUB_PAT', 'RENDER_API_KEY',
        'KILL_SWITCH_ACTIVE', 'SENDER_NAME', 'SENDER_EMAIL',
        'CANDIDATE_NAME', 'CANDIDATE_PHONE', 'LINKEDIN_URL',
        'TEST_RECEIVER_EMAIL', 'BREVO_SMTP_LOGIN', 'BREVO_SMTP_PASSWORD',
        'BREVO_ACCOUNT_EMAIL', 'BREVO_SENDER_EMAIL',
        'RENDER', 'RENDER_EXTERNAL_URL',
    ]
    for k in important_keys:
        v = os.getenv(k, '')
        if v:
            env_vars.append({'key': k, 'value': v})

    # Add new service ID and URL
    env_vars.append({'key': 'RENDER_SERVICE_ID', 'value': new_id})
    env_vars.append({'key': 'RENDER_EXTERNAL_URL', 'value': new_url or f'https://sam-bot-v3.onrender.com'})

    r2 = requests.put(
        f'https://api.render.com/v1/services/{new_id}/env-vars',
        headers=headers_render,
        json=env_vars,
        timeout=30
    )
    print(f"Env vars sync: {r2.status_code}")
    if r2.status_code in (200, 201):
        print(f"Synced {len(env_vars)} env vars!")

    print(f"\n{'='*60}")
    print(f"NEW SERVICE READY!")
    print(f"ID: {new_id}")
    print(f"URL: {new_url}")
    print(f"{'='*60}")
    print(f"\nUpdate .env with:")
    print(f"RENDER_SERVICE_ID={new_id}")

else:
    print(f"Error: {r.text[:500]}")
