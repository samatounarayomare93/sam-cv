"""
Full email provider diagnostic - tests Brevo, Zoho, Resend
and checks what's actually being sent to companies.
"""
import os, sys, json, requests, sqlite3
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("EMAIL PROVIDER DIAGNOSTIC")
print("=" * 60)

# ── 1. BREVO ──────────────────────────────────────────────────
print("\n📧 BREVO:")
brevo_key = os.getenv('BREVO_API_KEY', '')
if brevo_key:
    r = requests.get(
        'https://api.brevo.com/v3/account',
        headers={'api-key': brevo_key, 'Accept': 'application/json'},
        timeout=10
    )
    if r.status_code == 200:
        data = r.json()
        plan = data.get('plan', [{}])
        email_plan = next((p for p in plan if p.get('type') == 'payAsYouGo' or 'email' in str(p).lower()), plan[0] if plan else {})
        print(f"  Account: {data.get('email', '?')}")
        print(f"  Company: {data.get('companyName', '?')}")
        # Get today's stats
        r2 = requests.get(
            'https://api.brevo.com/v3/smtp/statistics/aggregatedReport',
            headers={'api-key': brevo_key, 'Accept': 'application/json'},
            timeout=10
        )
        if r2.status_code == 200:
            stats = r2.json()
            print(f"  Delivered: {stats.get('delivered', '?')}")
            print(f"  Opens:     {stats.get('uniqueOpens', '?')}")
            print(f"  Clicks:    {stats.get('uniqueClicks', '?')}")
            print(f"  Bounces:   {stats.get('hardBounces', 0) + stats.get('softBounces', 0)}")
            print(f"  Spam:      {stats.get('spamReports', '?')}")
        # Get sending limit
        r3 = requests.get(
            'https://api.brevo.com/v3/smtp/statistics/reports?limit=1',
            headers={'api-key': brevo_key, 'Accept': 'application/json'},
            timeout=10
        )
        print(f"  Status: ✅ WORKING")
    else:
        print(f"  Status: ❌ ERROR {r.status_code}: {r.text[:100]}")
else:
    print("  Status: ❌ NO API KEY")

# ── 2. BREVO - Last 10 emails sent ────────────────────────────
print("\n📬 BREVO - Last emails sent:")
if brevo_key:
    r = requests.get(
        'https://api.brevo.com/v3/smtp/emails?limit=10&sort=desc',
        headers={'api-key': brevo_key, 'Accept': 'application/json'},
        timeout=10
    )
    if r.status_code == 200:
        emails = r.json().get('transactionalEmails', [])
        if emails:
            for e in emails[:10]:
                to = e.get('to', [{}])
                to_email = to[0].get('email', '?') if to else '?'
                subject = e.get('subject', '?')[:50]
                status = e.get('events', [{}])[-1].get('name', '?') if e.get('events') else '?'
                date = e.get('date', '?')[:16]
                print(f"  {date}  {to_email:35}  {status:12}  {subject}")
        else:
            print("  No emails found in history")
    else:
        print(f"  Error: {r.status_code} - {r.text[:100]}")

# ── 3. ZOHO ───────────────────────────────────────────────────
print("\n📧 ZOHO:")
zoho_user = os.getenv('ZOHO_SMTP_USER', '')
zoho_pass = os.getenv('ZOHO_APP_PASSWORD', '')
zoho_user2 = os.getenv('ZOHO_SMTP_USER_2', '')
zoho_pass2 = os.getenv('ZOHO_APP_PASSWORD_2', '')

if zoho_user and zoho_pass:
    # Test SMTP connection
    import smtplib
    try:
        server = smtplib.SMTP('smtp.zoho.com', 587, timeout=10)
        server.starttls()
        server.login(zoho_user, zoho_pass)
        server.quit()
        print(f"  Account 1: {zoho_user} ✅ SMTP LOGIN OK")
    except Exception as e:
        print(f"  Account 1: {zoho_user} ❌ {e}")
else:
    print("  Account 1: ❌ NOT CONFIGURED")

if zoho_user2 and zoho_pass2:
    try:
        server = smtplib.SMTP('smtp.zoho.com', 587, timeout=10)
        server.starttls()
        server.login(zoho_user2, zoho_pass2)
        server.quit()
        print(f"  Account 2: {zoho_user2} ✅ SMTP LOGIN OK")
    except Exception as e:
        print(f"  Account 2: {zoho_user2} ❌ {e}")
else:
    print("  Account 2: ❌ NOT CONFIGURED")

