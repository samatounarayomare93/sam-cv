"""
Generate Cover Letter PDF - matches the reference PDF exactly.
Uses Playwright (HTML→PDF) when available, falls back to FPDF2.
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
    if not text:
        return ""
    return str(text).encode('latin-1', errors='replace').decode('latin-1')


def _build_cover_letter_html(company_name, job_title, hiring_manager="Hiring Manager"):
    """Build the HTML for the cover letter — matches reference PDF design exactly."""
    today = datetime.date.today().strftime("%B %d, %Y")
    # Use sam.dev1@hotmail.com as in the reference PDF
    phone = os.getenv("CANDIDATE_PHONE", "+961 70 841 1009")
    email_display = "sam.dev1@hotmail.com"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cover Letter - Sam Salameh</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: 'Segoe UI', Arial, sans-serif;
    background: white;
    color: #2c3e50;
    padding: 0;
    margin: 0;
  }}
  .page {{
    max-width: 800px;
    margin: 0 auto;
    background: white;
    padding: 0;
  }}
  /* Top gradient line — matches reference */
  .top-line {{
    height: 5px;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    width: 100%;
  }}
  /* Header — white background, centered */
  .header {{
    text-align: center;
    padding: 32px 48px 20px;
    border-bottom: 1px solid #e5e7eb;
  }}
  .header-name {{
    font-size: 32px;
    font-weight: 700;
    color: #667eea;
    letter-spacing: 1px;
    margin-bottom: 6px;
  }}
  .header-title {{
    font-size: 14px;
    color: #6b7280;
    margin-bottom: 14px;
  }}
  .header-contact {{
    font-size: 12px;
    color: #9ca3af;
    display: flex;
    justify-content: center;
    gap: 24px;
    flex-wrap: wrap;
  }}
  .header-contact span {{ display: flex; align-items: center; gap: 5px; }}
  /* Body */
  .body {{
    padding: 36px 48px 40px;
  }}
  .date {{
    font-size: 13px;
    color: #6b7280;
    text-align: right;
    margin-bottom: 28px;
  }}
  .recipient {{
    margin-bottom: 8px;
  }}
  .recipient .manager {{
    font-size: 14px;
    font-weight: 700;
    color: #1e2d3d;
  }}
  .recipient .company {{
    font-size: 14px;
    font-weight: 700;
    color: #1e2d3d;
  }}
  .subject-line {{
    font-size: 14px;
    color: #374151;
    margin-bottom: 24px;
    margin-top: 4px;
  }}
  .subject-line strong {{ color: #1e2d3d; }}
  .body p {{
    font-size: 13.5px;
    line-height: 1.85;
    color: #374151;
    margin-bottom: 16px;
    text-align: justify;
  }}
  .body p.salutation {{
    font-weight: 700;
    color: #1e2d3d;
    margin-bottom: 16px;
    text-align: left;
  }}
  /* Highlight box — matches reference style */
  .highlight-box {{
    background: #f3f4f6;
    border-left: 4px solid #667eea;
    padding: 18px 22px;
    margin: 20px 0;
    border-radius: 0 6px 6px 0;
  }}
  .highlight-box h4 {{
    font-size: 13px;
    color: #374151;
    font-weight: 700;
    margin-bottom: 12px;
  }}
  .highlight-box ul {{
    list-style: none;
    padding: 0;
  }}
  .highlight-box li {{
    font-size: 13px;
    color: #374151;
    line-height: 1.75;
    padding: 3px 0 3px 18px;
    position: relative;
  }}
  .highlight-box li::before {{
    content: '✓';
    position: absolute;
    left: 0;
    color: #667eea;
    font-weight: 700;
  }}
  .signoff {{
    margin-top: 24px;
  }}
  .signoff p {{
    font-size: 13.5px;
    color: #374151;
    margin-bottom: 4px;
  }}
  .signoff .name {{
    font-size: 14px;
    font-weight: 700;
    color: #1e2d3d;
    margin-top: 16px;
  }}
  .signoff .title {{
    font-size: 12px;
    color: #6b7280;
    margin-top: 2px;
  }}
  @media print {{
    body {{ background: white; }}
    .page {{ box-shadow: none; }}
  }}
</style>
</head>
<body>
<div class="page">
  <div class="top-line"></div>

  <div class="header">
    <div class="header-name">SAM SALAMEH</div>
    <div class="header-title">Senior Network Engineer</div>
    <div class="header-contact">
      <span>📱 {phone}</span>
      <span>✉ {email_display}</span>
      <span>📍 Beirut, Lebanon</span>
    </div>
  </div>

  <div class="body">
    <div class="date">{today}</div>

    <div class="recipient">
      <div class="manager">{hiring_manager}</div>
      <div class="company">{company_name}</div>
    </div>
    <div class="subject-line">Re: Application for <strong>{job_title}</strong> Position</div>

    <p class="salutation">Dear {hiring_manager},</p>

    <p>I am writing to express my strong interest in the <strong>{job_title}</strong> position
    at <strong>{company_name}</strong>. With over <strong>15 years</strong> of progressive experience in network
    engineering and infrastructure management, I am confident that my technical expertise
    and proven track record make me an ideal candidate for this role.</p>

    <div class="highlight-box">
      <h4>Why I'm a Perfect Fit:</h4>
      <ul>
        <li>Designed and deployed enterprise-grade networks for <strong>20+ clients</strong> achieving <strong>99.9% uptime SLA</strong></li>
        <li>Reduced security incidents by <strong>100%</strong> through FortiGate/Cisco ASA hardening</li>
        <li>Configured IPSec/SSL VPN infrastructure for <strong>50+ branch offices</strong></li>
        <li>Deep expertise in Cisco IOS, MikroTik RouterOS, Fortinet FortiGate, and Ubiquiti UniFi</li>
        <li>Advanced routing protocols: <strong>OSPF, BGP, EIGRP</strong> — ISP-grade topologies</li>
        <li>Fiber optic infrastructure spanning <strong>500km+</strong> with OTDR testing</li>
      </ul>
    </div>

    <p>My technical proficiency includes advanced routing protocols (OSPF, BGP, EIGRP), VPN
    configurations, firewall management, fiber optic installations, and traffic analysis. I have a
    proven track record of resolving 50+ daily complex technical issues while maintaining strict
    SLA compliance and customer satisfaction.</p>

    <p>What sets me apart is my ability to combine deep technical knowledge with strong
    problem-solving skills and effective communication. I excel at translating complex technical
    concepts into actionable business solutions, and I am committed to staying current with
    emerging technologies and industry best practices.</p>

    <p>I am particularly drawn to <strong>{company_name}</strong> because of your reputation for
    innovation and excellence in the industry. I am excited about the opportunity to contribute
    my expertise to your team and help drive your network infrastructure initiatives forward.</p>

    <p>I am available for <strong>immediate relocation</strong> to the UAE, KSA, Qatar, Kuwait, or Europe.
    I would welcome the opportunity to discuss how my experience and skills align with your
    needs. Thank you for considering my application. I look forward to speaking with you soon.</p>

    <div class="signoff">
      <p>Sincerely,</p>
      <div class="name">Sam Salameh</div>
      <div class="title">Senior Network Engineer</div>
    </div>
  </div>
</div>
</body>
</html>"""


