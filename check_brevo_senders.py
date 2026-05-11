import requests, os
from dotenv import load_dotenv
load_dotenv()

key = os.getenv('BREVO_API_KEY')
print("Checking Brevo senders...")
r = requests.get('https://api.brevo.com/v3/senders', headers={'api-key': key}, timeout=10)
data = r.json()
print(f"Status: {r.status_code}")
for s in data.get('senders', []):
    print(f"  Email: {s.get('email')} | Active: {s.get('active')} | Name: {s.get('name')}")

# Also check account info
r2 = requests.get('https://api.brevo.com/v3/account', headers={'api-key': key}, timeout=10)
acc = r2.json()
print(f"\nAccount: {acc.get('email')}")
print(f"Company: {acc.get('companyName')}")
for plan in acc.get('plan', []):
    print(f"Plan: {plan.get('type')} | Credits: {plan.get('credits')} | Limit: {plan.get('creditsType')}")
