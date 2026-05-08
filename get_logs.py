"""Fetch Render logs via SSE stream."""
import requests, json, time

RENDER_API_KEY = "rnd_X4vP0V0M4LOJEGbFiKs2TM72NgTg"
SERVICE_ID = "srv-d7s6rf6gvqtc73bt431g"
headers = {"Authorization": f"Bearer {RENDER_API_KEY}", "Accept": "text/event-stream"}

print("Fetching logs...")
try:
    r = requests.get(
        f"https://api.render.com/v1/services/{SERVICE_ID}/logs",
        headers=headers,
        params={"limit": 200},
        stream=True,
        timeout=30
    )
    print(f"Status: {r.status_code}")
    lines = []
    for line in r.iter_lines(decode_unicode=True):
        if line and line.startswith("data:"):
            try:
                data = json.loads(line[5:].strip())
                msg = data.get("log", {}).get("message", "") or data.get("message", "")
                if msg:
                    lines.append(msg)
            except:
                lines.append(line)
        if len(lines) >= 200:
            break
    for l in lines:
        print(l)
except Exception as e:
    print(f"Error: {e}")
    # Try alternative endpoint
    r2 = requests.get(
        f"https://api.render.com/v1/services/{SERVICE_ID}/events",
        headers={"Authorization": f"Bearer {RENDER_API_KEY}"},
        timeout=15
    )
    print(f"Events status: {r2.status_code}")
    print(r2.text[:3000])
