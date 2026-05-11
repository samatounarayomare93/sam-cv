import os, requests
from dotenv import load_dotenv
load_dotenv()

key = os.getenv('OPENROUTER_API_KEY', '')
headers = {'Authorization': f'Bearer {key}', 'Accept': 'application/json'}

r = requests.get('https://openrouter.ai/api/v1/models', headers=headers, timeout=15)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    models = r.json().get('data', [])
    # Filter free models
    free = [m for m in models if ':free' in m.get('id', '') or m.get('pricing', {}).get('prompt') == '0']
    print(f"\nFree models ({len(free)}):")
    for m in free[:20]:
        mid = m.get('id', '')
        ctx = m.get('context_length', 0)
        print(f"  {mid} (ctx: {ctx})")
else:
    print(r.text[:300])
