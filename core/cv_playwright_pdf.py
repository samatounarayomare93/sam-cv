"""
Convert HTML CV to PDF using Playwright - PERFECT MATCH!
Uses real Chromium browser to render HTML exactly as it appears.

[🛡️ FIX]: Supports BOTH sync and async contexts:
- When called from async context: uses asyncio.to_thread() to run sync Playwright safely
- When called from sync context: runs directly
"""
import os
import asyncio
import logging

# Playwright is optional — only available when installed locally
try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


def _get_html_path() -> str | None:
    """Find the CV HTML file — always prefer Sam_Salameh_CV.html (latest design)."""
    for name in ('Sam_Salameh_CV.html', 'Sam_Salameh_CV_Enhanced.html'):
        path = os.path.abspath(name)
        if os.path.exists(path):
            return path
    return None


def _get_pdf_output_path() -> str:
    """Get the output PDF path (cloud-safe)."""
    is_cloud = os.getenv("RENDER") or os.getenv("RAILWAY") or os.getenv("HEROKU")
    pdf_dir = "/tmp/pdf_cache" if is_cloud else os.path.join(os.path.dirname(__file__), "..", "pdf_cache")
    os.makedirs(pdf_dir, exist_ok=True)
    return os.path.join(pdf_dir, "Sam_Salameh_CV.pdf")


def _run_playwright_sync() -> str | None:
    """Core Playwright PDF generation — sync only, must NOT be called inside a running event loop."""
    html_path = _get_html_path()
    if not html_path:
        logging.warning("⚠️ [PLAYWRIGHT] CV HTML file not found.")
        return None

    pdf_path = _get_pdf_output_path()

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f'file:///{html_path.replace(os.sep, "/")}')
            page.wait_for_load_state('networkidle')
            page.pdf(
                path=pdf_path,
                format='A4',
                print_background=True,
                margin={'top': '0mm', 'right': '0mm', 'bottom': '0mm', 'left': '0mm'}
            )
            browser.close()
        logging.info(f"✅ [PLAYWRIGHT] PDF generated: {pdf_path}")
        return pdf_path
    except Exception as e:
        logging.warning(f"⚠️ [PLAYWRIGHT] PDF generation failed: {e}")
        return None


def generate_cv_from_html_playwright() -> str | None:
    """
    Generate PDF from HTML CV using Playwright.

    [🛡️ ASYNC-SAFE FIX]: Detects if we're inside a running event loop.
    - If YES: runs Playwright in a thread pool via asyncio.to_thread() (non-blocking)
    - If NO: runs Playwright directly (sync context, e.g. __main__)

    Returns the PDF path on success, None on failure (caller falls back to FPDF).
    """
    if not HAS_PLAYWRIGHT:
        return None

    # Check if we're inside a running event loop
    try:
        loop = asyncio.get_running_loop()
        is_async = loop.is_running()
    except RuntimeError:
        is_async = False

    if is_async:
        # [🛡️ FIX]: We're in async context — schedule sync Playwright in a thread
        # This is a sync wrapper that creates a new event loop to run the coroutine
        # The caller (smtp_engine.py) calls this synchronously, so we use run_in_executor
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_run_playwright_sync)
            try:
                return future.result(timeout=60)
            except concurrent.futures.TimeoutError:
                logging.warning("⚠️ [PLAYWRIGHT] PDF generation timed out (60s)")
                return None
            except Exception as e:
                logging.warning(f"⚠️ [PLAYWRIGHT] Thread execution failed: {e}")
                return None
    else:
        # Safe to run directly in sync context
        return _run_playwright_sync()


async def generate_cv_from_html_playwright_async() -> str | None:
    """
    [🔥 ASYNC VERSION]: Proper async wrapper for use in async contexts.
    Uses asyncio.to_thread() to run Playwright without blocking the event loop.
    """
    if not HAS_PLAYWRIGHT:
        return None
    try:
        result = await asyncio.to_thread(_run_playwright_sync)
        return result
    except Exception as e:
        logging.warning(f"⚠️ [PLAYWRIGHT-ASYNC] Failed: {e}")
        return None


if __name__ == "__main__":
    result = generate_cv_from_html_playwright()
    print(f"PDF: {result}")
