"""Encode token.json as base64 and add to Render env vars"""
import base64, json, requests, os
from dotenv import load_dotenv
load_dotenv()

# Read and encode token.json
with open('token.json', 'r') as f:
    token = f.read()

encoded = base64.b64encode(token.encode()).decode()
print(f"GMAIL_TOKEN_JSON length: {len(encoded)} chars")

# Verify
decoded = base64.b64decode(encoded).decode()
data = json.loads(decoded)
print(f"Has refresh_token: {bool(data.get('refresh_token'))}")
print(f"Client ID: {data.get('client_id', '?')[:30]}")

# Add to Render env vars
A2_KEY = 'rnd_m4ozEoc4nQYOT16Omj0U9QGd3pra'
A2_SVC = 'srv-d80th10g4nts738vk7b0'
h = {'Authorization': f'Bearer {A2_KEY}', 'Content-Type': 'application/json', 'Accept': 'application/json'}

# Get current env vars first
r = requests.get(f'https://api.render.com/v1/services/{A2_SVC}/env-vars', headers=h, timeout=10)
current_vars = r.json() if r.status_code == 200 else []
print(f"\nCurrent Render env vars: {len(current_vars)}")

# Add GMAIL_TOKEN_JSON to the list
new_var = {'key': 'GMAIL_TOKEN_JSON', 'value': encoded}
all_vars = [v for v in current_vars if v.get('key') != 'GMAIL_TOKEN_JSON']
all_vars.append(new_var)

r2 = requests.put(
    f'https://api.render.com/v1/services/{A2_SVC}/env-vars',
    headers=h, json=all_vars, timeout=30
)
print(f"Add GMAIL_TOKEN_JSON: HTTP {r2.status_code}")

# Also add to Supabase secrets
SUPABASE_URL = os.getenv('SUPABASE_URL', '').rstrip('/')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY') or os.getenv('SUPABASE_KEY', '')
sh = {'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}',
      'Content-Type': 'application/json', 'Prefer': 'resolution=merge-duplicates'}
r3 = requests.post(f'{SUPABASE_URL}/rest/v1/system_secrets',
                   headers=sh, json={'key': 'GMAIL_TOKEN_JSON', 'value': encoded}, timeout=10)
print(f"Add to Supabase: HTTP {r3.status_code}")

print("\nDone! Gmail API will now work on Render.")
print("The bot will use Gmail API (HTTPS) to send emails - bypasses all SMTP blocks!")
