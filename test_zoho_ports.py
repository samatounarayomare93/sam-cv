import smtplib, os
from dotenv import load_dotenv
load_dotenv()
user = os.getenv('ZOHO_SMTP_USER', '')
pwd = os.getenv('ZOHO_APP_PASSWORD', '')

for port, ssl in [(465, True), (587, False)]:
    try:
        if ssl:
            s = smtplib.SMTP_SSL('smtp.zoho.com', port, timeout=10)
        else:
            s = smtplib.SMTP('smtp.zoho.com', port, timeout=10)
            s.ehlo(); s.starttls(); s.ehlo()
        s.login(user, pwd)
        s.quit()
        print(f'PORT {port}: WORKS!')
    except Exception as e:
        print(f'PORT {port}: FAILED - {str(e)[:100]}')
