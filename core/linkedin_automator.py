import logging
import inspect
from typing import Optional
from core.ai_agent import OmniIntelligence

class NeuralLinkedIn:
    """
    [🕵️ PHASE NEURAL: COGNITIVE NETWORKING]
    The system's interpersonal influence engine. Generates hyper-personalized
    LinkedIn connection requests to bypass recruiter defenses.
    """
    def __init__(self, ai: OmniIntelligence):
        self.ai = ai

    async def generate_nudge(self, recruiter_name: str, company: str, job_title: str, recent_news: Optional[str] = None) -> str:
        """Generates a high-conversion connection request message."""
        logging.info(f"🧠 NEURAL: Generating personalized nudge for {recruiter_name} at {company}...")
        
        prompt = f"""
        Role: Sovereign Recruitment Strategist.
        Task: Return JSON with one key: nudge.
        The nudge must be a LinkedIn connection request with max 200 characters.
        Recipient: {recruiter_name} (Recruiter)
        Company: {company}
        Target Role: {job_title}
        Mission: Establish 'Human Parity' and 'Insider' status.
        
        Context:
        Recent Company News: {recent_news or 'Expanding operations in the region.'}
        
        Rules:
        1. MAX 200 characters including spaces.
        2. DO NOT use generic 'hope you are well'.
        3. Mention the specific news or a high-level strategic alignment.
        4. Tone: Professional, Efficient, Visionary.
        5. Output format: {{"nudge": "..."}}
        """
        
        try:
            # Use structural_query if available, otherwise use analyze_job
            if hasattr(self.ai, 'structural_query'):
                data = await self.ai.structural_query(prompt)
                message = ""
                if isinstance(data, dict):
                    message = str(data.get("nudge") or data.get("message") or "").strip()
            else:
                message = ""
            
            if not message:
                # Fallback to a high-converting static template if JSON parsing fails
                message = f"Hi {recruiter_name}, saw your work with {company}. Given your recent growth, I'd love to connect and share my expertise in {job_title} management. Best, Sam."
            
            # [🕵️ PHASE SHADOW]: Shield the message from automated keyword filters
            if hasattr(self.ai, 'encode_shadow_text'):
                message = self.ai.encode_shadow_text(message)
            
            return message[:200]
        except Exception as e:
            logging.error(f"Neural Nudge generation failed: {e}")
            fallback = f"Hi {recruiter_name}, I'm specialized in {job_title} and noticed {company}'s expansion. Would love to connect."
            return fallback[:200]

    async def record_nudge_task(self, db, recruiter_name: str, message: str, recruiter_url: str = None):
        """Saves the connection request for manual or automated execution."""
        logging.info(f"📝 NEURAL: Connection task recorded for {recruiter_name}.")
        task_data = {
            "type": "LINKEDIN_NUDGE",
            "target": recruiter_name,
            "message": f"URL: {recruiter_url}\n\nNudge: {message}"
        }
        save_task = getattr(db, "save_task", None)
        if not callable(save_task):
            raise AttributeError("Database object does not expose save_task")

        maybe_awaitable = save_task(task_data)
        if inspect.isawaitable(maybe_awaitable):
            await maybe_awaitable
