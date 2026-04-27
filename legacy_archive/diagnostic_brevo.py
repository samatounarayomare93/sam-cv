import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def test_brevo():
    login = os.getenv("BREVO_SMTP_LOGIN")
    password = os.getenv("BREVO_SMTP_PASSWORD")
    server_addr = "smtp-relay.brevo.com"
    port = 587
    
    print(f"Testing Brevo SMTP with Login: {login}")
    
    msg = MIMEMultipart()
    msg['From'] = f"Sam Salameh <{login}>"
    msg['To'] = "sam.dev1@hotmail.com"
    msg['Subject'] = "Brevo SMTP Diagnostic Strike"
    msg.attach(MIMEText("This is a diagnostic strike testing the recovered Brevo credentials. If you see this, the Credential Vault is partially restored.", 'plain'))
    
    try:
        print("Connecting to server...")
        server = smtplib.SMTP(server_addr, port, timeout=20)
        print("Starting TLS...")
        server.starttls()
        print("Logging in...")
        server.login(login, password)
        print("Sending message...")
        server.send_message(msg)
        server.quit()
        print("✅ SUCCESS: Brevo SMTP is operational.")
        return True
    except Exception as e:
        print(f"❌ FAILURE: {e}")
        return False

if __name__ == "__main__":
    test_brevo()
