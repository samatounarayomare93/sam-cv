"""
SAM EMAIL PREVIEW GENERATOR
============================
Generate what Sam would send to companies - Preview Only
"""

import os
import sys
import json
from datetime import datetime

def generate_sam_email():
    """Generate complete Sam application email preview"""
    
    job_title = "HR & Operations Manager"
    company_name = "Sample Company LLC"
    location = "Dubai, UAE"
    
    # ============================================
    # EMAIL HEADER
    # ============================================
    email_header = f"""
TO: hr@[company].com
FROM: sam.dev1@outlook.com
SUBJECT: Application for {job_title} - Sam Salameh
DATE: {datetime.now().strftime('%A, %B %d, %Y')}
    """
    
    # ============================================
    # EMAIL BODY
    # ============================================
    email_body = f"""
Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position 
at {company_name}. With my extensive background in Human Resources and 
Operations Management, I am confident that I can make a significant 
contribution to your team.

═══════════════════════════════════════════════════════════════
PROFESSIONAL SUMMARY
═══════════════════════════════════════════════════════════════

• Results-driven HR professional with proven expertise in talent 
  acquisition, employee relations, and organizational development
• Skilled in implementing efficient HR systems and processes that 
  drive productivity and employee satisfaction
• Strong communication and interpersonal abilities
• Experience in GCC/MENA region with multinational corporations

═══════════════════════════════════════════════════════════════
KEY QUALIFICATIONS
═══════════════════════════════════════════════════════════════

✓ Recruitment & Selection: End-to-end hiring, screening, onboarding
✓ Employee Relations: Conflict resolution, performance management
✓ Operations Management: Office administration, vendor management
✓ Training & Development: Staff training and professional development
✓ HRIS & Technology: Proficient in HR management systems

═══════════════════════════════════════════════════════════════
PROFESSIONAL EXPERIENCE
═══════════════════════════════════════════════════════════════

HR & Operations Coordinator
Sam Consulting - Beirut, Lebanon | 2020 - Present

• Oversee all HR functions including recruitment, onboarding, 
  and employee documentation
• Manage daily office operations and vendor relationships
• Implement cost-saving initiatives (25% reduction in expenses)
• Develop and deliver training programs for staff development

Administrative Manager
ABC Corporation - Beirut, Lebanon | 2018 - 2020

• Led administrative team of 5 staff members
• Streamlined onboarding (30% reduction in time-to-hire)
• Managed payroll processing and benefits administration
• Coordinated inter-departmental projects

═══════════════════════════════════════════════════════════════
EDUCATION & CERTIFICATIONS
═══════════════════════════════════════════════════════════════

• Bachelor's Degree in Business Administration
• SHRM-CP Certification (in progress)
• Microsoft Office Specialist Certification
• Fluent in English, Arabic, and French

═══════════════════════════════════════════════════════════════
WHY {company_name.upper()}?
═══════════════════════════════════════════════════════════════

I am particularly drawn to {company_name} because of your reputation 
for excellence and commitment to employee development. I would welcome 
the opportunity to discuss how my skills and experience align with 
your organization's needs.

I am available for immediate relocation to {location} and prepared to 
contribute meaningfully from day one.

═══════════════════════════════════════════════════════════════
CONTACT INFORMATION
═══════════════════════════════════════════════════════════════

Name:     Sam Salameh
Email:    sam.dev1@outlook.com
Phone:    +961 76 005 412 (WhatsApp)
LinkedIn: linkedin.com/in/samcordahi
Location: Beirut, Lebanon (Open to Relocation)

═══════════════════════════════════════════════════════════════
"""

    return email_header + "\n" + email_body

