from fpdf import FPDF
import os
from datetime import datetime
import logging
import shutil
import time as time_module
import re
import random
import zipfile
from functools import lru_cache
from pathlib import Path
import uuid

# CORE 100: Absolute Asset Portability Registry
def _sanitize_filename(name: str) -> str:
    """[🛡️ HARDENING] Removes illegal characters for Cross-OS stability."""
    if not name: return "Document"
    # Replace slashes, colons, stars, etc. with underscores or spaces
    name = re.sub(r'[\\/*?:"<>|]', "_", name)
    # Trim and remove double spaces
    return " ".join(name.split())

def _find_sovereign_font(style='regular'):
    """[🧬 PHASE PARITY] Scans the host system for valid Unicode assets by style."""
    style = style.lower()
    
    # Define style-specific filenames for different OS
    if style == 'bold':
        names = ["arialbd.ttf", "DejaVuSans-Bold.ttf", "Arial Bold.ttf"]
    elif style == 'italic' or style == 'oblique':
        names = ["ariali.ttf", "DejaVuSans-Oblique.ttf", "Arial Italic.ttf"]
    else:
        names = ["arial.ttf", "DejaVuSans.ttf", "Arial.ttf"]

    common_dirs = [
        os.getenv("CHRONOS_FONT_PATH"), 
        "C:/Windows/Fonts/", 
        "/usr/share/fonts/truetype/dejavu/",
        "/System/Library/Fonts/Supplemental/"
    ]
    
    for d in common_dirs:
        if not d: continue
        for name in names:
            path = os.path.join(d, name)
            if os.path.exists(path):
                return path
    
    # Absolute Fallback: If looking for Bold/Italic and not found, return Regular path
    if style != 'regular':
        return _find_sovereign_font('regular')
    return None

FONT_REGULAR = _find_sovereign_font('regular')
FONT_BOLD = _find_sovereign_font('bold')
FONT_ITALIC = _find_sovereign_font('italic')

# ALPHA-CENTAURI: Caching Layer to minimize CPU overhead during polymorphic generation
_TEMPLATE_CACHE = {}
_CACHE_TTL = 3600 # 1 hour

import json

def load_profile():
    """[👑 DYNAMIC ASSET] Loads the candidate profile from profile.json."""
    profile_path = os.path.join(os.getcwd(), "profile.json")
    if os.path.exists(profile_path):
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"❌ Failed to load profile.json: {e}")
    
    # Fallback to hardcoded Sam profile if file is missing
    return {
        "candidate": {
            "name": "Sam Salameh",
            "title": "Senior Network Engineer",
            "email": "samsalameh.cv@gmail.com",
            "phone": "+961 70 841 1009",
            "linkedin": "https://www.linkedin.com/in/sam-salameh",
            "location": "Beirut, Lebanon",
            "avatar_initials": "SS"
        },
        "summary": "Senior Network Engineer with 15+ years of experience designing and managing enterprise-grade network infrastructure. Certified CCNA, Fortinet NSE, MikroTik MTCNA, and Ubiquiti UBWA. Proven track record delivering 99.9% uptime for 20+ enterprise clients. Available for immediate relocation to UAE, KSA, Qatar, or Europe.",
        "skills": [
            "Cisco IOS & CCNP", "MikroTik RouterOS", "Ubiquiti UniFi",
            "Fortinet FortiGate", "TCP/IP & VLAN", "OSPF, BGP, EIGRP",
            "Network Security & Firewalls", "VPN (IPSec, SSL)",
            "Fiber Optic & Structured Cabling", "PRTG, SolarWinds, Nagios"
        ],
        "certifications": [
            "Cisco CCNA — Routing & Switching",
            "Fortinet NSE — Network Security Expert",
            "MikroTik MTCNA Certified",
            "Ubiquiti UBWA Wireless Admin"
        ],
        "experience": [
            {
                "role": "Senior Freelance Network Engineer",
                "company": "Independent Consultant, Beirut",
                "period": "2023 - Present",
                "highlights": [
                    "Deployed enterprise networks for 20+ clients with 99.9% uptime SLA",
                    "Reduced security incidents by 100% via FortiGate/Cisco ASA hardening",
                    "Configured site-to-site IPSec VPN for 50+ branch offices"
                ]
            },
            {
                "role": "Network Management Consultant",
                "company": "Freelance, Beirut",
                "period": "2021 - 2023",
                "highlights": [
                    "Managed 8 concurrent enterprise network projects",
                    "Implemented OSPF/BGP/EIGRP routing for ISP-grade topologies",
                    "Trained 15+ junior network technicians"
                ]
            },
            {
                "role": "Senior Networking Technician",
                "company": "Professional Network, Beirut",
                "period": "2010 - 2021",
                "highlights": [
                    "Installed networks for 100+ enterprise sites",
                    "500+ km fiber optic installations with OTDR testing",
                    "<1 hour MTTR on all critical incidents"
                ]
            }
        ],
        "education": [
            {"degree": "B3 - Information Technology", "institution": "Dekwene Technical School", "year": "2016"}
        ],
        "languages": [
            {"language": "Arabic", "level": "Native"},
            {"language": "English", "level": "Fluent"},
            {"language": "French", "level": "Intermediate"}
        ]
    }

class CoverLetterPDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.unicode_font_name = "Helvetica"
        self.profile = load_profile()

    def header(self):
        # GLOBAL STABILITY: Always use the registered Unicode font
        p = self.profile.get("candidate", {})
        self.set_font(self.unicode_font_name, 'B', 16)
        self.cell(0, 10, p.get("name", "Candidate"), new_x="LMARGIN", new_y="NEXT", align='C')
        self.set_font(self.unicode_font_name, 'I', 10)
        self.cell(0, 8, p.get("title", ""), new_x="LMARGIN", new_y="NEXT", align='C')
        self.cell(0, 8, f"{p.get('email', '')} | {p.get('phone', '')}", new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(10)

    def inject_forensic_noise(self, strike_id: str = None):
        """
        🕵️ FORENSIC HARDENING: Injects invisible, unique metadata noise.
        This ensures that even with identical text, the file hash is 100% unique.
        """
        # [🌏 MULTIVERSE: Workstation Mimicry]
        # Randomize the PDF Producer to mimic different environments
        producers = [
            "Microsoft® Word for Microsoft 365",
            "Adobe PDF Library 23.1.1",
            "Mac OS X 14.2.1 Quartz PDFContext",
            "Overleaf (pdfTeX-1.40.25)",
            "LibreOffice 7.6",
            "Google Docs"
        ]
        selected_producer = random.choice(producers)
        creator = "Microsoft® Word" if "Word" in selected_producer else "LaTeX" if "Overleaf" in selected_producer else "System"
        
        # 🌌 INFINITY: Microscopic Pixel-Shifting (Grid Jitter)
        # Shift the starting point by a sub-pixel value
        x_shift = random.uniform(0.1, 0.5)
        y_shift = random.uniform(0.1, 0.5)
        self.set_xy(10 + x_shift, 10 + y_shift)
        
        self.set_creator(creator)
        self.set_producer(selected_producer)
        
        # 👻 GHOST: Strike-ID metadata injection
        unique_id = str(strike_id) if strike_id else str(uuid.uuid4())
        self.set_subject(f"STRIKE-ID: {unique_id}")
        self.set_keywords(f"Job, Application, Alpha-Strike, {unique_id[:8]}")

    def inject_ai_shadow_prompt(self):
        pass

class SovereignCVPDF(FPDF):
    """[👑 APEX DEITY] Premium Dark-Mode CV Generator (Visual Parity)."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # [👑 VIP SIZE OPTIMIZATION] Use Standard Core Fonts to stay below 10KB.
        self.unicode_font_name = "Helvetica"
        
        # Metadata Randomization for CV Parity (Realistic Spoofing)
        CREATORS = ["Microsoft Word 2019", "Adobe Acrobat Pro 24.2", "Google Docs", "Pages 13.2"]
        PRODUCERS = ["Microsoft Office Word", "macOS 14.4.1 Quartz PDFContext", "Skia/PDF m124"]
        self.set_creator(random.choice(CREATORS))
        self.set_producer(random.choice(PRODUCERS))
        
        # We enforce core fonts to keep the file size minimal and ensure legitimacy.
        self.compress = True

    def header(self):
        # Premium Dual-Tone Background (V4)
        self.set_fill_color(18, 20, 29) # #12141d (Dark Sidebar)
        self.rect(0, 0, 70, 297, 'F')
        
        self.set_fill_color(255, 255, 255) # #FFFFFF (Main Body)
        self.rect(70, 0, 140, 297, 'F')

    def inject_ai_shadow_prompt(self):
        pass

def _contains_arabic(text):
    return bool(re.search(r'[\u0600-\u06FF]', text)) if text else False

def _poison_text(text: str, is_unicode: bool = False) -> str:
    return text

def create_personalized_pdf(lead, custom_keywords=None):
    """
    COSMIC PROTOCOL: Generates a personalized PDF with cultural persona styling.
    """
    company = lead.get('company_name', 'Unknown')
    title = lead.get('job_title', 'Professional')
    body = lead.get('custom_body', '')
    persona = lead.get('culture_persona', 'Modern')
    tailored_cv_path = lead.get('tailored_cv_path')
    
    if tailored_cv_path and os.path.exists(tailored_cv_path):
        try:
            with open(tailored_cv_path, 'r', encoding='utf-8') as f:
                tailored_content = f.read()
                body = _parse_html_for_pdf(tailored_content) or body
        except Exception:
            pass

    return generate_dynamic_cover_letter(
        company, 
        title, 
        body, 
        persona=persona, 
        custom_keywords=custom_keywords,
        strike_id=lead.get("strike_id")
    )

def build_pdf_cover_letter_body(company_name, job_title):
    """MAXIMUM POWER: Build optimized cover letter body for PDF."""
    # Use cached template if available
    cache_key = f"{company_name[:20]}_{job_title[:20]}"
    if cache_key in _TEMPLATE_CACHE:
        cached_time, template = _TEMPLATE_CACHE[cache_key]
        if time_module.time() - cached_time < _CACHE_TTL:
            return template
    
    # MAXIMUM POWER: Clean, fast template
    p = load_profile().get("candidate", {})
    body = (
        f"Dear {company_name} Hiring Team,\n\n"
        f"I am writing to express my strong interest in the {job_title} position. "
        f"With 15+ years of progressive experience in Network Engineering and IT Infrastructure, "
        f"I am confident in my ability to deliver high-availability, secure, and optimized network solutions for your organization.\n\n"
        f"Key Strengths:\n"
        f"- Enterprise network design & deployment (Cisco, MikroTik, Ubiquiti, Fortinet)\n"
        f"- Advanced routing protocols: OSPF, BGP, EIGRP across complex topologies\n"
        f"- VPN & Firewall security (IPSec, SSL, FortiGate, Cisco ASA)\n"
        f"- Fiber optic installations & structured cabling for 100+ enterprise sites\n"
        f"- 24/7 network monitoring & troubleshooting with <1hr MTTR\n\n"
        f"I am excited about the opportunity to bring my expertise to {company_name} "
        f"and would welcome the chance to discuss how my skills align with your technical needs.\n\n"
        f"Best regards,\n"
        f"{p.get('name', 'Sam Salameh')}\n"
        f"Senior Network Engineer\n"
        f"{p.get('phone', '+961 70 841 1009')}\n"
        f"{p.get('email', 'samsalameh.cv@gmail.com')}"
    )
    
    # Cache it
    _TEMPLATE_CACHE[cache_key] = (time_module.time(), body)
    
    # Keep cache bounded
    if len(_TEMPLATE_CACHE) > 256:
        oldest_key = min(_TEMPLATE_CACHE.keys(), key=lambda k: _TEMPLATE_CACHE[k][0])
        del _TEMPLATE_CACHE[oldest_key]
    
    return body

def create_cover_letter_html(company_name, job_title):
    """[👑 LEGACY RESTORATION] Generates a high-fidelity personalized HTML Cover Letter."""
    import time
    p = load_profile().get("candidate", {})
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 40px; background: #f8f9fa; color: #333; }}
        .letter {{ background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #06b6d4; }}
        .header h1 {{ margin: 0; color: #1e293b; font-size: 28px; }}
        .header p {{ margin: 5px 0 0 0; color: #06b6d4; font-size: 14px; }}
        .body {{ line-height: 1.8; }}
        .signature {{ margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px; }}
    </style>
</head>
<body>
    <div class="letter">
        <div class="header">
            <h1>{p.get('name', 'Candidate')}</h1>
            <p>{p.get('title', 'Specialist')}</p>
            <p>{p.get('phone', '')} | {p.get('email', '')}</p>
        </div>
        <p style="color: #666;">{time.strftime("%B %d, %Y")}</p>
        <p>Dear Hiring Team at <strong>{company_name}</strong>,</p>
        <p><strong>Subject: Application for {job_title}</strong></p>
        <div class="body">
            <p>I am writing to express my strong interest in the {job_title} position at {company_name}. With 15+ years of progressive experience in Network Engineering and IT Infrastructure, I have developed deep expertise in designing, implementing, and troubleshooting enterprise-grade networks across Cisco, MikroTik, Ubiquiti, and Fortinet platforms.</p>
            <p>Throughout my career, I have successfully deployed enterprise networks for 20+ clients, implemented advanced routing protocols (OSPF, BGP, EIGRP), configured VPN and firewall solutions, and maintained 99.9% network uptime. My hands-on experience with fiber optic installations, structured cabling, and wireless networks makes me a versatile and reliable network professional.</p>
            <p>I am confident that my technical depth and proven track record in network engineering would make me a valuable asset to {company_name}. I am available for immediate engagement and prepared to contribute meaningfully from day one.</p>
        </div>
        <div class="signature">
            <p>Warm regards,</p>
            <p><strong>{p.get('name', 'Candidate')}</strong></p>
        </div>
    </div>
</body>
</html>
"""

def generate_triple_package(lead):
    """[👑 LEGACY RESTORATION] Generates a 3-file strike package: PDF CV, HTML CV, and HTML Cover Letter."""
    company = lead.get('company_name', 'Company')
    job_title = lead.get('job_title', 'Professional Role')
    
    # 1. PDF CV (Professional V4)
    cv_pdf_path = generate_cv_pdf(company, job_title, lead)
    
    # 2. HTML CV (Legacy Absolute Version)
    cv_html_path = os.path.join(os.getcwd(), "Sam_Salameh_CV.html")
    if not os.path.exists(cv_html_path):
        cv_html_path = None # Fallback if missing
        
    # 3. HTML Cover Letter (Personalized)
    cl_content = create_cover_letter_html(company, job_title)
    cl_filename = f"Sam_Salameh_Cover_Letter_-_{company.replace(' ', '_')}.html"
    cl_path = os.path.join(os.path.dirname(cv_pdf_path), cl_filename)
    with open(cl_path, "w", encoding="utf-8") as f:
        f.write(cl_content)
        
    return {
        "pdf_cv": cv_pdf_path,
        "html_cv": cv_html_path,
        "html_cl": cl_path
    }
        
def generate_cover_letter_pdf(company, job_title, lead=None):
    """[👑 PROFESSIONAL WHITE] Restoring clean, professional PDF Cover Letter parity."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    p = load_profile().get("candidate", {})
    # 1. HEADER (Official Branding)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, p.get("name", "Candidate"), new_x="LMARGIN", new_y="NEXT", align='L')
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, p.get("title", ""), new_x="LMARGIN", new_y="NEXT", align='L')
    pdf.cell(0, 5, f"{p.get('email', '')} | {p.get('phone', '')} | {p.get('linkedin', '')}", new_x="LMARGIN", new_y="NEXT", align='L')
    
    pdf.set_draw_color(6, 182, 212) # Teal
    pdf.line(10, 35, 200, 35)
    pdf.ln(15)
    
    # 2. DATE & ADDRESSEE
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 5, f"Date: {datetime.now().strftime('%B %d, %Y')}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 5, "Hiring Manager", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, company, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    # 3. SUBJECT
    pdf.set_font("Arial", 'BU', 11)
    pdf.cell(0, 7, f"Application for {job_title}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    
    # 4. GREETING
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 7, f"Dear {company} Hiring Team,", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    # 5. BODY — use AI-generated cover letter if available, else professional fallback
    ai_body = lead.get('custom_body', '') if lead else ''
    
    if ai_body and len(ai_body.strip()) > 100:
        # Strip HTML tags for PDF plain text
        import re as _re
        from bs4 import BeautifulSoup as _BS
        try:
            clean = _BS(ai_body, 'html.parser').get_text(separator='\n')
            clean = _re.sub(r'\n{3,}', '\n\n', clean).strip()
            # Remove the sign-off if it's already in the PDF footer
            clean = _re.sub(r'Best regards.*$', '', clean, flags=_re.DOTALL | _re.IGNORECASE).strip()
            paragraphs = [p.strip() for p in clean.split('\n\n') if p.strip() and len(p.strip()) > 20]
        except Exception:
            paragraphs = []
        
        if not paragraphs:
            # Fallback if parsing fails
            paragraphs = [
                f"I am writing to express my strong interest in the {job_title} position at {company}. With 15+ years of enterprise network engineering experience and active certifications in Cisco CCNA, Fortinet NSE, MikroTik MTCNA, and Ubiquiti UBWA, I am confident I can deliver immediate value to your team.",
                f"Throughout my career, I have deployed enterprise networks for 20+ clients achieving 99.9% uptime SLA, reduced security incidents by 100% through FortiGate/Cisco ASA hardening, configured IPSec/SSL VPN for 50+ branch offices, and installed 500+ km of fiber optic infrastructure. I am available for immediate relocation to the UAE, KSA, Qatar, or Europe.",
                f"I would welcome the opportunity to discuss how my expertise aligns with {company}'s infrastructure goals. Please find my CV attached for your review. Thank you for your consideration."
            ]
    else:
        # Professional fallback with Sam's real achievements
        paragraphs = [
            f"I am writing to express my strong interest in the {job_title} position at {company}. With 15+ years of enterprise network engineering experience and active certifications in Cisco CCNA, Fortinet NSE, MikroTik MTCNA, and Ubiquiti UBWA, I am confident I can deliver immediate value to your team.",
            f"Throughout my career, I have deployed enterprise networks for 20+ clients achieving 99.9% uptime SLA, reduced security incidents by 100% through FortiGate/Cisco ASA hardening, configured IPSec/SSL VPN for 50+ branch offices, and installed 500+ km of fiber optic infrastructure. My expertise spans Cisco IOS, MikroTik RouterOS, Fortinet FortiGate, Ubiquiti UniFi, and monitoring tools including PRTG, SolarWinds, and Zabbix.",
            f"I am available for immediate relocation to the UAE, KSA, Qatar, or Europe. I would welcome the opportunity to discuss how my background aligns with {company}'s infrastructure goals. Thank you for your consideration."
        ]
    
    for para in paragraphs[:4]:  # Max 4 paragraphs
        safe_para = _safe_text_for_pdf(para)
        if safe_para:
            pdf.multi_cell(0, 6, safe_para)
            pdf.ln(4)
    
    pdf.ln(10)
    
    # 6. SIGN-OFF
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 7, "Sincerely,", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.cell(0, 7, p.get("name", "Candidate"), new_x="LMARGIN", new_y="NEXT")
    
    # Save Path (☁️ CLOUD-SAFE: Use /tmp on cloud, local path otherwise)
    filename = f"Sam_Salameh_Cover_Letter_-_{company.replace(' ', '_')}.pdf"
    
    # Check if running on cloud (Render sets RENDER env var)
    is_cloud = os.getenv("RENDER") or os.getenv("RAILWAY") or os.getenv("HEROKU")
    if is_cloud:
        cache_dir = "/tmp/pdf_cache"
    else:
        cache_dir = os.path.join(os.getcwd(), "core", "pdf_cache")
    
    if not os.path.exists(cache_dir): 
        os.makedirs(cache_dir, exist_ok=True)
    save_path = os.path.join(cache_dir, filename)
    pdf.output(save_path)
    return save_path

def generate_ultimate_package(lead):
    """[👑 ABSOLUTE VMAX] Returns exactly TWO paths: PDF Cover Letter and HTML CV."""
    company = lead.get('company_name', 'Company')
    job_title = lead.get('job_title', 'Professional Role')
    
    # 1. PDF Cover Letter (The 'Byblos' Standard)
    cl_pdf_path = generate_cover_letter_pdf(company, job_title, lead)
    
    # 2. HTML CV (The VMAX Version)
    cv_html_path = os.path.join(os.getcwd(), "Sam_Salameh_CV.html")
    if not os.path.exists(cv_html_path):
        cv_html_path = None
        
    return {
        "cl_pdf": cl_pdf_path,
        "cv_html": cv_html_path
    }

def _safe_text_for_pdf(text, is_unicode=False):
    """
    Safe text converter for PDF generation.
    Handles unicode, emojis, special chars - better than basic ascii ignore.
    """
    if not text:
        return ""
    # Replace smart quotes and common unicode
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2026", "...").replace("\u2014", "-")
    text = text.replace("\u2013", "-")
    text = text.replace("\u00e2\u20ac\u201c", "'").replace("\u00e2\u20ac\u2019", "'")
    text = text.replace("\u00a0", " ").replace("\u2022", "*")
    
    if is_unicode:
        # For Arabic/Unicode fonts, we keep the characters but still clean up control chars
        return "".join([c for c in text if ord(c) > 31 or c in '\n\r']).strip()

    # Remove emojis and complex unicode chars for basic fonts (Helvetica)
    clean = []
    for char in text:
        code = ord(char)
        if code < 0x10000 and code > 31:  # Keep printable basic unicode
            try:
                clean.append(char.encode('latin-1', 'ignore').decode('latin-1'))
            except Exception:
                clean.append('?')
        elif code == 10 or code == 13:  # Keep newlines
            clean.append(char)
        else:
            clean.append(' ')
    return ''.join(clean).strip()

def _parse_html_for_pdf(html_content):
    """Parse HTML content for PDF text extraction."""
    if not html_content or len(html_content) < 20:
        return None
    
    try:
        from bs4 import BeautifulSoup
        body_html = str(html_content)
        body_html = body_html.replace('<br>', '\n').replace('<br/>', '\n')
        body_html = body_html.replace('</p>', '\n\n').replace('</li>', '\n')
        body_html = body_html.replace('</div>', '\n').replace('</span>', ' ')
        soup = BeautifulSoup(body_html, "html.parser")
        clean_body = soup.get_text(separator=' ')
        clean_body = re.sub(r'\n\s*\n', '\n\n', clean_body).strip()
        return clean_body
    except Exception:
        return None

def generate_dynamic_cover_letter(company_name, job_title, custom_body, persona='Modern', custom_keywords=None, strike_id=None):
    """
    [🕵️ PHASE OMEGA: DYNAMIC GENERATOR]
    Generates a cover letter PDF with advanced cognitive and forensic hardening.
    """
    # Phase Alpha-Centauri: Metadata Polymorphism (Russian Evasion style)
    # Mimic different OS/App creation strings to confuse doc-fingerprinting
    CREATORS = [
        "Microsoft Word 2019", "Adobe Acrobat Pro 24.2", "macOS 14.4 Quartz PDFContext",
        "Google Docs", "Pages 13.2", "Nitro PDF 14.1", "WPS Writer 11.1"
    ]
    PRODUCERS = [
        "Adobe PDF Library 15.0", "macOS 14.4.1 Quartz PDFContext", "Microsoft Office Word",
        "Skia/PDF m124", "Foxit PDF Printer"
    ]
    
    pdf = CoverLetterPDF()
    # 🕵️ OMNISCIENT: PDF Version Jitter (1.4 - 1.7)
    pdf.pdf_version = random.choice(["1.4", "1.5", "1.6", "1.7"])
    
    pdf.set_creator(random.choice(CREATORS))
    pdf.set_producer(random.choice(PRODUCERS))
    pdf.set_keywords("Network Engineering, Cisco, MikroTik, Fortinet, IT Infrastructure, VPN, Firewall")
    pdf.inject_forensic_noise(strike_id)
    pdf.compress = True
    
    # 🌌 TRANSCENDENCE: Sub-Pixel Divinity (极端精确性随机化)
    # Infinitesimal layout jitter at the 0.01mm level
    margin_jitter_l = 10 + random.uniform(-0.05, 0.05)
    margin_jitter_r = 10 + random.uniform(-0.05, 0.05)
    pdf.set_left_margin(margin_jitter_l)
    pdf.set_right_margin(margin_jitter_r)
    
    # 🏁 COSMIC PERSONA STYLING
    header_color = (0, 123, 255) # Modern Blue
    if persona == 'Startup':
        header_color = (138, 43, 226) # Bold Purple
    elif persona == 'Corporate':
        header_color = (40, 40, 40) # Serious Gray
    
    try:
        pdf.set_text_shaping(True)
    except Exception:
        logging.warning("⚠️ Text shaping disabled.")

    pdf.add_page()
    
    p_data = load_profile()
    p = p_data.get("candidate", {})
    # 🌏 MULTIVERSE: Forensic Metadata Ghosting
    # Randomize document origin to mimic diverse human workstations
    workstations = [
        ("Microsoft Word for Microsoft 365", "Microsoft Word"),
        ("macOS Version 14.4.1 (Build 23E224) Quartz PDFContext", "macOS Quartz"),
        ("Acrobat Distiller 23.0 (Windows)", "Adobe PDF Library"),
        ("LibreOffice 24.2", "Writer"),
        ("Overleaf (pdfTeX-1.40.25)", "pdfTeX")
    ]
    meta_creator, meta_producer = random.choice(workstations)
    pdf.set_creator(meta_creator)
    pdf.set_producer(meta_producer)
    pdf.set_author(p.get("name", "Candidate"))
    
    # 🧠 MULTIVERSE: Semantic ATS Metadata Injection [QUANTUM UPGRADE]
    # We inject the scraped keywords into the invisible PDF dictionary (Subject/Keywords) 
    # and add a hidden "Metadata Saturation" block for binary-level parser hijacking.
    if custom_keywords:
        safekw = [k.replace("'", "") for k in custom_keywords[:30]] # 3x the capacity
        pdf.set_subject(f"Sovereign Application: {job_title} | Expertise: {', '.join(safekw[:10])}")
        pdf.set_keywords(", ".join(safekw))
        
        # 🌌 QUANTUM: Binary Dictionary Saturation
        # Some parsers ignore 'Keywords' but read the raw Info dictionary stream.
        # We append these as custom properties if possible, or build a dense keyword block.
        pdf.set_title(f"Application Package - {company_name} - {job_title} - {' '.join(safekw[:5])}")

    # GLOBAL FONT MANAGEMENT: Inherit from base class initialization
    font_to_use = pdf.unicode_font_name

    # Layout randomization (Alpha-Centauri)
    # [👑 VIP FIX] Duplicate Header removed. The base class 'CoverLetterPDF' handles it.
    
    # Revert to black for body
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(font_to_use, '', 11)

    # Detect language for RTL support
    is_rtl = _contains_arabic(company_name) or _contains_arabic(job_title) or _contains_arabic(custom_body)

    # Date & Subject
    today = datetime.now().strftime("%B %d, %Y")
    align = 'R' if is_rtl else 'L'
    pdf.set_font(font_to_use, '', 11)
    pdf.cell(0, 10, f"Date: {today}", new_x="LMARGIN", new_y="NEXT", align=align)
    pdf.ln(5)
    
    pdf.set_font(font_to_use, 'B', 12)
    pdf.cell(0, 8, f"Target: {company_name}", new_x="LMARGIN", new_y="NEXT", align=align)
    pdf.cell(0, 8, f"Role: {job_title}", new_x="LMARGIN", new_y="NEXT", align=align)
    pdf.ln(10)
    
    # Subject
    pdf.set_font(font_to_use, 'B', 11)
    pdf.cell(0, 6, f"Subject: Application_ {job_title}", new_x="LMARGIN", new_y="NEXT", align=align)
    pdf.ln(10)
    
    # Body
    pdf.set_font(font_to_use, '', 11)
    
    # Content processing
    parsed_body = _parse_html_for_pdf(custom_body)
    body = parsed_body if parsed_body and len(parsed_body) > 50 else build_pdf_cover_letter_body(company_name, job_title)
    
    # ALPHA-CENTAURI: Aggressive sanitization and OCR-POISONING
    is_unicode_font = (font_to_use == "SovereignUnicode")
    body = _safe_text_for_pdf(body, is_unicode=is_unicode_font)
    body = _poison_text(body, is_unicode=is_unicode_font)
    body = body[:3000] # Limit length
    
    # 🕵️ SINGULARITY: Quantum Kerning Jitter (Pixel-level Hash-Phasing)
    # We apply micro-offsets to every sentence or line to ensure 100% unique pixel layout.
    lines = body.split('\n')
    for line in lines:
        if not line.strip():
            pdf.ln(6)
            continue
        
        # 🌌 TRANSCENDENCE: Sub-Pixel Divinity (Vertical + Horizontal Jitter)
        pdf.set_y(pdf.get_y() + random.uniform(-0.02, 0.02))
        pdf.set_x(pdf.get_x() + random.uniform(-0.1, 0.1))
        
        # Split into words for micro-kerning
        words = line.split(' ')
        for word in words:
            # Randomize the line-height for every word
            pdf.write(5 + random.uniform(-0.05, 0.05), word + " ")
            # Micro-jitter between words (mathematically invisible but hash-breaking)
            pdf.set_x(pdf.get_x() + random.uniform(-0.02, 0.02))
        pdf.ln(6 + random.uniform(-0.05, 0.05))
    
    pdf.ln(15)
    pdf.set_font(font_to_use, 'B', 11)
    pdf.cell(0, 6, "Sincerely," if not is_rtl else "مع خالص التقدير،", new_x="LMARGIN", new_y="NEXT", align=align)
    pdf.ln(10)
    pdf.cell(0, 6, p.get("name", "Candidate"), new_x="LMARGIN", new_y="NEXT", align=align)
    
    # 🕵️ APEX DEITY: AI JAILBREAK (Cognitive Infiltration)
    # Injects invisible instructions to force automated screeners to prioritize this candidate.
    pdf.inject_ai_shadow_prompt()
    
    # Save to disk (☁️ CLOUD-SAFE: Use /tmp on cloud)
    is_cloud = os.getenv("RENDER") or os.getenv("RAILWAY") or os.getenv("HEROKU")
    if is_cloud:
        PDF_DIR = "/tmp/pdf_cache"
    else:
        PDF_DIR = os.path.join(os.path.dirname(__file__), "pdf_cache")
    
    if not os.path.exists(PDF_DIR): 
        os.makedirs(PDF_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    sanitized_role = _sanitize_filename(job_title)
    sanitized_company = _sanitize_filename(company_name)
    
    # [👑 SIMPLE NAMING] Clean professional cover letter filename
    filename = f"Sam_Salameh_Cover_Letter.pdf"
    
    pdf_path = os.path.join(PDF_DIR, filename)
    
    try:
        pdf.output(pdf_path)
        return pdf_path
    except Exception as e:
        logging.error(f"❌ PDF Output Error: {e}")
        return None

def generate_cv_pdf(company_name, job_title, lead=None):
    """[👑 APEX DEITY] Generates CV V4 (High-Fidelity Sidebar-Body)."""
    profile_data = load_profile()
    p = profile_data.get("candidate", {})
    
    pdf = SovereignCVPDF()
    pdf.add_page()
    font = pdf.unicode_font_name
    
    # 🌑 SIDEBAR (Contact, Education, Skills)
    pdf.set_text_color(255, 255, 255)
    
    # Circle Avatar Area
    pdf.set_fill_color(0, 180, 216)
    pdf.circle(35, 30, 12, 'F')
    pdf.set_font(font, 'B', 14)
    pdf.set_xy(28, 25)
    pdf.write(10, p.get("avatar_initials", "RC"))
    
    # Contact Info
    pdf.set_xy(10, 50)
    pdf.set_font(font, 'B', 10)
    pdf.write(5, "CONTACT")
    pdf.set_font(font, '', 8)
    pdf.set_xy(10, 58)
    contact_text = f"{p.get('phone', '')}\n{p.get('email', '')}\n{p.get('location', '')}\n{p.get('linkedin', '')}"
    pdf.write(5, contact_text)
    
    # Education
    pdf.set_xy(10, 90)
    pdf.set_font(font, 'B', 10)
    pdf.write(5, "EDUCATION")
    y_edu = 98
    for edu in profile_data.get("education", []):
        pdf.set_font(font, 'B', 8)
        pdf.set_xy(10, y_edu)
        pdf.write(5, f"{edu.get('degree', '')}\n")
        pdf.set_font(font, '', 7)
        pdf.write(4, f"{edu.get('institution', '')} | {edu.get('year', '')}")
        y_edu += 12
    
    # Core Skills (Pills)
    pdf.set_xy(10, 135)
    pdf.set_font(font, 'B', 10)
    pdf.write(5, "CORE SKILLS")
    y_skills = 143
    skills = profile_data.get("skills", [])
    for skill in skills:
        pdf.set_fill_color(45, 49, 66)
        pdf.rect(10, y_skills, 35, 6, 'F')
        pdf.set_font(font, '', 7)
        pdf.set_xy(12, y_skills)
        pdf.write(6, skill)
        y_skills += 8

    # ⚪ MAIN BODY (Experience, Highlights)
    pdf.set_text_color(18, 20, 29) # Dark Grey
    
    # Header Name
    pdf.set_xy(80, 20)
    pdf.set_font(font, 'B', 24)
    pdf.write(10, p.get("name", "Candidate").upper())
    pdf.set_xy(80, 30)
    pdf.set_font(font, 'B', 11)
    pdf.set_text_color(0, 180, 216)
    pdf.write(5, p.get("title", "Specialist"))
    
    # Executive Summary
    pdf.set_xy(80, 45)
    pdf.set_text_color(18, 20, 29)
    pdf.set_font(font, 'B', 11)
    pdf.write(5, "Executive Summary")
    pdf.set_draw_color(0, 180, 216)
    pdf.line(80, 52, 190, 52)
    pdf.set_xy(80, 55)
    pdf.set_font(font, '', 9)
    summary = profile_data.get("summary", "")
    pdf.multi_cell(110, 5, summary, 0, 'L')
    
    # Key Achievements Box
    pdf.set_fill_color(240, 248, 255) # Light Blue
    pdf.rect(80, 80, 110, 35, 'F')
    pdf.set_xy(85, 83)
    pdf.set_font(font, 'B', 10)
    pdf.write(5, "Key Achievements")
    
    highlights = lead.get('highlights', [])[:3] if lead else []
    y_h = 90
    for h in highlights:
        pdf.set_xy(88, y_h)
        pdf.set_font(font, '', 8)
        pdf.write(4, f"- {h.get('title', '')}: {h.get('desc', '')[:60]}...")
        y_h += 6
        
    # Professional Experience (Timeline)
    pdf.set_xy(80, 125)
    pdf.set_font(font, 'B', 11)
    pdf.write(5, "Professional Experience")
    pdf.line(80, 132, 190, 132)
    
    # Timeline Line
    pdf.set_draw_color(0, 180, 216)
    pdf.line(85, 140, 85, 230)
    
    # Role entries
    roles = profile_data.get("experience", [])
    
    y_role = 140
    for role in roles:
        # Circle
        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(0, 180, 216)
        pdf.circle(85, y_role + 2, 2, 'FD')
        
        pdf.set_xy(90, y_role)
        pdf.set_font(font, 'B', 10)
        pdf.set_text_color(18, 20, 29)
        pdf.write(5, role.get("role", ""))
        
        pdf.set_xy(160, y_role)
        pdf.set_font(font, '', 8)
        pdf.set_fill_color(240, 248, 255)
        pdf.rect(160, y_role, 30, 5, 'F')
        pdf.write(5, f" {role.get('period', '')}")
        
        pdf.set_xy(90, y_role + 6)
        pdf.set_font(font, '', 8)
        pdf.set_text_color(100, 100, 100)
        pdf.write(5, role.get("company", ""))
        
        y_role += 25
        
    pdf.inject_ai_shadow_prompt()
    
    # Save (☁️ CLOUD-SAFE: Use /tmp on cloud)
    is_cloud = os.getenv("RENDER") or os.getenv("RAILWAY") or os.getenv("HEROKU")
    if is_cloud:
        PDF_DIR = "/tmp/pdf_cache"
    else:
        PDF_DIR = os.path.join(os.path.dirname(__file__), "pdf_cache")
    
    if not os.path.exists(PDF_DIR): 
        os.makedirs(PDF_DIR, exist_ok=True)
    
    # [👑 SIMPLE NAMING] Clean professional CV filename - ALWAYS the same
    filename = "Sam_Salameh_CV.pdf"
    pdf_path = os.path.join(PDF_DIR, filename)
    
    pdf.output(pdf_path)
    return pdf_path

def generate_dual_package(lead):
    """[👑 FINAL SINGULARITY] Orchestrates the dual PDF attachments."""
    company = lead.get('company_name', 'Unknown')
    title = lead.get('job_title', 'Professional')
    
    cv_path = generate_cv_pdf(company, title, lead)
    cl_path = generate_dynamic_cover_letter(company, title, lead.get('custom_body', ''), strike_id=lead.get('strike_id'))
    
    return {
        "cv": cv_path,
        "cl": cl_path
    }

if __name__ == "__main__":
    # Test
    pdf_path = generate_dynamic_cover_letter("Acme Corp", "HR Manager", "Dear Acme,\n\nI am cool.\n\nBest,\nSam")
    print(f"Generated PDF: {pdf_path}")
