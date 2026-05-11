"""Get Render service logs via events API"""
import os, requests, json
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY')
service_id = os.getenv('RENDER_SERVICE_ID')
headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}

print("Getting Render events...")
r = requests.get(
    f'https://api.render.com/v1/services/{service_id}/events?limit=20',
    headers=headers, timeout=15
)
if r.status_code == 200:
    events = r.json()
    print(f"Events ({len(events)}):")
    for evt in events:
        e = evt.get('event', evt)
        etype = e.get('type', '?')
        ts = e.get('timestamp', '?')[:19]
        details = e.get('details', {})
        print(f"  {ts} | {etype}")
        if details:
            # Show relevant details
            if 'oomKilled' in str(details):
                print(f"    OOM KILLED! Memory limit exceeded")
            elif 'reason' in details:
                print(f"    Reason: {details.get('reason', {})}")
else:
    print(f"Error: {r.status_code} - {r.text[:200]}")

# Also check if service is actually running the bot
print("\nChecking service health endpoint...")
try:
    r2 = requests.get('https://sam-bot-v2.onrender.com/health', timeout=10)
    print(f"Health: {r2.status_code} - {r2.text[:100]}")
except Exception as e:
    print(f"Health check: {e}")

# Check the main page
try:
    r3 = requests.get('https://sam-bot-v2.onrender.com', timeout=10)
    print(f"Main page: {r3.status_code}")
    # Check if it has stats
    if 'strikes' in r3.text.lower() or 'scanned' in r3.text.lower():
        print("  Bot stats visible in response!")
    else:
        print("  Response preview:", r3.text[:200])
except Exception as e:
    print(f"Main page: {e}")
