"""
Convert HTML CV to PDF using Playwright - PERFECT MATCH!
Uses real Chromium browser to render HTML exactly as it appears
"""
import os
import asyncio

# Playwright is optional — only available when installed locally
try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


def generate_cv_from_html_playwright():
    """Generate PDF from HTML CV using Playwright.
    Returns None silently if Playwright is unavailable or called inside async context.
    Caller falls back to FPDF automatically.
    """
    if not HAS_PLAYWRIGHT:
        return None

    # Sync Playwright cannot run inside a running asyncio event loop
    try:
        loop = asyncio.get_running_loop()
        if loop and loop.is_running():
            return None  # Silent — caller uses FPDF
    except RuntimeError:
        pass  # No running loop — safe to proceed

    # Locate HTML CV
    html_path = os.path.abspath('Sam_Salameh_CV_Enhanced.html')
    if not os.path.exists(html_path):
        html_path = os.path.abspath('Sam_Salameh_CV.html')
    if not os.path.exists(html_path):
        return None

    # Output path
    is_cloud = os.getenv("RENDER") or os.getenv("RAILWAY") or os.getenv("HEROKU")
    pdf_dir = "/tmp/pdf_cache" if is_cloud else os.path.join(os.path.dirname(__file__), "..", "pdf_cache")
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, "Sam_Salameh_CV.pdf")

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
        return pdf_path
    except Exception:
        return None


if __name__ == "__main__":
    result = generate_cv_from_html_playwright()
    print(f"PDF: {result}")
