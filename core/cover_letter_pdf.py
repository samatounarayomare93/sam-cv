"""
Generate Cover Letter PDF - Playwright with FPDF fallback
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _get_pdf_dir():
    is_cloud = os.getenv("RENDER") or os.getenv("RAILWAY") or os.getenv("HEROKU")
    if is_cloud:
        pdf_dir = "/tmp/pdf_cache"
    else:
        pdf_dir = os.path.join(os.path.dirname(__file__), "..", "core", "pdf_cache")
    os.makedirs(pdf_dir, exist_ok=True)
    return pdf_dir


def _generate_cover_letter_fpdf(company_name, job_title, hiring_manager="Hiring Manager"):
    """Generate cover letter PDF using FPDF2 (works everywhere, no browser needed)"""
    try:
        from fpdf import FPDF
        import datetime

        pdf_dir = _get_pdf_dir()
        safe_company = "".join(c for c in company_name if c.isalnum() or c in ' _-').strip().replace(' ', '_')
        pdf_path = os.path.join(pdf_dir, f"Cover_Letter_{safe_company}.pdf")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_margins(20, 20, 20)
        pdf.set_auto_page_break(auto=True, margin=20)

        # Header - Name
        pdf.set_font("Helvetica", "B", 22)
        pdf.set_text_color(0, 180, 216)  # Blue
        pdf.cell(0, 12, "SAM SALAMEH", ln=True, align='C')

        # Contact info
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 6, "+961 70 841 100  |  samsalameh.cv@gmail.com  |  linkedin.com/in/sam-salameh", ln=True, align='C')
        pdf.ln(3)

        # Divider
        pdf.set_draw_color(0, 180, 216)
        pdf.set_line_width(0.5)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(8)

        # Date
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(100, 100, 100)
        today = datetime.date.today().strftime("%B %d, %Y")
        pdf.cell(0, 6, today, ln=True)
        pdf.ln(4)

        # Recipient
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 6, hiring_manager, ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, f"Hiring Team", ln=True)
        pdf.cell(0, 6, company_name, ln=True)
        pdf.ln(6)

        # Subject
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(0, 180, 216)
        pdf.cell(0, 7, f"Re: Application for {job_title}", ln=True)
        pdf.ln(4)

        # Body
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(50, 50, 50)

        paragraphs = [
            f"Dear {hiring_manager},",
            "",
            f"I am writing to express my strong interest in the {job_title} position at {company_name}. "
            "With a proven track record in operations management, human resources, and organizational leadership, "
            "I am confident in my ability to contribute meaningfully to your team from day one.",
            "",
            "Throughout my career, I have demonstrated expertise in streamlining workflows, managing cross-functional "
            "teams, and driving measurable improvements in efficiency and employee engagement. My approach combines "
            "strategic thinking with hands-on execution, ensuring that both short-term targets and long-term goals "
            "are consistently achieved.",
            "",
            f"I am particularly drawn to {company_name} because of its commitment to excellence and innovation. "
            "I believe my background aligns well with your organizational values and the requirements of this role. "
            "I would welcome the opportunity to discuss how my experience can benefit your team.",
            "",
            "Thank you for your time and consideration. I look forward to the possibility of contributing to "
            f"{company_name}'s continued success.",
            "",
            "Sincerely,",
            "",
            "Sam Salameh",
        ]

        for para in paragraphs:
            if para == "":
                pdf.ln(4)
            else:
                pdf.multi_cell(0, 6, para)

        pdf.output(pdf_path)
        print(f"✅ Cover Letter PDF generated (FPDF): {pdf_path}")
        return pdf_path

    except Exception as e:
        print(f"❌ FPDF cover letter generation failed: {e}")
        return None


def generate_cover_letter_pdf(company_name, job_title, hiring_manager="Hiring Manager"):
    """Generate cover letter PDF - tries Playwright first, falls back to FPDF"""

    pdf_dir = _get_pdf_dir()
    safe_company = "".join(c for c in company_name if c.isalnum() or c in ' _-').strip().replace(' ', '_')
    pdf_path = os.path.join(pdf_dir, f"Cover_Letter_{safe_company}.pdf")

    # Try Playwright first (best quality)
    try:
        from playwright.sync_api import sync_playwright

        # Generate HTML content
        try:
            from generate_cover_letter import generate_cover_letter
            html_content = generate_cover_letter(company_name, job_title, hiring_manager)
        except Exception:
            html_content = None

        if html_content:
            temp_html = os.path.join(pdf_dir, "temp_cover_letter.html")
            with open(temp_html, 'w', encoding='utf-8') as f:
                f.write(html_content)

            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(f'file:///{os.path.abspath(temp_html).replace(os.sep, "/")}')
                page.wait_for_load_state('networkidle')
                page.pdf(
                    path=pdf_path,
                    format='A4',
                    print_background=True,
                    margin={'top': '10mm', 'right': '15mm', 'bottom': '10mm', 'left': '15mm'}
                )
                browser.close()

            if os.path.exists(temp_html):
                os.remove(temp_html)

            print(f"✅ Cover Letter PDF generated (Playwright): {pdf_path}")
            return pdf_path

    except Exception as e:
        print(f"⚠️ Playwright cover letter failed: {e}, falling back to FPDF...")

    # Fallback: FPDF (works on Render without browser)
    return _generate_cover_letter_fpdf(company_name, job_title, hiring_manager)


if __name__ == "__main__":
    result = generate_cover_letter_pdf("Future Tech Industries", "Lead Automation Engineer")
    print("Result:", result)
