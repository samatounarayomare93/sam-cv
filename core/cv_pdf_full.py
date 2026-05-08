"""
Professional CV PDF Generator - Sam Salameh
Uses ReportLab for high-quality output with embedded fonts.
Produces a proper-sized PDF matching the reference design.
"""
import os


def generate_full_cv_pdf():
    """Generate complete professional CV PDF using ReportLab."""
    try:
        return _generate_reportlab_cv()
    except Exception as e:
        import logging
        logging.warning(f"ReportLab CV failed: {e}, falling back to FPDF")
        return _generate_fpdf_cv()


def _generate_reportlab_cv():
    """High-quality CV using ReportLab with embedded fonts and proper layout."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    import io

    # ── Register embedded fonts ───────────────────────────────────────────
    _font_dir = os.path.join(os.path.dirname(__file__), "fonts")
    _sys_font_dir = "C:/Windows/Fonts"
    def _reg(name, filename):
        for d in [_font_dir, _sys_font_dir, "/usr/share/fonts/truetype/liberation",
                  "/usr/share/fonts/truetype/freefont", "/usr/share/fonts"]:
            p = os.path.join(d, filename)
            if os.path.exists(p):
                try:
                    pdfmetrics.registerFont(TTFont(name, p))
                    return True
                except Exception:
                    pass
        return False

    has_arial = _reg("Arial", "Arial.ttf") and _reg("Arial-Bold", "Arial-Bold.ttf")
    if not has_arial:
        # Try alternate names
        has_arial = _reg("Arial", "arial.ttf") and _reg("Arial-Bold", "arialbd.ttf")

    FONT_REG  = "Arial"      if has_arial else "Helvetica"
    FONT_BOLD = "Arial-Bold" if has_arial else "Helvetica-Bold"
    FONT_ITA  = "Arial"      if has_arial else "Helvetica-Oblique"

    # ── Candidate data ────────────────────────────────────────────────────
    phone    = os.getenv("CANDIDATE_PHONE",     "+961 70 841 1009")
    em       = os.getenv("SENDER_EMAIL",        os.getenv("GMAIL_SMTP_USER", "samsalameh.cv@gmail.com"))
    linkedin = os.getenv("LINKEDIN_URL",        "linkedin.com/in/sam-salameh").replace("https://www.", "").replace("https://", "")

    # ── Colors ────────────────────────────────────────────────────────────
    DARK    = HexColor("#1e272e")
    ACCENT  = HexColor("#00b4d8")
    LIGHT   = HexColor("#c8d2dc")
    BODY    = HexColor("#323232")
    WHITE   = white

    W, H = A4          # 595.27 x 841.89 pt
    SW = 68 * mm       # sidebar width

    # ── Output path ───────────────────────────────────────────────────────
    is_cloud = os.getenv("RENDER") or os.getenv("RAILWAY") or os.getenv("HEROKU")
    pdf_dir  = "/tmp/pdf_cache" if is_cloud else os.path.join(os.path.dirname(__file__), "..", "core", "pdf_cache")
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, "Sam_Salameh_CV.pdf")

    c = canvas.Canvas(pdf_path, pagesize=A4)

    def draw_page(page_num):
        """Draw sidebar + main area for a page."""
        # Sidebar background
        c.setFillColor(DARK)
        c.rect(0, 0, SW, H, fill=1, stroke=0)
        # Main background
        c.setFillColor(WHITE)
        c.rect(SW, 0, W - SW, H, fill=1, stroke=0)

        if page_num == 1:
            # Avatar circle
            c.setFillColor(ACCENT)
            c.circle(SW / 2, H - 30 * mm, 14 * mm, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont(FONT_BOLD, 20)
            c.drawCentredString(SW / 2, H - 33 * mm, "SS")

            # Name + title in sidebar
            c.setFillColor(WHITE)
            c.setFont(FONT_BOLD, 10)
            c.drawCentredString(SW / 2, H - 52 * mm, "SAM SALAMEH")
            c.setFillColor(ACCENT)
            c.setFont(FONT_REG, 7)
            c.drawCentredString(SW / 2, H - 57 * mm, "SENIOR NETWORK ENGINEER")

    def sidebar_section(label, y_mm):
        y = H - y_mm * mm
        c.setFillColor(ACCENT)
        c.setFont(FONT_BOLD, 8)
        c.drawString(6 * mm, y, label)
        c.setStrokeColor(ACCENT)
        c.setLineWidth(0.4)
        c.line(6 * mm, y - 1.5 * mm, (SW - 6 * mm), y - 1.5 * mm)

    def sidebar_text(text, y_mm, bold=False, color=None):
        y = H - y_mm * mm
        c.setFillColor(color or LIGHT)
        c.setFont(FONT_BOLD if bold else FONT_REG, 7)
        c.drawString(6 * mm, y, text)

    def sidebar_bullet(text, y_mm):
        y = H - y_mm * mm
        c.setFillColor(ACCENT)
        c.circle(7.5 * mm, y + 1 * mm, 1 * mm, fill=1, stroke=0)
        c.setFillColor(LIGHT)
        c.setFont(FONT_REG, 7)
        c.drawString(10 * mm, y, text)

    def skill_bar(text, y_mm):
        y = H - y_mm * mm
        c.setFillColor(HexColor("#2c3740"))
        c.rect(6 * mm, y - 1 * mm, SW - 12 * mm, 5 * mm, fill=1, stroke=0)
        c.setFillColor(LIGHT)
        c.setFont(FONT_REG, 6.5)
        c.drawString(8 * mm, y + 0.5 * mm, text)

    def main_section(label, y_mm):
        y = H - y_mm * mm
        c.setFillColor(DARK)
        c.setFont(FONT_BOLD, 11)
        c.drawString(SW + 6 * mm, y, label)
        c.setStrokeColor(ACCENT)
        c.setLineWidth(0.5)
        c.line(SW + 6 * mm, y - 2 * mm, W - 6 * mm, y - 2 * mm)

    def main_multiline(text, y_mm, width_mm=None, font_size=8, color=None, x_offset=0, line_height=4.5):
        from reportlab.lib.utils import simpleSplit
        w = (width_mm or (210 - 68 - 12)) * mm
        x = SW + 6 * mm + x_offset
        c.setFillColor(color or BODY)
        c.setFont(FONT_REG, font_size)
        lines = simpleSplit(text, FONT_REG, font_size, w)
        y = H - y_mm * mm
        for line in lines:
            c.drawString(x, y, line)
            y -= line_height * mm
        return y_mm + len(lines) * line_height

    # ══════════════════════════════════════════════════════════════════════
    # PAGE 1
    # ══════════════════════════════════════════════════════════════════════
    draw_page(1)

    # ── Sidebar content ───────────────────────────────────────────────────
    sidebar_section("CONTACT", 65)
    sidebar_text(f"  {phone}",        72)
    sidebar_text(f"  {em}",           78)
    sidebar_text("  Beirut, Lebanon", 84)
    sidebar_text(f"  {linkedin}",     90)

    sidebar_section("EDUCATION", 100)
    sidebar_text("B3 - Information Technology", 107, bold=True)
    sidebar_text("Dekwene Technical School",    113)
    sidebar_text("2016",                        119)

    sidebar_section("CERTIFICATIONS", 128)
    certs = ["Cisco CCNA", "Fortinet NSE", "MikroTik MTCNA", "Ubiquiti UBWA"]
    cy = 135
    for cert in certs:
        sidebar_bullet(cert, cy)
        cy += 7

    sidebar_section("CORE SKILLS", cy + 3)
    skills = [
        "Network Design & Architecture",
        "Cisco IOS / CCNA",
        "MikroTik RouterOS",
        "Ubiquiti UniFi",
        "Fortinet FortiGate",
        "Fiber Optic (500km+)",
        "Firewalls & VPN",
        "OSPF / BGP / EIGRP",
        "IPSec / SSL VPN",
        "Traffic Analysis",
    ]
    sy = cy + 10
    for sk in skills:
        skill_bar(sk, sy)
        sy += 7

    if sy < 255:
        sidebar_section("LANGUAGES", sy + 3)
        langs = [("English", "Fluent"), ("Arabic", "Native"), ("French", "Intermediate")]
        ly = sy + 10
        for lang, level in langs:
            y = H - ly * mm
            c.setFillColor(LIGHT)
            c.setFont("Helvetica-Bold", 7)
            c.drawString(6 * mm, y, lang)
            c.setFillColor(ACCENT)
            c.setFont("Helvetica", 7)
            c.drawString(30 * mm, y, level)
            ly += 6

    # ── Main content page 1 ───────────────────────────────────────────────
    # Header
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(SW + 6 * mm, H - 16 * mm, "SAM SALAMEH")
    c.setFillColor(ACCENT)
    c.setFont("Helvetica", 13)
    c.drawString(SW + 6 * mm, H - 26 * mm, "Senior Network Engineer")
    # Accent bar
    c.setFillColor(ACCENT)
    c.rect(SW + 6 * mm, H - 30 * mm, W - SW - 12 * mm, 1.2 * mm, fill=1, stroke=0)

    # Certifications badges inline
    badges = ["CCNA", "NSE", "MTCNA", "UBWA"]
    bx = SW + 6 * mm
    by = H - 36 * mm
    for badge in badges:
        c.setFillColor(HexColor("#e8f4fd"))
        c.setStrokeColor(ACCENT)
        c.setLineWidth(0.5)
        c.roundRect(bx, by - 3 * mm, 14 * mm, 5 * mm, 1.5 * mm, fill=1, stroke=1)
        c.setFillColor(ACCENT)
        c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(bx + 7 * mm, by - 0.5 * mm, badge)
        bx += 16 * mm

    # Executive Summary
    main_section("Executive Summary", 44)
    summary = (
        "Accomplished Network Engineer with 15+ years of progressive experience designing, "
        "implementing, and troubleshooting enterprise-grade networking infrastructure. Proven "
        "expertise managing complex environments with 99.9% uptime SLA across Cisco, MikroTik, "
        "Ubiquiti, and Fortinet platforms. Strong background in fiber optic installations (500km+), "
        "VPN configurations, firewall hardening, and traffic analysis."
    )
    end_y = main_multiline(summary, 50, font_size=8.5)

    # Key Achievements box
    box_y = end_y + 3
    box_h = 30
    c.setFillColor(HexColor("#f0f8ff"))
    c.setStrokeColor(ACCENT)
    c.setLineWidth(1.5)
    c.rect(SW + 6 * mm, H - (box_y + box_h) * mm, W - SW - 12 * mm, box_h * mm, fill=1, stroke=0)
    c.setFillColor(ACCENT)
    c.rect(SW + 6 * mm, H - (box_y + box_h) * mm, 1.5 * mm, box_h * mm, fill=1, stroke=0)

    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(SW + 10 * mm, H - (box_y + 5) * mm, "Key Achievements")

    achievements = [
        "Deployed enterprise networks for 20+ clients achieving 99.9% uptime SLA",
        "Reduced security incidents by 100% through FortiGate/Cisco ASA hardening",
        "Configured IPSec/SSL VPN for 50+ branch offices across multiple regions",
    ]
    ay = box_y + 10
    for ach in achievements:
        c.setFillColor(ACCENT)
        c.circle(SW + 10 * mm, H - ay * mm + 1 * mm, 1 * mm, fill=1, stroke=0)
        c.setFillColor(BODY)
        c.setFont("Helvetica", 7.5)
        c.drawString(SW + 13 * mm, H - ay * mm, ach)
        ay += 7

    # Professional Experience
    exp_start = box_y + box_h + 5
    main_section("Professional Experience", exp_start)

    def draw_experience(job_title, period, location, desc, bullets, y_mm):
        # Title
        c.setFillColor(DARK)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(SW + 6 * mm, H - y_mm * mm, job_title)
        # Period badge
        c.setFillColor(HexColor("#e8f4fd"))
        c.rect(W - 36 * mm, H - (y_mm + 1) * mm, 30 * mm, 5 * mm, fill=1, stroke=0)
        c.setFillColor(ACCENT)
        c.setFont("Helvetica", 7)
        c.drawCentredString(W - 21 * mm, H - y_mm * mm, period)
        # Location
        c.setFillColor(HexColor("#787878"))
        c.setFont("Helvetica-Oblique", 7.5)
        c.drawString(SW + 6 * mm, H - (y_mm + 5) * mm, location)
        # Description
        next_y = main_multiline(desc, y_mm + 10, font_size=7.5)
        # Bullets
        by2 = next_y + 1
        for b in bullets:
            c.setFillColor(ACCENT)
            c.circle(SW + 8 * mm, H - by2 * mm + 1 * mm, 1 * mm, fill=1, stroke=0)
            c.setFillColor(BODY)
            c.setFont("Helvetica", 7)
            c.drawString(SW + 11 * mm, H - by2 * mm, b)
            by2 += 4.5
        return by2 + 4

    next_y = draw_experience(
        "Freelance Network Engineer", "2023 - Present", "Freelance, Beirut",
        "Providing comprehensive network engineering services to enterprise businesses, ISPs, and educational institutions.",
        [
            "Designed and deployed enterprise-grade networks for 20+ clients",
            "Implemented secure VPN solutions and firewall configurations",
            "Conducted network audits and performance optimization",
            "Provided 24/7 technical support and emergency response",
        ],
        exp_start + 8
    )

    next_y = draw_experience(
        "Network Management Consultant", "2021 - 2023", "Freelance, Beirut",
        "Consulted on network infrastructure planning, security implementations, and technology upgrades.",
        [
            "Managed network infrastructure for multiple concurrent projects",
            "Implemented advanced routing protocols (OSPF, BGP, EIGRP)",
            "Configured and maintained enterprise firewalls and security systems",
            "Trained technical teams on best practices and new technologies",
        ],
        next_y
    )

    if next_y < 255:
        draw_experience(
            "Networking Technician", "2010 - 2023", "Professional Network, Beirut",
            "Comprehensive networking support including installation, configuration, and troubleshooting.",
            [
                "Installed and configured routers, switches, and wireless access points",
                "Performed fiber optic cable installations and terminations (500km+)",
                "Monitored network performance and resolved connectivity issues",
                "Maintained detailed documentation of network configurations",
            ],
            next_y
        )

    c.showPage()

    # ══════════════════════════════════════════════════════════════════════
    # PAGE 2
    # ══════════════════════════════════════════════════════════════════════
    draw_page(2)

    # Sidebar page 2
    sidebar_section("CERTIFICATIONS", 65)
    cert_details = [
        ("Cisco CCNA",     "Routing & Switching"),
        ("Fortinet NSE",   "Network Security"),
        ("MikroTik MTCNA", "RouterOS Admin"),
        ("Ubiquiti UBWA",  "Wireless Admin"),
    ]
    cdy = 72
    for cert, detail in cert_details:
        y = H - cdy * mm
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(6 * mm, y, cert)
        c.setFillColor(ACCENT)
        c.setFont("Helvetica", 6.5)
        c.drawString(6 * mm, y - 4 * mm, detail)
        cdy += 11

    sidebar_section("TOOLS", cdy + 3)
    tools = ["Wireshark", "SolarWinds", "PRTG", "Nagios", "Cacti", "GNS3", "Packet Tracer"]
    ty2 = cdy + 10
    for tool in tools:
        skill_bar(tool, ty2)
        ty2 += 7

    sidebar_section("AVAILABILITY", ty2 + 3)
    avail_lines = ["Immediate relocation:", "UAE  |  KSA  |  Qatar", "Kuwait  |  Europe", "", "Visa sponsorship OK"]
    aly = ty2 + 10
    for line in avail_lines:
        sidebar_text(line, aly, color=LIGHT if line else None)
        aly += 6

    # Main content page 2
    main_section("Technical Expertise", 14)

    tech_sections = [
        ("Networking Protocols",
         "TCP/IP, VLAN, Trunking, STP/RSTP, OSPF, BGP, EIGRP, RIP, QoS, MPLS, SD-WAN"),
        ("Security & Firewalls",
         "FortiGate, Cisco ASA, pfSense, IPSec VPN, SSL VPN, ACL, NAT, IDS/IPS, 802.1X"),
        ("Platforms & Vendors",
         "Cisco IOS/IOS-XE, MikroTik RouterOS, Ubiquiti UniFi/EdgeOS, Fortinet FortiOS, HP ProCurve"),
        ("Infrastructure",
         "Fiber Optic SM/MM (500km+), Structured Cabling, Wireless 802.11 a/b/g/n/ac/ax, PoE"),
        ("Monitoring & Tools",
         "Wireshark, SolarWinds, PRTG, Nagios, Cacti, GNS3, Cisco Packet Tracer, NetFlow"),
        ("Cloud & Virtualization",
         "AWS VPC, Azure Networking, VMware vSphere, Hyper-V, Docker Networking"),
    ]

    tx_y = 22
    for sec_title, content in tech_sections:
        c.setFillColor(ACCENT)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(SW + 6 * mm, H - tx_y * mm, sec_title)
        tx_y = main_multiline(content, tx_y + 5, font_size=7.5)
        tx_y += 4

    # Notable Projects
    main_section("Notable Projects", tx_y + 2)

    projects = [
        ("ISP Core Network Upgrade",
         "Designed and deployed MPLS backbone for regional ISP serving 10,000+ subscribers. "
         "Achieved 99.99% uptime with redundant BGP peering and automated failover."),
        ("Enterprise Security Hardening",
         "Implemented FortiGate HA cluster with IPS/IDS, web filtering, and SSL inspection "
         "for 500-user corporate network. Reduced security incidents by 100%."),
        ("Multi-Site VPN Infrastructure",
         "Configured IPSec VPN mesh connecting 50+ branch offices across Lebanon and GCC. "
         "Centralized management via FortiManager with automated policy deployment."),
        ("Fiber Optic Network Deployment",
         "Led end-to-end deployment of 500km+ fiber optic infrastructure for educational "
         "institution network spanning 15 campuses."),
    ]

    py2 = tx_y + 10
    for proj_title, proj_desc in projects:
        if py2 > 265:
            break
        c.setFillColor(DARK)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(SW + 6 * mm, H - py2 * mm, proj_title)
        py2 = main_multiline(proj_desc, py2 + 5, font_size=7.5)
        py2 += 5

    c.save()
    return pdf_path


def _generate_fpdf_cv():
    """Fallback FPDF CV if ReportLab is unavailable."""
    from fpdf import FPDF
    import os

    phone    = os.getenv("CANDIDATE_PHONE",     "+961 70 841 1009")
    em       = os.getenv("SENDER_EMAIL",        os.getenv("GMAIL_SMTP_USER", "samsalameh.cv@gmail.com"))
    linkedin = os.getenv("LINKEDIN_URL",        "linkedin.com/in/sam-salameh").replace("https://www.", "").replace("https://", "")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Simple clean layout
    pdf.set_fill_color(30, 39, 46)
    pdf.rect(0, 0, 70, 297, 'F')

    pdf.set_xy(75, 15)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(30, 39, 46)
    pdf.cell(125, 10, "SAM SALAMEH")

    pdf.set_xy(75, 27)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(0, 180, 216)
    pdf.cell(125, 7, "Senior Network Engineer")

    pdf.set_xy(75, 40)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(80, 80, 80)
    summary = ("15+ years enterprise network engineering. Cisco CCNA, Fortinet NSE, "
               "MikroTik MTCNA, Ubiquiti UBWA. 20+ clients, 99.9% uptime SLA.")
    pdf.multi_cell(125, 5, summary)

    is_cloud = os.getenv("RENDER") or os.getenv("RAILWAY") or os.getenv("HEROKU")
    pdf_dir  = "/tmp/pdf_cache" if is_cloud else os.path.join(os.path.dirname(__file__), "..", "core", "pdf_cache")
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, "Sam_Salameh_CV.pdf")
    pdf.output(pdf_path)
    return pdf_path


if __name__ == "__main__":
    path = generate_full_cv_pdf()
    import os
    print(f"Generated: {path}  ({os.path.getsize(path):,} bytes)")
