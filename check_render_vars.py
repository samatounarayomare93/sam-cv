"""Check actual Render env vars with correct parsing"""
import requests
A2_KEY = 'rnd_m4ozEoc4nQYOT16Omj0U9QGd3pra'
A2_SVC = 'srv-d80th10g4nts738vk7b0'
h = {'Authorization': f'Bearer {A2_KEY}', 'Accept': 'application/json'}

r = requests.get(f'https://api.render.com/v1/services/{A2_SVC}/env-vars', headers=h, timeout=10)
evars = r.json()
print(f'Total items returned: {len(evars)}')
print(f'First item structure: {str(evars[0])[:100] if evars else "empty"}')

# Parse correctly - Render wraps in envVar object
keys = {}
for e in evars:
    if isinstance(e, dict):
        ev = e.get('envVar', e)
        k = ev.get('key', '')
        v = ev.get('value', '')
        if k:
            keys[k] = v

print(f'\nTotal unique keys: {len(keys)}')
critical = ['TELEGRAM_BOT_TOKEN', 'SUPABASE_URL', 'GROQ_API_KEY', 'BREVO_API_KEY',
            'ZOHO_SMTP_USER', 'GMAIL_SMTP_USER', 'GMAIL_TOKEN_JSON', 'KILL_SWITCH_ACTIVE']
for k in critical:
    val = keys.get(k, 'MISSING')
    if val == 'MISSING':
        print(f'  ❌ {k}: MISSING')
    else:
        masked = val[:15] + '...' if len(val) > 15 else val
        print(f'  ✅ {k}: {masked}')
