import asyncio
import logging
import os
from typing import Any, Dict, Optional

from core.cv_tailor import get_tailored_cv_path
from core.lead_schema import normalize_lead
from core.pdf_generator import create_personalized_pdf
from core.smtp_engine import send_strike

# Import threshold from config so it's controlled from one place
try:
    from core.config import MIN_MATCH_SCORE as _CFG_MIN_SCORE
    _MIN_SCORE = int(_CFG_MIN_SCORE)
except Exception:
    _MIN_SCORE = 75  # safe fallback


class LeadProcessor:
    def __init__(self, ai, db=None, telemetry=None, omni_crawler=None):
        self.ai = ai
        self.db = db
        self.telemetry = telemetry
        self.omni_crawler = omni_crawler
        self.cycle_stats = {
            'raw_leads': 0,
            'processed_leads': 0,
            'duplicates': 0,
            'rejected': 0,
            'sent': 0,
            'failed': 0,
        }

    def reset_cycle_stats(self):
        self.cycle_stats = {
            'raw_leads': 0,
            'processed_leads': 0,
            'duplicates': 0,
            'rejected': 0,
            'sent': 0,
            'failed': 0,
        }

    async def process_single_lead(self, lead: Dict[str, Any], scrape_description_cb=None):
        lead = normalize_lead(lead)
        company_name = lead.get("company_name", "Unknown")
        job_title = lead.get("job_title", "Role")
        job_url = lead.get("link", "")
        email = lead.get("email", "")
        description = lead.get("description", "")
        is_recon = lead.get("is_guessed", False)
        self.cycle_stats['processed_leads'] += 1
        identifier = job_url if job_url else email

        if self.db and identifier and await self.db.is_duplicate(identifier):
            self.cycle_stats['duplicates'] += 1
            return

        if not description and job_url and scrape_description_cb:
            description = await scrape_description_cb(job_url)

        if not self.ai:
            return

        try:
            is_relevant, reason, cover_letter, salary, score, advantage, keywords, persona, psych_variant, personality_archetype, highlights = await self.ai.analyze_job(
                job_title, description[:3000] if description else ""
            )
        except Exception as e:
            logging.warning(f"⚠️ [AI] analyze_job failed for {company_name}: {e} — skipping lead")
            return

        if not is_relevant or score < _MIN_SCORE:
            self.cycle_stats['rejected'] += 1
            return

        if not email and score >= 90 and self.omni_crawler:
            emails = await self.omni_crawler.recon_surge(company_name)
            if emails:
                email = emails[0]

        if not email:
            return

        tailored_html_path = await asyncio.to_thread(
            get_tailored_cv_path,
            company_name.replace(" ", "_"),
            job_title,
            advantage,
            keywords,
        )
        lead.update({
            "custom_body": cover_letter,
            "mission_type": "Evolutionary_Apex_Strike",
            "tailored_cv_path": tailored_html_path,
            "culture_persona": persona,
            "psychological_variant": psych_variant,
            "email": email,
        })

        pdf_path = await asyncio.to_thread(create_personalized_pdf, lead)
        if pdf_path and os.path.exists(pdf_path):
            success = await asyncio.to_thread(send_strike, lead, pdf_path)
            if success:
                self.cycle_stats['sent'] += 1
                if self.db:
                    await self.db.log_application({
                        "company_name": company_name,
                        "job_title": job_title,
                        "email": email,
                        "url": job_url,
                        "mission_type": "World_Class_Global_Strike",
                        "score": score,
                        "is_recon": is_recon,
                    })
            else:
                self.cycle_stats['failed'] += 1
