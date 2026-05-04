import smtplib

pwd = 'EGDUw41ADNmM'

emails_to_try = [
    'samsalameh.cv@zohomail.com',
    'samatou683@zohomail.com',
    'samsalameh2@zohomail.com',
    'sam.salameh@zohomail.com',
    'samsalameh1@zohomail.com',
    'samcv@zohomail.com',
]

print("Testing app password with different Zoho emails...")
for email in emails_to_try:
    try:
        s = smtplib.SMTP_SSL('smtp.zoho.com', 465, timeout=8)
        s.login(email, pwd)
        s.quit()
        print(f'FOUND: {email}')
    except smtplib.SMTPAuthenticationError:
        print(f'Wrong: {email}')
    except Exception as e:
        print(f'Error {email}: {str(e)[:50]}')
