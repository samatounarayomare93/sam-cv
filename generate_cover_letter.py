"""
Generate personalized cover letter for each job application
"""
import os
from datetime import datetime

def generate_cover_letter(company_name, job_title, hiring_manager="Hiring Manager"):
    """Generate a professional cover letter matching the CV design"""
    
    today = datetime.now().strftime("%B %d, %Y")
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cover Letter - Sam Salameh</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 60px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            border-radius: 12px;
            position: relative;
            overflow: hidden;
        }}
        
        .container::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 6px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 3px solid #f0f0f0;
        }}
        
        .header h1 {{
            font-size: 32px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
            font-weight: 700;
        }}
        
        .header h2 {{
            font-size: 16px;
            color: #666;
            font-weight: 500;
        }}
        
        .contact-info {{
            text-align: center;
            font-size: 13px;
            color: #888;
            margin-top: 15px;
        }}
        
        .contact-info span {{
            margin: 0 10px;
        }}
        
        .date {{
            text-align: right;
            color: #666;
            font-size: 14px;
            margin-bottom: 30px;
        }}
        
        .recipient {{
            margin-bottom: 30px;
        }}
        
        .recipient p {{
            color: #444;
            font-size: 15px;
            line-height: 1.6;
        }}
        
        .salutation {{
            font-size: 16px;
            color: #333;
            margin-bottom: 25px;
            font-weight: 600;
        }}
        
        .body-text {{
            color: #444;
            font-size: 15px;
            line-height: 1.9;
            margin-bottom: 20px;
            text-align: justify;
        }}
        
        .highlight {{
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            padding: 20px;
            border-left: 4px solid #667eea;
            border-radius: 8px;
            margin: 25px 0;
        }}
        
        .highlight p {{
            color: #555;
            font-size: 14px;
            line-height: 1.8;
        }}
        
        .closing {{
            margin-top: 40px;
        }}
        
        .closing p {{
            color: #444;
            font-size: 15px;
            margin-bottom: 10px;
        }}
        
        .signature {{
            margin-top: 50px;
        }}
        
        .signature-name {{
            font-size: 20px;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 5px;
        }}
        
        .signature-title {{
            font-size: 14px;
            color: #666;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
                border-radius: 0;
                padding: 40px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>SAM SALAMEH</h1>
            <h2>Senior Network Engineer</h2>
            <div class="contact-info">
                <span>📱 +961 70 841 1009</span>
                <span>✉️ sam.dev1@hotmail.com</span>
                <span>📍 Beirut, Lebanon</span>
            </div>
        </div>
        
        <div class="date">{today}</div>
        
        <div class="recipient">
            <p><strong>{hiring_manager}</strong></p>
            <p><strong>{company_name}</strong></p>
            <p>Re: Application for <strong>{job_title}</strong> Position</p>
        </div>
        
        <div class="salutation">Dear {hiring_manager},</div>
        
        <p class="body-text">
            I am writing to express my strong interest in the <strong>{job_title}</strong> position at <strong>{company_name}</strong>. 
            With over 15 years of progressive experience in network engineering and infrastructure management, I am confident 
            that my technical expertise and proven track record make me an ideal candidate for this role.
        </p>
        
        <div class="highlight">
            <p>
                <strong>Why I'm a Perfect Fit:</strong><br><br>
                Throughout my career, I have successfully designed, implemented, and maintained enterprise-grade networking 
                solutions across diverse platforms including Cisco, MikroTik, Ubiquiti, and Fortinet. My experience spans 
                from hands-on technical implementation to strategic network planning and optimization.
            </p>
        </div>
        
        <p class="body-text">
            In my current role as a Freelance Network Engineer, I have delivered comprehensive networking solutions to over 
            20 clients, including enterprise businesses, ISPs, and educational institutions. I specialize in network design, 
            implementation, troubleshooting, and optimization, consistently achieving 100% uptime maintenance and exceeding 
            client expectations.
        </p>
        
        <p class="body-text">
            My technical proficiency includes advanced routing protocols (OSPF, BGP, EIGRP), VPN configurations, firewall 
            management, fiber optic installations, and traffic analysis. I have a proven track record of resolving 50+ daily 
            complex technical issues while maintaining strict SLA compliance and customer satisfaction.
        </p>
        
        <p class="body-text">
            What sets me apart is my ability to combine deep technical knowledge with strong problem-solving skills and 
            effective communication. I excel at translating complex technical concepts into actionable business solutions, 
            and I am committed to staying current with emerging technologies and industry best practices.
        </p>
        
        <p class="body-text">
            I am particularly drawn to <strong>{company_name}</strong> because of your reputation for innovation and excellence 
            in the industry. I am excited about the opportunity to contribute my expertise to your team and help drive your 
            network infrastructure initiatives forward.
        </p>
        
        <div class="closing">
            <p>
                I would welcome the opportunity to discuss how my experience and skills align with your needs. Thank you for 
                considering my application. I look forward to speaking with you soon.
            </p>
            <p style="margin-top: 20px;">Sincerely,</p>
        </div>
        
        <div class="signature">
            <div class="signature-name">Sam Salameh</div>
            <div class="signature-title">Senior Network Engineer</div>
        </div>
    </div>
</body>
</html>"""
    
    return html_content

def save_cover_letter(company_name, job_title, hiring_manager="Hiring Manager"):
    """Save cover letter as HTML file"""
    
    html_content = generate_cover_letter(company_name, job_title, hiring_manager)
    
    # Create cover letters directory
    cover_dir = "cover_letters"
    if not os.path.exists(cover_dir):
        os.makedirs(cover_dir)
    
    # Save HTML
    filename = f"Cover_Letter_{company_name.replace(' ', '_')}.html"
    filepath = os.path.join(cover_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Cover letter saved: {filepath}")
    return filepath

if __name__ == "__main__":
    # Test
    save_cover_letter("Future Tech Industries", "Lead Automation Engineer")
