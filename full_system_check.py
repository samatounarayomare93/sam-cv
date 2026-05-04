import sys, os
sys.path.insert(0, '.')
os.environ['RENDER'] = 'true'
from dotenv import load_dotenv
load_dotenv()
import logging
logging.basicConfig(level=logging.WARNING)

print('=== FULL SYSTEM CHECK ===')
print()

# 1. Email rotation
from core.email_rotator import get_rotator
r = get_rotator()
print(f'Email providers configured: {len(r.providers)}')
for p in r.providers:
    used = r.usage.get(p["name"], {}).get("count", 0)
    print(f'  {p["display_name"]}: {used}/{p["limit"]} used')
print(f'Total daily capacity: {r.get_total_daily_limit()}')
print()

# 2. Test email send
from core import smtp_engine
print('Testing email send...')
result = smtp_engine.send_test_email('samsalameh.cv@gmail.com')
print(f'Email test: {"PASS" if result else "FAIL"}')
print()

# 3. Check Zoho accounts
import smtplib
zoho_accounts = [
    ('samsalameh.cv@zohomail.com', 'R0R6dqr5qL1g', 'Zoho #1'),
    ('samsalameh@zohomail.com', 'EGDUw41ADNmM', 'Zoho #2'),
]
for email, pwd, name in zoho_accounts:
    try:
        s = smtplib.SMTP_SSL('smtp.zoho.com', 465, timeout=10)
        s.login(email, pwd)
        s.quit()
        print(f'{name} ({email}): WORKING')
    except Exception as e:
        print(f'{name} ({email}): FAILED - {str(e)[:60]}')

print()

# 4. Check Resend
import requests
resend_key = os.getenv('RESEND_API_KEY', '')
if resend_key:
    print(f'Resend API key: SET ({resend_key[:15]}...)')
else:
    print('Resend API key: MISSING!')

# 5. Check Brevo
brevo_key = os.getenv('BREVO_API_KEY', '')
if brevo_key:
    r2 = requests.get('https://api.brevo.com/v3/account', 
        headers={'api-key': brevo_key}, timeout=10)
    if r2.status_code == 200:
        data = r2.json()
        credits = data.get('plan', [{}])[0].get('credits', 0)
        print(f'Brevo: WORKING ({credits} credits remaining)')
    else:
        print(f'Brevo: ERROR {r2.status_code}')
else:
    print('Brevo: NOT CONFIGURED')

print()
print('=== CHECK COMPLETE ===')
