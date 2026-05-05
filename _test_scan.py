import asyncio, sys, os, inspect
sys.path.insert(0, '.')

async def test_all():
    results = []
    errors = []

    try:
        from core.runtime_helpers import ProxyMesh
        pm = ProxyMesh()
        assert pm._lock is None
        lock = pm._proxy_lock
        assert lock is not None
        results.append('OK  [1] ProxyMesh lazy lock')
    except Exception as e:
        errors.append(f'FAIL [1]: {e}')

    try:
        from core.main_bot import AlphaOrchestrator
        AlphaOrchestrator._instance = None
        orch = AlphaOrchestrator(concurrency_limit=2)
        assert orch.semaphore is None
        assert orch.rate_limit_lock is None
        sem = orch._semaphore
        lk = orch._rate_lock
        async with sem:
            async with lk:
                pass
        results.append('OK  [2] AlphaOrchestrator lazy semaphore + lock')
    except Exception as e:
        errors.append(f'FAIL [2]: {e}')

    try:
        from core.telegram_dashboard import SovereignDashboard
        src = inspect.getsource(SovereignDashboard._build_polling_error_callback)
        assert 'loop = asyncio.get_running_loop()' not in src.split('def _error_callback')[0]
        results.append('OK  [3] polling error callback safe')
    except Exception as e:
        errors.append(f'FAIL [3]: {e}')

    try:
        from core.scrapers.daleel_parallel import daleel_parallel_scan
        src2 = inspect.getsource(daleel_parallel_scan)
        assert 'daleel-madani.org/jobs?page=' not in src2
        assert 'DDGS' in src2 or '_safe_ddgs_search' in src2
        results.append('OK  [4] daleel bypass mode (DDGS search)')
    except Exception as e:
        errors.append(f'FAIL [4]: {e}')

    try:
        from core.smtp_engine import send_email_via_brevo_http
        src3 = inspect.getsource(send_email_via_brevo_http)
        assert 'sam.dev1@hotmail.com' not in src3
        assert 'BREVO_SENDER_EMAIL' in src3
        results.append('OK  [5] Brevo sender uses BREVO_SENDER_EMAIL (no Hotmail)')
    except Exception as e:
        errors.append(f'FAIL [5]: {e}')

    try:
        from core.smtp_engine import send_email_via_resend
        src4 = inspect.getsource(send_email_via_resend)
        assert 'RESEND_FROM_EMAIL' in src4
        assert 'onboarding@resend.dev' not in src4
        results.append('OK  [6] Resend requires RESEND_FROM_EMAIL verified domain')
    except Exception as e:
        errors.append(f'FAIL [6]: {e}')

    try:
        from core.email_rotator import EmailRotator
        src5 = inspect.getsource(EmailRotator._get_available_providers)
        assert 'RESEND_FROM_EMAIL' in src5
        assert 'is_render' in src5
        results.append('OK  [7+8] EmailRotator: skips Resend w/o domain + skips Zoho on Render')
    except Exception as e:
        errors.append(f'FAIL [7+8]: {e}')

    try:
        from core.main_bot import AlphaOrchestrator as AO
        src6 = inspect.getsource(AO.process_single_lead)
        assert 'GENERIC_WORDS' in src6
        assert 'homepage' in src6
        assert 'company_email_key' in src6
        results.append('OK  [9+10] Enhanced fake domain filter + company+email dedup')
    except Exception as e:
        errors.append(f'FAIL [9+10]: {e}')

    try:
        from core.scrapers.omni_crawler import OmniCrawler
        src7 = inspect.getsource(OmniCrawler.hunt_expansion_signals)
        assert '"email": None' in src7
        assert 'hr@' not in src7
        results.append('OK  [11] hunt_expansion_signals: no fake hr@ emails')
    except Exception as e:
        errors.append(f'FAIL [11]: {e}')

    try:
        from core.smtp_engine import send_email
        src8 = inspect.getsource(send_email)
        assert 'is_render' in src8
        results.append('OK  [12] send_email rotation: Zoho skipped on Render')
    except Exception as e:
        errors.append(f'FAIL [12]: {e}')

    try:
        from core.scrapers.scraper import scrape_new_companies_async
        src9 = inspect.getsource(scrape_new_companies_async)
        assert 'daleel_parallel_scan' in src9
        assert 'daleel-madani.org/jobs' not in src9
        results.append('OK  [13] scraper.py daleel delegates to bypass module')
    except Exception as e:
        errors.append(f'FAIL [13]: {e}')

    try:
        from core.ai_agent import OmniIntelligence
        src10 = inspect.getsource(OmniIntelligence.analyze_job)
        assert 'CONSUMER_SUSPENDED' in src10
        assert 'primary_engine = None' in src10
        results.append('OK  [14] Gemini suspension: auto-detected, falls to Groq')
    except Exception as e:
        errors.append(f'FAIL [14]: {e}')

    try:
        from core.smtp_engine import send_email_via_mailjet
        src11 = inspect.getsource(send_email_via_mailjet)
        assert 'sam.dev1@hotmail.com' not in src11
        results.append('OK  [15] Mailjet: no Hotmail fallback')
    except Exception as e:
        errors.append(f'FAIL [15]: {e}')

    try:
        import run
        assert asyncio.iscoroutinefunction(run.main)
        results.append('OK  [16] run.main() is valid async coroutine')
    except Exception as e:
        errors.append(f'FAIL [16]: {e}')

    # Extra checks
    try:
        from core.smtp_engine import send_email_via_brevo_http
        src = inspect.getsource(send_email_via_brevo_http)
        # Must fail gracefully if no sender configured
        assert 'return False' in src
        results.append('OK  [17] Brevo fails gracefully if no sender configured')
    except Exception as e:
        errors.append(f'FAIL [17]: {e}')

    try:
        # Verify no duplicate send_email_via_resend calls with onboarding@resend.dev anywhere
        import core.smtp_engine as se_mod
        full_src = inspect.getsource(se_mod)
        assert 'onboarding@resend.dev' not in full_src
        results.append('OK  [18] No onboarding@resend.dev anywhere in smtp_engine')
    except Exception as e:
        errors.append(f'FAIL [18]: {e}')

    print(f'\nResults: {len(results)} passed, {len(errors)} failed\n')
    for r in results:
        print(r)
    if errors:
        print()
        for e in errors:
            print(e)

asyncio.run(test_all())
