"""
Complete system checkup and auto-fix.
"""
import os, sys, requests, json, smtplib, ssl
from dotenv import load_dotenv
load_dotenv()

# Force load DB keys
from core.api_key_manager import get_key_manager
mgr = get_key_manager()
for k in ['OPENROUTER_API_KEY', 'HUGGINGFACE_API_KEY', 'DEEPSEEK_API_KEY']:
    v = mgr.get(k)
    if v:
        os.environ[k] = v

supa_url = os.getenv('SUPABASE_URL', '')
supa_key = os.getenv('SUPABASE_KEY', '')
supa_headers = {'apikey': supa_key, 'Authorization': f'Bearer {supa_key}', 'Content-Type': 'application/json'}
token = os.getenv('TELEGRAM_BOT_TOKEN', '')
chat_id = os.getenv('TELEGRAM_CHAT_ID', '')

results = {}
fixes_applied = []

def check(name, ok, detail=""):
    icon = "OK" if ok else "FAIL"
    results[name] = ok
    print(f"  [{icon}] {name}: {detail}")
    return ok

print("=" * 65)
print("FULL SYSTEM CHECKUP")
print("=" * 65)

# ── 1. TELEGRAM ──────────────────────────────────────────────
print("\n[1] TELEGRAM:")
try:
    r = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10)
    d = r.json()
    check("Bot Token", d.get("ok"), f"@{d.get('result',{}).get('username','?')}")
except Exception as e:
    check("Bot Token", False, str(e)[:50])

# ── 2. RENDER SERVICE ─────────────────────────────────────────
print("\n[2] RENDER (sam-bot-v2):")
render_url = os.getenv('RENDER_EXTERNAL_URL', 'https://sam-bot-v2.onrender.com')
try:
    r = requests.get(render_url, timeout=20)
    check("Service Live", r.status_code == 200, f"HTTP {r.status_code} | {render_url}")
except Exception as e:
    check("Service Live", False, str(e)[:50])

# Check bot heartbeat
try:
    r = requests.get(
        f"{supa_url}/rest/v1/system_settings?key=eq.active_bot_heartbeat&select=value",
        headers=supa_headers, timeout=10
    )
    if r.status_code == 200 and r.json():
        hb = r.json()[0].get('value', '')
        from datetime import datetime, timezone
        hb_time = datetime.fromisoformat(hb.replace('Z', '+00:00'))
        now = datetime.now(hb_time.tzinfo)
        age_min = (now - hb_time).total_seconds() / 60
        ok = age_min < 30
        check("Bot Heartbeat", ok, f"{age_min:.0f} min ago {'(ALIVE)' if ok else '(STALE - may be crashed)'}")
        if not ok:
            fixes_applied.append("Bot heartbeat stale - triggering redeploy")
    else:
        check("Bot Heartbeat", False, "No heartbeat found")
except Exception as e:
    check("Bot Heartbeat", False, str(e)[:50])

# ── 3. EMAIL PROVIDERS ────────────────────────────────────────
print("\n[3] EMAIL PROVIDERS:")
# Resend
resend_key = os.getenv('RESEND_API_KEY', '')
try:
    r = requests.post('https://api.resend.com/emails',
        headers={'Authorization': f'Bearer {resend_key}', 'Content-Type': 'application/json'},
        json={'from': 'Sam Salameh <onboarding@resend.dev>', 'to': ['samsalameh.cv@gmail.com'],
              'subject': 'System Check', 'html': '<p>OK</p>'},
        timeout=15)
    check("Resend", r.json().get('id') is not None, f"ID: {r.json().get('id','?')[:15]}...")
except Exception as e:
    check("Resend", False, str(e)[:50])

# Gmail
gmail_user = os.getenv('GMAIL_SMTP_USER', '')
gmail_pass = os.getenv('GMAIL_APP_PASSWORD', '')
try:
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ctx, timeout=10) as s:
        s.login(gmail_user, gmail_pass)
    check("Gmail SMTP", True, gmail_user)
except Exception as e:
    check("Gmail SMTP", False, str(e)[:50])

# Zoho
zoho_user = os.getenv('ZOHO_SMTP_USER', '')
zoho_pass = os.getenv('ZOHO_APP_PASSWORD', '')
try:
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.zoho.com', 465, context=ctx, timeout=10) as s:
        s.login(zoho_user, zoho_pass)
    check("Zoho SMTP", True, zoho_user)
except Exception as e:
    check("Zoho SMTP", False, str(e)[:50])

# ── 4. AI SERVICES ────────────────────────────────────────────
print("\n[4] AI SERVICES:")
groq_key = os.getenv('GROQ_API_KEY', '')
try:
    r = requests.post('https://api.groq.com/openai/v1/chat/completions',
        headers={'Authorization': f'Bearer {groq_key}', 'Content-Type': 'application/json'},
        json={'model': 'llama-3.3-70b-versatile', 'messages': [{'role': 'user', 'content': 'Say OK'}], 'max_tokens': 3},
        timeout=15)
    d = r.json()
    check("Groq", d.get('choices') is not None, d.get('choices', [{}])[0].get('message', {}).get('content', 'no response')[:20] if d.get('choices') else str(d)[:50])
except Exception as e:
    check("Groq", False, str(e)[:50])

