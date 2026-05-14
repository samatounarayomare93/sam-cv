import logging
import json
import re
from typing import Dict, Optional
from core.ai_agent import OmniIntelligence
from urllib.parse import urlparse

class ScraperPatrol:
    """
    HEALER INTELLIGENCE: The self-healing immune system for crawlers.
    Uses the AI brain to automatically repair broken extraction logic.
    """
    
    def __init__(self, ai_agent: Optional[OmniIntelligence] = None, db = None):
        self.ai = ai_agent or OmniIntelligence()
        self.db = db
        self._pattern_cache = {}

    async def get_selectors(self, url: str) -> Dict:
        """Retrieves active selectors for a domain, with dynamic patch overlay."""
        domain = urlparse(url).netloc.replace("www.", "")
        
        # Default selectors (can be moved to a config file)
        default_selectors = {
            "title": "h1, h2, .job-title, .title",
            "company": ".company, .employer, .company-name",
            "description": ".description, .job-description, #job-details",
            "email": "auto" # regex extraction
        }
        
        if self.db:
            patch = await self.db.get_site_patch(domain)
            if patch:
                logging.info(f"🧬 APPLYING AI PATCH for {domain}...")
                return {**default_selectors, **patch}
        
        return default_selectors

    async def auto_repair(self, url: str, html_snippet: str) -> Dict:
        """
        SINGULARITY PROTOCOL: AI-driven autonomous repair.
        Takes broken HTML and returns corrected selectors.
        """
        domain = urlparse(url).netloc.replace("www.", "")
        logging.info(f"🛠️ REPAIRING SCRAPER: Analyzing broken structure for {domain}...")
        
        prompt = f"""
        Act as a Web Scraping Expert. A site's HTML has changed and my crawler broke. 
        Analyze this HTML snippet and provide valid CSS selectors for:
        1. 'job_title'
        2. 'company_name'
        3. 'job_description'
        
        HTML SNIPPET:
        {html_snippet[:2000]}
        
        Return ONLY valid JSON:
        {{
            "title": "css_selector",
            "company": "css_selector",
            "description": "css_selector"
        }}
        """
        
        try:
            # Fix: _extract_json_robustly is sync and parses JSON from text, not an AI call.
            # We need to call the AI first, then parse the response.
            if hasattr(self.ai, 'structural_query'):
                # structural_query calls Groq with json_object format — perfect for this
                selectors = await self.ai.structural_query(prompt)
            else:
                # Fallback: call analyze_job and extract from response
                selectors = {}
            if selectors and "title" in selectors:
                if self.db:
                    await self.db.save_site_patch(domain, selectors)
                return selectors
        except Exception as e:
            logging.error(f"❌ Scraper Healing Failed: {e}")
            
        return {}

# Singleton instance
_patrol_instance = None

def get_patrol(ai=None, db=None):
    global _patrol_instance
    if _patrol_instance is None:
        _patrol_instance = ScraperPatrol(ai, db)
    return _patrol_instance
