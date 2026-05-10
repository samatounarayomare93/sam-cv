"""Check sam-cv service full config."""
import requests, os, json
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY', 'rnd_X4vP0V0M4LOJEGbFiKs2TM72NgTg')
headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}

# Full service details
r = requests.get('https://api.render.com/v1/services/srv-d7numa5ckfvc73f9e7pg', headers=headers)
print("sam-cv full config:")
print(json.dumps(r.json(), indent=2)[:3000])

# Check if it's alive
import requests as req
try:
    resp = req.get('https://sam-cv-bot.onrender.com', timeout=10)
    print(f"\nHTTP check: {resp.status_code}")
    print(resp.text[:200])
except Exception as e:
    print(f"\nHTTP check failed: {e}")
