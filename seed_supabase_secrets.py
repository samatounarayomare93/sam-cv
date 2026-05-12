"""
Seed all critical env vars into Supabase system_secrets table.
The bot reads these at startup via _bootstrap_secrets() in db_client.py.
This means even if Render resets env vars, the bot will restore them from Supabase.
"""
import os, requests
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL', '').rstrip('/')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY') or os.getenv('SUPABASE_KEY', '')

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'resolution=merge-duplicates'
}

print("=" * 55)
print("SEEDING SUPABASE system_secrets TABLE")
print("=" * 55)

# First, create the table if it doesn't exist
create_sql = """
CREATE TABLE IF NOT EXISTS system_secrets (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
"""

# Try to create table via RPC (if available)
r_rpc = requests.post(
    f'{SUPABASE_URL}/rest/v1/rpc/exec_sql',
    headers=headers,
    json={'sql': create_sql},
    timeout=10
)
# Ignore errors - table might already exist

# All secrets to store
secrets = {
    'GROQ_API_KEY':             os.getenv('GROQ_API_KEY', ''),
    'GEMINI_API_KEY':           os.getenv('GEMINI_API_KEY', ''),
    'OPENROUTER_API_KEY':       os.getenv('OPENROUTER_API_KEY', ''),
    'DEEPSEEK_API_KEY':         os.getenv('DEEPSEEK_API_KEY', ''),
    'HUGGINGFACE_API_KEY':      os.getenv('HUGGINGFACE_API_KEY', ''),
    'TELEGRAM_BOT_TOKEN':       os.getenv('TELEGRAM_BOT_TOKEN', ''),
    'TELEGRAM_CHAT_ID':         os.getenv('TELEGRAM_CHAT_ID', ''),
    'TELEGRAM_API_ID':          os.getenv('TELEGRAM_API_ID', ''),
    'TELEGRAM_API_HASH':        os.getenv('TELEGRAM_API_HASH', ''),
    'TELEGRAM_SESSION_STRING':  os.getenv('TELEGRAM_SESSION_STRING', ''),
    'GMAIL_SMTP_USER':          os.getenv('GMAIL_SMTP_USER', ''),
    'GMAIL_APP_PASSWORD':       os.getenv('GMAIL_APP_PASSWORD', ''),
    'ZOHO_SMTP_USER':           os.getenv('ZOHO_SMTP_USER', ''),
    'ZOHO_APP_PASSWORD':        os.getenv('ZOHO_APP_PASSWORD', ''),
    'ZOHO_SMTP_USER_2':         os.getenv('ZOHO_SMTP_USER_2', ''),
    'ZOHO_APP_PASSWORD_2':      os.getenv('ZOHO_APP_PASSWORD_2', ''),
    'BREVO_API_KEY':            os.getenv('BREVO_API_KEY', ''),
    'BREVO_SMTP_LOGIN':         os.getenv('BREVO_SMTP_LOGIN', ''),
    'BREVO_SMTP_PASSWORD':      os.getenv('BREVO_SMTP_PASSWORD', ''),
    'RESEND_API_KEY':           os.getenv('RESEND_API_KEY', ''),
    'RENDER_API_KEY':           'rnd_m4ozEoc4nQYOT16Omj0U9QGd3pra',
    'RENDER_SERVICE_ID':        'srv-d80th10g4nts738vk7b0',
    'RENDER_EXTERNAL_URL':      'https://sam-bot-v2.onrender.com',
    'KILL_SWITCH_ACTIVE':       'false',
    'MAX_PARALLEL_STRIKES':     '3',
    'MIN_MATCH_SCORE':          '45',
    'SENDER_NAME':              'Sam Salameh',
    'SENDER_EMAIL':             'samsalameh.cv@gmail.com',
    'CANDIDATE_PHONE':          '+961 70 841 1009',
    'LINKEDIN_URL':             'https://www.linkedin.com/in/sam-salameh',
}

success = 0
failed = 0
for key, value in secrets.items():
    if not value:
        continue
    payload = [{'key': key, 'value': value}]
    r = requests.post(
        f'{SUPABASE_URL}/rest/v1/system_secrets',
        headers=headers,
        json=payload[0],
        timeout=10
    )
    if r.status_code in (200, 201, 409):
        success += 1
        masked = value[:8] + '...' if len(value) > 8 else '***'
        print(f"  ✅ {key}: {masked}")
    else:
        failed += 1
        print(f"  ❌ {key}: HTTP {r.status_code} - {r.text[:80]}")

print(f"\n✅ {success} secrets seeded, ❌ {failed} failed")
print("\nThe bot will now restore these from Supabase on every startup!")
print("Even if Render resets env vars, the bot will recover automatically.")
