"""
Deep diagnostic: test exactly what happens when test email is triggered.
Simulates what the Telegram bot does on Render.
"""
import os, sys, logging
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")

sys.path.insert(0, os.path.dirname(__file__))

TARGET = os.getenv("TEST_RECEIVER_EMAIL", "samsalameh.cv@gmail.com")
print(f"\n{'='*70}")
print(f"🧪 DEEP TEST EMAIL DIAGNOSTIC")
print(f"{'='*70}")
print(f"Target: {TARGET}")
print(f"Gmail user: {os.getenv('GMAIL_SMTP_USER')}")
print(f"Zoho user:  {os.getenv('ZOHO_SMTP_USER')}")
print(f"Brevo key:  {'SET' if os.getenv('BREVO_API_KEY') else 'NOT SET'}")
print(f"Resend key: {'SET' if os.getenv('RESEND_API_KEY') else 'NOT SET'}")
print(f"{'='*70}\n")

# Step 1: Test each provider individually
import smtplib, ssl

def test_smtp(name, server, port, user, password, use_ssl=False):
    print(f"\n🔌 Testing {name} ({server}:{port})...")
    try:
        if use_ssl:
            ctx = ssl.create_default_context()
            with smtplib.SMTP_SSL(server, port, context=ctx, timeout=10) as s:
                s.login(user, password)
                print(f"  ✅ {name}: LOGIN OK")
                return True
        else:
            with smtplib.SMTP(server, port, timeout=10) as s:
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(user, password)
                print(f"  ✅ {name}: LOGIN OK")
                return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"  ❌ {name}: AUTH FAILED - {e}")
    except smtplib.SMTPConnectError as e:
        print(f"  ❌ {name}: CONNECT FAILED - {e}")
    except ConnectionRefusedError as e:
        print(f"  ❌ {name}: PORT BLOCKED - {e}")
    except Exception as e:
        print(f"  ❌ {name}: {type(e).__name__}: {e}")
    return False

print("STEP 1: Testing SMTP connections...")
print("-"*70)

gmail_ok = test_smtp("Gmail SSL:465", "smtp.gmail.com", 465,
    os.getenv("GMAIL_SMTP_USER",""), os.getenv("GMAIL_APP_PASSWORD",""), use_ssl=True)

zoho1_ok = test_smtp("Zoho SSL:465", "smtp.zoho.com", 465,
    os.getenv("ZOHO_SMTP_USER",""), os.getenv("ZOHO_APP_PASSWORD",""), use_ssl=True)

zoho2_ok = test_smtp("Zoho2 SSL:465", "smtp.zoho.com", 465,
    os.getenv("ZOHO_SMTP_USER_2",""), os.getenv("ZOHO_APP_PASSWORD_2",""), use_ssl=True)

brevo_ok = test_smtp("Brevo TLS:587", "smtp-relay.brevo.com", 587,
    os.getenv("BREVO_SMTP_LOGIN",""), os.getenv("BREVO_SMTP_PASSWORD",""), use_ssl=False)

print(f"\n{'='*70}")
print(f"SMTP Summary: Gmail={gmail_ok} | Zoho1={zoho1_ok} | Zoho2={zoho2_ok} | Brevo={brevo_ok}")
print(f"{'='*70}\n")

# Step 2: Test Brevo HTTP API
print("STEP 2: Testing Brevo HTTP API...")
print("-"*70)
import requests
brevo_api = os.getenv("BREVO_API_KEY","")
if brevo_api:
    try:
        r = requests.get(
            "https://api.brevo.com/v3/account",
            headers={"api-key": brevo_api},
            timeout=10
        )
        if r.status_code == 200:
            data = r.json()
            plan = data.get('plan', [{}])
            credits = data.get('plan', [{}])
            print(f"  ✅ Brevo API: Account OK - {data.get('email','')}")
            # Check email credits
            for p in data.get('plan', []):
                if p.get('type') == 'payAsYouGo':
                    print(f"  📊 Credits: {p.get('credits', 'N/A')}")
        else:
            print(f"  ❌ Brevo API: {r.status_code} - {r.text[:100]}")
    except Exception as e:
        print(f"  ❌ Brevo API error: {e}")
else:
    print("  ⚠️ BREVO_API_KEY not set")

