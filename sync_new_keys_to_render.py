"""
Sync all API keys from .env to Render environment variables.
Run this once to push everything to Render.
"""
import os, sys, requests
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()

render_key = os.getenv('RENDER_API_KEY')
render_svc = os.getenv('RENDER_SERVICE_ID')
headers = {'Authorization': f'Bearer {render_key}', 'Content-Type': 'application/json'}

# All keys to sync
keys_to_sync = {
    'GROQ_API_KEY':         os.getenv('GROQ_API_KEY', ''),
    'GEMINI_API_KEY':       os.getenv('GEMINI_API_KEY', ''),
    'DEEPSEEK_API_KEY':     os.getenv('DEEPSEEK_API_KEY', ''),
    'OPENROUTER_API_KEY':   os.getenv('OPENROUTER_API_KEY', ''),
    'HUGGINGFACE_API_KEY':  os.getenv('HUGGINGFACE_API_KEY', ''),
    'TOGETHER_API_KEY':     os.getenv('TOGETHER_API_KEY', ''),
    'RESEND_API_KEY':       os.getenv('RESEND_API_KEY', ''),
    'BREVO_API_KEY':        os.getenv('BREVO_API_KEY', ''),
    'GMAIL_SMTP_USER':      os.getenv('GMAIL_SMTP_USER', ''),
    'GMAIL_APP_PASSWORD':   os.getenv('GMAIL_APP_PASSWORD', ''),
    'ZOHO_SMTP_USER':       os.getenv('ZOHO_SMTP_USER', ''),
    'ZOHO_APP_PASSWORD':    os.getenv('ZOHO_APP_PASSWORD', ''),
    'ZOHO_SMTP_USER_2':     os.getenv('ZOHO_SMTP_USER_2', ''),
    'ZOHO_APP_PASSWORD_2':  os.getenv('ZOHO_APP_PASSWORD_2', ''),
    'SUPABASE_URL':         os.getenv('SUPABASE_URL', ''),
    'SUPABASE_KEY':         os.getenv('SUPABASE_KEY', ''),
    'TELEGRAM_BOT_TOKEN':   os.getenv('TELEGRAM_BOT_TOKEN', ''),
    'TELEGRAM_CHAT_ID':     os.getenv('TELEGRAM_CHAT_ID', ''),
    'GITHUB_PAT':           os.getenv('GITHUB_PAT', ''),
    'RENDER_API_KEY':       os.getenv('RENDER_API_KEY', ''),
    'RENDER_SERVICE_ID':    os.getenv('RENDER_SERVICE_ID', ''),
    'KILL_SWITCH_ACTIVE':   os.getenv('KILL_SWITCH_ACTIVE', 'false'),
    'SENDER_NAME':          os.getenv('SENDER_NAME', 'Sam Salameh'),
    'SENDER_EMAIL':         os.getenv('SENDER_EMAIL', ''),
    'CANDIDATE_NAME':       os.getenv('CANDIDATE_NAME', 'Sam Salameh'),
    'CANDIDATE_PHONE':      os.getenv('CANDIDATE_PHONE', ''),
    'LINKEDIN_URL':         os.getenv('LINKEDIN_URL', ''),
    'TEST_RECEIVER_EMAIL':  os.getenv('TEST_RECEIVER_EMAIL', ''),
}

# Filter out empty values
payload = [
    {"key": k, "value": v}
    for k, v in keys_to_sync.items()
    if v
]

print(f"Syncing {len(payload)} env vars to Render...")

r = requests.put(
    f'https://api.render.com/v1/services/{render_svc}/env-vars',
    headers=headers,
    json=payload,
    timeout=30
)

print(f"Status: {r.status_code}")
if r.status_code in (200, 201):
    print("SUCCESS! All keys synced to Render.")
    print("\nSynced keys:")
    for item in payload:
        k = item['key']
        v = item['value']
        masked = f"{v[:6]}...{v[-3:]}" if len(v) > 9 else "SET"
        print(f"  OK: {k} = {masked}")
else:
    print(f"FAILED: {r.text[:300]}")
