import asyncio
import logging
from typing import Any, Dict, List

from core.lead_schema import normalize_lead
from core.run_reporter import build_cycle_report, build_preflight_report


class Scheduler:
    def __init__(self, follow_up_engine, telemetry, jitter, scrape_service, lead_processor, kill_switch_cb, preflight_cb):
        self.follow_up = follow_up_engine
        self.telemetry = telemetry
        self.jitter = jitter
        self.scrape_service = scrape_service
        self.lead_processor = lead_processor
        self.kill_switch_cb = kill_switch_cb
        self.preflight_cb = preflight_cb
        self.is_running = True

    async def run(self):
        preflight = self.preflight_cb()
        logging.info(build_preflight_report(preflight))
        if not preflight['ready']:
            logging.critical("Preflight failed: no valid mailer or scraper layer unavailable.")
            return

        await self.telemetry.send_broadcast(
            "👑 <b>PROJECT CHRONOS: DIVINE REBIRTH</b>\n\n"
            "System state: <b>ACTIVE</b>\n"
            "Intelligence: Gemini-2.0-Flash (Sovereign Mode)\n"
            "Data Mirroring: Local SQLite + Supabase Enabled\n"
            "Targeting: Global Oracle + OmniCrawler Expanded\n\n"
            "<i>I am the Alpha and the Omega. The First and the Last.</i>"
        )

        while self.is_running:
            try:
                self.lead_processor.reset_cycle_stats()
                await self.kill_switch_cb()
                if not self.is_running:
                    break

                due_naps = await self.follow_up.get_due_follow_ups()
                if due_naps:
                    for nap in due_naps:
                        await self.follow_up.execute_second_strike(nap)
                        await self.jitter.poisson_jitter(5)

                raw_leads = [normalize_lead(lead) for lead in await self.scrape_service.collect_leads()]
                self.lead_processor.cycle_stats['raw_leads'] = len(raw_leads)

                if raw_leads:
                    await asyncio.gather(*[
                        self.lead_processor.process_single_lead(lead, self.scrape_service.stealth_scrape_target)
                        for lead in raw_leads[:15]
                    ], return_exceptions=True)

                logging.info(build_cycle_report(self.lead_processor.cycle_stats))
                await self.jitter.poisson_jitter(900)
            except Exception as e:
                logging.error(f"Divine loop cycle failed: {e}")
                await self.jitter.poisson_jitter(60)