# ── 4. RESEND ─────────────────────────────────────────────────
print("\n📧 RESEND:")
resend_key = os.getenv('RESEND_API_KEY', '')
resend_from = os.getenv('RESEND_FROM_EMAIL', '')

if resend_key:
    r = requests.get(
        'https://api.resend.com/domains',
        headers={'Authorization': f'Bearer {resend_key}', 'Accept': 'application/json'},
        timeout=10
    )
    if r.status_code == 200:
        domains = r.json().get('data', [])
        if domains:
            for d in domains:
                print(f"  Domain: {d.get('name')} | Status: {d.get('status')} | Region: {d.get('region')}")
        else:
            print("  No verified domains — Resend CANNOT send to external emails!")
            print("  ⚠️  You need to verify a custom domain at resend.com/domains")
    else:
        print(f"  Error: {r.status_code} - {r.text[:100]}")
    
    # Check emails sent
    r2 = requests.get(
        'https://api.resend.com/emails',
        headers={'Authorization': f'Bearer {resend_key}', 'Accept': 'application/json'},
        timeout=10
    )
    if r2.status_code == 200:
        emails = r2.json().get('data', [])
        print(f"  Emails in history: {len(emails)}")
        for e in emails[:5]:
            print(f"    To: {e.get('to', ['?'])[0] if e.get('to') else '?'}  Status: {e.get('last_event', '?')}  Subject: {e.get('subject','?')[:40]}")
    
    if not resend_from:
        print("  RESEND_FROM_EMAIL: ❌ NOT SET — Resend is DISABLED (correct)")
    else:
        free_domains = {'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com'}
        domain = resend_from.split('@')[-1].lower()
        if domain in free_domains:
            print(f"  RESEND_FROM_EMAIL: ⚠️  {resend_from} — free domain, Resend DISABLED (correct)")
        else:
            print(f"  RESEND_FROM_EMAIL: ✅ {resend_from} — custom domain, Resend ENABLED")
else:
    print("  Status: ❌ NO API KEY")

# ── 5. EMAIL ROTATOR STATUS ───────────────────────────────────
print("\n🔄 EMAIL ROTATOR (what Render uses):")
os.environ['RENDER'] = '1'
try:
    from core.email_rotator import EmailRotator
    r = EmailRotator()
    if r.providers:
        for p in r.providers:
            name = p['display_name']
            limit = p['limit']
            used = r.usage.get(p['name'], {}).get('count', 0)
            remaining = limit - used
            bar = '█' * int((used/limit)*20) + '░' * (20 - int((used/limit)*20)) if limit else '░'*20
            print(f"  {name:15} {bar} {used:3}/{limit} used ({remaining} remaining)")
    else:
        print("  ❌ NO PROVIDERS AVAILABLE ON RENDER!")
except Exception as e:
    print(f"  Error: {e}")

# ── 6. LOCAL DB - Applications sent ──────────────────────────
print("\n📊 LOCAL DB - Applications sent:")
db_path = 'sam_ultimate.db'
if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Total sent
        cursor.execute("SELECT COUNT(*) FROM applications")
        total = cursor.fetchone()[0]
        print(f"  Total applications: {total}")
        
        # Today's sent
        cursor.execute("SELECT COUNT(*) FROM applications WHERE timestamp >= date('now')")
        today = cursor.fetchone()[0]
        print(f"  Today: {today}")
        
        # Last 10
        cursor.execute("SELECT company_name, company_email, job_title, status, timestamp FROM applications ORDER BY timestamp DESC LIMIT 10")
        rows = cursor.fetchall()
        if rows:
            print(f"\n  Last 10 applications:")
            for row in rows:
                company, email, title, status, ts = row
                ts_short = str(ts)[:16] if ts else '?'
                print(f"    {ts_short}  {str(company)[:25]:25}  {str(email)[:30]:30}  {status}")
        conn.close()
    except Exception as e:
        print(f"  Error reading DB: {e}")
else:
    print("  No local DB found")

# ── 7. LEADS STATUS ───────────────────────────────────────────
print("\n📋 LEADS STATUS (what's pending):")
if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT status, COUNT(*) FROM leads GROUP BY status ORDER BY COUNT(*) DESC")
        rows = cursor.fetchall()
        for status, count in rows:
            print(f"  {str(status):20} {count:5}")
        conn.close()
    except Exception as e:
        print(f"  Error: {e}")

print("\n" + "=" * 60)
print("DIAGNOSIS COMPLETE")
print("=" * 60)
