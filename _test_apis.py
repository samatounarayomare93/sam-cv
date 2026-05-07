"""Test all critical API connections."""
import asyncio, httpx, os
from dotenv import load_dotenv
load_dotenv()

async def test_all():
    results = {}
    
    # Test Brevo
    key = os.getenv('BREVO_API_KEY', '')
    if key:
        try:
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.get('https://api.brevo.com/v3/account', headers={'api-key': key})
                if r.status_code == 200:
                    d = r.json()
                    email = d.get('email', '?')
                    print(f'BREVO: ✅ OK - Account: {email}')
                    results['brevo'] = True
                else:
                    print(f'BREVO: ❌ FAIL {r.status_code} - {r.text[:100]}')
                    results['brevo'] = False
        except Exception as e:
            print(f'BREVO: ❌ ERROR {e}')
            results['brevo'] = False
    else:
        print('BREVO: ⚠️ KEY NOT SET')
        results['brevo'] = False

    # Test Telegram
    token = os.getenv('TELEGRAM_BOT_TOKEN', '')
    if token:
        try:
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.get(f'https://api.telegram.org/bot{token}/getMe')
                if r.status_code == 200:
                    d = r.json()
                    username = d.get('result', {}).get('username', '?')
                    print(f'TELEGRAM: ✅ OK - Bot: @{username}')
                    results['telegram'] = True
                else:
                    print(f'TELEGRAM: ❌ FAIL {r.status_code}')
                    results['telegram'] = False
        except Exception as e:
            print(f'TELEGRAM: ❌ ERROR {e}')
            results['telegram'] = False
    else:
        print('TELEGRAM: ⚠️ TOKEN NOT SET')
        results['telegram'] = False

    # Test Gemini
    gemini_key = os.getenv('GEMINI_API_KEY', '')
    if gemini_key:
        try:
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.get(f'https://generativelanguage.googleapis.com/v1beta/models?key={gemini_key}')
                if r.status_code == 200:
                    print('GEMINI: ✅ OK - API working')
                    results['gemini'] = True
                else:
                    print(f'GEMINI: ❌ FAIL {r.status_code} - {r.text[:150]}')
                    results['gemini'] = False
        except Exception as e:
            print(f'GEMINI: ❌ ERROR {e}')
            results['gemini'] = False
    else:
        print('GEMINI: ⚠️ KEY NOT SET')
        results['gemini'] = False

    # Test Groq
    groq_key = os.getenv('GROQ_API_KEY', '')
    if groq_key:
        try:
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.get('https://api.groq.com/openai/v1/models',
                                headers={'Authorization': f'Bearer {groq_key}'})
                if r.status_code == 200:
                    print('GROQ: ✅ OK - API working')
                    results['groq'] = True
                else:
                    print(f'GROQ: ❌ FAIL {r.status_code}')
                    results['groq'] = False
        except Exception as e:
            print(f'GROQ: ❌ ERROR {e}')
            results['groq'] = False
    else:
        print('GROQ: ⚠️ KEY NOT SET')
        results['groq'] = False

    # Test Supabase
    sb_url = os.getenv('SUPABASE_URL', '')
    sb_key = os.getenv('SUPABASE_KEY', '')
    if sb_url and sb_key:
        try:
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.get(
                    f'{sb_url}/rest/v1/applications?limit=1',
                    headers={'apikey': sb_key, 'Authorization': f'Bearer {sb_key}'}
                )
                if r.status_code in (200, 206):
                    print('SUPABASE: ✅ OK - Database connected')
                    results['supabase'] = True
                else:
                    print(f'SUPABASE: ❌ FAIL {r.status_code}')
                    results['supabase'] = False
        except Exception as e:
            print(f'SUPABASE: ❌ ERROR {e}')
            results['supabase'] = False
    else:
        print('SUPABASE: ⚠️ NOT CONFIGURED')
        results['supabase'] = False

    # Test Render API
    render_key = os.getenv('RENDER_API_KEY', '')
    render_svc = os.getenv('RENDER_SERVICE_ID', '')
    if render_key and render_svc:
        try:
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.get(
                    f'https://api.render.com/v1/services/{render_svc}',
                    headers={'Authorization': f'Bearer {render_key}'}
                )
                if r.status_code == 200:
                    d = r.json()
                    svc = d.get('service', d)
                    name = svc.get('name', '?')
                    status = svc.get('suspended', 'unknown')
                    print(f'RENDER: ✅ OK - Service: {name} | Suspended: {status}')
                    results['render'] = True
                else:
                    print(f'RENDER: ❌ FAIL {r.status_code} - {r.text[:100]}')
                    results['render'] = False
        except Exception as e:
            print(f'RENDER: ❌ ERROR {e}')
            results['render'] = False
    else:
        print('RENDER: ⚠️ API KEY NOT SET')
        results['render'] = False

    # Test Zoho SMTP connectivity
    zoho_user = os.getenv('ZOHO_SMTP_USER', '')
    zoho_pass = os.getenv('ZOHO_APP_PASSWORD', '')
    if zoho_user and zoho_pass:
        try:
            import smtplib
            with smtplib.SMTP('smtp.zoho.com', 587, timeout=10) as s:
                s.starttls()
                s.login(zoho_user, zoho_pass)
                print(f'ZOHO SMTP: ✅ OK - Login successful')
                results['zoho'] = True
        except Exception as e:
            print(f'ZOHO SMTP: ❌ FAIL - {e}')
            results['zoho'] = False
    else:
        print('ZOHO SMTP: ⚠️ NOT CONFIGURED')
        results['zoho'] = False

    # Test Gmail SMTP
    gmail_user = os.getenv('GMAIL_SMTP_USER', '')
    gmail_pass = os.getenv('GMAIL_APP_PASSWORD', '')
    if gmail_user and gmail_pass:
        try:
            import smtplib
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10) as s:
                s.login(gmail_user, gmail_pass)
                print(f'GMAIL SMTP: ✅ OK - Login successful')
                results['gmail'] = True
        except Exception as e:
            print(f'GMAIL SMTP: ❌ FAIL - {e}')
            results['gmail'] = False
    else:
        print('GMAIL SMTP: ⚠️ NOT CONFIGURED')
        results['gmail'] = False

    print()
    print('=' * 50)
    ok = sum(1 for v in results.values() if v)
    total = len(results)
    print(f'TOTAL: {ok}/{total} services working')
    if ok == total:
        print('STATUS: ✅ ALL SYSTEMS GO - 100% READY')
    elif ok >= total * 0.7:
        print('STATUS: 🟡 MOSTLY WORKING - Minor issues')
    else:
        print('STATUS: ❌ CRITICAL ISSUES - Needs fixing')
    
    return results

asyncio.run(test_all())
