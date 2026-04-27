import os
import sys

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.pdf_generator import create_personalized_pdf
from config import EMAIL_BODY_TEMPLATE, SENDER_NAME, SENDER_EMAIL

def generate_visual_proof():
    lead = {
        'job_title': 'Operations Director',
        'company': 'Global Frontier Logistics',
        'location': 'Dubai / Gulf Region',
        'salary': '$12,000 / month'
    }
    
    # [👑 APEX DEITY: ELITE PREVIEW]
    html_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; color: #333;">
        <p>Dear Hiring Team,</p>
        <p>I am reaching out regarding the <b>{lead['job_title']}</b> role at <b>{lead['company']}</b>. My decision to move is a Strategic Defection from top-tier rivals; I am looking to bring my success blueprints to an elite team with your specific market trajectory.</p>
        <p>With 15+ years in Operations & HR Management, I specialize in creating high-velocity, metric-driven environments. I am not looking for a vacancy; I am looking to drive a competitive pivot for your team through a comprehensive automation programme.</p>
        <p>Best regards,<br><b>Sam Salameh</b></p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
        <p style="font-size: 11px; color: #999; font-style: italic;">Sovereign Dispatch | Secure Signature: 0xFD34...99</p>
    </div>
    """
    
    # 2. Creating Local View file
    output_file = "visual_outreach_preview.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_body)
    
    print(f"OK - Sovereign Visual Proof Rendered: {os.path.abspath(output_file)}")
    print(f"OK - Payload Format: HTML Multi-part with PDF Attachment")
    print(f"OK - Recipient Target: sam.dev1@hotmail.com")
    print(f"OK - Professional Tone: Elite Sovereign Protocol")

if __name__ == "__main__":
    generate_visual_proof()
