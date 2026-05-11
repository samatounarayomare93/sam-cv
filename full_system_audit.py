"""
Full system audit - checks every service with its actual API/token
"""
import os, sys, requests, smtplib, ssl, json
from dotenv import load_dotenv
load_dotenv()

results = {}

def check(name, ok, detail=""):
    icon = "✅" if ok else "❌"
    results[name] = ok
    print(f"  {icon} {name}: {detail}")

print("\n" + "="*60)
print("🔍 FULL SYSTEM AUDIT")
print("="*60)

# ── 1. TELEGRAM ──────────────────────────────────────────────
print("\n📱 TELEGRAM:")
token = os.getenv("TELEGRAM_BOT_TOKEN","")
chat_id = os.getenv("TELEGRAM_CHAT_ID","")
try:
    r = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10)
    d = r.json()
    if d.get("ok"):
        check("Bot Token", True, f"@{d['result']['username']} (id:{d['result']['id']})")
    else:
        check("Bot Token", False, d.get("description",""))
except Exception as e:
    check("Bot Token", False, str(e)[:60])

try:
    r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": "🔍 System audit ping - all good!"}, timeout=10)
    d = r.json()
    check("Send Message", d.get("ok"), f"chat_id={chat_id}")
except Exception as e:
    check("Send Message", False, str(e)[:60])

# ── 2. RESEND ─────────────────────────────────────────────────
print("\n📧 RESEND API:")
resend_key = os.getenv("RESEND_API_KEY","")
try:
    r = requests.post("https://api.resend.com/emails",
        headers={"Authorization": f"Bearer {resend_key}", "Content-Type": "application/json"},
        json={"from": "Sam Salameh <onboarding@resend.dev>",
              "to": ["samsalameh.cv@gmail.com"],
              "subject": "✅ Audit Test - Resend Working",
              "html": "<h2>✅ Resend API is working!</h2>"},
        timeout=15)
    d = r.json()
    if d.get("id"):
        check("Resend Send", True, f"ID: {d['id'][:20]}...")
    else:
        check("Resend Send", False, str(d)[:80])
except Exception as e:
    check("Resend Send", False, str(e)[:60])

# ── 3. BREVO ──────────────────────────────────────────────────
print("\n📧 BREVO:")
brevo_key = os.getenv("BREVO_API_KEY","")
try:
    r = requests.get("https://api.brevo.com/v3/account",
        headers={"api-key": brevo_key}, timeout=10)
    d = r.json()
    credits = next((p.get("credits",0) for p in d.get("plan",[]) if p.get("type")=="free"), 0)
    check("Brevo Account", r.status_code==200, f"email={d.get('email')} credits={credits}")
    check("Brevo Credits", credits > 0, f"{credits} remaining")
except Exception as e:
    check("Brevo Account", False, str(e)[:60])

# Brevo SMTP
brevo_login = os.getenv("BREVO_SMTP_LOGIN","")
brevo_pass  = os.getenv("BREVO_SMTP_PASSWORD","")
try:
    with smtplib.SMTP("smtp-relay.brevo.com", 587, timeout=10) as s:
        s.ehlo(); s.starttls(); s.ehlo()
        s.login(brevo_login, brevo_pass)
    check("Brevo SMTP", True, f"{brevo_login}")
except Exception as e:
    check("Brevo SMTP", False, str(e)[:60])

# ── 4. ZOHO ───────────────────────────────────────────────────
print("\n📧 ZOHO:")
zoho1_user = os.getenv("ZOHO_SMTP_USER","")
zoho1_pass = os.getenv("ZOHO_APP_PASSWORD","")
try:
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.zoho.com", 465, context=ctx, timeout=10) as s:
        s.login(zoho1_user, zoho1_pass)
    check("Zoho Account 1", True, zoho1_user)
except Exception as e:
    check("Zoho Account 1", False, str(e)[:60])

zoho2_user = os.getenv("ZOHO_SMTP_USER_2","")
zoho2_pass = os.getenv("ZOHO_APP_PASSWORD_2","")
try:
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.zoho.com", 465, context=ctx, timeout=10) as s:
        s.login(zoho2_user, zoho2_pass)
    check("Zoho Account 2", True, zoho2_user)
except Exception as e:
    check("Zoho Account 2", False, str(e)[:60])

# ── 5. GMAIL ──────────────────────────────────────────────────
print("\n📧 GMAIL:")
gmail_user = os.getenv("GMAIL_SMTP_USER","")
gmail_pass = os.getenv("GMAIL_APP_PASSWORD","")
try:
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx, timeout=10) as s:
        s.login(gmail_user, gmail_pass)
    check("Gmail SMTP", True, gmail_user)
except Exception as e:
    check("Gmail SMTP", False, str(e)[:60])

# ── 6. SUPABASE ───────────────────────────────────────────────
print("\n💾 SUPABASE:")
supa_url = os.getenv("SUPABASE_URL","")
supa_key = os.getenv("SUPABASE_KEY","")
try:
    r = requests.get(f"{supa_url}/rest/v1/system_settings?select=key,value",
        headers={"apikey": supa_key, "Authorization": f"Bearer {supa_key}"}, timeout=10)
    if r.status_code == 200:
        data = r.json()
        settings = {s["key"]: s["value"] for s in data}
        check("Supabase DB", True, f"{len(data)} settings rows")
        check("Kill Switch", settings.get("kill_switch","?") == "false",
              f"kill_switch={settings.get('kill_switch','?')}")
    else:
        check("Supabase DB", False, f"HTTP {r.status_code}")
