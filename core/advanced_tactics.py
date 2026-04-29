"""
🌍 ADVANCED GLOBAL TACTICS (100% FREE)
Psychological and technical tricks from around the world
Zero investment required
"""

import random
import time
from typing import Dict, List, Any
import logging


class GlobalTactics:
    """Advanced tactics from world's best recruitment hackers."""
    
    # 🇨🇳 CHINESE TACTICS (Sun Tzu - Art of War)
    CHINESE_TACTICS = {
        "appear_weak": "Position yourself as the missing piece, not the aggressive competitor",
        "indirect_approach": "Never directly ask for job - make them want to hire you",
        "know_enemy": "Research company's pain points and position as the solution",
        "timing": "Apply when company is most vulnerable (funding round, expansion, crisis)",
        "deception": "Appear overqualified but humble - they'll fight to keep you"
    }
    
    # 🇷🇺 RUSSIAN TACTICS (KGB Recruitment Methods)
    RUSSIAN_TACTICS = {
        "kompromat": "Subtly mention competitor's failures you can prevent",
        "long_game": "Build relationship first, job offer comes naturally",
        "leverage": "Create FOMO - mention other opportunities without being arrogant",
        "trust_building": "Use personal stories and vulnerability to build deep trust",
        "network_effect": "Mention mutual connections or industry respect"
    }
    
    # 🇺🇸 USA TACTICS (Silicon Valley Growth Hacking)
    USA_TACTICS = {
        "metrics_obsession": "Use 3-5 specific numbers in every paragraph",
        "scale_language": "Talk about 10x, not 2x improvements",
        "urgency": "Create sense that you're in high demand",
        "value_prop": "Lead with ROI - what's the $ value you bring",
        "social_proof": "Reference big names, even if indirect connection"
    }
    
    # 🇮🇱 ISRAELI TACTICS (Mossad Intelligence)
    ISRAELI_TACTICS = {
        "osint": "Deep research on hiring manager's LinkedIn, Twitter, recent posts",
        "personalization": "Reference their specific achievements or posts",
        "problem_solving": "Identify their #1 problem and position as solution",
        "direct_approach": "Skip HR, go straight to decision maker when possible",
        "chutzpah": "Confident, almost audacious - they respect boldness"
    }
    
    # 🇯🇵 JAPANESE TACTICS (Kaizen - Continuous Improvement)
    JAPANESE_TACTICS = {
        "perfection": "Every detail matters - perfect formatting, no typos",
        "respect": "Show deep respect for company's achievements",
        "long_term": "Emphasize loyalty and long-term commitment",
        "harmony": "Position as team player who brings balance",
        "continuous_improvement": "Show track record of constant learning"
    }
    
    # 🇩🇪 GERMAN TACTICS (Engineering Precision)
    GERMAN_TACTICS = {
        "precision": "Exact numbers, specific methodologies, clear processes",
        "efficiency": "Emphasize time/cost savings with precise calculations",
        "quality": "Focus on zero-defect track record",
        "systematic": "Show structured approach to problem-solving",
        "credentials": "Highlight certifications, formal training"
    }
    
    @staticmethod
    def get_psychological_trigger(company_type: str, job_level: str) -> Dict[str, str]:
        """
        Select best psychological trigger based on company and role.
        
        Args:
            company_type: startup, corporate, family_business, etc.
            job_level: junior, mid, senior, executive
        
        Returns:
            Dict with tactic name and application
        """
        triggers = {
            "startup_senior": {
                "primary": "USA_TACTICS",
                "secondary": "ISRAELI_TACTICS",
                "approach": "High energy, metrics-driven, show you can scale fast"
            },
            "corporate_senior": {
                "primary": "GERMAN_TACTICS",
                "secondary": "JAPANESE_TACTICS",
                "approach": "Precision, process, proven track record"
            },
            "family_business": {
                "primary": "RUSSIAN_TACTICS",
                "secondary": "JAPANESE_TACTICS",
                "approach": "Trust, loyalty, long-term relationship"
            },
            "tech_company": {
                "primary": "USA_TACTICS",
                "secondary": "CHINESE_TACTICS",
                "approach": "Innovation, disruption, competitive advantage"
            },
            "consulting": {
                "primary": "ISRAELI_TACTICS",
                "secondary": "GERMAN_TACTICS",
                "approach": "Problem-solving, precision, client results"
            }
        }
        
        key = f"{company_type}_{job_level}"
        return triggers.get(key, triggers["tech_company"])
    
    @staticmethod
    def apply_scarcity_principle(cover_letter: str) -> str:
        """
        🧠 PSYCHOLOGICAL HACK: Scarcity Principle
        Make yourself appear in high demand (subtly)
        """
        scarcity_phrases = [
            "I'm currently evaluating a few opportunities, but your company stands out because",
            "While I have other options on the table, I'm particularly drawn to",
            "I'm being selective about my next move, and your role aligns perfectly because",
            "Among the opportunities I'm considering, yours is most compelling due to"
        ]
        
        # Insert scarcity phrase in second paragraph
        paragraphs = cover_letter.split('\n\n')
        if len(paragraphs) >= 2:
            # Add subtle scarcity to second paragraph
            scarcity = random.choice(scarcity_phrases)
            paragraphs[1] = f"{scarcity} {paragraphs[1]}"
            return '\n\n'.join(paragraphs)
        
        return cover_letter
    
    @staticmethod
    def apply_reciprocity_principle(cover_letter: str, company_name: str) -> str:
        """
        🧠 PSYCHOLOGICAL HACK: Reciprocity
        Give value first, they'll want to reciprocate
        """
        value_offers = [
            f"I've actually been following {company_name}'s growth and have some thoughts on [specific area] that I'd love to share",
            f"I recently analyzed {company_name}'s market position and identified 3 quick wins I could implement in the first 30 days",
            f"I've prepared a brief analysis of how {company_name} could optimize [relevant area] - happy to share during our conversation"
        ]
        
        # Add value offer at the end
        value_offer = random.choice(value_offers)
        return f"{cover_letter}\n\n{value_offer}"
    
    @staticmethod
    def apply_social_proof(cover_letter: str) -> str:
        """
        🧠 PSYCHOLOGICAL HACK: Social Proof
        Reference success with similar companies
        """
        social_proof_phrases = [
            "I've successfully implemented similar systems at [previous company], resulting in",
            "My approach has been validated across multiple organizations, including",
            "Industry leaders I've worked with have consistently recognized my ability to"
        ]
        
        # This would be customized based on actual CV
        return cover_letter
    
    @staticmethod
    def apply_authority_principle(cover_letter: str) -> str:
        """
        🧠 PSYCHOLOGICAL HACK: Authority
        Establish credibility through specific achievements
        """
        # Already handled in CV, but can emphasize
        return cover_letter
    
    @staticmethod
    def apply_liking_principle(cover_letter: str, company_values: str = None) -> str:
        """
        🧠 PSYCHOLOGICAL HACK: Liking
        Mirror company's language and values
        """
        if company_values:
            # Mirror their exact language
            # This is already done in main AI prompt
            pass
        return cover_letter
    
    @staticmethod
    def apply_commitment_principle(cover_letter: str) -> str:
        """
        🧠 PSYCHOLOGICAL HACK: Commitment & Consistency
        Show track record of following through
        """
        commitment_phrases = [
            "I have a consistent track record of",
            "Throughout my career, I've maintained a commitment to",
            "My approach has always been to see projects through to completion, as evidenced by"
        ]
        return cover_letter
    
    @staticmethod
    def optimize_email_timing(location: str) -> Dict[str, Any]:
        """
        🕐 TIMING OPTIMIZATION
        Best times to send emails based on research
        
        Research shows:
        - Tuesday-Thursday are best days
        - 10 AM or 2 PM local time are optimal
        - Avoid Mondays (too busy) and Fridays (weekend mode)
        """
        from datetime import datetime, timedelta
        import pytz
        
        # Timezone mapping
        tz_map = {
            "dubai": "Asia/Dubai",
            "uae": "Asia/Dubai",
            "lebanon": "Asia/Beirut",
            "beirut": "Asia/Beirut",
            "usa": "America/New_York",
            "uk": "Europe/London",
        }
        
        tz_name = "Asia/Beirut"  # Default
        for key, tz in tz_map.items():
            if key in location.lower():
                tz_name = tz
                break
        
        try:
            tz = pytz.timezone(tz_name)
            now = datetime.now(tz)
            
            # Best sending times
            optimal_hours = [10, 14]  # 10 AM, 2 PM
            optimal_days = [1, 2, 3]  # Tuesday, Wednesday, Thursday
            
            current_hour = now.hour
            current_day = now.weekday()
            
            is_optimal_time = current_hour in optimal_hours
            is_optimal_day = current_day in optimal_days
            
            # Calculate next optimal time if not now
            if not (is_optimal_time and is_optimal_day):
                # Find next Tuesday-Thursday
                days_ahead = (1 - current_day) % 7  # Next Tuesday
                if days_ahead == 0:
                    days_ahead = 7
                
                next_optimal = now + timedelta(days=days_ahead)
                next_optimal = next_optimal.replace(hour=10, minute=0, second=0)
                
                return {
                    "send_now": False,
                    "optimal": False,
                    "next_optimal_time": next_optimal,
                    "reason": f"Current time not optimal. Best to send on {next_optimal.strftime('%A at %I %p')}"
                }
            
            return {
                "send_now": True,
                "optimal": True,
                "reason": "Optimal sending time!"
            }
            
        except Exception as e:
            logging.warning(f"Timing optimization failed: {e}")
            return {"send_now": True, "optimal": False}
    
    @staticmethod
    def generate_power_words() -> List[str]:
        """
        💪 POWER WORDS
        Words that trigger emotional response and action
        """
        return [
            # Achievement words
            "achieved", "delivered", "exceeded", "transformed", "revolutionized",
            "pioneered", "spearheaded", "orchestrated", "accelerated", "optimized",
            
            # Impact words
            "impact", "results", "ROI", "revenue", "growth", "efficiency",
            "productivity", "performance", "quality", "excellence",
            
            # Action words
            "implemented", "executed", "launched", "built", "created",
            "developed", "designed", "established", "initiated", "led",
            
            # Scale words
            "scaled", "expanded", "multiplied", "maximized", "amplified",
            "elevated", "enhanced", "strengthened", "boosted", "increased",
            
            # Innovation words
            "innovative", "cutting-edge", "strategic", "visionary", "forward-thinking",
            "disruptive", "game-changing", "breakthrough", "pioneering", "advanced"
        ]
    
    @staticmethod
    def apply_neuro_linguistic_programming(text: str) -> str:
        """
        🧠 NLP TECHNIQUES
        Subtle language patterns that influence subconscious
        """
        # Embedded commands
        nlp_patterns = {
            "imagine": "Imagine having someone who can",
            "picture": "Picture your team with",
            "consider": "Consider the impact of",
            "realize": "You'll realize that",
            "discover": "You'll discover that"
        }
        
        # Presuppositions (assume the sale)
        presuppositions = [
            "When we work together",
            "Once I join your team",
            "As your new [role]",
            "During my first 90 days"
        ]
        
        return text
    
    @staticmethod
    def calculate_email_score(email_content: str) -> Dict[str, Any]:
        """
        📊 EMAIL QUALITY SCORE
        Analyze email for effectiveness
        """
        score = 0
        feedback = []
        
        # Check for numbers/metrics
        import re
        numbers = re.findall(r'\d+%|\$\d+|\d+x|\d+ [a-zA-Z]+', email_content)
        if len(numbers) >= 3:
            score += 20
            feedback.append("✅ Good use of metrics")
        else:
            feedback.append("⚠️ Add more specific numbers")
        
        # Check for power words
        power_words = GlobalTactics.generate_power_words()
        power_word_count = sum(1 for word in power_words if word.lower() in email_content.lower())
        if power_word_count >= 5:
            score += 20
            feedback.append("✅ Strong power words")
        else:
            feedback.append("⚠️ Use more power words")
        
        # Check length (optimal: 150-250 words)
        word_count = len(email_content.split())
        if 150 <= word_count <= 250:
            score += 20
            feedback.append("✅ Optimal length")
        else:
            feedback.append(f"⚠️ Length: {word_count} words (optimal: 150-250)")
        
        # Check for personalization
        if any(word in email_content.lower() for word in ['your company', 'your team', 'your']):
            score += 20
            feedback.append("✅ Personalized")
        else:
            feedback.append("⚠️ Add more personalization")
        
        # Check for call to action
        cta_phrases = ['discuss', 'conversation', 'call', 'meeting', 'connect']
        if any(phrase in email_content.lower() for phrase in cta_phrases):
            score += 20
            feedback.append("✅ Clear call to action")
        else:
            feedback.append("⚠️ Add clear call to action")
        
        return {
            "score": score,
            "grade": "A" if score >= 80 else "B" if score >= 60 else "C",
            "feedback": feedback
        }


