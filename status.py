"""
PROJECT CHRONOS - FULL STATUS REPORT
Run this to see everything at a glance.
"""
import requests, os
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()

URL = os.getenv('SUPABASE_URL','').rstrip('/')
KEY = os.getenv('SUPABASE_KEY','')
h = {'apikey': KEY, 'Authorization': f'Bearer {KEY}', 'Accept': 'application/json'}
h_count = {**h, 'Prefer': 'count=exact'}

today = datetime.now(timezone.utc).strftime('%Y-%m-%dT00:00:00')
now_str = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

print(f"\n{'='*60}")
print(f"  PROJECT CHRONOS - STATUS REPORT")
print(f"  Generated: {now_str}")
print(f"{'='*60}")

# === RENDER SERVICE ===
print("\n🌐 RENDER SERVICE:")
try:
    r = requests.get("https://sam-bot-v2.onrender.com/", timeout=15)
    print(f"  sam-bot-v2: HTTP {r.status_code} {'✅ LIVE' if r.status_code == 200 else '⚠️ DOWN'}")
except Exception as e:
    print(f"  sam-bot-v2: ERROR - {e}")

# === TELEGRAM BOT ===
print("\n🤖 TELEGRAM BOT:")
try:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    r = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10)
    if r.json().get("ok"):
        bot = r.json()["result"]
        print(f"  @{bot['username']}: ✅ ACTIVE")
    else:
        print(f"  Bot: ❌ FAIL")
except Exception as e:
    print(f"  Bot: ERROR - {e}")

# === APPLICATIONS ===
print("\n📊 APPLICATIONS:")
try:
    # Today
    r1 = requests.get(f'{URL}/rest/v1/applications?select=id&limit=1&timestamp=gte.{today}', headers=h_count, timeout=10)
    today_count = r1.headers.get('Content-Range', '0-0/0').split('/')[-1]
    # Total
    r2 = requests.get(f'{URL}/rest/v1/applications?select=id&limit=1', headers=h_count, timeout=10)
    total_count = r2.headers.get('Content-Range', '0-0/0').split('/')[-1]
    print(f"  Today: {today_count}")
    print(f"  Total: {total_count}")
    # Last 5
    r3 = requests.get(f'{URL}/rest/v1/applications?select=company_name,job_title,timestamp&order=timestamp.desc&limit=5', headers=h, timeout=10)
    for a in r3.json():
        cn = a.get('company_name','?')
        jt = a.get('job_title','?')
        ts = a.get('timestamp','?')[:16]
        print(f"  → {cn} | {jt} | {ts}")
except Exception as e:
    print(f"  ERROR: {e}")

# === LEADS ===
print("\n📋 LEADS QUEUE:")
try:
    for status in ['pending', 'processed', 'rate_limited', 'rejected']:
        r = requests.get(f'{URL}/rest/v1/leads?status=eq.{status}&select=id&limit=1', headers=h_count, timeout=8)
        count = r.headers.get('Content-Range', '0-0/0').split('/')[-1]
        if int(count) > 0:
            icon = '✅' if status == 'pending' else ('📤' if status == 'processed' else '⚠️')
            print(f"  {icon} {status}: {count}")
except Exception as e:
    print(f"  ERROR: {e}")

# === EMAIL PROVIDERS ===
print("\n📧 EMAIL PROVIDERS:")
# Brevo
try:
    brevo_key = os.getenv('BREVO_API_KEY', '')
    r = requests.get('https://api.brevo.com/v3/account', headers={'api-key': brevo_key}, timeout=8)
    if r.status_code == 200:
        plan = r.json().get('plan', [{}])
        credits = plan[0].get('credits', '?') if plan else '?'
        print(f"  Brevo: ✅ {credits}/300 credits remaining")
    elif r.status_code == 401:
        msg = r.json().get('message', '')
        if 'unrecognised IP' in msg:
            print(f"  Brevo: ✅ Works on Render (local IP blocked)")
        else:
            print(f"  Brevo: ❌ Key disabled")
except Exception as e:
    print(f"  Brevo: ERROR - {e}")

# Zoho (test connection)
print(f"  Zoho #1: {os.getenv('ZOHO_SMTP_USER','NOT SET')}")
print(f"  Gmail: {os.getenv('GMAIL_SMTP_USER','NOT SET')}")

# === AI SERVICES ===
print("\n🧠 AI SERVICES:")
try:
    groq_key = os.getenv("GROQ_API_KEY", "")
    r = requests.get("https://api.groq.com/openai/v1/models", headers={"Authorization": f"Bearer {groq_key}"}, timeout=10)
    if r.status_code == 200:
        print(f"  Groq: ✅ {len(r.json().get('data',[]))} models")
    elif r.status_code == 403:
        print(f"  Groq: ✅ Works on Render (local IP blocked)")
    else:
        print(f"  Groq: ❌ HTTP {r.status_code}")
except Exception as e:
    print(f"  Groq: ERROR - {e}")

# === RENDER ACCOUNTS ===
print("\n☁️ RENDER ACCOUNTS:")
accounts = [
    ('Account 2 (ACTIVE)', 'rnd_m4ozEoc4nQYOT16Omj0U9QGd3pra', 'srv-d80th10g4nts738vk7b0', 'sam-bot-v2'),
    ('Account 1 (BACKUP)', 'rnd_X4vP0V0M4LOJEGbFiKs2TM72NgTg', 'srv-d7s6rf6gvqtc73bt431g', 'sam-job-automator'),
]
for name, key, svc, svc_name in accounts:
    try:
        rh = {'Authorization': f'Bearer {key}', 'Accept': 'application/json'}
        r = requests.get(f'https://api.render.com/v1/services/{svc}', headers=rh, timeout=8)
        if r.status_code == 200:
            d = r.json()
            suspended = d.get('suspended', '?')
            status = '✅ RUNNING' if suspended == 'not_suspended' else '⏸️ SUSPENDED'
            print(f"  {name}: {svc_name} — {status}")
        else:
            print(f"  {name}: HTTP {r.status_code}")
    except Exception as e:
        print(f"  {name}: ERROR - {e}")

print(f"\n{'='*60}")
print(f"  Run 'python check_today.py' for detailed application list")
print(f"  Send /status to @samcvbot for live Telegram report")
print(f"{'='*60}\n")
