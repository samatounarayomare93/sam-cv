"""
SYNC ALL ENV VARS TO ACCOUNT 2 (sam-bot-v2)
This is the ACTIVE account - needs all credentials to work.
"""
import os, requests, re
from dotenv import load_dotenv
load_dotenv()

A2_KEY = 'rnd_m4ozEoc4nQYOT16Omj0U9QGd3pra'
A2_SVC = 'srv-d80th10g4nts738vk7b0'
A2_URL = 'https://sam-bot-v2.onrender.com'

headers = {
    'Authorization': f'Bearer {A2_KEY}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

print("=" * 60)
print("SYNCING ALL ENV VARS TO ACCOUNT 2 (sam-bot-v2)")
print("=" * 60)

# Build complete env vars list
env_vars = [
    # ── Database ──────────────────────────────────────────────
    {'key': 'SUPABASE_URL',              'value': os.getenv('SUPABASE_URL', '')},
    {'key': 'SUPABASE_KEY',              'value': os.getenv('SUPABASE_KEY', '')},
    {'key': 'SUPABASE_SERVICE_ROLE_KEY', 'value': os.getenv('SUPABASE_SERVICE_ROLE_KEY', '')},
    # ── AI ────────────────────────────────────────────────────
    {'key': 'GROQ_API_KEY',              'value': os.getenv('GROQ_API_KEY', '')},
    {'key': 'GEMINI_API_KEY',            'value': os.getenv('GEMINI_API_KEY', '')},
    {'key': 'OPENROUTER_API_KEY',        'value': os.getenv('OPENROUTER_API_KEY', '')},
    {'key': 'DEEPSEEK_API_KEY',          'value': os.getenv('DEEPSEEK_API_KEY', '')},
    {'key': 'HUGGINGFACE_API_KEY',       'value': os.getenv('HUGGINGFACE_API_KEY', '')},
    # ── Telegram ──────────────────────────────────────────────
    {'key': 'TELEGRAM_BOT_TOKEN',        'value': os.getenv('TELEGRAM_BOT_TOKEN', '')},
    {'key': 'TELEGRAM_CHAT_ID',          'value': os.getenv('TELEGRAM_CHAT_ID', '')},
    {'key': 'TELEGRAM_API_ID',           'value': os.getenv('TELEGRAM_API_ID', '')},
    {'key': 'TELEGRAM_API_HASH',         'value': os.getenv('TELEGRAM_API_HASH', '')},
    {'key': 'TELEGRAM_SESSION_STRING',   'value': os.getenv('TELEGRAM_SESSION_STRING', '')},
    # ── Email: Gmail ──────────────────────────────────────────
    {'key': 'GMAIL_SMTP_USER',           'value': os.getenv('GMAIL_SMTP_USER', '')},
    {'key': 'GMAIL_APP_PASSWORD',        'value': os.getenv('GMAIL_APP_PASSWORD', '')},
    # ── Email: Zoho ───────────────────────────────────────────
    {'key': 'ZOHO_SMTP_USER',            'value': os.getenv('ZOHO_SMTP_USER', '')},
    {'key': 'ZOHO_APP_PASSWORD',         'value': os.getenv('ZOHO_APP_PASSWORD', '')},
    {'key': 'ZOHO_SMTP_USER_2',          'value': os.getenv('ZOHO_SMTP_USER_2', '')},
    {'key': 'ZOHO_APP_PASSWORD_2',       'value': os.getenv('ZOHO_APP_PASSWORD_2', '')},
    # ── Email: Brevo ──────────────────────────────────────────
    {'key': 'BREVO_API_KEY',             'value': os.getenv('BREVO_API_KEY', '')},
    {'key': 'BREVO_SMTP_LOGIN',          'value': os.getenv('BREVO_SMTP_LOGIN', '')},
    {'key': 'BREVO_SMTP_PASSWORD',       'value': os.getenv('BREVO_SMTP_PASSWORD', '')},
    {'key': 'BREVO_ACCOUNT_EMAIL',       'value': os.getenv('BREVO_ACCOUNT_EMAIL', '')},
    {'key': 'BREVO_SENDER_EMAIL',        'value': os.getenv('BREVO_SENDER_EMAIL', '')},
    {'key': 'BREVO_PRIMARY_SENDER',      'value': os.getenv('BREVO_PRIMARY_SENDER', '')},
    # ── Email: Resend ─────────────────────────────────────────
    {'key': 'RESEND_API_KEY',            'value': os.getenv('RESEND_API_KEY', '')},
    {'key': 'RESEND_FROM_EMAIL',         'value': os.getenv('RESEND_FROM_EMAIL', '')},
    # ── Email: Outlook ────────────────────────────────────────
    {'key': 'OUTLOOK_USER',              'value': os.getenv('OUTLOOK_USER', '')},
    {'key': 'OUTLOOK_PASSWORD',          'value': os.getenv('OUTLOOK_PASSWORD', '')},
    # ── Render (self-reference) ───────────────────────────────
    {'key': 'RENDER_API_KEY',            'value': A2_KEY},
    {'key': 'RENDER_SERVICE_ID',         'value': A2_SVC},
    {'key': 'RENDER_EXTERNAL_URL',       'value': A2_URL},
    {'key': 'RENDER',                    'value': 'true'},
    # ── GitHub ────────────────────────────────────────────────
    {'key': 'GITHUB_PAT',                'value': os.getenv('GITHUB_PAT', '')},
    # ── Identity ──────────────────────────────────────────────
    {'key': 'SENDER_NAME',               'value': os.getenv('SENDER_NAME', 'Sam Salameh')},
    {'key': 'SENDER_EMAIL',              'value': os.getenv('SENDER_EMAIL', '')},
    {'key': 'CANDIDATE_NAME',            'value': os.getenv('CANDIDATE_NAME', 'Sam Salameh')},
    {'key': 'CANDIDATE_PHONE',           'value': os.getenv('CANDIDATE_PHONE', '')},
    {'key': 'LINKEDIN_URL',              'value': os.getenv('LINKEDIN_URL', '')},
    {'key': 'TEST_RECEIVER_EMAIL',       'value': os.getenv('TEST_RECEIVER_EMAIL', '')},
    # ── System config ─────────────────────────────────────────
    {'key': 'KILL_SWITCH_ACTIVE',        'value': 'false'},
    {'key': 'MAX_PARALLEL_STRIKES',      'value': '5'},
    {'key': 'MAX_EMAILS_PER_DAY',        'value': '1900'},
    {'key': 'MAX_APPLICATIONS_PER_DAY',  'value': '1500'},
    {'key': 'MAX_APPLICATIONS_PER_HOUR', 'value': '120'},
    {'key': 'MIN_MATCH_SCORE',           'value': '45'},
    {'key': 'DIVINE_LOG_LEVEL',          'value': 'INFO'},
    {'key': 'USE_AI_ANALYSIS',           'value': 'true'},
    {'key': 'ENABLE_DEDUPLICATION',      'value': 'true'},
    {'key': 'FOLLOWUP_ENABLED',          'value': 'true'},
    {'key': 'BUSINESS_HOURS_START',      'value': '5'},
    {'key': 'BUSINESS_HOURS_END',        'value': '23'},
    {'key': 'PORT',                      'value': '10000'},
]

# Filter out empty values
env_vars = [e for e in env_vars if e['value'].strip()]
print(f"Syncing {len(env_vars)} env vars...")

# Send to Render
r = requests.put(
    f'https://api.render.com/v1/services/{A2_SVC}/env-vars',
    headers=headers,
    json=env_vars,
    timeout=30
)

if r.status_code == 200:
    print(f"✅ SUCCESS! {len(env_vars)} env vars synced to sam-bot-v2")
    
    # Update local .env to make sure it points to Account 2
    env_path = '.env'
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'^RENDER_API_KEY=.*$', f'RENDER_API_KEY={A2_KEY}', content, flags=re.MULTILINE)
    content = re.sub(r'^RENDER_SERVICE_ID=.*$', f'RENDER_SERVICE_ID={A2_SVC}', content, flags=re.MULTILINE)
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Local .env updated to point to Account 2")
    
    # Trigger a redeploy so the new env vars take effect
    print("\nTriggering redeploy with new env vars...")
    r2 = requests.post(
        f'https://api.render.com/v1/services/{A2_SVC}/deploys',
        headers=headers,
        json={'clearCache': 'do_not_clear'},
        timeout=15
    )
    if r2.status_code in (200, 201):
        dep = r2.json().get('deploy', r2.json())
        print(f"✅ Redeploy triggered! Deploy ID: {dep.get('id', '?')[:12]}")
        print(f"   Status: {dep.get('status', '?')}")
        print(f"\n⏳ Wait 2-3 minutes then test: @samcvbot → /status")
    else:
        print(f"⚠️ Redeploy: HTTP {r2.status_code} - {r2.text[:100]}")
else:
    print(f"❌ FAILED: HTTP {r.status_code}")
    print(r.text[:300])

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Active service: sam-bot-v2")
print(f"URL: {A2_URL}")
print(f"Service ID: {A2_SVC}")
print(f"Account: samsalameh.cv@gmail.com")
print(f"Account 1 (sam-job-automator): SUSPENDED (backup)")
