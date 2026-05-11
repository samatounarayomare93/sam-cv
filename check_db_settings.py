import os, requests
from dotenv import load_dotenv
load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
headers = {'apikey': key, 'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}

# Check system settings
r = requests.get(f'{url}/rest/v1/system_settings?select=*', headers=headers, timeout=10)
print("System settings:")
for s in r.json():
    print(f"  {s['key']}: {str(s['value'])[:60]}")

# Fix: reset heartbeat to force bot to claim leadership
print("\nResetting bot heartbeat to force leadership claim...")
r2 = requests.patch(
    f'{url}/rest/v1/system_settings?key=eq.active_bot_heartbeat',
    headers={**headers, 'Prefer': 'return=representation'},
    json={'value': '2020-01-01T00:00:00'},
    timeout=10
)
print(f"Reset heartbeat: {r2.status_code}")

# Also reset kill switch
r3 = requests.patch(
    f'{url}/rest/v1/system_settings?key=eq.kill_switch',
    headers={**headers, 'Prefer': 'return=representation'},
    json={'value': 'false'},
    timeout=10
)
print(f"Kill switch off: {r3.status_code}")

print("\nDone! Bot should claim leadership and start polling within 15 seconds.")