# Step 3: Test Resend API
print("\nSTEP 3: Testing Resend API...")
print("-"*70)
resend_key = os.getenv("RESEND_API_KEY","")
if resend_key:
    try:
        r = requests.get(
            "https://api.resend.com/domains",
            headers={"Authorization": f"Bearer {resend_key}"},
            timeout=10
        )
        if r.status_code == 200:
            data = r.json()
            domains = data.get('data', [])
            print(f"  ✅ Resend API: OK - {len(domains)} domains")
            for d in domains:
                print(f"     Domain: {d.get('name')} | Status: {d.get('status')}")
        else:
            print(f"  ❌ Resend API: {r.status_code} - {r.text[:100]}")
    except Exception as e:
        print(f"  ❌ Resend API error: {e}")
else:
    print("  ⚠️ RESEND_API_KEY not set")

# Step 4: Actually send a test email using the best available method
print(f"\n{'='*70}")
print(f"STEP 4: Sending actual test email to {TARGET}...")
print(f"{'='*70}")

# Try Brevo HTTP API first (most reliable)
sent = False

if brevo_api and not sent:
    print("\n📧 Trying Brevo HTTP API...")
    try:
        payload = {
            "sender": {"name": "Sam Salameh", "email": "samatou683@gmail.com"},
            "to": [{"email": TARGET}],
            "subject": "✅ TEST EMAIL - Sam CV Bot Working!",
            "htmlContent": """
            <div style="font-family:Arial;padding:20px;background:#1a1a2e;color:#e2e8f0;">
                <h2 style="color:#00ff88;">✅ TEST EMAIL SUCCESS!</h2>
                <p>This is a test email from your Sam CV Bot.</p>
                <p><strong>If you received this, the email system is working correctly!</strong></p>
                <hr style="border-color:#333;">
                <p>Sent via: Brevo HTTP API</p>
                <p>Bot: @samcvbot</p>
                <p>Time: """ + str(__import__('datetime').datetime.now()) + """</p>
            </div>
            """
        }
        r = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={"api-key": brevo_api, "Content-Type": "application/json"},
            json=payload,
            timeout=15
        )
        if r.status_code in (200, 201):
            print(f"  ✅ BREVO HTTP: Email sent! ID: {r.json().get('messageId','')}")
            sent = True
        else:
            print(f"  ❌ BREVO HTTP: {r.status_code} - {r.text[:200]}")
    except Exception as e:
        print(f"  ❌ BREVO HTTP error: {e}")

# Try Gmail SMTP
if gmail_ok and not sent:
    print("\n📧 Trying Gmail SMTP...")
    try:
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        gmail_user = os.getenv("GMAIL_SMTP_USER","")
        gmail_pass = os.getenv("GMAIL_APP_PASSWORD","")
        msg = MIMEMultipart()
        msg['From'] = f"Sam Salameh <{gmail_user}>"
        msg['To'] = TARGET
        msg['Subject'] = "✅ TEST EMAIL - Sam CV Bot Working!"
        msg.attach(MIMEText("<h2>✅ Test email from Sam CV Bot!</h2><p>Gmail SMTP is working.</p>", 'html'))
        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx, timeout=10) as s:
            s.login(gmail_user, gmail_pass)
            s.sendmail(gmail_user, [TARGET], msg.as_bytes())
        print(f"  ✅ GMAIL SMTP: Email sent!")
        sent = True
    except Exception as e:
        print(f"  ❌ GMAIL SMTP error: {e}")

# Try Zoho SMTP
if zoho1_ok and not sent:
    print("\n📧 Trying Zoho SMTP...")
    try:
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        zoho_user = os.getenv("ZOHO_SMTP_USER","")
        zoho_pass = os.getenv("ZOHO_APP_PASSWORD","")
        msg = MIMEMultipart()
        msg['From'] = f"Sam Salameh <{zoho_user}>"
        msg['To'] = TARGET
        msg['Subject'] = "✅ TEST EMAIL - Sam CV Bot Working!"
        msg.attach(MIMEText("<h2>✅ Test email from Sam CV Bot!</h2><p>Zoho SMTP is working.</p>", 'html'))
        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.zoho.com", 465, context=ctx, timeout=10) as s:
            s.login(zoho_user, zoho_pass)
            s.sendmail(zoho_user, [TARGET], msg.as_bytes())
        print(f"  ✅ ZOHO SMTP: Email sent!")
        sent = True
    except Exception as e:
        print(f"  ❌ ZOHO SMTP error: {e}")

print(f"\n{'='*70}")
if sent:
    print(f"🎉 SUCCESS! Test email sent to {TARGET}")
    print(f"Check your inbox (and spam folder)!")
else:
    print(f"❌ FAILED! Could not send test email to {TARGET}")
    print(f"\nPossible causes:")
    print(f"  1. All SMTP credentials are wrong")
    print(f"  2. Brevo API has no credits")
    print(f"  3. Network/firewall blocking")
print(f"{'='*70}\n")