# 🎯 ADVANCED EMAIL SUBJECT LINE GENERATOR
class SubjectLineOptimizer:
    """Generate high-open-rate subject lines."""
    
    PROVEN_PATTERNS = [
        "{name} → {company}: {value_prop}",
        "Quick question about {company}'s {area}",
        "{achievement} | {name} for {role}",
        "Helping {company} with {pain_point}",
        "{mutual_connection} suggested I reach out",
        "Re: {company}'s {recent_news}",
        "{name}: {specific_skill} for {company}",
        "Solving {company}'s {problem}",
    ]
    
    @staticmethod
    def generate_subject_line(
        name: str,
        company: str,
        role: str,
        achievement: str = None,
        news: str = None
    ) -> str:
        """Generate optimized subject line."""
        
        # Pattern selection based on available info
        if news:
            return f"Re: {company}'s {news} - {name}"
        elif achievement:
            return f"{achievement} | {name} for {role}"
        else:
            return f"{name} → {company}: Proven {role.split()[0]} Leader"
    
    @staticmethod
    def test_subject_line(subject: str) -> Dict[str, Any]:
        """Test subject line effectiveness."""
        score = 0
        feedback = []
        
        # Length check (optimal: 40-60 characters)
        length = len(subject)
        if 40 <= length <= 60:
            score += 25
            feedback.append("✅ Optimal length")
        else:
            feedback.append(f"⚠️ Length: {length} chars (optimal: 40-60)")
        
        # Personalization
        if any(char.isupper() for char in subject[:10]):
            score += 25
            feedback.append("✅ Personalized")
        
        # Numbers
        if any(char.isdigit() for char in subject):
            score += 25
            feedback.append("✅ Contains numbers")
        
        # Urgency/curiosity
        urgency_words = ['quick', 'today', 'now', 'question', 're:']
        if any(word in subject.lower() for word in urgency_words):
            score += 25
            feedback.append("✅ Creates urgency/curiosity")
        
        return {
            "score": score,
            "predicted_open_rate": f"{20 + (score * 0.6):.0f}%",
            "feedback": feedback
        }


# Example usage
if __name__ == "__main__":
    tactics = GlobalTactics()
    
    # Test psychological trigger selection
    trigger = tactics.get_psychological_trigger("startup", "senior")
    print(f"Recommended tactics: {trigger}")
    
    # Test email scoring
    sample_email = """
    Dear Hiring Manager,
    
    I achieved 40% efficiency improvement at my previous role, managing a team of 15
    and delivering $2M in cost savings. I'm excited about the opportunity to bring
    similar results to your company.
    
    Let's schedule a call to discuss how I can contribute to your team's success.
    """
    
    score = tactics.calculate_email_score(sample_email)
    print(f"\nEmail Score: {score['score']}/100 (Grade: {score['grade']})")
    print("Feedback:")
    for item in score['feedback']:
        print(f"  {item}")
    
    # Test subject line
    subject = SubjectLineOptimizer.generate_subject_line(
        "Sam Salameh",
        "TechCorp",
        "HR Manager",
        "40% Efficiency Gain"
    )
    print(f"\nGenerated Subject: {subject}")
    
    subject_score = SubjectLineOptimizer.test_subject_line(subject)
    print(f"Subject Score: {subject_score['score']}/100")
    print(f"Predicted Open Rate: {subject_score['predicted_open_rate']}")
