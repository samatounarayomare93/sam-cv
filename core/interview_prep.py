"""
Project Chronos: Interview Prep Singularity
Modernized Q&A Engine for HR & Operations Roles.
"""

from typing import Dict, List, Optional

INTERVIEW_DATA = {
    "general": {
        "title": "📋 General Questions",
        "questions": [
            {
                "question": "Tell me about yourself.",
                "category": "Introduction",
                "tips": [
                    "Keep it professional, 2-3 minutes max",
                    "Focus on HR experience and achievements",
                    "End with why you're interested in THIS role"
                ],
                "sample_answer": "I graduated with a Bachelor's degree in Human Resources from Lebanese Canadian University in 2016. My HR journey began in recruitment... [refer to full legacy script]"
            },
            {
                "question": "What are your greatest strengths?",
                "category": "Self-Assessment",
                "tips": [
                    "Choose 3 strengths relevant to the role",
                    "Use the STAR method (Situation, Task, Action, Result)"
                ],
                "sample_answer": "My three greatest strengths are Recruitment Expertise, Compliance, and Process Optimization..."
            },
            {
                "question": "What is your biggest weakness?",
                "category": "Self-Assessment",
                "tips": [
                    "Be honest but strategic",
                    "Show how you're improving it",
                    "Never say 'I have no weaknesses'"
                ],
                "sample_answer": "One area I've been working to improve is public speaking. I've taken proactive steps including communication courses..."
            }
        ]
    },
    "hr": {
        "title": "💼 HR-Specific Questions",
        "questions": [
            {
                "question": "Describe your experience with HRIS systems.",
                "category": "Technical",
                "tips": [
                    "List specific systems (SAP, Workday, etc.)",
                    "Describe your proficiency level"
                ],
                "sample_answer": "I've worked extensively with SAP SuccessFactors and Workday, managing employee data and complex reporting..."
            },
            {
                "question": "How would you handle a conflict between employees?",
                "category": "Employee Relations",
                "tips": [
                    "Follow structured resolution steps",
                    "Emphasize confidentiality and mediation"
                ],
                "sample_answer": "I follow a multi-step approach: separate assessment, identifying common ground, facilitated dialogue, and follow-up..."
            }
        ]
    },
    "behavioral": {
        "title": "🎯 Behavioral (STAR)",
        "questions": [
            {
                "question": "Tell me about a time you improved a process.",
                "category": "Problem Solving",
                "star": {
                    "S": "Onboarding was taking 3 weeks due to disconnected steps.",
                    "T": "Streamline to improve new hire satisfaction.",
                    "A": "Mapped process, parallelized tasks with IT/HR.",
                    "R": "Reduced time to 1 week; satisfaction rose to 92%."
                }
            }
        ]
    },
    "salary": {
        "title": "💰 Salary Negotiation",
        "questions": [
            {
                "question": "What are your salary expectations?",
                "strategy": "Open discussion focused on value impact.",
                "sample_answer": "Based on my 5+ years of HR experience and GCC market research, a competitive range would be [X-Y]. However, I'm focused on impact and growth..."
            }
        ]
    }
}

class InterviewPrepEngine:
    """The Sovereign Prep Engine: High-fidelity Q&A for mission dominance."""
    
    @staticmethod
    def get_categories():
        return {k: v["title"] for k, v in INTERVIEW_DATA.items()}
    
    @staticmethod
    def get_questions(category: str) -> Optional[List[Dict]]:
        return INTERVIEW_DATA.get(category, {}).get("questions")

    @staticmethod
    def get_formatted_question(question_data: Dict) -> str:
        """Formats a question with Sovereign/Cyberpunk aesthetics."""
        text = f"📌 *QUESTION*: {question_data['question']}\n\n"
        
        if "category" in question_data:
            text += f"📂 *CATEGORY*: {question_data['category']}\n"
            
        if "tips" in question_data:
            text += "\n💡 *TIPS*:\n"
            for tip in question_data["tips"]:
                text += f"- {tip}\n"
                
        if "sample_answer" in question_data:
            text += f"\n✅ *SAMPLE ANSWER*:\n_{question_data['sample_answer']}_"
            
        if "star" in question_data:
            star = question_data["star"]
            text += "\n📝 *STAR EXAMPLE*:\n"
            text += f"*S*: {star['S']}\n"
            text += f"*T*: {star['T']}\n"
            text += f"*A*: {star['A']}\n"
            text += f"*R*: {star['R']}\n"
            
        return text