except Exception as e:
    check("Supabase DB", False, str(e)[:60])

# Check leads count
try:
    r = requests.get(f"{supa_url}/rest/v1/leads?select=status&limit=500",
        headers={"apikey": supa_key, "Authorization": f"Bearer {supa_key}"}, timeout=10)
    total = len(r.json()) if r.status_code == 200 else 0
    statuses = {}
    for row in (r.json() if r.status_code==200 else []):
        s = row.get("status","?")
        statuses[s] = statuses.get(s,0)+1
    check("DB Leads", total > 0, f"total={total} | " + " | ".join(f"{k}={v}" for k,v in list(statuses.items())[:4]))
except Exception as e:
    check("DB Leads", False, str(e)[:60])

# ── 7. RENDER ─────────────────────────────────────────────────
print("\n☁️ RENDER:")
render_key = os.getenv("RENDER_API_KEY","")
render_svc = os.getenv("RENDER_SERVICE_ID","")
try:
    r = requests.get(f"https://api.render.com/v1/services/{render_svc}",
        headers={"Authorization": f"Bearer {render_key}"}, timeout=15)
    d = r.json()
    suspended = d.get("suspended","?")
    url = d.get("serviceDetails",{}).get("url","?")
    check("Render API Key", r.status_code==200, f"service={d.get('name','?')}")
    check("Render Service", suspended=="not_suspended", f"url={url}")
except Exception as e:
    check("Render API Key", False, str(e)[:60])

# Check service is responding
try:
    r = requests.get("https://sam-job-automator.onrender.com", timeout=15)
    check("Render Live URL", r.status_code==200, f"HTTP {r.status_code}")
except Exception as e:
    check("Render Live URL", False, str(e)[:60])

# Check latest deploy
try:
    r = requests.get(f"https://api.render.com/v1/services/{render_svc}/deploys?limit=1",
        headers={"Authorization": f"Bearer {render_key}"}, timeout=10)
    deploys = r.json()
    if deploys:
        dep = deploys[0].get("deploy", deploys[0])
        status = dep.get("status","?")
        created = dep.get("createdAt","?")[:19]
        check("Latest Deploy", status=="live", f"status={status} at {created}")
except Exception as e:
    check("Latest Deploy", False, str(e)[:60])

# ── 8. GITHUB ─────────────────────────────────────────────────
print("\n🐙 GITHUB:")
github_pat = os.getenv("GITHUB_PAT","")
try:
    r = requests.get("https://api.github.com/user",
        headers={"Authorization": f"token {github_pat}",
                 "Accept": "application/vnd.github.v3+json"}, timeout=10)
    d = r.json()
    if r.status_code == 200:
        check("GitHub PAT", True, f"user={d.get('login')} scopes OK")
    else:
        check("GitHub PAT", False, d.get("message","")[:60])
except Exception as e:
    check("GitHub PAT", False, str(e)[:60])

# ── 9. AI SERVICES ────────────────────────────────────────────
print("\n🧠 AI SERVICES:")
groq_key = os.getenv("GROQ_API_KEY","")
try:
    r = requests.post("https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
        json={"model": "llama-3.3-70b-versatile", "messages": [{"role":"user","content":"Say OK"}],
              "max_tokens": 5},
        timeout=15)
    d = r.json()
    if d.get("choices"):
        check("Groq API", True, f"model=llama-3.3-70b response={d['choices'][0]['message']['content'][:20]}")
    else:
        check("Groq API", False, str(d)[:80])
except Exception as e:
    check("Groq API", False, str(e)[:60])

gemini_key = os.getenv("GEMINI_API_KEY","")
try:
    r = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_key}",
        json={"contents": [{"parts": [{"text": "Say OK"}]}]}, timeout=15)
    d = r.json()
    if d.get("candidates"):
        check("Gemini API", True, d["candidates"][0]["content"]["parts"][0]["text"][:20])
    else:
        err = d.get("error",{}).get("message","")[:60]
        check("Gemini API", False, err)
except Exception as e:
    check("Gemini API", False, str(e)[:60])

# ── 10. EMBEDDED PDFs ─────────────────────────────────────────
print("\n📄 EMBEDDED PDFs:")
try:
    sys.path.insert(0, os.path.dirname(__file__))
    from core.embedded_pdfs import get_cv_pdf_path, get_cover_letter_pdf_path
    cv = get_cv_pdf_path()
    cl = get_cover_letter_pdf_path("Test Co","Engineer")
    check("CV PDF", cv and os.path.exists(cv), f"{os.path.getsize(cv):,} bytes" if cv and os.path.exists(cv) else "missing")
    check("Cover Letter PDF", cl and os.path.exists(cl), f"{os.path.getsize(cl):,} bytes" if cl and os.path.exists(cl) else "missing")
except Exception as e:
    check("Embedded PDFs", False, str(e)[:60])

# ── SUMMARY ───────────────────────────────────────────────────
print("\n" + "="*60)
passed = sum(1 for v in results.values() if v)
total  = len(results)
print(f"📊 RESULT: {passed}/{total} checks passed")
failed = [k for k,v in results.items() if not v]
if failed:
    print(f"❌ FAILED: {', '.join(failed)}")
else:
    print("🎉 ALL SYSTEMS OPERATIONAL!")
print("="*60)
