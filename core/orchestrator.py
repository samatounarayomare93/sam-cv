import asyncio
import logging
import os
from typing import Any, Dict

from dotenv import load_dotenv

from core.ai_agent import OmniIntelligence
from core.db_client import RealityShapingDB
from core.follow_up_engine import FollowUpEngine
from core.lead_processor import LeadProcessor
from core.runtime_helpers import HumanParityJitter, TelegramNotifier
from core.scrape_service import ScrapeService
from core.scheduler import Scheduler

load_dotenv()

logging.basicConfig(
    level=getattr(logging, os.getenv("DIVINE_LOG_LEVEL", "INFO")),
    format="%(asctime)s - [CHRONOS] %(levelname)s - %(message)s",
)


class AlphaOrchestrator:
    @staticmethod
    def validate_preflight() -> Dict[str, Any]:
        from core.scrape_service import ScrapeService
        required = {
            'telemetry_enabled': bool(os.getenv('TELEGRAM_BOT_TOKEN') and os.getenv('TELEGRAM_CHAT_ID')),
            'db_available': bool(os.getenv('SUPABASE_URL') and os.getenv('SUPABASE_KEY')),
            'brevo_ready': bool(os.getenv('BREVO_SMTP_LOGIN') and (os.getenv('BREVO_SMTP_PASSWORD') or os.getenv('BREVO_API_KEY'))),
            'gmail_ready': bool(os.getenv('GMAIL_SMTP_USER') and os.getenv('GMAIL_APP_PASSWORD')),
            'outlook_ready': bool(os.getenv('OUTLOOK_USER') and os.getenv('OUTLOOK_PASSWORD')),
            'scraper_available': ScrapeService.is_available(),
        }
        required['at_least_one_mailer'] = any([required['brevo_ready'], required['gmail_ready'], required['outlook_ready']])
        required['ready'] = required['at_least_one_mailer'] and required['scraper_available']
        return required

    def __init__(self, concurrency_limit: int = int(os.getenv("MAX_PARALLEL_STRIKES", "5"))):
        self.semaphore = asyncio.Semaphore(concurrency_limit)
        self.telemetry = TelegramNotifier()
        self.jitter = HumanParityJitter()
        self.is_running = True
        self.db = RealityShapingDB() if RealityShapingDB else None
        self.ai = OmniIntelligence() if OmniIntelligence else None
        self.follow_up = FollowUpEngine(self.db, self.ai)
        self.lead_processor = LeadProcessor(self.ai, db=self.db, telemetry=self.telemetry)
        self.scrape_service = ScrapeService(self.semaphore, omni_crawler=None)
        self.scheduler = Scheduler(
            follow_up_engine=self.follow_up,
            telemetry=self.telemetry,
            jitter=self.jitter,
            scrape_service=self.scrape_service,
            lead_processor=self.lead_processor,
            kill_switch_cb=self.check_kill_switch,
            preflight_cb=self.validate_preflight,
        )

    async def check_kill_switch(self) -> bool:
        kill_switch = os.getenv("KILL_SWITCH_ACTIVE", "False").lower() == "true"
        if kill_switch:
            logging.critical("🛑 KILL SWITCH ENGAGED. HALTING ALL OPERATIONS.")
            self.is_running = False
            self.scheduler.is_running = False
        return kill_switch

    async def execute_divine_loop(self):
        await self.scheduler.run()

    async def close(self):
        await self.scrape_service.close()
        if self.db:
            await self.db.close()
        if self.ai:
            await self.ai.close()


async def run_orchestrator():
    bot = AlphaOrchestrator()
    try:
        await bot.execute_divine_loop()
    finally:
        await bot.close()
