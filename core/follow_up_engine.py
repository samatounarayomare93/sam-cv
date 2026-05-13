import asyncio
import logging


class FollowUpEngine:
    """The Second Strike: persistence protocol for follow-up outreach."""

    def __init__(self, db_client, ai_agent):
        self.db = db_client
        self.ai = ai_agent
        self.days_threshold = 7

    async def get_due_follow_ups(self):
        if not self.db:
            return []
        try:
            return await self.db.get_old_applications(days=self.days_threshold)
        except Exception as e:
            logging.error(f"FollowUpEngine Scan Error: {e}")
            return []

    async def generate_nudge(self, company_name, job_title):
        try:
            if self.ai:
                result = await self.ai.analyze_job(job_title, "Follow up nudge request")
                # result is an 11-tuple: (is_relevant, reason, cover_letter, salary, score, advantage, keywords, persona, variant, archetype, highlights)
                nudge_body = result[2] if result and len(result) > 2 else ""
                return nudge_body[:500] if nudge_body else ""
        except Exception as e:
            logging.warning(f"AI nudge generation failed: {e}")
        return (
            f"<p>Dear {company_name} Hiring Team,</p>"
            f"<p>I am following up on my application for the <b>{job_title}</b> position I submitted last week. "
            "I remain highly interested in joining your team and would welcome the opportunity for a brief call. "
            "Please find my CV attached for your reference.</p>"
            "<p>Best regards,<br>Sam Salameh<br>+961 70 841 1009</p>"
        )

    async def execute_second_strike(self, lead):
        company = lead.get("company_name")
        email = lead.get("email")
        title = lead.get("job_title")

        if not email:
            return False

        nudge = await self.generate_nudge(company, title)

        from core.smtp_engine import send_email
        success = await asyncio.to_thread(send_email, email, company, title, nudge, "followup", "second_strike")

        if success:
            if self.db:
                await self.db.mark_follow_up_sent(lead.get("link") or email)
            logging.info(f"🧬 SECOND STRIKE SUCCESSFUL: {company}")
            return True
        return False
