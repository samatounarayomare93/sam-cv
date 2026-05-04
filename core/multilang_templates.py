"""
Multi-Language Email Templates
Arabic and English email templates
"""

from typing import Dict, Any

class MultiLanguageTemplates:
    """Email templates in multiple languages"""
    
    @staticmethod
    def detect_language(company: str, location: str, description: str) -> str:
        """Detect preferred language based on company/location"""
        text = f"{company} {location} {description}".lower()
        
        # Arabic indicators
        arabic_keywords = ["الشرق الأوسط", "العربية", "دبي", "السعودية", "لبنان"]
        if any(keyword in text for keyword in arabic_keywords):
            return "ar"
        
        # Lebanese/Gulf companies
        lebanese_domains = [".lb", "lebanon", "beirut", "tripoli"]
        gulf_domains = [".ae", ".sa", ".qa", ".kw", "dubai", "riyadh", "doha"]
        
        if any(domain in text for domain in lebanese_domains + gulf_domains):
            # Check if company is international or local
            international_keywords = ["international", "global", "worldwide", "multinational"]
            if any(keyword in text for keyword in international_keywords):
                return "en"
            return "ar"
        
        return "en"
    
    @staticmethod
    def get_subject_line(job_title: str, lang: str = "en") -> str:
        """Get subject line in specified language"""
        if lang == "ar":
            return f"طلب توظيف - {job_title} - Sam Salameh"
        else:
            return f"Application for {job_title} - Sam Salameh"
    
    @staticmethod
    def get_email_body(job: Dict[str, Any], lang: str = "en") -> str:
        """Get email body in specified language"""
        if lang == "ar":
            return MultiLanguageTemplates._get_arabic_template(job)
        else:
            return MultiLanguageTemplates._get_english_template(job)
    
    @staticmethod
    def _get_english_template(job: Dict[str, Any]) -> str:
        """English email template"""
        company = job.get("company", "Hiring Team")
        title = job.get("title", "the position")
        
        return f"""Dear {company} Hiring Team,

I am writing to express my strong interest in the {title} position at {company}.

With over 5 years of experience in network engineering and infrastructure management, I have developed a comprehensive skill set that aligns perfectly with your requirements. My expertise includes:

• Network Design & Implementation: Cisco, Juniper, Aruba
• Routing & Switching: BGP, OSPF, EIGRP, VLANs
• Network Security: Firewalls, VPNs, ACLs, IDS/IPS
• Cloud Networking: AWS, Azure, SD-WAN
• Monitoring & Troubleshooting: Wireshark, SolarWinds, Nagios
• Automation: Python, Ansible, Bash scripting

I am particularly drawn to this opportunity because it aligns with my career goals and allows me to contribute my technical expertise to your team's success.

I have attached my CV and cover letter for your review. I would welcome the opportunity to discuss how my background and skills can benefit {company}.

Thank you for considering my application. I look forward to hearing from you.

Best regards,
Sam Salameh
Senior Network Engineer

📧 samsalameh.cv@gmail.com
📱 +961 70 841 1009
🔗 linkedin.com/in/sam-salameh
"""
    
    @staticmethod
    def _get_arabic_template(job: Dict[str, Any]) -> str:
        """Arabic email template"""
        company = job.get("company", "فريق التوظيف")
        title = job.get("title", "الوظيفة")
        
        return f"""السادة المحترمون في {company}،

تحية طيبة وبعد،

أتقدم بطلبي هذا للتقدم لوظيفة {title} في شركتكم الموقرة.

أنا مهندس شبكات محترف مع خبرة تزيد عن 5 سنوات في تصميم وإدارة البنية التحتية للشبكات. أمتلك مهارات واسعة تشمل:

• تصميم وتنفيذ الشبكات: Cisco, Juniper, Aruba
• التوجيه والتبديل: BGP, OSPF, EIGRP, VLANs
• أمن الشبكات: Firewalls, VPNs, ACLs, IDS/IPS
• الشبكات السحابية: AWS, Azure, SD-WAN
• المراقبة وحل المشاكل: Wireshark, SolarWinds, Nagios
• الأتمتة: Python, Ansible, Bash

أنا مهتم بشدة بهذه الفرصة لأنها تتماشى مع أهدافي المهنية وتتيح لي المساهمة بخبرتي التقنية في نجاح فريقكم.

أرفق طياً سيرتي الذاتية ورسالة التغطية للاطلاع عليها. أرحب بفرصة مناقشة كيف يمكن لخلفيتي ومهاراتي أن تفيد {company}.

شاكراً لكم حسن اهتمامكم، وفي انتظار ردكم الكريم.

مع أطيب التحيات،
سام سلامة
مهندس شبكات أول

📧 samsalameh.cv@gmail.com
📱 +961 70 841 1009
🔗 linkedin.com/in/sam-salameh
"""
    
    @staticmethod
    def get_cover_letter_intro(job: Dict[str, Any], lang: str = "en") -> str:
        """Get cover letter introduction"""
        if lang == "ar":
            return f"""
# رسالة التغطية

## التقديم لوظيفة: {job.get('title', 'N/A')}
## الشركة: {job.get('company', 'N/A')}

السادة المحترمون،

أتقدم بطلبي هذا للتقدم لوظيفة {job.get('title', 'الوظيفة المعلن عنها')} في شركتكم الموقرة.
"""
        else:
            return f"""
# Cover Letter

## Application for: {job.get('title', 'N/A')}
## Company: {job.get('company', 'N/A')}

Dear Hiring Manager,

I am writing to express my strong interest in the {job.get('title', 'advertised position')} at {job.get('company', 'your company')}.
"""


def get_email_content(job: Dict[str, Any], auto_detect: bool = True) -> Dict[str, str]:
    """
    Get email content (subject + body) in appropriate language
    
    Returns:
        {
            "subject": "...",
            "body": "...",
            "language": "en" or "ar"
        }
    """
    templates = MultiLanguageTemplates()
    
    if auto_detect:
        lang = templates.detect_language(
            job.get("company", ""),
            job.get("location", ""),
            job.get("description", "")
        )
    else:
        lang = "en"
    
    return {
        "subject": templates.get_subject_line(job.get("title", "Position"), lang),
        "body": templates.get_email_body(job, lang),
        "language": lang
    }