def generate_cover_letter_pdf(company_name, job_title, hiring_manager="Hiring Manager"):
    """Generate cover letter PDF. Uses Playwright if available, else FPDF2."""
    pdf_dir = _get_pdf_dir()
    safe_company = "".join(
        c for c in company_name if c.isalnum() or c in ' _-'
    ).strip().replace(' ', '_')[:40]
    pdf_path = os.path.join(pdf_dir, f"Cover_Letter_{safe_company}.pdf")

    # ── Try Playwright first (best quality, matches reference) ────────────
    try:
        from playwright.sync_api import sync_playwright
        import tempfile, concurrent.futures

        # Suppress WeasyPrint warnings if it gets imported later
        logging.getLogger("weasyprint").setLevel(logging.ERROR)
        logging.getLogger("weasyprint.css").setLevel(logging.ERROR)

        html_content = _build_cover_letter_html(company_name, job_title, hiring_manager)

        def _playwright_render():
            # Write HTML to temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html',
                                             delete=False, encoding='utf-8') as tmp:
                tmp.write(html_content)
                tmp_path = tmp.name
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch()
                    page = browser.new_page()
                    page.goto(f'file:///{tmp_path.replace(os.sep, "/")}')
                    page.wait_for_load_state('networkidle')
                    page.pdf(
                        path=pdf_path,
                        format='A4',
                        print_background=True,
                        margin={'top': '10mm', 'right': '0mm',
                                'bottom': '10mm', 'left': '0mm'}
                    )
                    browser.close()
                return pdf_path
            finally:
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass

        # Run in thread to avoid event loop conflicts
        import asyncio
        try:
            asyncio.get_running_loop()
            # We're in async context — use thread pool
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
                result = ex.submit(_playwright_render).result(timeout=60)
        except RuntimeError:
            # Sync context — run directly
            result = _playwright_render()

        if result and os.path.exists(result) and os.path.getsize(result) > 5000:
            size = os.path.getsize(result)
            logging.info(f"✅ Cover Letter PDF (Playwright): {result} ({size:,} bytes)")
            return result

    except ImportError:
        logging.debug("⏭️ Playwright not available for cover letter, using FPDF2")
    except Exception as e:
        logging.warning(f"⚠️ Playwright cover letter failed: {e}, falling back to FPDF2")

    # ── Fallback: FPDF2 ───────────────────────────────────────────────────
    try:
        from fpdf import FPDF
        from fpdf.enums import XPos, YPos

        today = datetime.date.today().strftime("%B %d, %Y")
        candidate_email = os.getenv("SENDER_EMAIL", os.getenv("GMAIL_SMTP_USER", "samsalameh.cv@gmail.com"))
        phone = os.getenv("CANDIDATE_PHONE", "+961 70 841 1009")

        pdf = FPDF()
        pdf.set_margins(25, 20, 25)
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.add_page()

        # Header background
        pdf.set_fill_color(30, 60, 114)
        pdf.rect(0, 0, 210, 42, 'F')

        # Name
        pdf.set_y(8)
        pdf.set_font("Helvetica", "B", 20)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, "SAM SALAMEH", align='C',
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Title
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(144, 202, 249)
        pdf.cell(0, 6, "Senior Network Engineer  |  CCNA  |  NSE  |  MTCNA  |  UBWA",
                 align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Contact
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(220, 220, 220)
        pdf.cell(0, 6,
                 _safe(f"{phone}  |  {candidate_email}  |  linkedin.com/in/sam-salameh"),
                 align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Blue accent line
        pdf.set_draw_color(0, 180, 216)
        pdf.set_line_width(1.0)
        pdf.line(0, 42, 210, 42)

        pdf.set_y(50)
        pdf.set_text_color(40, 40, 40)

        # Date
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(107, 114, 128)
        pdf.cell(0, 6, today, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(4)

        # Recipient
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 6, _safe(hiring_manager), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(107, 114, 128)
        pdf.cell(0, 6, _safe(company_name[:60]), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(4)

        # Subject
        pdf.set_fill_color(240, 247, 255)
        pdf.set_draw_color(0, 119, 182)
        pdf.set_line_width(0.8)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(0, 119, 182)
        pdf.cell(0, 8, _safe(f"Re: Application for {job_title[:60]}"),
                 fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(6)

        # Body paragraphs
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(55, 65, 81)
        pdf.set_line_width(0.2)

        paragraphs = [
            f"Dear {hiring_manager},",
            (f"I am writing to express my strong interest in the {job_title} position "
             f"at {company_name}. With over 15 years of progressive experience in network "
             "engineering and infrastructure management, I am confident that my technical "
             "expertise and proven track record make me an ideal candidate for this role."),
            ("Throughout my career, I have successfully designed, implemented, and maintained "
             "enterprise-grade networking solutions across diverse platforms including Cisco, "
             "MikroTik, Ubiquiti, and Fortinet. My experience spans from hands-on technical "
             "implementation to strategic network planning and optimization."),
            ("In my current role as a Freelance Network Engineer, I have delivered comprehensive "
             "networking solutions to over 20 clients, including enterprise businesses, ISPs, and "
             "educational institutions. I specialize in network design, implementation, "
             "troubleshooting, and optimization, consistently achieving 100% uptime maintenance "
             "and exceeding client expectations."),
            ("My technical proficiency includes advanced routing protocols (OSPF, BGP, EIGRP), "
             "VPN configurations, firewall management, fiber optic installations, and traffic "
             "analysis. I have a proven track record of resolving 50+ daily complex technical "
             "issues while maintaining strict SLA compliance and customer satisfaction."),
            (f"I am available for immediate relocation to the UAE, KSA, Qatar, Kuwait, or Europe. "
             f"I would welcome the opportunity to discuss how my experience and skills align with "
             f"your needs. Thank you for considering my application. I look forward to speaking "
             f"with you soon."),
        ]

        for para in paragraphs:
            pdf.multi_cell(0, 6, _safe(para))
            pdf.ln(4)

        # Sign-off
        pdf.ln(4)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, "Sincerely,", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(4)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(30, 45, 61)
        pdf.cell(0, 6, "Sam Salameh", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(107, 114, 128)
        pdf.cell(0, 5, "Senior Network Engineer", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(0, 119, 182)
        pdf.cell(0, 5, _safe(f"{phone}  |  {candidate_email}"),
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.output(pdf_path)
        size = os.path.getsize(pdf_path)
        logging.info(f"✅ Cover Letter PDF (FPDF2): {pdf_path} ({size:,} bytes)")
        return pdf_path

    except Exception as e:
        logging.error(f"❌ Cover letter PDF failed: {type(e).__name__}: {e}")
        import traceback
        logging.error(traceback.format_exc())
        return None
