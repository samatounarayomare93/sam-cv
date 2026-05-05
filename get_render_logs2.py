import requests

RENDER_API_KEY = 'rnd_X4vP0V0M4LOJEGbFiKs2TM72NgTg'
SERVICE_ID = 'srv-d7s6rf6gvqtc73bt431g'

headers = {
    'Authorization': f'Bearer {RENDER_API_KEY}',
    'Accept': 'application/json'
}

# Try correct logs endpoint
endpoints_to_try = [
    f'https://api.render.com/v1/services/{SERVICE_ID}/log-stream',
    f'https://api.render.com/v1/logs?resource={SERVICE_ID}',
    f'https://api.render.com/v1/logs?ownerId={SERVICE_ID}',
]

for url in endpoints_to_try:
    r = requests.get(url, headers=headers, timeout=10)
    print(f"GET {url.split('render.com')[1]}: {r.status_code}")
    if r.status_code == 200:
        print(r.text[:500])
        break
    else:
        print(f"  Error: {r.text[:100]}")

# Check env vars are set correctly
print("\n=== CHECKING ENV VARS ON RENDER ===")
r2 = requests.get(
    f'https://api.render.com/v1/services/{SERVICE_ID}/env-vars',
    headers=headers, timeout=15
)
if r2.status_code == 200:
    vars_list = r2.json()
    print(f"Total env vars set: {len(vars_list)}")
    for item in vars_list:
        ev = item.get('envVar', {})
        key = ev.get('key', '')
        val = ev.get('value', '')
        if key in ['ZOHO_SMTP_USER', 'ZOHO_SMTP_USER_2', 'RESEND_API_KEY', 
                   'TELEGRAM_BOT_TOKEN', 'SUPABASE_URL', 'GROQ_API_KEY']:
            masked = val[:8] + '...' if len(val) > 8 else val
            print(f"  {key} = {masked}")
else:
    print(f"Error: {r2.status_code} - {r2.text[:200]}")
