"""
AI Interview Simulator
Interactive mock interview system with dynamic questions and feedback
"""

import random
from typing import Dict, List, Any, Tuple

class InterviewSimulator:
    """AI-powered interview simulator"""
    
    def __init__(self):
        self.question_bank = {
            "technical": {
                "easy": [
                    "What is the difference between a router and a switch?",
                    "Explain what an IP address is.",
                    "What is DNS and how does it work?",
                    "What is the purpose of a subnet mask?",
                    "Explain the difference between TCP and UDP."
                ],
                "medium": [
                    "How would you troubleshoot a network connectivity issue?",
                    "Explain VLANs and their benefits.",
                    "What is NAT and why is it used?",
                    "Describe the OSI model and its layers.",
                    "How do routing protocols like OSPF and BGP differ?"
                ],
                "hard": [
                    "Design a network for a company with 3 offices in different cities.",
                    "How would you implement SD-WAN for a distributed organization?",
                    "Explain how you would secure a network against DDoS attacks.",
                    "Describe your approach to network capacity planning.",
                    "How would you migrate a legacy network to a modern infrastructure?"
                ]
            },
            "behavioral": [
                "Tell me about yourself.",
                "Why do you want to work for our company?",
                "Describe a challenging project you worked on.",
                "How do you handle stress and pressure?",
                "Tell me about a time you disagreed with a colleague.",
                "What are your greatest strengths?",
                "What is your biggest weakness?",
                "Where do you see yourself in 5 years?",
                "Why are you leaving your current job?",
                "Describe a time you failed and what you learned."
            ],
            "situational": [
                "What would you do if a critical server goes down at 3 AM?",
                "How would you handle a disagreement with your manager?",
                "What if you're asked to implement something you think is wrong?",
                "How would you prioritize multiple urgent tasks?",
                "What would you do if you made a mistake that affected production?"
            ]
        }
        
        self.evaluation_criteria = {
            "technical_accuracy": {
                "weight": 0.3,
                "description": "Correctness of technical information"
            },
            "communication": {
                "weight": 0.25,
                "description": "Clarity and structure of answers"
            },
            "confidence": {
                "weight": 0.15,
                "description": "Confidence and professionalism"
            },
            "relevance": {
                "weight": 0.15,
                "description": "Relevance to the question"
            },
            "depth": {
                "weight": 0.15,
                "description": "Depth of knowledge demonstrated"
            }
        }
    
    def generate_interview(self, difficulty: str = "medium", duration: int = 30) -> List[Dict[str, Any]]:
        """Generate interview questions"""
        
        questions = []
        
        # Calculate number of questions based on duration
        num_technical = duration // 5  # 5 min per technical question
        num_behavioral = 3  # Always 3 behavioral
        num_situational = 2  # Always 2 situational
        
        # Add technical questions
        if difficulty in self.question_bank["technical"]:
            tech_questions = random.sample(
                self.question_bank["technical"][difficulty],
                min(num_technical, len(self.question_bank["technical"][difficulty]))
            )
            for q in tech_questions:
                questions.append({
                    "type": "technical",
                    "difficulty": difficulty,
                    "question": q,
                    "time_limit": 5  # minutes
                })
        
        # Add behavioral questions
        behavioral = random.sample(self.question_bank["behavioral"], num_behavioral)
        for q in behavioral:
            questions.append({
                "type": "behavioral",
                "question": q,
                "time_limit": 3
            })
        
        # Add situational questions
        situational = random.sample(self.question_bank["situational"], num_situational)
        for q in situational:
            questions.append({
                "type": "situational",
                "question": q,
                "time_limit": 4
            })
        
        # Shuffle questions
        random.shuffle(questions)
        
        return questions
    
    def evaluate_answer(self, question: Dict[str, Any], answer: str) -> Dict[str, Any]:
        """Evaluate interview answer"""
        
        # Simple evaluation (in production, use AI)
        scores = {}
        
        # Technical accuracy (check for keywords)
        if question["type"] == "technical":
            keywords = self._extract_keywords(question["question"])
            keyword_count = sum(1 for kw in keywords if kw.lower() in answer.lower())
            scores["technical_accuracy"] = min(100, (keyword_count / len(keywords)) * 100) if keywords else 50
        else:
            scores["technical_accuracy"] = 70  # Default for non-technical
        
        # Communication (based on length and structure)
        word_count = len(answer.split())
        if 50 <= word_count <= 200:
            scores["communication"] = 85
        elif word_count < 50:
            scores["communication"] = 60
        else:
            scores["communication"] = 75
        
        # Confidence (check for filler words)
        filler_words = ["um", "uh", "like", "you know", "basically"]
        filler_count = sum(answer.lower().count(word) for word in filler_words)
        scores["confidence"] = max(50, 100 - (filler_count * 10))
        
        # Relevance (simple check)
        scores["relevance"] = 80  # Default
        
        # Depth (based on length and detail)
        if word_count > 100:
            scores["depth"] = 85
        elif word_count > 50:
            scores["depth"] = 70
        else:
            scores["depth"] = 55
        
        # Calculate overall score
        overall = sum(
            scores[criterion] * self.evaluation_criteria[criterion]["weight"]
            for criterion in scores
        )
        
        # Generate feedback
        feedback = self._generate_feedback(scores, question, answer)
        
        return {
            "scores": scores,
            "overall_score": round(overall, 1),
            "feedback": feedback,
            "grade": self._get_grade(overall)
        }
    
    def _extract_keywords(self, question: str) -> List[str]:
        """Extract keywords from question"""
        # Simple keyword extraction
        keywords = []
        if "router" in question.lower():
            keywords.extend(["router", "routing", "layer 3"])
        if "switch" in question.lower():
            keywords.extend(["switch", "switching", "layer 2"])
        if "tcp" in question.lower() or "udp" in question.lower():
            keywords.extend(["tcp", "udp", "protocol", "connection"])
        if "vlan" in question.lower():
            keywords.extend(["vlan", "virtual", "segment"])
        if "troubleshoot" in question.lower():
            keywords.extend(["ping", "traceroute", "check", "test"])
        
        return keywords if keywords else ["network", "system", "configure"]
    
    def _generate_feedback(self, scores: Dict[str, float], question: Dict[str, Any], answer: str) -> List[str]:
        """Generate feedback based on scores"""
        
        feedback = []
        
        # Technical accuracy feedback
        if scores["technical_accuracy"] < 70:
            feedback.append("💡 Include more technical details and specific terminology")
        elif scores["technical_accuracy"] > 85:
            feedback.append("✅ Excellent technical knowledge demonstrated")
        
        # Communication feedback
        if scores["communication"] < 70:
            if len(answer.split()) < 50:
                feedback.append("💡 Provide more detailed explanations")
            else:
                feedback.append("💡 Try to be more concise and structured")
        elif scores["communication"] > 85:
            feedback.append("✅ Clear and well-structured answer")
        
        # Confidence feedback
        if scores["confidence"] < 70:
            feedback.append("💡 Reduce filler words (um, uh, like) to sound more confident")
        elif scores["confidence"] > 85:
            feedback.append("✅ Confident and professional delivery")
        
        # Depth feedback
        if scores["depth"] < 70:
            feedback.append("💡 Provide more examples and details to demonstrate depth")
        elif scores["depth"] > 85:
            feedback.append("✅ Great depth of knowledge shown")
        
        # Question-specific feedback
        if question["type"] == "behavioral":
            if "star" not in answer.lower():
                feedback.append("💡 Use the STAR method (Situation, Task, Action, Result)")
        
        return feedback
    
    def _get_grade(self, score: float) -> str:
        """Convert score to grade"""
        if score >= 90:
            return "A (Excellent)"
        elif score >= 80:
            return "B (Good)"
        elif score >= 70:
            return "C (Satisfactory)"
        elif score >= 60:
            return "D (Needs Improvement)"
        else:
            return "F (Poor)"
    
    def generate_interview_report(self, results: List[Dict[str, Any]]) -> str:
        """Generate comprehensive interview report"""
        
        total_score = sum(r["overall_score"] for r in results) / len(results)
        
        report = f"""
# 🎤 Mock Interview Report

## Overall Performance

**Overall Score:** {total_score:.1f}/100
**Grade:** {self._get_grade(total_score)}

---

## Question-by-Question Analysis

"""
        
        for i, result in enumerate(results, 1):
            report += f"""
### Question {i}: {result['question']['question']}

**Type:** {result['question']['type'].title()}
**Your Score:** {result['overall_score']}/100
**Grade:** {result['grade']}

**Detailed Scores:**
"""
            for criterion, score in result['scores'].items():
                report += f"- {criterion.replace('_', ' ').title()}: {score:.1f}/100\n"
            
            report += "\n**Feedback:**\n"
            for feedback in result['feedback']:
                report += f"{feedback}\n"
            
            report += "\n---\n"
        
        # Overall feedback
        report += """
## 📊 Overall Feedback

"""
        
        if total_score >= 85:
            report += "🌟 **Excellent performance!** You're well-prepared for interviews.\n\n"
        elif total_score >= 75:
            report += "👍 **Good performance!** With some practice, you'll be interview-ready.\n\n"
        elif total_score >= 65:
            report += "📚 **Decent performance.** Focus on the areas highlighted above.\n\n"
        else:
            report += "💪 **Keep practicing!** Review the feedback and try again.\n\n"
        
        report += """
## 🎯 Recommendations

1. **Practice More:** Do 2-3 mock interviews per week
2. **Record Yourself:** Watch your body language and delivery
3. **Study Technical Topics:** Review networking fundamentals
4. **Use STAR Method:** Structure behavioral answers properly
5. **Get Feedback:** Practice with friends or mentors

---

## 📚 Resources

- **Technical Prep:** Review OSI model, routing protocols, network security
- **Behavioral Prep:** Prepare 5-7 STAR stories
- **Practice Platforms:** Pramp, Interviewing.io, LeetCode

---

**Keep practicing and you'll ace the real interview! 🚀**
"""
        
        return report


def start_mock_interview(difficulty: str = "medium", duration: int = 30) -> List[Dict[str, Any]]:
    """Start a mock interview session"""
    simulator = InterviewSimulator()
    return simulator.generate_interview(difficulty, duration)


def evaluate_interview_answer(question: Dict[str, Any], answer: str) -> Dict[str, Any]:
    """Evaluate a single answer"""
    simulator = InterviewSimulator()
    return simulator.evaluate_answer(question, answer)


def generate_interview_report(results: List[Dict[str, Any]]) -> str:
    """Generate interview report"""
    simulator = InterviewSimulator()
    return simulator.generate_interview_report(results)
