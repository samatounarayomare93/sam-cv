"""
🎭 EMAIL PERSONALIZATION TOKENS (100% FREE)
Dynamic content that makes every email feel 100% personalized

Tokens:
- {first_name} - Hiring manager's first name
- {company} - Company name
- {recent_news} - Latest company news
- {relevant_skill} - Your matching skill
- {pain_point} - Company's challenge you can solve
- {metric} - Your achievement number
- {similar_company} - Similar company you worked with

Result: Feels completely personalized, not templated
"""

import logging
import os
import json
import re
from typing import Dict, List, Any, Optional
from pathlib import Path

# Enable/disable personalization
PERSONALIZATION_ENABLED = os.getenv("EMAIL_PERSONALIZATION_ENABLED", "true").lower() == "true"


class EmailPersonalizer:
    """Advanced email personalization with dynamic tokens."""
    
    def __init__(self):
        self.candidate_data = self._load_candidate_data()
        self.company_data = {}
    
    def _load_candidate_data(self) -> Dict[str, Any]:
        """Load candidate's data from environment."""
        return {
            "name": os.getenv("CANDIDATE_NAME", "Sam Salameh"),
            "phone": os.getenv("CANDIDATE_PHONE", "+961 70 841 1009"),
            "email": os.getenv("SENDER_EMAIL", "sam.dev1@hotmail.com"),
            "linkedin": os.getenv("LINKEDIN_URL", "https://www.linkedin.com/in/sam-salameh"),
            "profession": os.getenv("CANDIDATE_PROFESSION", "Senior Network Engineer"),
            
            # Key achievements (extracted from CV)
            "achievements": [
                "40% efficiency improvement",
                "$2M cost savings",
                "15-person team management",
                "Zero downtime deployment",
                "300+ successful implementations"
            ],
            
            # Skills
            "skills": [
                "Network Engineering",
                "Team Leadership",
                "Process Optimization",
                "Cost Reduction",
                "Infrastructure Management"
            ],
            
            # Industries worked in
            "industries": [
                "Technology",
                "Telecommunications",
                "Enterprise IT"
            ],
            
            # Similar companies
            "similar_companies": [
                "Tech companies",
                "Enterprise organizations",
                "Telecom providers"
            ]
        }
    
    def extract_first_name(self, full_name: str) -> str:
        """
        Extract first name from full name.
        
        Args:
            full_name: Full name
        
        Returns:
            First name
        """
        if not full_name:
            return "Hiring Manager"
        
        parts = full_name.strip().split()
        return parts[0] if parts else "Hiring Manager"
    
    def extract_company_pain_points(self, job_description: str) -> List[str]:
        """
        Extract potential pain points from job description.
        
        Args:
            job_description: Job description text
        
        Returns:
            List of pain points
        """
        pain_point_keywords = {
            "scaling": "scaling operations",
            "growth": "managing rapid growth",
            "efficiency": "improving efficiency",
            "cost": "reducing costs",
            "team": "building strong teams",
            "process": "optimizing processes",
            "quality": "maintaining quality",
            "deadline": "meeting tight deadlines",
            "innovation": "driving innovation",
            "customer": "improving customer satisfaction"
        }
        
        pain_points = []
        desc_lower = job_description.lower()
        
        for keyword, pain_point in pain_point_keywords.items():
            if keyword in desc_lower:
                pain_points.append(pain_point)
        
        return pain_points[:3]  # Top 3
    
    def match_relevant_skills(self, job_description: str) -> List[str]:
        """
        Match candidate's skills to job requirements.
        
        Args:
            job_description: Job description text
        
        Returns:
            List of matching skills
        """
        matching_skills = []
        desc_lower = job_description.lower()
        
        for skill in self.candidate_data["skills"]:
            if skill.lower() in desc_lower:
                matching_skills.append(skill)
        
        return matching_skills[:3]  # Top 3
    
    def select_best_achievement(self, job_description: str) -> str:
        """
        Select most relevant achievement for this job.
        
        Args:
            job_description: Job description text
        
        Returns:
            Best matching achievement
        """
        desc_lower = job_description.lower()
        
        # Score each achievement
        scores = {}
        for achievement in self.candidate_data["achievements"]:
            score = 0
            achievement_lower = achievement.lower()
            
            # Check for keyword matches
            if "efficiency" in desc_lower and "efficiency" in achievement_lower:
                score += 10
            if "cost" in desc_lower and "cost" in achievement_lower:
                score += 10
            if "team" in desc_lower and "team" in achievement_lower:
                score += 10
            if "save" in desc_lower or "saving" in desc_lower:
                score += 5
            
            scores[achievement] = score
        
        # Return highest scoring achievement
        if scores:
            best = max(scores.items(), key=lambda x: x[1])
            return best[0]
        
        # Default to first achievement
        return self.candidate_data["achievements"][0]
    
    def generate_personalization_tokens(
        self,
        company_name: str,
        job_title: str,
        job_description: str,
        hiring_manager_name: str = None,
        recent_news: str = None
    ) -> Dict[str, str]:
        """
        Generate all personalization tokens for email.
        
        Args:
            company_name: Company name
            job_title: Job title
            job_description: Job description
            hiring_manager_name: Hiring manager's name (optional)
            recent_news: Recent company news (optional)
        
        Returns:
            Dict of tokens and their values
        """
        tokens = {}
        
        # Basic tokens
        tokens["company"] = company_name
        tokens["role"] = job_title
        tokens["candidate_name"] = self.candidate_data["name"]
        tokens["candidate_phone"] = self.candidate_data["phone"]
        tokens["candidate_email"] = self.candidate_data["email"]
        tokens["candidate_linkedin"] = self.candidate_data["linkedin"]
        
        # Hiring manager
        if hiring_manager_name:
            tokens["first_name"] = self.extract_first_name(hiring_manager_name)
            tokens["hiring_manager"] = hiring_manager_name
        else:
            tokens["first_name"] = "Hiring Manager"
            tokens["hiring_manager"] = "Hiring Manager"
        
        # Recent news
        if recent_news:
            tokens["recent_news"] = recent_news
        else:
            tokens["recent_news"] = f"{company_name}'s continued growth"
        
        # Skills matching
        matching_skills = self.match_relevant_skills(job_description)
        if matching_skills:
            tokens["relevant_skill"] = matching_skills[0]
            tokens["relevant_skills"] = ", ".join(matching_skills)
        else:
            tokens["relevant_skill"] = self.candidate_data["skills"][0]
            tokens["relevant_skills"] = ", ".join(self.candidate_data["skills"][:3])
        
        # Pain points
        pain_points = self.extract_company_pain_points(job_description)
        if pain_points:
            tokens["pain_point"] = pain_points[0]
            tokens["pain_points"] = ", ".join(pain_points)
        else:
            tokens["pain_point"] = "operational challenges"
            tokens["pain_points"] = "operational challenges"
        
        # Best achievement
        tokens["metric"] = self.select_best_achievement(job_description)
        
        # Similar company
        tokens["similar_company"] = self.candidate_data["similar_companies"][0]
        
        # Industry
        tokens["industry"] = self.candidate_data["industries"][0]
        
        return tokens
    
    def personalize_email(
        self,
        template: str,
        tokens: Dict[str, str]
    ) -> str:
        """
        Replace tokens in email template.
        
        Args:
            template: Email template with {tokens}
            tokens: Dict of token values
        
        Returns:
            Personalized email
        """
        if not PERSONALIZATION_ENABLED:
            return template
        
        personalized = template
        
        # Replace all tokens
        for token, value in tokens.items():
            placeholder = f"{{{token}}}"
            personalized = personalized.replace(placeholder, str(value))
        
        return personalized
    
    def generate_personalized_subject(
        self,
        company_name: str,
        job_title: str,
        style: str = "direct"
    ) -> str:
        """
        Generate personalized subject line.
        
        Args:
            company_name: Company name
            job_title: Job title
            style: Subject line style (direct, question, value_prop)
        
        Returns:
            Personalized subject line
        """
        candidate_name = self.candidate_data["name"]
        achievement = self.candidate_data["achievements"][0]
        
        if style == "direct":
            return f"{candidate_name} → {company_name}: Proven {job_title.split()[0]} Leader"
        
        elif style == "question":
            return f"Looking for a {job_title} who achieved {achievement}?"
        
        elif style == "value_prop":
            return f"{achievement} | {candidate_name} for {job_title}"
        
        elif style == "news_based":
            return f"Re: {company_name}'s growth - {job_title} application"
        
        else:
            return f"{candidate_name} - {job_title} at {company_name}"
    
    def generate_personalized_opening(
        self,
        tokens: Dict[str, str],
        style: str = "news_based"
    ) -> str:
        """
        Generate personalized email opening.
        
        Args:
            tokens: Personalization tokens
            style: Opening style
        
        Returns:
            Personalized opening paragraph
        """
        if style == "news_based" and tokens.get("recent_news"):
            return (
                f"Dear {tokens['first_name']},\n\n"
                f"I noticed {tokens['company']} recently {tokens['recent_news']}. "
                f"As someone with proven experience in {tokens['relevant_skill']}, "
                f"I believe I can contribute significantly to this growth phase."
            )
        
        elif style == "pain_point":
            return (
                f"Dear {tokens['first_name']},\n\n"
                f"I understand {tokens['company']} is focused on {tokens['pain_point']}. "
                f"In my previous role, I achieved {tokens['metric']}, which directly addresses "
                f"this challenge."
            )
        
        elif style == "achievement":
            return (
                f"Dear {tokens['first_name']},\n\n"
                f"I'm writing to express my interest in the {tokens['role']} position at {tokens['company']}. "
                f"With a track record of {tokens['metric']}, I'm confident I can deliver "
                f"similar results for your team."
            )
        
        else:  # professional
            return (
                f"Dear {tokens['first_name']},\n\n"
                f"I'm excited to apply for the {tokens['role']} position at {tokens['company']}. "
                f"My experience in {tokens['relevant_skills']} aligns perfectly with your requirements."
            )


