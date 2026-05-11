import os, requests
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('RENDER_API_KEY')
service_id = os.getenv('RENDER_SERVICE_ID')
print(f"Service: {service_id}")
print(f"API Key: {api_key[:20]}...")

headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json', 'Accept': 'application/json'}

r = requests.post(
    f'https://api.render.com/v1/services/{service_id}/deploys',
    headers=headers,
    json={'clearCache': 'do_not_clear'},
    timeout=15
)
print(f"Status: {r.status_code}")
print(f"Response: {r.text[:200]}")
