"""Check current deploy status of Account 2"""
import requests
A2_KEY = 'rnd_m4ozEoc4nQYOT16Omj0U9QGd3pra'
A2_SVC = 'srv-d80th10g4nts738vk7b0'
h = {'Authorization': f'Bearer {A2_KEY}', 'Accept': 'application/json'}

r = requests.get(f'https://api.render.com/v1/services/{A2_SVC}/deploys?limit=3', headers=h, timeout=10)
if r.status_code == 200:
    for item in r.json()[:3]:
        d = item.get('deploy', item)
        did = d.get('id', '?')[:12]
        status = d.get('status', '?')
        created = d.get('createdAt', '?')[:19]
        print(f"Deploy {did}: {status} @ {created}")

r2 = requests.get(f'https://api.render.com/v1/services/{A2_SVC}', headers=h, timeout=10)
if r2.status_code == 200:
    svc = r2.json()
    print(f"\nService: {svc.get('name')} | suspended={svc.get('suspended')}")
    url = svc.get('serviceDetails', {}).get('url', '?')
    print(f"URL: {url}")

# Check if live
try:
    r3 = requests.get('https://sam-bot-v2.onrender.com/', timeout=15)
    print(f"\nLive check: HTTP {r3.status_code}")
    if r3.status_code == 200:
        print("Bot is UP and responding!")
    elif r3.status_code == 503:
        print("Bot is starting up (503 = still deploying or sleeping)")
except Exception as e:
    print(f"\nLive check error: {e}")
