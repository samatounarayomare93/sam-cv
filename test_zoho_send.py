import smtplib, os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
load_dotenv()
user = os.getenv('ZOHO_SMTP_USER', '')
pwd = os.getenv('ZOHO_APP_PASSWORD', '')

msg = MIMEMultipart()
msg['From'] = f'Sam Salameh <{user}>'
msg['To'] = 'samsalameh.cv@gmail.com'
msg['Subject'] = 'Zoho Test - Unblocked and Working!'
msg.attach(MIMEText('<h2>Zoho is working! 500 emails/day unlocked!</h2>', 'html'))

try:
    s = smtplib.SMTP_SSL('smtp.zoho.com', 465, timeout=15)
    s.login(user, pwd)
    s.send_message(msg)
    s.quit()
    print('EMAIL SENT via Zoho!')
except Exception as e:
    print('FAILED:', e)
