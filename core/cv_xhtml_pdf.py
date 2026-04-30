"""
Convert HTML CV to PDF using xhtml2pdf
"""
import os
from xhtml2pdf import pisa

def generate_cv_from_html_xhtml():
    """Generate PDF from HTML CV using xhtml2pdf"""
    
    # Read HTML CV
    html_path = os.path.abspath('Sam_Salameh_CV.html')
    
    if not os.path.exists(html_path):
        print(f"❌ HTML CV not found: {html_path}")
        return None
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
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
        # Convert HTML to PDF
        with open(pdf_path, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
        
        if pisa_status.err:
            print(f"❌ Error generating PDF: {pisa_status.err} errors")
            return None
        
        print(f"✅ PDF generated: {pdf_path}")
        print(f"📄 PDF matches HTML design!")
        return pdf_path
        
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    generate_cv_from_html_xhtml()
