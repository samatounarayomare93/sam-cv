import os, sys, requests
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()

render_key = os.getenv('RENDER_API_KEY')
render_svc = os.getenv('RENDER_SERVICE_ID')
headers = {'Authorization': f'Bearer {render_key}', 'Accept': 'application/json'}

r = requests.get(f'https://api.render.com/v1/services/{render_svc}/env-vars', headers=headers, timeout=15)
print('Status:', r.status_code)
data = r.json()

keys = [v.get('envVar',{}).get('key','?') for v in data if v.get('envVar')]
print(f'Total env vars on Render: {len(keys)}')

check_keys = ['OPENROUTER_API_KEY', 'HUGGINGFACE_API_KEY', 'DEEPSEEK_API_KEY', 'GROQ_API_KEY', 'GEMINI_API_KEY']
print("\nKey status on Render:")
for k in check_keys:
    found = k in keys
    icon = "OK" if found else "MISSING"
    print(f"  {icon}: {k}")
