"""Get logs from the ACTIVE Render service (Account 2 - sam-bot-v2)"""
import requests, json, os
from dotenv import load_dotenv
load_dotenv()

A2_KEY = 'rnd_m4ozEoc4nQYOT16Omj0U9QGd3pra'
A2_SVC = 'srv-d80th10g4nts738vk7b0'
h = {'Authorization': f'Bearer {A2_KEY}', 'Accept': 'application/json'}

print("=" * 60)
print("RENDER LOGS - sam-bot-v2 (Account 2)")
print("=" * 60)

# Try SSE logs endpoint
import urllib.request, ssl

url = f"https://api.render.com/v1/services/{A2_SVC}/logs?limit=200&direction=backward"
req = urllib.request.Request(url, headers={'Authorization': f'Bearer {A2_KEY}', 'Accept': 'application/json'})
ctx = ssl.create_default_context()

try:
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        raw = resp.read().decode('utf-8')
        try:
            data = json.loads(raw)
            logs = data if isinstance(data, list) else data.get('logs', [])
            print(f"Got {len(logs)} log entries\n")
            for entry in logs[-80:]:
                ts = entry.get('timestamp', '')[:19] if isinstance(entry, dict) else ''
                msg = entry.get('message', str(entry)) if isinstance(entry, dict) else str(entry)
                print(f"[{ts}] {msg}")
        except json.JSONDecodeError:
            # Raw text logs
            lines = raw.strip().split('\n')
            print(f"Got {len(lines)} log lines\n")
            for line in lines[-80:]:
                if line.strip():
                    print(line)
except Exception as e:
    print(f"Logs endpoint error: {e}")
    
    # Try alternative: get deploy logs
    print("\nTrying deploy logs...")
    r = requests.get(f'https://api.render.com/v1/services/{A2_SVC}/deploys?limit=1', headers=h, timeout=10)
    if r.status_code == 200:
        deploys = r.json()
        if deploys:
            dep = deploys[0].get('deploy', deploys[0])
            dep_id = dep.get('id', '')
            print(f"Latest deploy: {dep_id[:12]} | status={dep.get('status')}")
            
            # Get deploy logs
            r2 = requests.get(f'https://api.render.com/v1/services/{A2_SVC}/deploys/{dep_id}/logs', headers=h, timeout=10)
            if r2.status_code == 200:
                dlog = r2.json()
                logs = dlog if isinstance(dlog, list) else dlog.get('logs', [])
                for entry in logs[-50:]:
                    msg = entry.get('message', str(entry)) if isinstance(entry, dict) else str(entry)
                    print(msg)
            else:
                print(f"Deploy logs: HTTP {r2.status_code} - {r2.text[:200]}")
