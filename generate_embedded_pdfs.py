"""
Run this ONCE locally to generate PDFs and embed them as base64 in core/embedded_pdfs.py
This file is then committed to GitHub so Render can use the PDFs without generating them.
"""
import os, sys, base64
sys.path.insert(0, os.path.dirname(__file__))
from dotenv import load_dotenv
load_dotenv()

print("Generating PDFs locally...")

from core.cv_pdf_full import generate_full_cv_pdf
from core.cover_letter_pdf import generate_cover_letter_pdf

cv_path = generate_full_cv_pdf()
cl_path = generate_cover_letter_pdf('Future Tech Industries', 'Lead Automation Engineer')

cv_b64  = base64.b64encode(open(cv_path,  'rb').read()).decode()
cl_b64  = base64.b64encode(open(cl_path,  'rb').read()).decode()

print(f"CV PDF:    {os.path.getsize(cv_path):,} bytes")
print(f"Cover Letter: {os.path.getsize(cl_path):,} bytes")

# Write the embedded module
out = f'''"""
Pre-generated PDF attachments embedded as base64.
Generated locally and committed to GitHub so Render can use them without
generating PDFs at runtime (avoids OOM on 512MB free tier).

To regenerate: python generate_embedded_pdfs.py
"""
import base64, os, tempfile

# CV PDF - Sam Salameh
_CV_PDF_B64 = """{cv_b64}"""

# Cover Letter PDF - generic template
_CL_PDF_B64 = """{cl_b64}"""


def get_cv_pdf_path() -> str:
    """Write the embedded CV PDF to /tmp and return the path."""
    path = "/tmp/Sam_Salameh_CV.pdf" if os.getenv("RENDER") or os.getenv("RAILWAY") else os.path.join(
        os.path.dirname(__file__), "..", "core", "pdf_cache", "Sam_Salameh_CV.pdf"
    )
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(base64.b64decode(_CV_PDF_B64))
    return path


def get_cover_letter_pdf_path(company_name: str = "Future Tech Industries",
                               job_title: str = "Lead Automation Engineer") -> str:
    """Write the embedded Cover Letter PDF to /tmp and return the path."""
    safe = "".join(c for c in company_name if c.isalnum() or c in " _-").strip().replace(" ", "_")[:30]
    path = f"/tmp/Cover_Letter_{{safe}}.pdf" if os.getenv("RENDER") or os.getenv("RAILWAY") else os.path.join(
        os.path.dirname(__file__), "..", "core", "pdf_cache", f"Cover_Letter_{{safe}}.pdf"
    )
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(base64.b64decode(_CL_PDF_B64))
    return path
'''

output_path = os.path.join(os.path.dirname(__file__), 'core', 'embedded_pdfs.py')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(out)

print(f"\n✅ Written to: {output_path}")
print(f"   Size: {os.path.getsize(output_path):,} bytes")
print("\nNow commit and push to GitHub!")
print("  git add core/embedded_pdfs.py")
print("  git commit -m 'feat: embed pre-generated PDFs for Render free tier'")
print("  git push origin main")
