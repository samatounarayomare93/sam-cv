import requests, os, smtplib
from dotenv import load_dotenv
load_dotenv()

key = os.getenv('BREVO_API_KEY')
print("="*60)
print("BREVO DIAGNOSTIC")
print("="*60)

# Check account
r = requests.get('https://api.brevo.com/v3/account', headers={'api-key': key}, timeout=10)
print(f"Account status: {r.status_code}")
if r.status_code == 200:
    d = r.json()
    print(f"Email: {d.get('email')}")
    for p in d.get('plan', []):
        ptype = p.get('type', '?')
        credits = p.get('credits', 0)
        print(f"Plan: {ptype} | Credits: {credits}")
else:
    print(f"Error: {r.text[:100]}")

# Get SMTP users/credentials
print("\nChecking SMTP users...")
r2 = requests.get('https://api.brevo.com/v3/smtp/settings', headers={'api-key': key}, timeout=10)
print(f"SMTP settings: {r2.status_code}")
if r2.status_code == 200:
    smtp_data = r2.json()
    print(f"SMTP enabled: {smtp_data.get('enabled')}")
    print(f"SMTP relay: {smtp_data.get('relay')}")
    print(f"SMTP port: {smtp_data.get('port')}")
    print(f"SMTP username: {smtp_data.get('username')}")
else:
    print(f"Response: {r2.text[:200]}")

# Try to get SMTP credentials via API
print("\nChecking SMTP credentials in .env...")
login = os.getenv('BREVO_SMTP_LOGIN', '')
password = os.getenv('BREVO_SMTP_PASSWORD', '')
print(f"Login: {login}")
print(f"Password: {password[:10]}...")

# Test SMTP connection
print("\nTesting SMTP connection...")
try:
    with smtplib.SMTP('smtp-relay.brevo.com', 587, timeout=10) as s:
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(login, password)
        print("SMTP: LOGIN OK")
except smtplib.SMTPAuthenticationError as e:
    print(f"SMTP AUTH FAILED: {e}")
    print("\nThe SMTP password may have changed.")
    print("To fix: Go to app.brevo.com → SMTP & API → Generate new SMTP key")
except Exception as e:
    print(f"SMTP Error: {e}")

# Test Brevo HTTP API (doesn't need SMTP)
print("\nTesting Brevo HTTP API (alternative to SMTP)...")
payload = {
    "sender": {"name": "Sam Salameh", "email": "samatou683@gmail.com"},
    "to": [{"email": "samsalameh.cv@gmail.com"}],
    "subject": "Brevo API Test",
    "htmlContent": "<p>Test</p>"
}
r3 = requests.post('https://api.brevo.com/v3/smtp/email',
    headers={'api-key': key, 'Content-Type': 'application/json'},
    json=payload, timeout=15)
print(f"HTTP API: {r3.status_code}")
if r3.status_code in (200, 201):
    print(f"SUCCESS: {r3.json().get('messageId', '')[:30]}")
else:
    print(f"Failed: {r3.text[:200]}")