def generate_html_preview():
    """Generate HTML version of the email"""
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Sam Application Email Preview</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            background: #f0f2f5;
            padding: 20px;
        }
        .email-container {
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 32px;
            font-weight: 600;
        }
        .header p {
            margin: 10px 0 0 0;
            font-size: 16px;
            opacity: 0.9;
        }
        .content {
            padding: 40px;
            background: white;
        }
        .section {
            background: #f8f9fa;
            padding: 25px;
            margin: 20px 0;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        .section h2 {
            color: #667eea;
            margin-top: 0;
            font-size: 18px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .section ul {
            margin: 0;
            padding-left: 20px;
        }
        .section li {
            margin: 8px 0;
            line-height: 1.6;
        }
        .skills {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .skill {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 13px;
        }
        .experience {
            background: white;
            border: 1px solid #e0e0e0;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
        }
        .experience h3 {
            color: #333;
            margin: 0 0 10px 0;
        }
        .experience .company {
            color: #667eea;
            font-weight: 600;
        }
        .experience .date {
            color: #999;
            font-size: 14px;
        }
        .contact-box {
            background: linear-gradient(135deg, #333 0%, #1a1a1a 100%);
            color: white;
            padding: 30px;
            text-align: center;
            margin-top: 30px;
            border-radius: 10px;
        }
        .contact-box h2 {
            color: white;
            margin: 0 0 20px 0;
        }
        .contact-info {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 30px;
        }
        .contact-item {
            text-align: center;
        }
        .contact-item strong {
            display: block;
            font-size: 18px;
            margin-bottom: 5px;
        }
        .contact-item span {
            opacity: 0.8;
            font-size: 14px;
        }
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 12px;
        }
        .meta-info {
            background: #fff3cd;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border: 1px solid #ffc107;
        }
        .meta-info strong {
            color: #856404;
        }
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>Sam Salameh</h1>
            <p>HR & Operations Professional | Open to GCC Relocation</p>
            <p>+961 76 005 412 | sam.dev1@outlook.com</p>
        </div>
        
        <div class="content">
            <div class="meta-info">
                <strong>This is a PREVIEW of what Sam sends to companies.</strong><br>
                To actually send this email, configure Gmail in .env file.
            </div>
            
            <h2 style="color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px;">
                Application for HR & Operations Manager
            </h2>
            
            <p>Dear Hiring Manager,</p>
            
            <p>I am writing to express my strong interest in the <strong>HR & Operations Manager</strong> 
            position. With my extensive background in Human Resources and Operations Management, 
            I am confident that I can make a significant contribution to your team.</p>
            
            <div class="section">
                <h2>Professional Summary</h2>
                <ul>
                    <li>Results-driven HR professional with proven expertise in talent acquisition, 
                        employee relations, and organizational development</li>
                    <li>Skilled in implementing efficient HR systems and processes that drive 
                        productivity and employee satisfaction</li>
                    <li>Strong communication and interpersonal abilities with collaborative 
                        approach to problem-solving</li>
                    <li>Experience in GCC/MENA region with multinational corporations</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>Key Qualifications</h2>
                <div class="skills">
                    <span class="skill">Recruitment & Selection</span>
                    <span class="skill">Employee Relations</span>
                    <span class="skill">Operations Management</span>
                    <span class="skill">Training & Development</span>
                    <span class="skill">HRIS & Technology</span>
                    <span class="skill">Performance Management</span>
                    <span class="skill">Policy Development</span>
                    <span class="skill">Vendor Management</span>
                </div>
            </div>
            
            <div class="section">
                <h2>Professional Experience</h2>
                
                <div class="experience">
                    <h3>HR & Operations Coordinator</h3>
                    <p><span class="company">Sam Consulting</span> | <span class="date">2020 - Present</span></p>
                    <ul>
                        <li>Oversee all HR functions including recruitment, onboarding, and employee documentation</li>
                        <li>Manage daily office operations and vendor relationships</li>
                        <li>Implement cost-saving initiatives resulting in 25% reduction in operational expenses</li>
                        <li>Develop and deliver training programs for staff development</li>
                    </ul>
                </div>
                
                <div class="experience">
                    <h3>Administrative Manager</h3>
                    <p><span class="company">ABC Corporation</span> | <span class="date">2018 - 2020</span></p>
                    <ul>
                        <li>Led administrative team of 5 staff members</li>
                        <li>Streamlined onboarding processes reducing time-to-hire by 30%</li>
                        <li>Managed payroll processing and benefits administration</li>
                    </ul>
                </div>
            </div>
            
            <div class="section">
                <h2>Education & Certifications</h2>
                <ul>
                    <li><strong>Bachelor's Degree</strong> in Business Administration</li>
                    <li><strong>SHRM-CP Certification</strong> (in progress)</li>
                    <li><strong>Microsoft Office Specialist</strong> Certification</li>
                    <li>Fluent in <strong>English, Arabic, and French</strong></li>
                </ul>
            </div>
            
            <p>I am particularly drawn to your organization because of your reputation for 
            excellence and commitment to employee development. I would welcome the opportunity 
            to discuss how my skills and experience align with your needs.</p>
            
            <p>I am available for immediate relocation and prepared to contribute meaningfully 
            from day one. My enclosed CV provides additional details about my professional background.</p>
            
            <p>Thank you for considering my application. I look forward to the opportunity 
            to discuss this position further.</p>
            
            <p style="margin-top: 30px;">Warm regards,<br><strong>Sam Salameh</strong></p>
            
            <div class="contact-box">
                <h2>Contact Information</h2>
                <div class="contact-info">
                    <div class="contact-item">
                        <strong>Email</strong>
                        <span>sam.dev1@outlook.com</span>
                    </div>
                    <div class="contact-item">
                        <strong>Phone</strong>
                        <span>+961 76 005 412</span>
                    </div>
                    <div class="contact-item">
                        <strong>WhatsApp</strong>
                        <span>+961 76 005 412</span>
                    </div>
                    <div class="contact-item">
                        <strong>LinkedIn</strong>
                        <span>linkedin.com/in/samcordahi</span>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            This email was generated by SAM Job Automator | Open to Relocation - GCC/MENA
        </div>
    </div>
</body>
</html>"""
    return html

def main():
    print("\n" + "="*70)
    print("SAM EMAIL PREVIEW GENERATOR")
    print("="*70)
    
    # Generate plain text version
    text_email = generate_sam_email()
    
    # Generate HTML version
    html_email = generate_html_preview()
    
    # Save plain text version
    with open("sam_email_preview.txt", 'w', encoding='utf-8') as f:
        f.write(text_email)
    print("\n[OK] Saved: sam_email_preview.txt")
    
    # Save HTML version
    with open("sam_email_preview.html", 'w', encoding='utf-8') as f:
        f.write(html_email)
    print("[OK] Saved: sam_email_preview.html")
    
    # Print preview to console
    print("\n" + "="*70)
    print("SAM EMAIL PREVIEW (Plain Text)")
    print("="*70)
    print(text_email)
    
    print("\n" + "="*70)
    print("NEXT STEPS TO SEND REAL EMAILS:")
    print("="*70)
    print("""
1. Open .env file and add your Gmail credentials:
   
   GMAIL_SMTP_USER=your-gmail@gmail.com
   GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx

2. To get Gmail App Password:
   - Go to: myaccount.google.com
   - Security > Enable 2-Step Verification
   - App passwords > Create new app password
   - Copy the 16-character password

3. Run: python send_test_email.py

4. Check your email (sam.dev1@hotmail.com) for the test email!
""")
    print("="*70)

if __name__ == "__main__":
    main()