import requests

RENDER_API_KEY = 'rnd_X4vP0V0M4LOJEGbFiKs2TM72NgTg'
SERVICE_ID = 'srv-d7s6rf6gvqtc73bt431g'

headers = {
    'Authorization': f'Bearer {RENDER_API_KEY}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

print("Triggering Render redeploy...")
r = requests.post(
    f'https://api.render.com/v1/services/{SERVICE_ID}/deploys',
    headers=headers,
    json={"clearCache": "do_not_clear"},
    timeout=15
)
print(f"Status: {r.status_code}")
if r.status_code in (200, 201):
    data = r.json()
    deploy_id = data.get('id', 'unknown')
    print(f"✅ Redeploy triggered! Deploy ID: {deploy_id}")
    print("Bot will restart with new env vars in ~3 minutes")
else:
    print(f"Response: {r.text[:300]}")
