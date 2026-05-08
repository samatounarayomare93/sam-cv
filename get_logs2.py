"""Try all Render log endpoints."""
import requests

KEY = "rnd_X4vP0V0M4LOJEGbFiKs2TM72NgTg"
SID = "srv-d7s6rf6gvqtc73bt431g"
h = {"Authorization": f"Bearer {KEY}"}

endpoints = [
    f"https://api.render.com/v1/services/{SID}/logs",
    f"https://api.render.com/v1/logs?serviceId={SID}",
    f"https://api.render.com/v1/services/{SID}/log-streams",
    f"https://api.render.com/v1/services/{SID}/deploys",
]

for url in endpoints:
    r = requests.get(url, headers=h, timeout=10)
    print(f"{r.status_code} | {url}")
    if r.status_code == 200:
        print(r.text[:1000])
    print()
