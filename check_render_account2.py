"""Check Account 2 Render service status, deploys, and env vars"""
import requests, os
from dotenv import load_dotenv
load_dotenv()

A2_KEY = 'rnd_m4ozEoc4nQYOT16Omj0U9QGd3pra'
A2_SVC = 'srv-d80th10g4nts738vk7b0'
A1_KEY = 'rnd_X4vP0V0M4LOJEGbFiKs2TM72NgTg'
A1_SVC = 'srv-d7s6rf6gvqtc73bt431g'

h2 = {'Authorization': f'Bearer {A2_KEY}', 'Accept': 'application/json'}
h1 = {'Authorization': f'Bearer {A1_KEY}', 'Accept': 'application/json'}

print("=" * 60)
print("RENDER DUAL-ACCOUNT STATUS CHECK")
print("=" * 60)

# Account 2 deploys
print("\n[Account 2 - samsalameh.cv@gmail.com - sam-bot-v2]")
r = requests.get(f'https://api.render.com/v1/services/{A2_SVC}/deploys?limit=5', headers=h2, timeout=10)
if r.status_code == 200:
    for d in r.json()[:3]:
        dep = d.get('deploy', d)
        did = dep.get('id', '?')[:12]
        status = dep.get('status', '?')
        created = dep.get('createdAt', '?')[:19]
        print(f"  Deploy {did}: {status} @ {created}")
else:
    print(f"  Deploys: HTTP {r.status_code}")

# Account 2 env vars
r2 = requests.get(f'https://api.render.com/v1/services/{A2_SVC}/env-vars', headers=h2, timeout=10)
if r2.status_code == 200:
    evars = r2.json()
    print(f"\n  Env vars on Render: {len(evars)}")
    keys_on_render = {e.get('key', ''): e.get('value', '') for e in evars}
    critical = ['TELEGRAM_BOT_TOKEN', 'SUPABASE_URL', 'GROQ_API_KEY',
                'ZOHO_SMTP_USER', 'GMAIL_SMTP_USER', 'RENDER_SERVICE_ID',
                'RENDER_EXTERNAL_URL', 'KILL_SWITCH_ACTIVE']
    for k in critical:
        val = keys_on_render.get(k, 'MISSING')
        if val == 'MISSING':
            print(f"  ❌ {k}: MISSING!")
        else:
            masked = val[:15] + '...' if len(val) > 15 else val
            print(f"  ✅ {k}: {masked}")
else:
    print(f"  Env vars: HTTP {r2.status_code}")

# Account 1 status
print("\n[Account 1 - samatou683@gmail.com - sam-job-automator]")
r3 = requests.get(f'https://api.render.com/v1/services/{A1_SVC}', headers=h1, timeout=10)
if r3.status_code == 200:
    d = r3.json()
    print(f"  Status: suspended={d.get('suspended', '?')}")
    print(f"  URL: {d.get('serviceDetails', {}).get('url', '?')}")
else:
    print(f"  HTTP {r3.status_code}")

# Check if sam-bot-v2 is actually responding
print("\n[Live URL Check]")
try:
    r4 = requests.get('https://sam-bot-v2.onrender.com/', timeout=15)
    print(f"  sam-bot-v2.onrender.com: HTTP {r4.status_code}")
except Exception as e:
    print(f"  sam-bot-v2.onrender.com: {e}")

try:
    r5 = requests.get('https://sam-job-automator.onrender.com/', timeout=10)
    print(f"  sam-job-automator.onrender.com: HTTP {r5.status_code}")
except Exception as e:
    print(f"  sam-job-automator.onrender.com: {e}")

print("\n" + "=" * 60)
print("MISSING ENV VARS (need to sync to Account 2):")
print("=" * 60)
if r2.status_code == 200:
    keys_on_render = {e.get('key', '') for e in r2.json()}
    local_keys = {
        'TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID', 'SUPABASE_URL', 'SUPABASE_KEY',
        'SUPABASE_SERVICE_ROLE_KEY', 'GROQ_API_KEY', 'GEMINI_API_KEY',
        'GMAIL_SMTP_USER', 'GMAIL_APP_PASSWORD', 'ZOHO_SMTP_USER', 'ZOHO_APP_PASSWORD',
        'ZOHO_SMTP_USER_2', 'ZOHO_APP_PASSWORD_2', 'RESEND_API_KEY',
        'BREVO_API_KEY', 'BREVO_SMTP_LOGIN', 'BREVO_SMTP_PASSWORD',
        'SENDER_NAME', 'SENDER_EMAIL', 'CANDIDATE_PHONE', 'LINKEDIN_URL',
        'KILL_SWITCH_ACTIVE', 'MAX_PARALLEL_STRIKES', 'MIN_MATCH_SCORE',
        'RENDER_SERVICE_ID', 'RENDER_API_KEY', 'RENDER_EXTERNAL_URL',
        'OPENROUTER_API_KEY', 'DEEPSEEK_API_KEY', 'HUGGINGFACE_API_KEY',
        'TELEGRAM_API_ID', 'TELEGRAM_API_HASH', 'TELEGRAM_SESSION_STRING',
    }
    missing = local_keys - keys_on_render
    if missing:
        for k in sorted(missing):
            print(f"  ❌ {k}")
    else:
        print("  ✅ All critical keys present!")
