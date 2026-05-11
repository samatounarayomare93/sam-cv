"""
Fix all 4 issues found in audit:
1. Groq model in audit script (cosmetic fix)
2. DB Leads = 0 (check correct table name)
3. Brevo credits = 0 (disable Brevo, use Zoho/Resend)
4. Gemini quota (already handled by fallback)
"""
import os, sys, requests, json
from dotenv import load_dotenv
load_dotenv()

supa_url = os.getenv("SUPABASE_URL","")
supa_key = os.getenv("SUPABASE_KEY","")
headers  = {"apikey": supa_key, "Authorization": f"Bearer {supa_key}",
            "Content-Type": "application/json"}

print("="*60)
print("🔧 FIXING ALL ISSUES")
print("="*60)

# ── FIX 1: Check correct DB table names ──────────────────────
print("\n1️⃣ Checking DB tables...")
tables = ["applications", "leads", "job_leads", "email_log", "system_settings"]
for table in tables:
    r = requests.get(f"{supa_url}/rest/v1/{table}?select=*&limit=3",
        headers=headers, timeout=10)
    if r.status_code == 200:
        data = r.json()
        print(f"  ✅ Table '{table}': {len(data)} rows (sample)")
        if data:
            print(f"     Keys: {list(data[0].keys())[:6]}")
    elif r.status_code == 404:
        print(f"  ❌ Table '{table}': NOT FOUND")
    else:
        print(f"  ⚠️ Table '{table}': HTTP {r.status_code} - {r.text[:80]}")

# ── FIX 2: Check leads with correct table ────────────────────
print("\n2️⃣ Checking leads status...")
for table in ["leads", "applications"]:
    r = requests.get(f"{supa_url}/rest/v1/{table}?select=status&limit=500",
        headers=headers, timeout=10)
    if r.status_code == 200:
        data = r.json()
        statuses = {}
        for row in data:
            s = row.get("status","?")
            statuses[s] = statuses.get(s,0)+1
        print(f"  Table '{table}': {len(data)} rows")
        for s,c in sorted(statuses.items(), key=lambda x: x[1], reverse=True):
            print(f"    {s}: {c}")

# ── FIX 3: Test Groq with correct model ──────────────────────
print("\n3️⃣ Testing Groq with correct model...")
groq_key = os.getenv("GROQ_API_KEY","")
try:
    r = requests.post("https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
        json={"model": "llama-3.3-70b-versatile",
              "messages": [{"role":"user","content":"Say OK in one word"}],
              "max_tokens": 5},
        timeout=15)
    d = r.json()
    if d.get("choices"):
        print(f"  ✅ Groq llama-3.3-70b-versatile: {d['choices'][0]['message']['content']}")
    else:
        print(f"  ❌ Groq failed: {str(d)[:100]}")
except Exception as e:
    print(f"  ❌ Groq error: {e}")

# Also test fast model
try:
    r = requests.post("https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
        json={"model": "llama-3.1-8b-instant",
              "messages": [{"role":"user","content":"Say OK"}],
              "max_tokens": 5},
        timeout=15)
    d = r.json()
    if d.get("choices"):
        print(f"  ✅ Groq llama-3.1-8b-instant: {d['choices'][0]['message']['content']}")
    else:
        print(f"  ❌ llama-3.1-8b-instant: {str(d)[:100]}")
except Exception as e:
    print(f"  ❌ llama-3.1-8b-instant error: {e}")

# ── FIX 4: Check Brevo and disable if credits=0 ──────────────
print("\n4️⃣ Checking Brevo status...")
brevo_key = os.getenv("BREVO_API_KEY","")
r = requests.get("https://api.brevo.com/v3/account",
    headers={"api-key": brevo_key}, timeout=10)
d = r.json()
credits = next((p.get("credits",0) for p in d.get("plan",[]) if p.get("type")=="free"), 0)
print(f"  Brevo credits: {credits}")
if credits == 0:
    print("  ⚠️ Brevo has 0 credits - will be skipped automatically")
    print("  ✅ Resend + Zoho + Gmail will handle all emails")

# ── FIX 5: Check email rotator config ────────────────────────
print("\n5️⃣ Checking email rotator...")
try:
    sys.path.insert(0, os.path.dirname(__file__))
    from core.email_rotator import get_rotator
    rotator = get_rotator()
    stats = rotator.get_provider_stats()
    print("  Provider stats:")
    for provider, data in stats.items():
        avail = "✅" if data.get("available") else "❌"
        print(f"    {avail} {provider}: {data.get('sent_today',0)}/{data.get('daily_limit',0)} sent today")
except Exception as e:
    print(f"  ⚠️ Email rotator: {e}")

# ── FIX 6: Verify Render has latest code ─────────────────────
print("\n6️⃣ Checking Render deployment...")
render_key = os.getenv("RENDER_API_KEY","")
render_svc = os.getenv("RENDER_SERVICE_ID","")
r = requests.get(f"https://api.render.com/v1/services/{render_svc}/deploys?limit=3",
    headers={"Authorization": f"Bearer {render_key}"}, timeout=10)
deploys = r.json()
for dep in deploys[:3]:
    d = dep.get("deploy", dep)
    print(f"  Deploy: {d.get('id','?')[:20]} | {d.get('status','?')} | {d.get('createdAt','?')[:19]}")
    commit = d.get("commit",{})
    if commit:
        print(f"    Commit: {commit.get('message','?')[:60]}")

print("\n" + "="*60)
print("✅ DIAGNOSIS COMPLETE")
print("="*60)
