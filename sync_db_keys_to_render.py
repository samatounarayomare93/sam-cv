"""
Reads API keys from Supabase DB (set via /setkey) and syncs them to Render env vars.
Also updates local .env file.
"""
import os, sys, requests
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()

supa_url = os.getenv('SUPABASE_URL')
supa_key = os.getenv('SUPABASE_KEY')
render_key = os.getenv('RENDER_API_KEY')
render_svc = os.getenv('RENDER_SERVICE_ID')

supa_headers = {'apikey': supa_key, 'Authorization': f'Bearer {supa_key}'}
render_headers = {'Authorization': f'Bearer {render_key}', 'Content-Type': 'application/json'}

print("=" * 60)
print("SYNCING DB KEYS TO RENDER")
print("=" * 60)

# Step 1: Get all apikey: entries from Supabase
r = requests.get(
    f'{supa_url}/rest/v1/system_settings?key=like.apikey%3A*&select=key,value',
    headers=supa_headers, timeout=15
)

db_keys = {}
if r.status_code == 200:
    for row in r.json():
        raw_key = row['key']  # e.g. "apikey:OPENROUTER_API_KEY"
        env_key = raw_key.replace('apikey:', '')
        db_keys[env_key] = row['value']
        print(f"  Found in DB: {env_key} = {row['value'][:10]}...")
else:
    print(f"  DB error: {r.status_code}")

if not db_keys:
    print("  No keys found in DB via /setkey")
    print("  (Keys set via /setkey are stored as 'apikey:KEY_NAME' in system_settings)")
else:
    print(f"\n  Found {len(db_keys)} keys in DB")

# Step 2: Get current Render env vars
r_get = requests.get(
    f'https://api.render.com/v1/services/{render_svc}/env-vars',
    headers={'Authorization': f'Bearer {render_key}', 'Accept': 'application/json'},
    timeout=15
)

current_render_vars = {}
if r_get.status_code == 200:
    for item in r_get.json():
        ev = item.get('envVar', {})
        if ev.get('key'):
            current_render_vars[ev['key']] = ev['value']

print(f"\n  Current Render env vars: {len(current_render_vars)}")

# Step 3: Merge DB keys + existing .env keys into Render
# Priority: DB keys > .env keys
all_keys_to_sync = {}

# Start with important .env keys
important_env_keys = [
    'GROQ_API_KEY', 'GEMINI_API_KEY', 'RESEND_API_KEY', 'BREVO_API_KEY',
    'GMAIL_SMTP_USER', 'GMAIL_APP_PASSWORD',
    'ZOHO_SMTP_USER', 'ZOHO_APP_PASSWORD',
    'ZOHO_SMTP_USER_2', 'ZOHO_APP_PASSWORD_2',
    'SUPABASE_URL', 'SUPABASE_KEY', 'SUPABASE_SERVICE_ROLE_KEY',
    'TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID', 'TELEGRAM_API_ID',
    'TELEGRAM_API_HASH', 'TELEGRAM_SESSION_STRING',
    'GITHUB_PAT', 'RENDER_API_KEY', 'RENDER_SERVICE_ID',
    'KILL_SWITCH_ACTIVE', 'SENDER_NAME', 'SENDER_EMAIL',
    'CANDIDATE_NAME', 'CANDIDATE_PHONE', 'LINKEDIN_URL',
    'TEST_RECEIVER_EMAIL', 'BREVO_SMTP_LOGIN', 'BREVO_SMTP_PASSWORD',
    'BREVO_ACCOUNT_EMAIL', 'BREVO_SENDER_EMAIL',
    'OPENROUTER_API_KEY', 'HUGGINGFACE_API_KEY', 'DEEPSEEK_API_KEY',
    'TOGETHER_API_KEY',
]

for k in important_env_keys:
    v = os.getenv(k, '')
    if v:
        all_keys_to_sync[k] = v

# Override with DB keys (these are the ones set via /setkey)
for k, v in db_keys.items():
    if v:
        all_keys_to_sync[k] = v
        print(f"  DB override: {k}")

# Step 4: Push to Render
payload = [{"key": k, "value": v} for k, v in all_keys_to_sync.items()]

print(f"\nPushing {len(payload)} env vars to Render...")
r_put = requests.put(
    f'https://api.render.com/v1/services/{render_svc}/env-vars',
    headers=render_headers,
    json=payload,
    timeout=30
)

print(f"Render response: {r_put.status_code}")
if r_put.status_code in (200, 201):
    print("SUCCESS!")
    print("\nSynced to Render:")
    for item in payload:
        k = item['key']
        v = item['value']
        masked = f"{v[:6]}...{v[-3:]}" if len(v) > 9 else "SET"
        src = "DB" if k in db_keys else "env"
        print(f"  [{src}] {k} = {masked}")
else:
    print(f"FAILED: {r_put.text[:300]}")

# Step 5: Also update local .env with DB keys
if db_keys:
    print("\nUpdating local .env with DB keys...")
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for k, v in db_keys.items():
        if f'{k}=' in content:
            # Update existing
            import re
            content = re.sub(f'^{k}=.*$', f'{k}={v}', content, flags=re.MULTILINE)
            print(f"  Updated: {k}")
        else:
            # Add new
            content += f'\n{k}={v}'
            print(f"  Added: {k}")

    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("  .env updated!")

print("\n" + "=" * 60)
print("DONE! Render will auto-redeploy with new keys.")
print("=" * 60)
