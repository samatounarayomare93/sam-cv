# -*- coding: utf-8 -*-
import smtplib, os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
load_dotenv()
user = os.getenv('ZOHO_SMTP_USER', '')
pwd = os.getenv('ZOHO_APP_PASSWORD', '')
print('User:', user)
print('Pass len:', len(pwd))

for port, use_ssl in [(465, True), (587, False)]:
    try:
        if use_ssl:
            s = smtplib.SMTP_SSL('smtp.zoho.com', port, timeout=15)
        else:
            s = smtplib.SMTP('smtp.zoho.com', port, timeout=15)
            s.ehlo(); s.starttls(); s.ehlo()
        s.login(user, pwd)
        msg = MIMEMultipart()
        msg['From'] = 'Sam Salameh <' + user + '>'
        msg['To'] = 'samsalameh.cv@gmail.com'
        msg['Subject'] = 'Zoho Test Port ' + str(port)
        msg.attach(MIMEText('<h2>Zoho port ' + str(port) + ' works!</h2>', 'html'))
        s.send_message(msg)
        s.quit()
        print('OK port', port)
    except Exception as e:
        print('FAIL port', port, ':', e)