deepseek_key = os.getenv('DEEPSEEK_API_KEY', '')
if deepseek_key:
    try:
        r = requests.post('https://api.deepseek.com/chat/completions',
            headers={'Authorization': f'Bearer {deepseek_key}', 'Content-Type': 'application/json'},
            json={'model': 'deepseek-chat', 'messages': [{'role': 'user', 'content': 'Say OK'}], 'max_tokens': 3},
            timeout=15)
        d = r.json()
        check("DeepSeek", d.get('choices') is not None, "Working" if d.get('choices') else str(d)[:50])
    except Exception as e:
        check("DeepSeek", False, str(e)[:50])
else:
    check("DeepSeek", False, "No key (load from DB)")

openrouter_key = os.getenv('OPENROUTER_API_KEY', '')
if openrouter_key:
    try:
        r = requests.post('https://openrouter.ai/api/v1/chat/completions',
            headers={'Authorization': f'Bearer {openrouter_key}', 'Content-Type': 'application/json',
                     'HTTP-Referer': 'https://sam-bot-v2.onrender.com'},
            json={'model': 'openrouter/free', 'messages': [{'role': 'user', 'content': 'Say OK'}], 'max_tokens': 5},
            timeout=15)
        d = r.json()
        check("OpenRouter", d.get('choices') is not None, "Working" if d.get('choices') else f"HTTP {r.status_code}: {str(d)[:50]}")
    except Exception as e:
        check("OpenRouter", False, str(e)[:50])
else:
    check("OpenRouter", False, "No key (load from DB)")

# ── 5. DATABASE ───────────────────────────────────────────────
print("\n[5] DATABASE:")
try:
    r = requests.get(f"{supa_url}/rest/v1/system_settings?select=key,value", headers=supa_headers, timeout=10)
    check("Supabase", r.status_code == 200, f"{len(r.json())} settings rows")
    settings = {s['key']: s['value'] for s in r.json()}
    check("Kill Switch", settings.get('kill_switch', '?') == 'false', f"kill_switch={settings.get('kill_switch','?')}")
except Exception as e:
    check("Supabase", False, str(e)[:50])

# Check leads
try:
    r = requests.get(f"{supa_url}/rest/v1/leads?select=status&limit=500", headers=supa_headers, timeout=10)
    if r.status_code == 200:
        leads = r.json()
        statuses = {}
        for l in leads:
            s = l.get('status', '?')
            statuses[s] = statuses.get(s, 0) + 1
        pending = statuses.get('pending', 0)
        check("Leads Queue", pending > 0, f"pending={pending} | " + " | ".join(f"{k}={v}" for k,v in list(statuses.items())[:4]))
        if pending == 0:
            fixes_applied.append("No pending leads - need to reset some")
    else:
        check("Leads Queue", False, f"HTTP {r.status_code}")
except Exception as e:
    check("Leads Queue", False, str(e)[:50])

# ── 6. GITHUB ─────────────────────────────────────────────────
print("\n[6] GITHUB:")
github_pat = os.getenv('GITHUB_PAT', '')
try:
    r = requests.get('https://api.github.com/user',
        headers={'Authorization': f'token {github_pat}', 'Accept': 'application/vnd.github.v3+json'}, timeout=10)
    d = r.json()
    check("GitHub PAT", r.status_code == 200, f"user={d.get('login','?')}")
except Exception as e:
    check("GitHub PAT", False, str(e)[:50])

# ── SUMMARY ───────────────────────────────────────────────────
print("\n" + "=" * 65)
passed = sum(1 for v in results.values() if v)
total = len(results)
failed = [k for k, v in results.items() if not v]
print(f"RESULT: {passed}/{total} checks passed")
if failed:
    print(f"FAILED: {', '.join(failed)}")
else:
    print("ALL SYSTEMS OPERATIONAL!")

# ── AUTO-FIXES ────────────────────────────────────────────────
if fixes_applied:
    print(f"\nAUTO-FIXES NEEDED:")
    for f in fixes_applied:
        print(f"  - {f}")

print("=" * 65)

# ── FIX: Reset stale leads if needed ─────────────────────────
pending_count = 0
try:
    r = requests.get(f"{supa_url}/rest/v1/leads?select=status&status=eq.pending&limit=1", headers=supa_headers, timeout=10)
    if r.status_code == 200:
        pending_count = len(r.json())
except Exception:
    pass

if pending_count == 0:
    print("\nFIXING: Resetting rate_limited leads to pending...")
    try:
        r = requests.patch(
            f"{supa_url}/rest/v1/leads?status=eq.rate_limited",
            headers={**supa_headers, 'Prefer': 'return=representation'},
            json={'status': 'pending'},
            timeout=15
        )
        if r.status_code in (200, 204):
            print(f"  Reset rate_limited leads to pending")
        # Also reset some rejected leads
        r2 = requests.patch(
            f"{supa_url}/rest/v1/leads?status=eq.failed",
            headers={**supa_headers, 'Prefer': 'return=representation'},
            json={'status': 'pending'},
            timeout=15
        )
        if r2.status_code in (200, 204):
            print(f"  Reset failed leads to pending")
    except Exception as e:
        print(f"  Error: {e}")

# ── FIX: Wake up bot if heartbeat stale ──────────────────────
hb_stale = not results.get("Bot Heartbeat", True)
if hb_stale:
    print("\nFIXING: Bot heartbeat stale - sending /resume command...")
    try:
        r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
            json={'chat_id': chat_id, 'text': '/resume'}, timeout=10)
        print(f"  /resume sent: {r.json().get('ok')}")
    except Exception as e:
        print(f"  Error: {e}")

print("\nCheckup complete!")
