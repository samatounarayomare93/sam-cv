import requests
import os
from dotenv import load_dotenv
from collections import Counter

load_dotenv()

api_key = os.getenv('BREVO_API_KEY')
headers = {'api-key': api_key}

response = requests.get('https://api.brevo.com/v3/smtp/statistics/events', headers=headers, params={'limit': 100})
data = response.json()
events = data.get('events', [])

delivered = [e for e in events if e.get('event') == 'delivered']
errors = [e for e in events if e.get('event') == 'error']

print(f"DELIVERED: {len(delivered)}")
print(f"ERRORS: {len(errors)}")

print("\n=== DELIVERED emails ===")
for e in delivered[:10]:
    email = e.get('email', '')
    subject = e.get('subject', '')[:40]
    print(f"  To: {email} | {subject}")

print("\n=== ERROR domains ===")
error_domains = Counter()
for e in errors:
    email = e.get('email', '')
    domain = email.split('@')[-1] if '@' in email else 'unknown'
    error_domains[domain] += 1
for domain, count in error_domains.most_common(10):
    print(f"  {domain}: {count} errors")

print("\n=== DELIVERED domains ===")
delivered_domains = Counter()
for e in delivered:
    email = e.get('email', '')
    domain = email.split('@')[-1] if '@' in email else 'unknown'
    delivered_domains[domain] += 1
for domain, count in delivered_domains.most_common(10):
    print(f"  {domain}: {count} delivered")
