#!/usr/bin/env python3
"""Simple email test WITHOUT attachments"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

gmail_user = os.getenv('GMAIL_SMTP_USER')
gmail_pass = os.getenv('GMAIL_APP_PASSWORD')

msg = MIMEMultipart()
msg['From'] = f"Sam Salameh <{gmail_user}>"
msg['To'] = gmail_user
msg['Subject'] = "✅ Simple Test - No Attachments"

body = """
<html>
<body style="font-family: Arial; padding: 20px;">
    <h2 style="color: #00b4d8;">✅ This is a SIMPLE test email</h2>
    <p>No attachments, just text.</p>
    <p>If you receive this in your INBOX (not spam), Gmail SMTP is working!</p>
    <hr>
    <p style="color: #666; font-size: 12px;">Sent via Gmail SMTP Port 465</p>
</body>
</html>
"""

msg.attach(MIMEText(body, 'html'))

print("Sending simple email (no attachments)...")
server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=15)
server.login(gmail_user, gmail_pass)
server.send_message(msg)
server.quit()
print("✅ Email sent! Check your inbox at:", gmail_user)
