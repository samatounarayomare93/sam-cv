"""
Interview Preparation AI
Prepares candidates for job interviews with AI-generated questions and answers
"""

import os
from typing import Dict, List, Any
import asyncio

class InterviewPreparationAI:
    """AI-powered interview preparation system"""
    
    def __init__(self):
        self.common_questions = {
            "network_engineer": [
                "Tell me about yourself and your experience in network engineering",
                "What is the difference between TCP and UDP?",
                "Explain the OSI model and its layers",
                "How do you troubleshoot network connectivity issues?",
                "What is VLAN and why is it used?",
                "Explain BGP and OSPF routing protocols",
                "How do you secure a network?",
                "What is your experience with firewalls and VPNs?",
                "Describe a challenging network problem you solved",
                "What network monitoring tools have you used?",
                "How do you handle network downtime?",
                "What is SD-WAN and its benefits?",
                "Explain subnetting and CIDR notation",
                "What is your experience with cloud networking (AWS/Azure)?",
                "How do you stay updated with networking technologies?",
            ],
            "behavioral": [
                "Why do you want to work for our company?",
                "What are your strengths and weaknesses?",
                "Describe a time you worked in a team",
                "How do you handle stress and pressure?",
                "Where do you see yourself in 5 years?",
                "Why are you leaving your current job?",
                "Tell me about a time you failed and what you learned",
                "How do you prioritize tasks?",
                "Describe your ideal work environment",
                "What motivates you?",
            ],
            "situational": [
                "What would you do if a critical server goes down at 3 AM?",
                "How would you handle a disagreement with a colleague?",
                "What if you're asked to implement a solution you disagree with?",
                "How would you explain a technical issue to a non-technical person?",
                "What would you do if you made a mistake that affected production?",
            ]
        }
        
        self.sample_answers = {
            "tell_me_about_yourself": """
I'm a Senior Network Engineer with over 5 years of experience in designing, implementing, 
and managing enterprise network infrastructure. I specialize in Cisco and Juniper technologies, 
with expertise in routing protocols (BGP, OSPF), network security, and cloud networking.

In my previous role, I managed a network serving 500+ users across multiple locations, 
implemented SD-WAN solutions, and reduced network downtime by 40% through proactive monitoring.

I'm passionate about network automation and have developed Python scripts to automate 
routine tasks, saving the team 10+ hours per week. I hold CCNP certification and 
continuously update my skills with the latest networking technologies.
""",
            "tcp_vs_udp": """
TCP (Transmission Control Protocol) is connection-oriented and provides reliable, 
ordered delivery of data with error checking and retransmission. It's used for applications 
requiring guaranteed delivery like HTTP, FTP, and email.

UDP (User Datagram Protocol) is connectionless and provides faster, but unreliable delivery 
without error checking. It's used for real-time applications like video streaming, VoIP, 
and online gaming where speed is more important than perfect delivery.

Key differences:
- TCP: Reliable, slower, connection-oriented, error checking
- UDP: Faster, unreliable, connectionless, no error checking
""",
            "network_troubleshooting": """
My systematic approach to network troubleshooting:

1. **Identify the problem**: Gather information from users and monitoring tools
2. **Check physical layer**: Verify cables, ports, and hardware status
3. **Test connectivity**: Use ping, traceroute, and telnet
4. **Check configurations**: Review router/switch configs, VLANs, ACLs
5. **Analyze logs**: Check system logs and SNMP traps
6. **Isolate the issue**: Narrow down to specific device or segment
7. **Implement solution**: Apply fix and test thoroughly
8. **Document**: Record the issue and resolution for future reference

I also use tools like Wireshark for packet analysis and SolarWinds for network monitoring.
"""
        }
    
    async def generate_interview_prep(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive interview preparation"""
        
        title = job.get("title", "").lower()
        company = job.get("company", "Unknown Company")
        description = job.get("description", "")
        
        prep = {
            "job_title": job.get("title"),
            "company": company,
            "technical_questions": [],
            "behavioral_questions": [],
            "situational_questions": [],
            "company_research": {},
            "questions_to_ask": [],
            "preparation_tips": []
        }
        
        # Technical questions
        prep["technical_questions"] = self.common_questions["network_engineer"]
        
        # Behavioral questions
        prep["behavioral_questions"] = self.common_questions["behavioral"]
        
        # Situational questions
        prep["situational_questions"] = self.common_questions["situational"]
        
        # Company research points
        prep["company_research"] = {
            "about": f"Research {company}'s history, mission, and values",
            "products": f"Understand {company}'s products/services",
            "news": f"Check recent news about {company}",
            "culture": f"Learn about {company}'s work culture",
            "competitors": f"Know {company}'s main competitors"
        }
        
        # Questions to ask interviewer
        prep["questions_to_ask"] = [
            "What does a typical day look like for this position?",
            "What are the biggest challenges facing the team right now?",
            "How do you measure success in this role?",
            "What opportunities are there for professional development?",
            "Can you describe the team I'll be working with?",
            "What is the company's approach to work-life balance?",
            "What are the next steps in the interview process?",
            f"What do you enjoy most about working at {company}?",
            "How does the company support employee growth?",
            "What technologies and tools does the team use?"
        ]
        
        # Preparation tips
        prep["preparation_tips"] = [
            "✅ Review your CV and be ready to discuss each point",
            "✅ Prepare specific examples of your achievements (STAR method)",
            "✅ Research the company thoroughly",
            "✅ Practice answering common questions out loud",
            "✅ Prepare questions to ask the interviewer",
            "✅ Test your internet connection and equipment (for virtual interviews)",
            "✅ Dress professionally",
            "✅ Arrive 10-15 minutes early (or log in early for virtual)",
            "✅ Bring copies of your CV and a notepad",
            "✅ Follow up with a thank-you email within 24 hours"
        ]
        
        return prep
    
    def format_prep_document(self, prep: Dict[str, Any]) -> str:
        """Format interview prep as readable document"""
        
        doc = f"""
# 🎤 Interview Preparation Guide

## Position: {prep['job_title']}
## Company: {prep['company']}

---

## 📋 Technical Questions to Prepare

"""
        for i, q in enumerate(prep['technical_questions'], 1):
            doc += f"{i}. {q}\n"
        
        doc += "\n---\n\n## 💼 Behavioral Questions\n\n"
        for i, q in enumerate(prep['behavioral_questions'], 1):
            doc += f"{i}. {q}\n"
        
        doc += "\n---\n\n## 🎯 Situational Questions\n\n"
        for i, q in enumerate(prep['situational_questions'], 1):
            doc += f"{i}. {q}\n"
        
        doc += "\n---\n\n## 🔍 Company Research Checklist\n\n"
        for key, value in prep['company_research'].items():
            doc += f"- [ ] {value}\n"
        
        doc += "\n---\n\n## ❓ Questions to Ask the Interviewer\n\n"
        for i, q in enumerate(prep['questions_to_ask'], 1):
            doc += f"{i}. {q}\n"
        
        doc += "\n---\n\n## ✅ Preparation Checklist\n\n"
        for tip in prep['preparation_tips']:
            doc += f"{tip}\n"
        
        doc += "\n---\n\n## 💡 Pro Tips\n\n"
        doc += """
- **STAR Method**: Structure your answers using Situation, Task, Action, Result
- **Be Specific**: Use concrete examples and numbers when possible
- **Stay Positive**: Even when discussing challenges or failures
- **Be Honest**: Don't exaggerate or lie about your experience
- **Show Enthusiasm**: Let your passion for the role shine through
- **Listen Carefully**: Make sure you understand the question before answering
- **Take Your Time**: It's okay to pause and think before answering
- **Follow Up**: Send a thank-you email within 24 hours

---

## 🎯 Sample Answers

### "Tell me about yourself"
{self.sample_answers['tell_me_about_yourself']}

### "What is the difference between TCP and UDP?"
{self.sample_answers['tcp_vs_udp']}

### "How do you troubleshoot network issues?"
{self.sample_answers['network_troubleshooting']}

---

**Good luck with your interview! 🍀**
"""
        return doc


async def generate_interview_prep(job: Dict[str, Any]) -> Dict[str, Any]:
    """Quick helper to generate interview prep"""
    ai = InterviewPreparationAI()
    return await ai.generate_interview_prep(job)


async def save_interview_prep(job: Dict[str, Any], filename: str = None):
    """Generate and save interview prep to file"""
    ai = InterviewPreparationAI()
    prep = await ai.generate_interview_prep(job)
    doc = ai.format_prep_document(prep)
    
    if not filename:
        company = job.get("company", "Company").replace(" ", "_")
        filename = f"interview_prep_{company}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(doc)
    
    return filename
