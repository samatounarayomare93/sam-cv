import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

user = 'samsalameh@zohomail.com'
pwd = 'EGDUw41ADNmM'

print(f"Testing: {user}")
try:
    s = smtplib.SMTP_SSL('smtp.zoho.com', 465, timeout=15)
    s.login(user, pwd)
    
    msg = MIMEMultipart()
    msg['From'] = f'Sam Salameh <{user}>'
    msg['To'] = 'samsalameh.cv@gmail.com'
    msg['Subject'] = 'Zoho Account #2 - Working!'
    msg.attach(MIMEText('<h2>Zoho #2 is working! +500 emails/day added!</h2>', 'html'))
    
    s.send_message(msg)
    s.quit()
    print(f'SUCCESS! Zoho #2 works!')
except Exception as e:
    print(f'FAILED: {e}')