# Global instance
_personalizer = None


def get_personalizer() -> EmailPersonalizer:
    """Get global email personalizer instance."""
    global _personalizer
    if _personalizer is None:
        _personalizer = EmailPersonalizer()
    return _personalizer


def generate_tokens(
    company_name: str,
    job_title: str,
    job_description: str,
    hiring_manager_name: str = None,
    recent_news: str = None
) -> Dict[str, str]:
    """Generate personalization tokens."""
    return get_personalizer().generate_personalization_tokens(
        company_name, job_title, job_description, hiring_manager_name, recent_news
    )


def personalize_email(template: str, tokens: Dict[str, str]) -> str:
    """Personalize email template."""
    return get_personalizer().personalize_email(template, tokens)


# Example usage
if __name__ == "__main__":
    personalizer = EmailPersonalizer()
    
    print("🎭 Email Personalization System")
    print("=" * 50)
    
    # Test data
    company = "TechCorp"
    role = "HR Manager"
    description = """
    We're looking for an HR Manager to help us scale our team efficiently.
    Must have experience in cost reduction and process optimization.
    Team leadership skills essential.
    """
    
    # Generate tokens
    print(f"\n📊 Generating tokens for {company}...")
    
    tokens = personalizer.generate_personalization_tokens(
        company_name=company,
        job_title=role,
        job_description=description,
        hiring_manager_name="John Smith",
        recent_news="announced Series B funding"
    )
    
    print(f"\n✅ Generated Tokens:")
    for key, value in list(tokens.items())[:10]:
        print(f"   {{{key}}}: {value}")
    
    # Test template
    template = """Dear {first_name},

I noticed {company} recently {recent_news}. As someone with proven experience in {relevant_skill}, I believe I can help with {pain_point}.

I've achieved {metric} in my previous role, and I'm confident I can deliver similar results for {company}.

Looking forward to discussing how I can contribute to your team's success.

Best regards,
{candidate_name}"""
    
    # Personalize
    personalized = personalizer.personalize_email(template, tokens)
    
    print(f"\n📧 Personalized Email:")
    print(personalized)
    
    # Generate subject lines
    print(f"\n📝 Subject Line Options:")
    for style in ["direct", "question", "value_prop"]:
        subject = personalizer.generate_personalized_subject(company, role, style)
        print(f"   {style}: {subject}")
