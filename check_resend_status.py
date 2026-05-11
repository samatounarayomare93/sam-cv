import requests, os
from dotenv import load_dotenv
load_dotenv()

key = os.getenv('RESEND_API_KEY')
print(f"Resend key: {key[:20]}...")

# Check domains
r = requests.get('https://api.resend.com/domains', headers={'Authorization': f'Bearer {key}'}, timeout=10)
print(f"\nDomains status: {r.status_code}")
data = r.json()
for d in data.get('data', []):
    print(f"  Domain: {d.get('name')} | Status: {d.get('status')}")

# Try sending a test email directly via Resend
print("\nTrying to send test email via Resend...")
payload = {
    "from": "Sam Salameh <onboarding@resend.dev>",
    "to": ["samsalameh.cv@gmail.com"],
    "subject": "✅ Resend Test - Sam CV Bot",
    "html": "<h2>✅ Resend is working!</h2><p>This confirms Resend API is functional.</p>"
}
r2 = requests.post(
    'https://api.resend.com/emails',
    headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
    json=payload,
    timeout=15
)
print(f"Send status: {r2.status_code}")
print(f"Response: {r2.text[:300]}")
