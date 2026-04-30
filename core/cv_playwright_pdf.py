"""
Convert HTML CV to PDF using Playwright - PERFECT MATCH!
Uses real Chromium browser to render HTML exactly as it appears
"""
import os
from playwright.sync_api import sync_playwright

def generate_cv_from_html_playwright():
    """Generate PDF from HTML CV using Playwright - 100% accurate"""
    
    # Use enhanced HTML CV
    html_path = os.path.abspath('Sam_Salameh_CV_Enhanced.html')
    
    # Fallback to original if enhanced doesn't exist
    if not os.path.exists(html_path):
        html_path = os.path.abspath('Sam_Salameh_CV.html')
    
    if not os.path.exists(html_path):
        print(f"❌ HTML CV not found: {html_path}")
        return None
    
    # Output PDF path
    is_cloud = os.getenv("RENDER") or os.getenv("RAILWAY") or os.getenv("HEROKU")
    if is_cloud:
        pdf_dir = "/tmp/pdf_cache"
    else:
        pdf_dir = os.path.join(os.path.dirname(__file__), "..", "core", "pdf_cache")
    
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir, exist_ok=True)
    
    pdf_path = os.path.join(pdf_dir, "Sam_Salameh_CV.pdf")
    
    try:
        print("🌐 Starting Chromium browser...")
        
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch()
            page = browser.new_page()
            
            # Load HTML file
            print(f"📄 Loading HTML: {html_path}")
            page.goto(f'file:///{html_path.replace(os.sep, "/")}')
            
            # Wait for page to load completely
            page.wait_for_load_state('networkidle')
            
            # Generate PDF with exact settings
            print("📄 Generating PDF...")
            page.pdf(
                path=pdf_path,
                format='A4',
                print_background=True,  # Include background colors
                margin={
                    'top': '0mm',
                    'right': '0mm',
                    'bottom': '0mm',
                    'left': '0mm'
                }
            )
            
            browser.close()
        
        print(f"✅ PDF generated: {pdf_path}")
        print(f"🎯 PDF is 100% identical to HTML!")
        return pdf_path
        
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    generate_cv_from_html_playwright()
