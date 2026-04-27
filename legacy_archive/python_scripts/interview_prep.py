"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    📚 INTERVIEW PREPARATION SYSTEM 📚                          ║
║                                                                              ║
║         AI-Generated Questions & Answers for HR Interviews                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
"""

INTERVIEW_DATA = {
    "general_questions": [
        {
            "question": "Tell me about yourself.",
            "category": "Introduction",
            "tips": [
                "Keep it professional, 2-3 minutes max",
                "Start with education and early career",
                "Focus on HR experience and achievements",
                "End with why you're interested in THIS role"
            ],
            "sample_answer": """I graduated with a Bachelor's degree in Human Resources from Lebanese Canadian University in 2016. 

My HR journey began in recruitment, where I discovered my passion for connecting the right people with the right opportunities. I spent several years honing my skills in full-cycle recruitment, payroll administration, and employee relations.

In my most recent role as HR & Operations Coordinator, I've been responsible for managing all HR functions including recruitment, onboarding, employee documentation, and payroll synchronization. I've implemented cost-saving initiatives that resulted in a 25% reduction in operational expenses.

What excites me about this opportunity is [company name]'s commitment to [specific company value or goal], and I believe my experience in [relevant skill] would allow me to contribute meaningfully from day one."""
        },
        {
            "question": "What are your greatest strengths?",
            "category": "Self-Assessment",
            "tips": [
                "Choose 3 strengths relevant to the role",
                "Provide specific examples for each",
                "Use the STAR method (Situation, Task, Action, Result)"
            ],
            "sample_answer": """My three greatest strengths are:

1. RECRUITMENT EXPERTISE: I've successfully placed over 50 candidates across various industries using LinkedIn, job boards, and direct sourcing. My time-to-fill has decreased by 30% through optimized screening processes.

2. COMPLIANCE & ATTENTION TO DETAIL: I've maintained 100% accuracy in employee records and payroll processing across high-volume workloads. I understand the critical nature of HR compliance.

3. PROCESS OPTIMIZATION: I identified inefficiencies in our onboarding workflow and redesigned it, reducing administrative overhead by 25% while improving new hire satisfaction scores."""
        },
        {
            "question": "What is your biggest weakness?",
            "category": "Self-Assessment",
            "tips": [
                "Be honest but strategic",
                "Choose a real weakness",
                "Show how you're improving it",
                "Never say 'I have no weaknesses'"
            ],
            "sample_answer": """One area I've been working to improve is public speaking. Early in my career, I avoided presenting to large groups.

However, I've taken proactive steps to address this. I've enrolled in communication courses and volunteered to lead team meetings. Last year, I successfully conducted training sessions for 50+ employees on our new HRIS system.

I'm now comfortable presenting to larger groups and view these opportunities as valuable for team alignment. I've learned that preparation and practice are the best remedies for presentation anxiety."""
        },
        {
            "question": "Why do you want to work here?",
            "category": "Motivation",
            "tips": [
                "Research the company beforehand",
                "Align your values with theirs",
                "Show genuine interest",
                "Be specific about what attracts you"
            ],
            "sample_answer": """I'm particularly drawn to [Company Name] for several reasons:

1. YOUR REPUTATION: [Company] is recognized as a leader in [industry], and I want to be part of a team that sets industry standards.

2. GROWTH OPPORTUNITY: Your focus on [specific initiative] aligns perfectly with my career goals in [area]. I'm excited about the possibility of growing alongside an organization that's committed to innovation.

3. CULTURE FIT: Your values of [specific values] resonate with my personal approach to work. I believe in [relevant value] and have demonstrated this throughout my career.

4. IMPACT POTENTIAL: In this role, I see an opportunity to make a significant impact on [specific area], which is something I'm passionate about."""
        },
        {
            "question": "Where do you see yourself in 5 years?",
            "category": "Career Goals",
            "tips": [
                "Be realistic but ambitious",
                "Show commitment to the company",
                "Align with their career paths",
                "Include professional development"
            ],
            "sample_answer": """In five years, I see myself as a Senior HR Business Partner or HR Director, depending on the organization's structure.

My plan to get there includes:
- Earning my SHRM-CP certification within the next year
- Developing expertise in [relevant HR area]
- Building strong relationships with business leaders
- Mentoring junior HR team members

I believe this role at [Company] offers the perfect foundation for this growth, with its emphasis on [relevant aspect] and commitment to developing talent."""
        }
    ],
    
    "hr_specific_questions": [
        {
            "question": "Describe your experience with HRIS systems.",
            "category": "Technical",
            "tips": [
                "List specific systems you've used",
                "Describe your proficiency level",
                "Mention any implementation experience"
            ],
            "sample_answer": """I've worked extensively with several HRIS platforms:

SAP SuccessFactors: Used for employee data management, time tracking, and reporting. I'm proficient in running complex reports and maintaining data integrity.

Workday: Implemented at a previous employer. I was involved in the configuration phase and trained 30+ employees on the system.

Custom CRM Systems: Built and optimized recruitment workflows in our proprietary ATS, reducing time-to-hire by 20%.

I'm also proficient in Microsoft Suite, particularly Excel for HR analytics and reporting. I'm a quick learner and adapt easily to new systems."""
        },
        {
            "question": "How do you stay updated with employment laws?",
            "category": "Compliance",
            "tips": [
                "Show proactive learning attitude",
                "Mention specific resources",
                "Give examples of recent changes you've handled"
            ],
            "sample_answer": """Staying current with employment laws is critical in HR. Here's how I ensure compliance:

1. INDUSTRY RESOURCES: I subscribe to SHRM, HR Daily, and local labor department updates. I also participate in HR forums and webinars.

2. PROFESSIONAL NETWORK: I'm part of an HR community where we share regulatory updates and best practices. This provides real-world insights.

3. CONTINUOUS TRAINING: I completed a Health & Safety certification recently to broaden my compliance knowledge.

4. LOCAL KNOWLEDGE: Given my location in Lebanon with openness to GCC relocation, I stay informed about both Lebanese labor laws and GCC regulations."""
        },
        {
            "question": "How would you handle a conflict between employees?",
            "category": "Employee Relations",
            "tips": [
                "Follow proper conflict resolution steps",
                "Emphasize confidentiality",
                "Show mediation skills"
            ],
            "sample_answer": """I follow a structured approach to conflict resolution:

1. INITIAL ASSESSMENT: Meet with each party separately to understand their perspective. Document the issues while maintaining confidentiality.

2. IDENTIFY COMMON GROUND: Find shared goals or interests that can serve as a foundation for resolution.

3. FACILITATE DIALOGUE: Bring parties together in a neutral setting. I guide the conversation using active listening and ask solution-focused questions.

4. DEVELOP ACTION PLAN: Collaboratively create an agreement with specific, measurable steps.

5. FOLLOW-UP: Check in after 2-4 weeks to ensure resolution is holding.

For example, I resolved a conflict between two team members over workload distribution by facilitating a conversation that led to a new task allocation system that worked for everyone."""
        },
        {
            "question": "Describe your recruitment process from start to finish.",
            "category": "Recruitment",
            "tips": [
                "Be detailed and methodical",
                "Include metrics where possible",
                "Show end-to-end ownership"
            ],
            "sample_answer": """My recruitment process follows these steps:

1. NEEDS ANALYSIS: Meet with hiring manager to understand role requirements, team dynamics, and must-have vs. nice-to-have qualifications.

2. JOB DESCRIPTION: Create compelling JD that reflects company culture while clearly stating requirements.

3. SOURCING: Use multi-channel approach:
   - LinkedIn Recruiter and job boards (60%)
   - Employee referrals (25%)
   - Direct sourcing/cold outreach (15%)

4. SCREENING: Initial phone/video screening (30 min) to assess:
   - Communication skills
   - Cultural fit indicators
   - Basic qualifications

5. ASSESSMENT: Skills testing or case study relevant to role.

6. INTERVIEW: Structured interviews with behavior-based questions. Debrief with panel within 24 hours.

7. REFERENCE CHECK: 3 professional references with standardized questions.

8. OFFER: Compensation discussion, negotiation if needed, and onboarding coordination.

9. ONBOARDING: Ensure smooth transition with welcome package, system access, and buddy assignment."""
        },
        {
            "question": "How do you measure HR success?",
            "category": "Metrics",
            "tips": [
                "Know key HR metrics",
                "Show business acumen",
                "Balance hard and soft metrics"
            ],
            "sample_answer": """I believe HR success should be measured across three dimensions:

SOFT METRICS:
- Employee satisfaction/engagement scores
- Manager effectiveness ratings
- Culture and values alignment

HARD METRICS:
- Time-to-fill (I aim for 30-45 days for standard roles)
- Retention rates (target: 85%+ first-year retention)
- Cost-per-hire
- Training ROI

BUSINESS IMPACT:
- Revenue per employee
- HR operating cost as % of total
- Compliance incidents/audits passed
- Employee productivity gains

I regularly track these metrics and present quarterly reports to leadership showing HR's contribution to business outcomes."""
        },
        {
            "question": "Tell me about a time you had to handle a difficult termination.",
            "category": "Sensitive Situations",
            "tips": [
                "Show empathy and professionalism",
                "Follow legal guidelines",
                "Emphasize support provided"
            ],
            "sample_answer": """I once had to manage the termination of a long-tenured employee due to company restructuring.

MY APPROACH:

1. PREPARATION: I reviewed all documentation, ensured legal compliance, and prepared a comprehensive severance package approved by leadership.

2. PRIVATE MEETING: I scheduled a private, dignified conversation. I led with empathy while being clear about the decision.

3. EXPLANATION: I explained the business rationale (restructuring, not performance) and provided documentation.

4. SUPPORT: I offered:
   - Severance pay
   - Career counseling services
   - Positive reference letter
   - Extended benefits

5. TRANSITION: We discussed how to communicate to the team, ensuring professionalism and respect.

The employee appreciated the transparency and dignity with which the process was handled. They later sent a thank-you note for the support provided."""
        },
        {
            "question": "How would you onboard a new employee effectively?",
            "category": "Onboarding",
            "tips": [
                "Show systematic approach",
                "Include first-day, first-week, first-month",
                "Emphasize engagement and retention"
            ],
            "sample_answer": """Effective onboarding is critical for retention. I follow a 30-60-90 day framework:

DAY 1:
- Welcome meeting with team
- System access and workspace setup
- Company handbook and policies review
- Introduction to key contacts

FIRST WEEK:
- Role-specific training begins
- Meet with direct manager for goal setting
- Buddy/mentor introduction
- Social integration activities

FIRST MONTH:
- 30-day check-in to address questions
- Initial skill assessment
- First small project assignment
- Informal feedback session

90-DAY PLAN:
- Goal review and adjustment
- Full productivity expectation
- 90-day performance discussion
- Long-term career path discussion

I track onboarding completion and new hire satisfaction through surveys to continuously improve the process."""
        },
        {
            "question": "How do you handle confidential information?",
            "category": "Ethics",
            "tips": [
                "Show integrity",
                "Give examples",
                "Mention systems/protocols"
            ],
            "sample_answer": """Handling confidential information is a cornerstone of HR. Here's my approach:

SYSTEMS:
- Password-protected HRIS with role-based access
- Encrypted file storage for sensitive documents
- Clean desk policy for physical documents

PROTOCOLS:
- I only access information necessary for my role
- Employee data is shared on need-to-know basis only
- All discussions happen in private settings

EXAMPLES:
- Salary information is never discussed openly
- Performance issues are handled confidentially
- Medical information is stored separately with restricted access

I understand that trust is essential in HR, and breaches of confidentiality can have serious legal and personal consequences."""
        }
    ],
    
    "behavioral_questions": [
        {
            "question": "Tell me about a time you improved a process.",
            "category": "Problem Solving",
            "star_example": {
                "situation": "Our employee onboarding process was taking 3 weeks due to multiple disconnected steps.",
                "task": "I was tasked with streamlining the onboarding to improve new hire satisfaction.",
                "action": "I mapped out the entire process, identified bottlenecks (IT setup delays, paperwork back-and-forth), and created a centralized onboarding checklist. I coordinated with IT, HR, and managers to parallelize tasks.",
                "result": "Reduced onboarding time to 1 week. New hire satisfaction scores increased from 70% to 92%. HR time spent per onboarding decreased by 40%."
            }
        },
        {
            "question": "Describe a time you had to manage multiple priorities.",
            "category": "Time Management",
            "star_example": {
                "situation": "During a busy quarter, our HR team of 2 had to handle recruitment for 15 open positions while also managing annual benefits enrollment.",
                "task": "Ensure all deadlines were met without compromising quality.",
                "action": "I prioritized tasks using urgency/importance matrix. I batched similar activities, delegated where possible, and worked with management to extend non-critical deadlines by 1 week.",
                "result": "All 15 positions were filled within SLA. Benefits enrollment completed on time with 98% participation rate. Zero quality issues reported."
            }
        },
        {
            "question": "Tell me about a time you failed and what you learned.",
            "category": "Growth Mindset",
            "star_example": {
                "situation": "I implemented a new performance review system without adequately training managers on the new process.",
                "task": "Roll out the new system on schedule.",
                "action": "I pushed forward with a quick training session because of time constraints. The result was inconsistent adoption and incomplete reviews.",
                "result": "I took ownership, provided additional 1:1 coaching to managers, and created quick-reference guides. The system was eventually adopted successfully. I now build in more training buffer time and pilot programs before full rollout."
            }
        }
    ],
    
    "salary_negotiation": {
        "question": "What are your salary expectations?",
        "best_response": """I'm open to discussing compensation and am confident we'll find a mutually beneficial arrangement. 

Based on my research of similar roles in the GCC market and my 5+ years of HR experience, I believe a competitive range would be [X-Y] USD annually, plus benefits.

However, I'm more focused on finding a role where I can make a meaningful impact and grow professionally. I'm confident that [Company] offers the growth opportunity I'm seeking, and I'm sure we can come to an agreement that reflects the value I'll bring to the team."""
    }
}

