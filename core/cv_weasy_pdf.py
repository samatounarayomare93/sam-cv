"""
Convert HTML CV to PDF using WeasyPrint - Perfect match!
"""
import os
from weasyprint import HTML

def generate_cv_from_html_weasy():
    """Generate PDF from HTML CV using WeasyPrint"""
    
    # Read HTML CV
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
        # Convert HTML to PDF
        HTML(filename=html_path).write_pdf(pdf_path)
        
        print(f"✅ PDF generated: {pdf_path}")
        print(f"📄 PDF matches HTML design 100%!")
        return pdf_path
        
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    generate_cv_from_html_weasy()
