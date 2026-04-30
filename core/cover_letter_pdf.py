"""
Generate Cover Letter PDF using Playwright
"""
import os
from playwright.sync_api import sync_playwright
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def generate_cover_letter_pdf(company_name, job_title, hiring_manager="Hiring Manager"):
    """Generate cover letter PDF from HTML"""
    
    # Import the generator
    from generate_cover_letter import generate_cover_letter
    
    # Generate HTML content
    html_content = generate_cover_letter(company_name, job_title, hiring_manager)
    
    # Create temp HTML file
    temp_html = "temp_cover_letter.html"
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Output PDF path
    is_cloud = os.getenv("RENDER") or os.getenv("RAILWAY") or os.getenv("HEROKU")
    if is_cloud:
        pdf_dir = "/tmp/pdf_cache"
    else:
        pdf_dir = os.path.join(os.path.dirname(__file__), "..", "core", "pdf_cache")
    
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir, exist_ok=True)
    
    pdf_path = os.path.join(pdf_dir, f"Cover_Letter_{company_name.replace(' ', '_')}.pdf")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            
            # Load HTML
            page.goto(f'file:///{os.path.abspath(temp_html).replace(os.sep, "/")}')
            page.wait_for_load_state('networkidle')
            
            # Generate PDF
            page.pdf(
                path=pdf_path,
                format='A4',
                print_background=True,
                margin={
                    'top': '10mm',
                    'right': '15mm',
                    'bottom': '10mm',
                    'left': '15mm'
                }
            )
            
            browser.close()
        
        # Clean up temp file
        if os.path.exists(temp_html):
            os.remove(temp_html)
        
        print(f"✅ Cover Letter PDF generated: {pdf_path}")
        return pdf_path
        
    except Exception as e:
        print(f"❌ Error generating cover letter PDF: {e}")
        # Clean up temp file
        if os.path.exists(temp_html):
            os.remove(temp_html)
        return None

if __name__ == "__main__":
    generate_cover_letter_pdf("Future Tech Industries", "Lead Automation Engineer")
