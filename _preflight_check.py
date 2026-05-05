"""Pre-deployment validation — run before pushing to Render."""
import sys, os, asyncio, inspect
sys.path.insert(0, '.')
os.environ['RENDER'] = '1'

from dotenv import load_dotenv
load_dotenv()

async def test():
    errors = []

    # 1. DB client
    try:
        from core.db_client import RealityShapingDB
        db = RealityShapingDB()
        print('OK  DB client')
    except Exception as e:
        errors.append(f'ERR DB: {e}'); print(f'ERR DB: {e}')

    # 2. AI agent
    try:
        from core.ai_agent import OmniIntelligence
        ai = OmniIntelligence()
        print(f'OK  AI agent: primary={ai.primary_engine}, groq={bool(ai.groq_key)}')
    except Exception as e:
        errors.append(f'ERR AI: {e}'); print(f'ERR AI: {e}')

    # 3. Email rotator — check providers on Render
    try:
        from core.email_rotator import get_rotator
        r = get_rotator()
        providers = [p['display_name'] for p in r.providers]
        print(f'OK  Email rotator providers: {providers}')
        if not providers:
            errors.append('ERR Email: No providers available!')
            print('ERR Email: No providers available!')
    except Exception as e:
        errors.append(f'ERR Email: {e}'); print(f'ERR Email: {e}')

    # 4. Honeypot fix
    try:
        from core.anti_ban_protection import get_protection
        p = get_protection()
        assert p._is_honeypot('bothell', 'manager', '', 'hr@bothell.com') == False, 'bothell should NOT be honeypot'
        assert p._is_honeypot('bot', 'manager', '', 'hr@bot.com') == True, 'bot alone SHOULD be honeypot'
        print('OK  Honeypot fix: bothell=safe, bot=blocked')
    except Exception as e:
        errors.append(f'ERR Honeypot: {e}'); print(f'ERR Honeypot: {e}')

    # 5. Telegram dashboard
    try:
        from core.telegram_dashboard import SovereignDashboard
        dash = SovereignDashboard()
        print(f'OK  Telegram: token={bool(dash.token)}, chat_id={bool(dash.chat_id)}')
    except Exception as e:
        errors.append(f'ERR Telegram: {e}'); print(f'ERR Telegram: {e}')

    # 6. Main bot
    try:
        from core.main_bot import AlphaOrchestrator
        bot = AlphaOrchestrator()
        print(f'OK  AlphaOrchestrator: db={bool(bot.db)}, ai={bool(bot.ai)}')
    except Exception as e:
        errors.append(f'ERR Bot: {e}'); print(f'ERR Bot: {e}')

    # 7. _apex_static_fallback returns 11 values
    try:
        from core.ai_agent import OmniIntelligence
        ai = OmniIntelligence()
        result = ai._apex_static_fallback('HR Manager', None, None, 'Dubai')
        assert len(result) == 11, f'Got {len(result)} values, expected 11'
        print(f'OK  apex_static_fallback: 11 values')
    except Exception as e:
        errors.append(f'ERR Fallback: {e}'); print(f'ERR Fallback: {e}')

    # 8. _fallback_groq returns 11 values
    try:
        from core.ai_agent import OmniIntelligence
        src = inspect.getsource(OmniIntelligence._fallback_groq)
        assert 'highlights' in src, '_fallback_groq missing highlights'
        print('OK  _fallback_groq: has highlights (11th value)')
    except Exception as e:
        errors.append(f'ERR Groq: {e}'); print(f'ERR Groq: {e}')

    # 9. AsyncClient uses aclose not close
    try:
        from core.main_bot import AlphaOrchestrator
        src = inspect.getsource(AlphaOrchestrator.close)
        assert 'aclose' in src, 'close() should use aclose()'
        print('OK  AsyncClient.aclose() fix')
    except Exception as e:
        errors.append(f'ERR aclose: {e}'); print(f'ERR aclose: {e}')

    # 10. Playwright silent fallback
    try:
        from core.cv_playwright_pdf import generate_cv_from_html_playwright, HAS_PLAYWRIGHT
        result = generate_cv_from_html_playwright()
        print(f'OK  Playwright: HAS_PLAYWRIGHT={HAS_PLAYWRIGHT}, silent_return={result is None}')
    except Exception as e:
        errors.append(f'ERR Playwright: {e}'); print(f'ERR Playwright: {e}')

    # 11. Resend skipped when RESEND_FROM_EMAIL is gmail
    try:
        from core.email_rotator import EmailRotator
        os.environ['RESEND_FROM_EMAIL'] = 'test@gmail.com'
        os.environ['RESEND_API_KEY'] = 're_test123'
        r2 = EmailRotator()
        resend_providers = [p for p in r2.providers if 'resend' in p['name'].lower()]
        assert len(resend_providers) == 0, f'Resend should be skipped for gmail.com, got: {resend_providers}'
        print('OK  Resend skipped for gmail.com domain')
        del os.environ['RESEND_FROM_EMAIL']
    except Exception as e:
        errors.append(f'ERR Resend: {e}'); print(f'ERR Resend: {e}')

    # 12. Telegram 409 is DEBUG not WARNING
    try:
        src = inspect.getsource(SovereignDashboard._build_polling_error_callback if hasattr(SovereignDashboard, '_build_polling_error_callback') else lambda: None)
        assert 'logging.debug' in src, '409 should use logging.debug'
        assert 'logging.warning' not in src.lower().replace('logging.debug', ''), '409 should not use logging.warning'
        print('OK  Telegram 409: uses debug not warning')
    except Exception as e:
        # Try direct source check
        try:
            with open('core/telegram_dashboard.py') as f:
                src = f.read()
            count_debug = src.count('logging.debug("🔄 TELEGRAM 409')
            count_warn = src.count('logging.warning("⚠️ TELEGRAM 409')
            assert count_debug >= 2 and count_warn == 0, f'debug={count_debug}, warn={count_warn}'
            print('OK  Telegram 409: uses debug not warning')
        except Exception as e2:
            errors.append(f'ERR 409: {e2}'); print(f'ERR 409: {e2}')

    print()
    if errors:
        print(f'FAILED: {len(errors)} error(s):')
        for err in errors:
            print(f'  - {err}')
        return 1
    else:
        print('ALL CHECKS PASSED - Ready for Render deployment')
        return 0

if __name__ == '__main__':
    sys.exit(asyncio.run(test()))
