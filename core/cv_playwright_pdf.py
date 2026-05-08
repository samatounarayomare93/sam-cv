"""
Convert HTML CV to PDF.
Priority: Playwright (best) → WeasyPrint (cloud-safe) → ReportLab fallback
"""
import os
import asyncio
import logging

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

try:
    import weasyprint
    HAS_WEASYPRINT = True
    # Suppress WeasyPrint CSS warnings — they spam the logs with hundreds of lines
    # for unsupported properties like box-shadow, print-color-adjust, etc.
    logging.getLogger("weasyprint").setLevel(logging.ERROR)
    logging.getLogger("weasyprint.css").setLevel(logging.ERROR)
    logging.getLogger("weasyprint.document").setLevel(logging.ERROR)
    logging.getLogger("weasyprint.html").setLevel(logging.ERROR)
    logging.getLogger("fontTools").setLevel(logging.ERROR)
except ImportError:
    HAS_WEASYPRINT = False


def _get_html_path() -> str | None:
    """Find Sam_Salameh_CV.html — check multiple locations."""
    candidates = [
        os.path.abspath('Sam_Salameh_CV.html'),
        os.path.join(os.path.dirname(__file__), '..', 'Sam_Salameh_CV.html'),
        '/opt/render/project/src/Sam_Salameh_CV.html',
    ]
    for path in candidates:
        path = os.path.normpath(path)
        if os.path.exists(path):
            logging.info(f"✅ [CV-HTML] Found: {path}")
            return path
    logging.warning("⚠️ [CV-HTML] Sam_Salameh_CV.html not found in any location")
    return None


def _get_pdf_output_path() -> str:
    is_cloud = os.getenv("RENDER") or os.getenv("RAILWAY") or os.getenv("HEROKU")
    pdf_dir = "/tmp/pdf_cache" if is_cloud else os.path.join(
        os.path.dirname(__file__), "..", "pdf_cache")
    os.makedirs(pdf_dir, exist_ok=True)
    return os.path.join(pdf_dir, "Sam_Salameh_CV.pdf")


def _get_html_content_and_path():
    """Get HTML content + a temp file path. Uses file if found, else embedded fallback."""
    import tempfile

    html_path = _get_html_path()
    if html_path:
        return html_path, False  # (path, is_temp)

    # Fallback: use embedded HTML
    try:
        from core.cv_html_embedded import CV_HTML
        tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.html',
                                          delete=False, encoding='utf-8')
        tmp.write(CV_HTML)
        tmp.close()
        logging.info(f"✅ [CV-HTML] Using embedded HTML → {tmp.name}")
        return tmp.name, True  # (path, is_temp)
    except ImportError:
        pass

    # Try relative import
    try:
        from cv_html_embedded import CV_HTML
        tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.html',
                                          delete=False, encoding='utf-8')
        tmp.write(CV_HTML)
        tmp.close()
        return tmp.name, True
    except ImportError:
        logging.error("❌ [CV-HTML] No HTML source available (file not found, embedded not found)")
        return None, False


def _run_playwright_sync() -> str | None:
    html_path, is_temp = _get_html_content_and_path()
    if not html_path:
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
        logging.warning(f"⚠️ [PLAYWRIGHT] Failed: {e}")
        return None
    finally:
        if is_temp and html_path and os.path.exists(html_path):
            try:
                os.unlink(html_path)
            except Exception:
                pass


def _run_weasyprint() -> str | None:
    """WeasyPrint: HTML→PDF without a browser. Works on Render."""
    html_path, is_temp = _get_html_content_and_path()
    if not html_path:
        return None
    pdf_path = _get_pdf_output_path()
    try:
        import weasyprint as _wp
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        base_url = f'file:///{os.path.dirname(html_path).replace(os.sep, "/")}/'
        _wp.HTML(string=html_content, base_url=base_url).write_pdf(pdf_path)
        size = os.path.getsize(pdf_path)
        logging.info(f"✅ [WEASYPRINT] PDF generated: {pdf_path} ({size:,} bytes)")
        return pdf_path
    except Exception as e:
        logging.warning(f"⚠️ [WEASYPRINT] Failed: {e}")
        return None
    finally:
        if is_temp and html_path and os.path.exists(html_path):
            try:
                os.unlink(html_path)
            except Exception:
                pass


def generate_cv_from_html_playwright() -> str | None:
    """
    Generate PDF from HTML CV.
    Tries: Playwright → WeasyPrint → None (caller falls back to ReportLab)
    """
    # ── Try Playwright ────────────────────────────────────────────────────
    if HAS_PLAYWRIGHT:
        try:
            loop = asyncio.get_running_loop()
            is_async = loop.is_running()
        except RuntimeError:
            is_async = False

        if is_async:
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(_run_playwright_sync)
                try:
                    result = future.result(timeout=60)
                    if result:
                        return result
                except Exception as e:
                    logging.warning(f"⚠️ [PLAYWRIGHT] Thread failed: {e}")
        else:
            result = _run_playwright_sync()
            if result:
                return result

    # ── Try WeasyPrint ────────────────────────────────────────────────────
    if HAS_WEASYPRINT:
        result = _run_weasyprint()
        if result:
            return result

    logging.warning("⚠️ [CV-PDF] Both Playwright and WeasyPrint unavailable — falling back to ReportLab")
    return None


async def generate_cv_from_html_playwright_async() -> str | None:
    if not (HAS_PLAYWRIGHT or HAS_WEASYPRINT):
        return None
    try:
        result = await asyncio.to_thread(_run_playwright_sync if HAS_PLAYWRIGHT else _run_weasyprint)
        return result
    except Exception as e:
        logging.warning(f"⚠️ [CV-PDF-ASYNC] Failed: {e}")
        return None


if __name__ == "__main__":
    result = generate_cv_from_html_playwright()
    print(f"PDF: {result}")