def get_interview_prep(role="HR Manager"):
    """Get comprehensive interview preparation for HR role"""
    return INTERVIEW_DATA

def print_question(q, num):
    """Pretty print a question"""
    print(f"\n{'═'*60}")
    print(f"  QUESTION #{num}")
    print(f"{'═'*60}")
    print(f"\n  📌 {q['question']}")
    print(f"  📂 Category: {q.get('category', 'General')}")
    
    if 'tips' in q:
        print(f"\n  💡 Tips:")
        for tip in q['tips']:
            print(f"     • {tip}")
    
    if 'sample_answer' in q:
        print(f"\n  ✅ Sample Answer:")
        print("  " + "─"*55)
        for line in q['sample_answer'].strip().split('\n'):
            print(f"  {line}")
        print("  " + "─"*55)
    
    if 'star_example' in q:
        star = q['star_example']
        print(f"\n  📝 STAR Method Example:")
        print(f"     Situation: {star['situation']}")
        print(f"     Task: {star['task']}")
        print(f"     Action: {star['action']}")
        print(f"     Result: {star['result']}")

def main():
    print("""
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║                  📚 INTERVIEW PREPARATION SYSTEM 📚                         ║
    ║                                                                              ║
    ║                    HR & Operations Manager Interview                         ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    print("\n  Select category to prepare:\n")
    print("  [1] 📋 General Questions (Tell me about yourself, strengths, etc.)")
    print("  [2] 💼 HR-Specific Questions (Recruitment, compliance, HRIS)")
    print("  [3] 🎯 Behavioral Questions (STAR method examples)")
    print("  [4] 💰 Salary Negotiation")
    print("  [5] 🎲 Random Practice (All questions)")
    print("  [0] ❌ Exit")
    
    choice = input("\n  Select (0-5): ").strip()
    
    data = INTERVIEW_DATA
    
    if choice == '1':
        questions = data['general_questions']
    elif choice == '2':
        questions = data['hr_specific_questions']
    elif choice == '3':
        questions = data['behavioral_questions']
    elif choice == '4':
        print(f"\n  💰 SALARY NEGOTIATION")
        print(f"\n  📌 {data['salary_negotiation']['question']}")
        print(f"\n  ✅ Best Response Strategy:")
        print("  " + "─"*55)
        print(data['salary_negotiation']['best_response'])
        print("  " + "─"*55)
        return
    elif choice == '5':
        questions = (data['general_questions'] + 
                    data['hr_specific_questions'] + 
                    data['behavioral_questions'])
    else:
        return
    
    print(f"\n\n  Preparing {len(questions)} questions...\n")
    input("  Press ENTER to start...")
    
    for i, q in enumerate(questions, 1):
        print_question(q, i)
        if i < len(questions):
            input("\n  Press ENTER for next question...")
    
    print("\n\n" + "═"*60)
    print("  🎉 INTERVIEW PREP COMPLETE!")
    print("  Good luck with your interview! 🍀")
    print("═"*60)

if __name__ == "__main__":
    main()
