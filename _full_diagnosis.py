"""
FULL SYSTEM DIAGNOSIS - checks everything and reports all issues
"""
import asyncio
import httpx
import os
import sys
import smtplib
import sqlite3
from dotenv import load_dotenv
load_dotenv()

ISSUES = []
FIXES_NEEDED = []

async def run_diagnosis():
    url = os.getenv('SUPABASE_URL', '')
    key = os.getenv('SUPABASE_KEY', '')
    h = {'apikey': key, 'Authorization': f'Bearer {key}'}

    print("=" * 60)
    print("  FULL SYSTEM DIAGNOSIS - Project Chronos")
    print("=" * 60)

    async with httpx.AsyncClient(timeout=15) as c:

        # ── 1. LEADS STATUS ──────────────────────────────────────────
        print("\n📊 LEADS IN DATABASE:")
        r = await c.get(url + '/rest/v1/leads?select=status&limit=1000', headers=h)
        if r.status_code == 200:
            from collections import Counter
            data = r.json()
            counts = Counter(l.get('status') for l in data)
            for status, count in sorted(counts.items(), key=lambda x: -x[1]):
                print(f"   {status}: {count}")
            print(f"   TOTAL: {len(data)}")
            
            pending = counts.get('pending', 0)
            if pending < 10:
                ISSUES.append(f"⚠️ Only {pending} pending leads - queue almost empty!")
                FIXES_NEEDED.append("INJECT MORE LEADS into Supabase")
        else:
            ISSUES.append(f"❌ Cannot read leads: {r.status_code}")

        # ── 2. APPLICATIONS STATUS ───────────────────────────────────
        print("\n📧 APPLICATIONS SENT:")
        r2 = await c.get(url + '/rest/v1/applications?select=status,timestamp&limit=500', headers=h)
        if r2.status_code == 200:
            apps = r2.json()
            from collections import Counter
            app_counts = Counter(a.get('status') for a in apps)
            for status, count in sorted(app_counts.items(), key=lambda x: -x[1]):
                print(f"   {status}: {count}")
            print(f"   TOTAL: {len(apps)}")
            
            # Check last application time
            if apps:
                last_ts = max(a.get('timestamp', '') for a in apps)
                print(f"   Last sent: {str(last_ts)[:19]}")
        else:
            ISSUES.append(f"❌ Cannot read applications: {r2.status_code}")

        # ── 3. BOT HEARTBEAT ─────────────────────────────────────────
        print("\n💓 BOT HEARTBEAT (is it running on Render?):")
        r3 = await c.get(url + '/rest/v1/system_settings?key=eq.active_bot_heartbeat&select=value', headers=h)
        if r3.status_code == 200 and r3.json():
            from datetime import datetime, timezone
            hb_str = r3.json()[0].get('value', '')
            try:
                hb = datetime.fromisoformat(hb_str.replace('Z', '+00:00'))
                now = datetime.now(timezone.utc)
                age = (now - hb).total_seconds()
                print(f"   Last heartbeat: {hb_str[:19]}")
                print(f"   Age: {age:.0f} seconds ago")
                if age < 120:
                    print("   Status: ✅ BOT IS ALIVE AND RUNNING ON RENDER!")
                elif age < 600:
                    print("   Status: 🟡 Bot was active recently (< 10 min)")
                    ISSUES.append(f"⚠️ Bot heartbeat is {age:.0f}s old - may be slow")
                else:
                    print(f"   Status: ❌ BOT MAY BE STOPPED (last seen {age/60:.0f} min ago)")
                    ISSUES.append(f"❌ Bot heartbeat is {age/60:.0f} minutes old - bot may be down!")
                    FIXES_NEEDED.append("RESTART bot on Render or redeploy")
            except Exception as e:
                print(f"   Parse error: {e}")
        else:
            ISSUES.append("❌ No heartbeat found - bot may never have started")

        # ── 4. PENDING LEADS DETAIL ──────────────────────────────────
        print("\n🎯 PENDING LEADS (next to be processed):")
        r4 = await c.get(url + '/rest/v1/leads?status=eq.pending&select=company_name,email,job_title,priority_score&order=priority_score.desc&limit=10', headers=h)
        if r4.status_code == 200:
            leads = r4.json()
            if leads:
                for l in leads:
                    company = l.get('company_name', '?')
                    email = l.get('email', 'NO EMAIL')
                    title = l.get('job_title', '?')
                    score = l.get('priority_score', 0)
                    print(f"   [{score}] {company} | {email} | {title}")
            else:
                print("   ⚠️ NO PENDING LEADS!")
                ISSUES.append("❌ No pending leads in queue - bot has nothing to process!")
                FIXES_NEEDED.append("Run _inject_leads.py to add leads")
        else:
            ISSUES.append(f"❌ Cannot read pending leads: {r4.status_code}")

    # ── 5. EMAIL PROVIDERS ───────────────────────────────────────────
    print("\n📬 EMAIL PROVIDERS:")
    
    # Zoho
    zoho_user = os.getenv('ZOHO_SMTP_USER', '')
    zoho_pass = os.getenv('ZOHO_APP_PASSWORD', '')
    if zoho_user and zoho_pass:
        try:
            with smtplib.SMTP('smtp.zoho.com', 587, timeout=10) as s:
                s.starttls()
                s.login(zoho_user, zoho_pass)
                print(f"   Zoho SMTP: ✅ OK ({zoho_user})")
        except Exception as e:
            print(f"   Zoho SMTP: ❌ FAIL - {e}")
            ISSUES.append(f"❌ Zoho SMTP failed: {e}")
    else:
        print("   Zoho SMTP: ⚠️ Not configured")

    # Gmail
    gmail_user = os.getenv('GMAIL_SMTP_USER', '')
    gmail_pass = os.getenv('GMAIL_APP_PASSWORD', '')
    if gmail_user and gmail_pass:
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10) as s:
                s.login(gmail_user, gmail_pass)
                print(f"   Gmail SMTP: ✅ OK ({gmail_user})")
        except Exception as e:
            print(f"   Gmail SMTP: ❌ FAIL - {e}")
            ISSUES.append(f"❌ Gmail SMTP failed: {e}")
    else:
        print("   Gmail SMTP: ⚠️ Not configured")

    # Brevo API
    brevo_key = os.getenv('BREVO_API_KEY', '')
    if brevo_key:
        try:
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.get('https://api.brevo.com/v3/account', headers={'api-key': brevo_key})
                if r.status_code == 200:
                    print(f"   Brevo API: ✅ OK")
                else:
                    print(f"   Brevo API: ❌ FAIL {r.status_code}")
                    ISSUES.append(f"❌ Brevo API failed: {r.status_code}")
        except Exception as e:
            print(f"   Brevo API: ❌ ERROR {e}")
    else:
        print("   Brevo API: ⚠️ Not configured")

    # ── 6. AI ENGINES ────────────────────────────────────────────────
    print("\n🧠 AI ENGINES:")
    
    groq_key = os.getenv('GROQ_API_KEY', '')
    if groq_key:
        try:
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.get('https://api.groq.com/openai/v1/models',
                               headers={'Authorization': f'Bearer {groq_key}'})
                if r.status_code == 200:
                    print("   Groq: ✅ OK (primary AI)")
                else:
                    print(f"   Groq: ❌ FAIL {r.status_code}")
                    ISSUES.append("❌ Groq AI not working - bot will use static templates")
        except Exception as e:
            print(f"   Groq: ❌ ERROR {e}")
    
    gemini_key = os.getenv('GEMINI_API_KEY', '')
    if gemini_key:
        try:
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.get(f'https://generativelanguage.googleapis.com/v1beta/models?key={gemini_key}')
                if r.status_code == 200:
                    print("   Gemini: ✅ OK")
                else:
                    print(f"   Gemini: ❌ FAIL {r.status_code} - API not enabled in Google Cloud")
                    ISSUES.append("⚠️ Gemini API disabled - using Groq as fallback (OK)")
        except Exception as e:
            print(f"   Gemini: ❌ ERROR {e}")

    # ── 7. LOCAL DB ──────────────────────────────────────────────────
    print("\n💾 LOCAL DATABASE (SQLite):")
    try:
        conn = sqlite3.connect('sam_ultimate.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM applications")
        count = cursor.fetchone()[0]
        print(f"   Applications in local DB: {count}")
        cursor.execute("SELECT company_name, status, timestamp FROM applications ORDER BY timestamp DESC LIMIT 5")
        rows = cursor.fetchall()
        for row in rows:
            print(f"   {row[0]} | {row[1]} | {str(row[2])[:16]}")
        conn.close()
    except Exception as e:
        print(f"   SQLite: ❌ ERROR {e}")
        ISSUES.append(f"❌ SQLite DB error: {e}")

    # ── 8. CRITICAL FILES ────────────────────────────────────────────
    print("\n📁 CRITICAL FILES:")
    critical_files = [
        'run.py', 'core/main_bot.py', 'core/smtp_engine.py',
        'core/db_client.py', 'core/ai_agent.py', 'core/pdf_generator.py',
        'core/telegram_dashboard.py', 'profile.json',
        'Sam_Salameh_CV.html', 'Sam_Salameh_CV.pdf',
        'requirements.txt', 'render.yaml', '.env'
    ]
    for f in critical_files:
        exists = os.path.exists(f)
        size = os.path.getsize(f) if exists else 0
        status = f"✅ ({size:,} bytes)" if exists else "❌ MISSING"
        print(f"   {f}: {status}")
        if not exists:
            ISSUES.append(f"❌ Critical file missing: {f}")

    # ── SUMMARY ──────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  DIAGNOSIS SUMMARY")
    print("=" * 60)
    
    if not ISSUES:
        print("\n✅ ALL SYSTEMS 100% WORKING - NO ISSUES FOUND!")
    else:
        print(f"\n⚠️ FOUND {len(ISSUES)} ISSUES:")
        for i, issue in enumerate(ISSUES, 1):
            print(f"   {i}. {issue}")
    
    if FIXES_NEEDED:
        print(f"\n🔧 FIXES NEEDED:")
        for fix in FIXES_NEEDED:
            print(f"   → {fix}")
    
    print("\n" + "=" * 60)
    return ISSUES

asyncio.run(run_diagnosis())
