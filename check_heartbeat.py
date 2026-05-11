import os, requests
from dotenv import load_dotenv
from datetime import datetime, timezone
load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
headers = {'apikey': key, 'Authorization': f'Bearer {key}'}

r = requests.get(f'{url}/rest/v1/system_settings?key=eq.active_bot_heartbeat&select=value', headers=headers, timeout=10)
hb = r.json()[0]['value'] if r.json() else 'none'

hb_time = datetime.fromisoformat(hb.replace('Z', '+00:00'))
now = datetime.now(hb_time.tzinfo)
age = (now - hb_time).total_seconds()

print(f"Heartbeat: {hb}")
print(f"Age: {age:.0f} seconds ({age/60:.1f} minutes)")

if age < 120:
    print("Bot status: ALIVE - bot is running and processing")
elif age < 600:
    print("Bot status: RECENT - bot ran recently, may be between cycles")
else:
    print("Bot status: STALE - bot may have crashed")
