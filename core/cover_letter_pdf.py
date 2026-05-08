"""
Generate Cover Letter PDF - FPDF2 (works on Render without browser)
Simple, reliable, no custom fonts needed.
"""
import os
import sys
import logging
import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _get_pdf_dir():
    is_cloud = (os.getenv("RENDER") or os.getenv("RAILWAY") or
                os.getenv("HEROKU") or os.getenv("RENDER_EXTERNAL_URL") or
                os.getenv("RENDER_SERVICE_ID"))
    if is_cloud:
        pdf_dir = "/tmp/pdf_cache"
    else:
        pdf_dir = os.path.join(os.path.dirname(__file__), "..", "core", "pdf_cache")
    os.makedirs(pdf_dir, exist_ok=True)
    return pdf_dir


def _safe(text):
    """Encode text safely for FPDF latin-1."""
    if not text:
        return ""
    return str(text).encode('latin-1', errors='replace').decode('latin-1')


def generate_cover_letter_pdf(company_name, job_title, hiring_manager="Hiring Manager"):
    """Generate cover letter PDF using FPDF2 built-in fonts. Works everywhere."""
    try:
        from fpdf import FPDF
        from fpdf.enums import XPos, YPos

        pdf_dir = _get_pdf_dir()
        safe_company = "".join(
            c for c in company_name if c.isalnum() or c in ' _-'
        ).strip().replace(' ', '_')[:40]
        pdf_path = os.path.join(pdf_dir, f"Cover_Letter_{safe_company}.pdf")

        pdf = FPDF()
        pdf.set_margins(25, 20, 25)
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.add_page()

        # ── Header ────────────────────────────────────────────────────────────
        pdf.set_font("Helvetica", "B", 18)
        pdf.set_text_color(0, 120, 180)
        pdf.cell(0, 10, "SAM SALAMEH",
                 align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 5, "Senior Network Engineer  |  CCNA  |  NSE  |  MTCNA  |  UBWA",
                 align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(0, 5, "+961 70 841 1009  |  samsalameh.cv@gmail.com  |  linkedin.com/in/sam-salameh",
                 align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(3)

        # Divider
        pdf.set_draw_color(0, 120, 180)
        pdf.set_line_width(0.4)
        pdf.line(25, pdf.get_y(), 185, pdf.get_y())
        pdf.ln(7)

        # ── Date ──────────────────────────────────────────────────────────────
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 6, datetime.date.today().strftime("%B %d, %Y"),
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(4)

        # ── Recipient ─────────────────────────────────────────────────────────
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 6, _safe(hiring_manager),
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, "Hiring Team",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(0, 6, _safe(company_name[:60]),
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(6)

        # ── Subject ───────────────────────────────────────────────────────────
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(0, 120, 180)
        pdf.cell(0, 7, _safe(f"Re: Application for {job_title}"[:80]),
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(4)

        # ── Body ──────────────────────────────────────────────────────────────
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(40, 40, 40)

        body_paragraphs = [
            f"Dear {hiring_manager},",
            (f"I am writing to express my strong interest in the {job_title} position "
             f"at {company_name}. With 15+ years of enterprise network engineering experience "
             "and active certifications in Cisco CCNA, Fortinet NSE, MikroTik MTCNA, and "
             "Ubiquiti UBWA, I am confident I can deliver immediate value to your team."),
            ("Throughout my career, I have deployed enterprise-grade networks for 20+ clients "
             "achieving 99.9% uptime SLA, reduced security incidents by 100% through FortiGate "
             "and Cisco ASA hardening, and configured IPSec/SSL VPN for 50+ branch offices. "
             "My expertise spans Cisco IOS, MikroTik RouterOS, Fortinet FortiGate, and Ubiquiti "
             "UniFi with deep knowledge in OSPF/BGP/EIGRP routing and fiber optic infrastructure "
             "spanning 500km+."),
            (f"I am available for immediate relocation to the UAE, KSA, Qatar, Kuwait, or Europe. "
             f"Please find my CV attached. I would welcome the opportunity to discuss how my "
             f"background aligns with {company_name}'s infrastructure goals."),
            "Thank you for your time and consideration.",
        ]

        for para in body_paragraphs:
            pdf.multi_cell(0, 6, _safe(para))
            pdf.ln(4)

        # ── Sign-off ──────────────────────────────────────────────────────────
        pdf.ln(4)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, "Best regards,",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 6, "Sam Salameh",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 5, "Senior Network Engineer",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(0, 5, "+961 70 841 1009  |  samsalameh.cv@gmail.com",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.output(pdf_path)
        size = os.path.getsize(pdf_path)
        logging.info(f"✅ Cover Letter PDF: {pdf_path} ({size:,} bytes)")
        return pdf_path

    except Exception as e:
        logging.error(f"❌ Cover letter PDF failed: {type(e).__name__}: {e}")
        import traceback
        logging.error(traceback.format_exc())
        return None
