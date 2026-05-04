import smtplib, os
from dotenv import load_dotenv
load_dotenv()
user = os.getenv('ZOHO_SMTP_USER', '')
pwd = os.getenv('ZOHO_APP_PASSWORD', '')
print('User:', user)
print('Testing Zoho port 465...')
try:
    s = smtplib.SMTP_SSL('smtp.zoho.com', 465, timeout=15)
    s.login(user, pwd)
    print('SUCCESS - Zoho is UNBLOCKED!')
    s.quit()
except Exception as e:
    print('STILL BLOCKED:', str(e)[:200])
