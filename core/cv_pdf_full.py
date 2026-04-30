"""
Full Professional CV PDF Generator
Generates a complete 2-page CV matching the HTML design
"""
from fpdf import FPDF
import os

class ProfessionalCVPDF(FPDF):
    """Professional CV with sidebar layout"""
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        pass  # No header needed
        
    def footer(self):
        pass  # No footer needed

def generate_full_cv_pdf():
    """Generate complete professional CV PDF"""
    
    pdf = ProfessionalCVPDF()
    pdf.add_page()
    
    # ============================================================
    # SIDEBAR (Dark Blue Background)
    # ============================================================
    
    # Sidebar background
    pdf.set_fill_color(44, 62, 80)  # #2c3e50
    pdf.rect(0, 0, 70, 297, 'F')
    
    # Circle Avatar
    pdf.set_fill_color(52, 152, 219)  # #3498db
    pdf.circle(35, 30, 15, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_xy(25, 23)
    pdf.cell(20, 10, 'SS', align='C')
    
    # CONTACT Section
    pdf.set_xy(10, 55)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(52, 152, 219)
    pdf.cell(50, 6, 'CONTACT', ln=True)
    
    pdf.set_xy(10, 63)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(236, 240, 241)
    pdf.multi_cell(50, 5, '+961 70 841 1009\nsam.dev1@hotmail.com\nBeirut, Lebanon\nlinkedin.com/in/sam-salameh')
    
    # EDUCATION Section
    pdf.set_xy(10, 95)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(52, 152, 219)
    pdf.cell(50, 6, 'EDUCATION', ln=True)
    
    pdf.set_xy(10, 103)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_text_color(236, 240, 241)
    pdf.multi_cell(50, 4, 'B3 - Information Technology')
    pdf.set_xy(10, 110)
    pdf.set_font('Helvetica', '', 7)
    pdf.multi_cell(50, 4, 'Dekwene Technical School\n2016')
    
    # CORE SKILLS Section
    pdf.set_xy(10, 130)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(52, 152, 219)
    pdf.cell(50, 6, 'CORE SKILLS', ln=True)
    
    skills = [
        'Network Design', 'Cisco IOS', 'MikroTik RouterOS',
        'Ubiquiti UniFi', 'Fortinet', 'Fiber Optic',
        'Firewalls & VPN', 'Traffic Analysis'
    ]
    
    y_skill = 138
    for skill in skills:
        pdf.set_fill_color(52, 73, 94)  # #34495e
        pdf.rect(10, y_skill, 50, 6, 'F')
        pdf.set_xy(12, y_skill + 1)
        pdf.set_font('Helvetica', '', 7)
        pdf.set_text_color(236, 240, 241)
        pdf.cell(46, 4, skill)
        y_skill += 7
    
    # LANGUAGES Section
    pdf.set_xy(10, y_skill + 5)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(52, 152, 219)
    pdf.cell(50, 6, 'LANGUAGES', ln=True)
    
    pdf.set_xy(10, y_skill + 13)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(236, 240, 241)
    pdf.multi_cell(50, 5, 'English - Fluent\nArabic - Native\nFrench - Intermediate')
    
    # ============================================================
    # MAIN CONTENT (White Background)
    # ============================================================
    
    # Header
    pdf.set_xy(80, 20)
    pdf.set_font('Helvetica', 'B', 24)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(120, 10, 'SAM SALAMEH', ln=True)
    
    pdf.set_xy(80, 32)
    pdf.set_font('Helvetica', '', 14)
    pdf.set_text_color(52, 152, 219)
    pdf.cell(120, 8, 'Senior Network Engineer', ln=True)
    
    # Executive Summary
    pdf.set_xy(80, 50)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(120, 6, 'Executive Summary', ln=True)
    pdf.set_draw_color(52, 152, 219)
    pdf.line(80, 57, 200, 57)
    
    pdf.set_xy(80, 60)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(85, 85, 85)
    summary = (
        "Accomplished Network Engineer with 15+ years of progressive experience designing, "
        "implementing, configuring, and troubleshooting enterprise-grade networking infrastructure. "
        "Proven expertise in managing complex network environments, optimizing performance, and "
        "ensuring high availability across diverse platforms including Cisco, MikroTik, Ubiquiti, and Fortinet."
    )
    pdf.multi_cell(120, 4, summary)
    
    # Key Achievements Box
    pdf.set_xy(80, 85)
    pdf.set_fill_color(240, 248, 255)
    pdf.rect(80, 85, 120, 35, 'F')
    
    pdf.set_xy(82, 87)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(52, 152, 219)
    pdf.cell(116, 5, 'Key Achievements', ln=True)
    
    pdf.set_xy(82, 93)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(85, 85, 85)
    achievements = [
        "OPERATIONS LIFECYCLE: Proven expertise in managing high-volume network deployments",
        "SERVICE & RETENTION: A track record of resolving 50+ daily complex technical issues",
        "WORKFLOW OPTIMIZATION: Experience in standardizing network configurations"
    ]
    y_ach = 93
    for ach in achievements:
        pdf.set_xy(84, y_ach)
        pdf.multi_cell(114, 4, f"- {ach}")
        y_ach += 9
    
    # Professional Experience
    pdf.set_xy(80, 125)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(120, 6, 'Professional Experience', ln=True)
    pdf.line(80, 132, 200, 132)
    
    # Timeline line
    pdf.set_draw_color(52, 152, 219)
    pdf.line(85, 140, 85, 270)
    
    # Experience 1
    y_exp = 140
    
    # Circle
    pdf.set_fill_color(255, 255, 255)
    pdf.circle(85, y_exp, 2, 'FD')
    
    pdf.set_xy(90, y_exp - 2)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(80, 5, 'Freelance Network Engineer')
    
    pdf.set_xy(170, y_exp - 2)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_fill_color(240, 248, 255)
    pdf.rect(170, y_exp - 2, 28, 5, 'F')
    pdf.set_text_color(52, 152, 219)
    pdf.cell(28, 5, '2023 - Present', align='C')
    
    pdf.set_xy(90, y_exp + 4)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(127, 140, 141)
    pdf.cell(100, 4, 'Freelance, Beirut')
    
    pdf.set_xy(90, y_exp + 9)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(85, 85, 85)
    desc1 = "Providing comprehensive network engineering services to diverse clients including enterprise businesses, ISPs, and educational institutions. Specializing in network design, implementation, troubleshooting, and optimization across multiple vendor platforms."
    pdf.multi_cell(108, 4, desc1)
    
    # Bullet points for Experience 1
    pdf.set_xy(92, y_exp + 24)
    pdf.set_font('Helvetica', '', 7)
    bullets1 = [
        "Designed and deployed enterprise-grade networks for 20+ clients",
        "Implemented secure VPN solutions and firewall configurations",
        "Conducted network audits and performance optimization",
        "Provided 24/7 technical support and emergency response"
    ]
    y_bullet = y_exp + 24
    for bullet in bullets1:
        pdf.set_xy(92, y_bullet)
        pdf.multi_cell(106, 3, f"- {bullet}")
        y_bullet += 4
    
    # Experience 2
    y_exp = 195
    pdf.set_fill_color(255, 255, 255)
    pdf.circle(85, y_exp, 2, 'FD')
    
    pdf.set_xy(90, y_exp - 2)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(80, 5, 'Network Management Consultant')
    
    pdf.set_xy(170, y_exp - 2)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_fill_color(240, 248, 255)
    pdf.rect(170, y_exp - 2, 28, 5, 'F')
    pdf.set_text_color(52, 152, 219)
    pdf.cell(28, 5, '2021 - 2023', align='C')
    
    pdf.set_xy(90, y_exp + 4)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(127, 140, 141)
    pdf.cell(100, 4, 'Freelance, Beirut')
    
    pdf.set_xy(90, y_exp + 9)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(85, 85, 85)
    desc2 = "Consulted with organizations on network infrastructure planning, security implementations, and technology upgrades. Delivered strategic recommendations and hands-on technical solutions."
    pdf.multi_cell(108, 4, desc2)
    
    # Bullet points for Experience 2
    pdf.set_xy(92, y_exp + 22)
    pdf.set_font('Helvetica', '', 7)
    bullets2 = [
        "Managed network infrastructure for multiple concurrent projects",
        "Implemented advanced routing protocols (OSPF, BGP, EIGRP)",
        "Configured and maintained enterprise firewalls and security systems",
        "Trained technical teams on best practices and new technologies"
    ]
    y_bullet = y_exp + 22
    for bullet in bullets2:
        pdf.set_xy(92, y_bullet)
        pdf.multi_cell(106, 3, f"- {bullet}")
        y_bullet += 4
    
    # Experience 3
    y_exp = 250
    pdf.set_fill_color(255, 255, 255)
    pdf.circle(85, y_exp, 2, 'FD')
    
    pdf.set_xy(90, y_exp - 2)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(80, 5, 'Networking Technician')
    
    pdf.set_xy(170, y_exp - 2)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_fill_color(240, 248, 255)
    pdf.rect(170, y_exp - 2, 28, 5, 'F')
    pdf.set_text_color(52, 152, 219)
    pdf.cell(28, 5, '2010 - 2023', align='C')
    
    # Add second page for more details
    pdf.add_page()
    
    # Sidebar on page 2
    pdf.set_fill_color(44, 62, 80)
    pdf.rect(0, 0, 70, 297, 'F')
    
    # Technical Expertise on page 2
    pdf.set_xy(80, 20)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(120, 6, 'Technical Expertise', ln=True)
    pdf.line(80, 27, 200, 27)
    
    pdf.set_xy(80, 32)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(120, 5, 'Networking:', ln=True)
    pdf.set_xy(80, 37)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(85, 85, 85)
    pdf.multi_cell(120, 4, 'TCP/IP, VLAN, Routing & Switching, QoS, Network Security')
    
    pdf.set_xy(80, 48)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(120, 5, 'Platforms:', ln=True)
    pdf.set_xy(80, 53)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(85, 85, 85)
    pdf.multi_cell(120, 4, 'Cisco IOS, MikroTik RouterOS, Ubiquiti UniFi, Fortinet FortiGate')
    
    pdf.set_xy(80, 64)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(120, 5, 'Infrastructure:', ln=True)
    pdf.set_xy(80, 69)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(85, 85, 85)
    pdf.multi_cell(120, 4, 'Fiber Optic, Structured Cabling, Wireless Networks')
    
    pdf.set_xy(80, 80)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(120, 5, 'Security:', ln=True)
    pdf.set_xy(80, 85)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(85, 85, 85)
    pdf.multi_cell(120, 4, 'Firewalls, VPN (IPSec, SSL), Access Control, Intrusion Detection')
    
    # Save PDF
    is_cloud = os.getenv("RENDER") or os.getenv("RAILWAY") or os.getenv("HEROKU")
    if is_cloud:
        pdf_dir = "/tmp/pdf_cache"
    else:
        pdf_dir = os.path.join(os.path.dirname(__file__), "..", "core", "pdf_cache")
    
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir, exist_ok=True)
    
    pdf_path = os.path.join(pdf_dir, "Sam_Salameh_CV.pdf")
    pdf.output(pdf_path)
    
    return pdf_path

if __name__ == "__main__":
    # Test
    path = generate_full_cv_pdf()
    print(f"✅ Generated CV: {path}")
