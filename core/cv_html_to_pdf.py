"""
Convert HTML CV to PDF - Exact match!
Uses pdfkit (wkhtmltopdf) to convert HTML to PDF with perfect styling
"""
import os
import sys

def generate_cv_from_html():
    """Generate PDF from HTML CV file"""
    
    # Check if wkhtmltopdf is installed
    try:
        import pdfkit
    except ImportError:
        print("❌ pdfkit not installed. Installing...")
        os.system(f"{sys.executable} -m pip install pdfkit")
        import pdfkit
    
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
    
    # PDF options for better quality
    options = {
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None,
        'print-media-type': None
    }
    
    try:
        # Try to find wkhtmltopdf
        config = None
        
        # Common Windows paths
        possible_paths = [
            r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe',
            r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe',
            r'C:\wkhtmltopdf\bin\wkhtmltopdf.exe'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                config = pdfkit.configuration(wkhtmltopdf=path)
                break
        
        # Convert HTML to PDF
        pdfkit.from_file(html_path, pdf_path, options=options, configuration=config)
        
        print(f"✅ PDF generated: {pdf_path}")
        return pdf_path
        
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        print("\n⚠️ wkhtmltopdf not found!")
        print("Download from: https://wkhtmltopdf.org/downloads.html")
        print("Or use the FPDF version instead")
        return None

if __name__ == "__main__":
    generate_cv_from_html()
