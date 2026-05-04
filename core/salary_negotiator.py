"""
Salary Negotiation Assistant
Provides salary insights and negotiation strategies
"""

from typing import Dict, List, Any, Tuple

class SalaryNegotiator:
    """AI-powered salary negotiation assistant"""
    
    def __init__(self):
        # Salary ranges by location (USD per year)
        self.salary_ranges = {
            "lebanon": {
                "junior": (12000, 18000),
                "mid": (18000, 30000),
                "senior": (30000, 50000),
                "lead": (50000, 70000)
            },
            "dubai": {
                "junior": (36000, 54000),
                "mid": (54000, 84000),
                "senior": (84000, 132000),
                "lead": (132000, 180000)
            },
            "saudi_arabia": {
                "junior": (30000, 48000),
                "mid": (48000, 72000),
                "senior": (72000, 120000),
                "lead": (120000, 168000)
            },
            "qatar": {
                "junior": (42000, 60000),
                "mid": (60000, 90000),
                "senior": (90000, 144000),
                "lead": (144000, 192000)
            },
            "remote": {
                "junior": (40000, 60000),
                "mid": (60000, 90000),
                "senior": (90000, 140000),
                "lead": (140000, 200000)
            }
        }
        
        # Benefits to negotiate
        self.negotiable_benefits = [
            "Base salary",
            "Sign-on bonus",
            "Annual bonus/performance bonus",
            "Stock options/equity",
            "Health insurance (family coverage)",
            "Life insurance",
            "Retirement/pension plan",
            "Paid time off (vacation days)",
            "Sick leave",
            "Remote work options",
            "Flexible hours",
            "Professional development budget",
            "Certification reimbursement",
            "Conference attendance",
            "Relocation assistance",
            "Housing allowance",
            "Transportation allowance",
            "Phone/internet allowance",
            "Gym membership",
            "Meal allowance"
        ]
    
    def estimate_salary(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate salary range for a job"""
        
        title = job.get("title", "").lower()
        location = job.get("location", "").lower()
        
        # Determine experience level
        level = "mid"  # default
        if any(word in title for word in ["senior", "lead", "principal", "architect"]):
            level = "senior"
        elif any(word in title for word in ["junior", "entry", "associate"]):
            level = "junior"
        elif any(word in title for word in ["lead", "manager", "director"]):
            level = "lead"
        
        # Determine location
        region = "remote"
        if "lebanon" in location or "beirut" in location:
            region = "lebanon"
        elif "dubai" in location or "uae" in location or "abu dhabi" in location:
            region = "dubai"
        elif "saudi" in location or "riyadh" in location or "jeddah" in location:
            region = "saudi_arabia"
        elif "qatar" in location or "doha" in location:
            region = "qatar"
        elif "remote" in location or "work from home" in location:
            region = "remote"
        
        # Get salary range
        salary_range = self.salary_ranges.get(region, {}).get(level, (50000, 80000))
        
        return {
            "level": level,
            "region": region,
            "min_salary": salary_range[0],
            "max_salary": salary_range[1],
            "target_salary": int((salary_range[0] + salary_range[1]) / 2),
            "currency": "USD",
            "period": "annual"
        }
    
    def generate_negotiation_strategy(self, job: Dict[str, Any], current_salary: int = None) -> Dict[str, Any]:
        """Generate comprehensive negotiation strategy"""
        
        estimate = self.estimate_salary(job)
        
        strategy = {
            "salary_estimate": estimate,
            "negotiation_tips": [],
            "what_to_say": {},
            "what_not_to_say": [],
            "benefits_to_negotiate": [],
            "timing_advice": {},
            "counter_offer_strategy": {}
        }
        
        # Negotiation tips
        strategy["negotiation_tips"] = [
            "🎯 Research the market rate thoroughly before negotiating",
            "💪 Know your worth and be confident",
            "📊 Use data and market research to support your ask",
            "🤝 Be professional and collaborative, not confrontational",
            "⏰ Wait for them to make the first offer if possible",
            "🎁 Consider the total compensation package, not just salary",
            "📈 Highlight your unique value and achievements",
            "🔄 Be prepared to negotiate multiple times",
            "📝 Get everything in writing",
            "🚪 Be willing to walk away if the offer doesn't meet your needs"
        ]
        
        # What to say
        strategy["what_to_say"] = {
            "when_asked_salary_expectations": f"""
"Based on my research of the market rate for this position in {estimate['region']}, 
and considering my {estimate['level']}-level experience and skills, I'm looking for 
a salary in the range of ${estimate['min_salary']:,} to ${estimate['max_salary']:,}. 
However, I'm flexible and would like to learn more about the complete compensation package."
""",
            "when_receiving_low_offer": f"""
"Thank you for the offer. I'm excited about this opportunity. However, based on my 
research and experience, I was expecting something closer to ${estimate['target_salary']:,}. 
Is there flexibility in the salary range?"
""",
            "when_negotiating_benefits": """
"I understand the salary range may be fixed. Are there other aspects of the compensation 
package we could discuss, such as sign-on bonus, additional vacation days, or professional 
development budget?"
""",
            "when_accepting": """
"Thank you for working with me on this. I'm excited to accept the offer and join the team. 
Could you please send me the offer letter with all the details we discussed?"
"""
        }
        
        # What NOT to say
        strategy["what_not_to_say"] = [
            "❌ 'I need this salary because of personal expenses'",
            "❌ 'My friend makes more than this'",
            "❌ 'I'll accept any salary'",
            "❌ 'This is my final offer' (unless you mean it)",
            "❌ 'I have another offer' (unless you actually do)",
            "❌ Comparing yourself negatively to others",
            "❌ Being aggressive or demanding",
            "❌ Accepting immediately without negotiating"
        ]
        
        # Benefits to negotiate
        strategy["benefits_to_negotiate"] = self.negotiable_benefits
        
        # Timing advice
        strategy["timing_advice"] = {
            "best_time": "After receiving a formal offer but before accepting",
            "avoid": "During the first interview or before an offer is made",
            "deadline": "Ask for 24-48 hours to review the offer",
            "follow_up": "If no response in 3-5 business days, follow up politely"
        }
        
        # Counter offer strategy
        target = estimate['target_salary']
        ask_for = int(target * 1.15)  # Ask for 15% more than target
        
        strategy["counter_offer_strategy"] = {
            "target_salary": target,
            "ask_for": ask_for,
            "minimum_acceptable": estimate['min_salary'],
            "rationale": f"""
Your target salary is ${target:,}, but you should ask for ${ask_for:,} (15% higher).
This gives you room to negotiate down while still reaching your target.

Never go below ${estimate['min_salary']:,} unless the benefits package is exceptional.
""",
            "email_template": f"""
Subject: Re: Job Offer - [Position Title]

Dear [Hiring Manager],

Thank you for extending the offer for the [Position Title] role. I'm very excited about 
the opportunity to join [Company] and contribute to the team.

After careful consideration of the offer and market research, I would like to discuss 
the compensation package. Based on my experience and the value I can bring to the role, 
I was hoping for a salary closer to ${ask_for:,}.

I'm confident that my skills in [key skills] and my track record of [achievements] 
will make a significant impact on your team.

I'm flexible and open to discussion. Could we schedule a call to discuss this further?

Thank you for your consideration.

Best regards,
Sam Salameh
"""
        }
        
        return strategy
    
    def format_negotiation_guide(self, strategy: Dict[str, Any], job: Dict[str, Any]) -> str:
        """Format negotiation strategy as readable guide"""
        
        estimate = strategy['salary_estimate']
        
        doc = f"""
# 💰 Salary Negotiation Guide

## Position: {job.get('title', 'N/A')}
## Company: {job.get('company', 'N/A')}
## Location: {job.get('location', 'N/A')}

---

## 📊 Salary Estimate

**Experience Level:** {estimate['level'].title()}
**Region:** {estimate['region'].replace('_', ' ').title()}

**Salary Range:**
- Minimum: ${estimate['min_salary']:,} {estimate['currency']}/{estimate['period']}
- Target: ${estimate['target_salary']:,} {estimate['currency']}/{estimate['period']}
- Maximum: ${estimate['max_salary']:,} {estimate['currency']}/{estimate['period']}

---

## 🎯 Negotiation Tips

"""
        for tip in strategy['negotiation_tips']:
            doc += f"{tip}\n"
        
        doc += "\n---\n\n## 💬 What to Say\n\n"
        for situation, response in strategy['what_to_say'].items():
            doc += f"### {situation.replace('_', ' ').title()}\n{response}\n\n"
        
        doc += "---\n\n## ❌ What NOT to Say\n\n"
        for item in strategy['what_not_to_say']:
            doc += f"{item}\n"
        
        doc += "\n---\n\n## 🎁 Benefits to Negotiate\n\n"
        for i, benefit in enumerate(strategy['benefits_to_negotiate'], 1):
            doc += f"{i}. {benefit}\n"
        
        doc += "\n---\n\n## ⏰ Timing Advice\n\n"
        for key, value in strategy['timing_advice'].items():
            doc += f"**{key.replace('_', ' ').title()}:** {value}\n\n"
        
        counter = strategy['counter_offer_strategy']
        doc += f"""---

## 🔄 Counter Offer Strategy

**Your Target:** ${counter['target_salary']:,}
**Ask For:** ${counter['ask_for']:,}
**Minimum Acceptable:** ${counter['minimum_acceptable']:,}

### Rationale:
{counter['rationale']}

### Email Template:
```
{counter['email_template']}
```

---

## 📝 Negotiation Checklist

- [ ] Research market rates for this position
- [ ] Know your minimum acceptable salary
- [ ] Prepare your value proposition
- [ ] List your achievements and skills
- [ ] Research the company's compensation philosophy
- [ ] Prepare questions about benefits
- [ ] Practice your negotiation conversation
- [ ] Get the offer in writing
- [ ] Take 24-48 hours to review
- [ ] Negotiate professionally and respectfully
- [ ] Get final agreement in writing
- [ ] Celebrate your success! 🎉

---

**Remember: Negotiation is expected and respected. Good luck! 💪**
"""
        return doc


def estimate_salary(job: Dict[str, Any]) -> Dict[str, Any]:
    """Quick helper to estimate salary"""
    negotiator = SalaryNegotiator()
    return negotiator.estimate_salary(job)


def generate_negotiation_guide(job: Dict[str, Any]) -> str:
    """Quick helper to generate negotiation guide"""
    negotiator = SalaryNegotiator()
    strategy = negotiator.generate_negotiation_strategy(job)
    return negotiator.format_negotiation_guide(strategy, job)
