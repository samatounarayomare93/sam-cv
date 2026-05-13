"""
ENHANCED OMNICRAWLER - MAXIMUM DISCOVERY
=========================================
Multiplied search queries for 10x more targets
"""

import json
import logging
import os
import random
import re
import time
import urllib.parse
import asyncio
import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning, module='ddgs')
warnings.filterwarnings('ignore', message='.*duckduckgo_search.*')
warnings.filterwarnings('ignore', message='.*has been renamed.*')
logging.getLogger("ddgs").setLevel(logging.CRITICAL)
from typing import Optional, Dict, Any

from core.scrapers.stealth_config import USER_AGENTS
from core.scrapers.scraper import fetch_page, _get_deep_dive_count, _increment_deep_dive
from core.db_manager import db_manager
from core.ai_agent import OmniIntelligence
from core.scrapers.healer_intelligence import get_patrol
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS
from urllib.parse import urlparse


def _safe_ddgs_search(query: str, max_results: int = 5, proxy: str = None, headers: dict = None, region: str = 'wt-wt', timeout: int = 20) -> list:
    """[👑 FIX] Thread-safe DDGS search with warning suppression and auto-evasion."""
    import warnings
    warnings.filterwarnings('ignore')
    
    from core.runtime_helpers import get_evasion, get_proxy_mesh
    import logging
    import time
    
    evasion = None
    proxy_mesh = None
    try:
        evasion = get_evasion()
        proxy_mesh = get_proxy_mesh()
    except Exception:
        pass

    for attempt in range(3):
        current_proxy = proxy
        current_headers = headers
        
        if not current_headers and evasion:
            try:
                evasion.rotate_identity()
                current_headers = evasion.get_stealth_headers()
            except Exception:
                pass
                
        if not current_proxy and proxy_mesh:
            try:
                current_proxy = proxy_mesh.get_next_sync()
            except Exception:
                pass
                
        try:
            kwargs = {"timeout": timeout}
            if current_proxy:
                kwargs['proxy'] = current_proxy
            if current_headers:
                kwargs['headers'] = current_headers
                
            with DDGS(**kwargs) as ddgs:
                results = list(ddgs.text(query, max_results=max_results, region=region))
                if results:
                    return results
                return []
        except Exception as e:
            err_str = str(e).lower()
            if "403" in err_str or "rate limit" in err_str or "202" in err_str:
                logging.debug(f"DDGS Rate Limited (attempt {attempt+1}): {e}")
                time.sleep(1 + attempt)
                continue
            return []
            
    return []

class PatternRecon:
    """Russian-style Pattern Discovery: Deduces hidden HR emails from domain intelligence."""
    
    PATTERNS = ["hr", "careers", "jobs", "recruitment", "talent", "info", "contact", "apply"]

    @staticmethod
    def guess_hr_emails(company_url: str) -> list:
        if not company_url: return []
        try:
            domain = urlparse(company_url).netloc
            if not domain: return []
            # Remove www.
            domain = domain.replace("www.", "")
            
            # 🛡️ DNS CHECK: Only guess emails for domains that actually exist
            import socket
            try:
                old_timeout = socket.getdefaulttimeout()
                socket.setdefaulttimeout(3)
                try:
                    socket.getaddrinfo(domain, None, socket.AF_INET, socket.SOCK_STREAM)
                finally:
                    socket.setdefaulttimeout(old_timeout)
            except (socket.gaierror, OSError, socket.timeout):
                logging.debug(f"🚫 DNS FAIL: Domain '{domain}' doesn't exist — skipping email guess")
                return []
            
            # Only return hr@ and careers@ — most reliable patterns
            return [f"hr@{domain}", f"careers@{domain}"]
        except Exception:
            return []

BAD_EMAILS = ['example@', 'support@', 'no-reply@', 'noreply@', 'test@', 'yourname@']
EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# [🎯 SOVEREIGN JOB FILTER]: Only these domains/patterns are valid job sources
JOB_URL_ALLOWLIST = [
    'linkedin.com', 'indeed.com', 'glassdoor.com', 'monster.com', 'reed.co.uk',
    'bayt.com', 'naukri.com', 'naukrigulf.com', 'workable.com', 'greenhouse.io',
    'lever.co', 'weworkremotely.com', 'remoteok.com', 'flexjobs.com', 'wellfound.com',
    'simplyhired.com', 'ziprecruiter.com', 'cv-library.co.uk', 'totaljobs.com',
    'stepstone.de', 'xing.com', 'jobup.ch', 'jobsora.com', 'jobrapido.com',
    'themuse.com', 'builtin.com', 'workday.com', 'smartrecruiters.com', 'icims.com',
    'bamboohr.com', 'ashbyhq.com', 'myworkdayjobs.com', 'taleo.net'
]

# [🚫 NOISE DOMAINS]: These produce garbage results — skip entirely
NOISE_DOMAINS = [
    'youtube.com', 'youtu.be', 'wikipedia.org', 'reddit.com', 'whatsapp.com',
    'facebook.com', 'twitter.com', 'x.com', 'tiktok.com', 'instagram.com',
    'snapchat.com', 'pinterest.com', 'baidu.com', 'zhihu.com',
    'pornhub.com', 'xnxx.com', 'xvideos.com',
    'amazon.com', 'ebay.com', 'aliexpress.com', 'alibaba.com',
    'google.com/search', 'bing.com', 'yahoo.com', 'duckduckgo.com',
    'spotify.com', 'netflix.com', 'apple.com/app', 'play.google.com',
    'microsoft.com/download', 'support.microsoft.com', 'zoom.us/download',
    'nordvpn.com', 'skyscanner', 'booking.com', 'expedia', 'tripadvisor',
    'stackoverflow.com', 'github.com/README', 'w3schools',
    'leboncoin.fr', 'craigslist', 'olx.', 'avito.',
    'zdf.de', 'bis.gov', 'legislation.gov', 'gov.uk', 'state.gov', 'un.org',
    'notion.site', 'docs.google.com', 't.me', 'medium.com', 'substack.com'
]

def _is_valid_job_url(url: str) -> bool:
    """[🎯 SOVEREIGN GATE]: Returns True only if URL looks like a real job/company source."""
    if not url:
        return False
    url_lower = url.lower()
    # Block known noise domains immediately
    for noise in NOISE_DOMAINS:
        if noise in url_lower:
            return False
    # Must match at least one job-related pattern
    for allowed in JOB_URL_ALLOWLIST:
        if allowed in url_lower:
            return True
    return False

def _extract_company_from_title(title: str) -> dict:
    """[🎯 SMART EXTRACT]: Parse company and job title from a search result title."""
    # Common patterns: 'Job Title at Company - Source', 'Company | Job Title', 'Job Title - Company'
    result = {"company": "", "job_title": ""}
    if not title:
        return result
    
    title = title.strip()
    
    # Pattern 1: "Job Title at Company Name"
    if " at " in title:
        parts = title.split(" at ", 1)
        result["job_title"] = parts[0].strip()
        result["company"] = parts[1].split("|")[0].split("-")[0].split("|")[0].strip()
        return result
    
    # Pattern 2: "Company Name hiring Job Title"
    if " hiring " in title.lower():
        parts = title.lower().split(" hiring ", 1)
        result["company"] = title[:len(parts[0])].strip()
        result["job_title"] = title[len(parts[0])+len(" hiring "):].split("|")[0].strip()
        return result
    
    # Pattern 3: "Job Title - Company | Source" or "Job Title | Company"
    for sep in [" - ", " | ", " – "]:
        if sep in title:
            parts = title.split(sep)
            if len(parts) >= 2:
                result["job_title"] = parts[0].strip()
                result["company"] = parts[1].split("|")[0].split("-")[0].strip()
                return result
    
    # Fallback: use title as job_title
    result["job_title"] = title
    return result

class MarketOracle:
    """Singularity Protocol: Finds expansion signals and pre-emptive hiring intent."""
    
    EXPANSION_QUERIES = [
        'company "opening new office" worldwide "HR"',
        'startup "raised funding" Europe "Operations"',
        'corporation "expanding to USA" "Administrative"',
        '"new recruitment drive" global 2024'
    ]

    @staticmethod
    def detect_intent(title: str, snippet: str) -> bool:
        keywords = ['expanding', 'office', 'funding', 'growth', 'hiring', 'recruitment', 'opening']
        return any(k in f"{title} {snippet}".lower() for k in keywords)

    @staticmethod
    async def get_latest_news(company: str) -> str:
        """
        [👑 APEX DEITY] Fetches the latest headline for hyping recon.
        """
        try:
            results = await asyncio.to_thread(_safe_ddgs_search, f"{company} news 2024", 3)
            if results:
                return f"{results[0]['title']}: {results[0]['body'][:100]}..."
        except Exception:
            pass
        return "Expanding global operations and talent acquisition."

    @staticmethod
    async def get_news_pulse(company: str) -> Dict[str, str]:
        """
        [🕵️ APEX DEITY: ORACLE PULSE]
        Detects 'Fear, Uncertainty, Doubt' (FUD) or 'FOMO' signals in company news.
        Allows the AI to pivot Sam as either a 'Crisis Stabilizer' or a 'Growth Rocket'.
        """
        pulse = {"sentiment": "neutral", "event": "Stable Operations", "strategy": "Standard"}
        try:
            results = await asyncio.to_thread(_safe_ddgs_search, f'"{company}" (layoffs OR growth OR "new CEO" OR acquisition OR expansion)', 5)
            
            content = " ".join([r.get('body', '').lower() for r in results if r.get('body')])
            
            if any(x in content for x in ["layoff", "job cuts", "downsizing", "restructuring"]):
                pulse = {"sentiment": "negative", "event": "Restructuring", "strategy": "Efficiency & Stability"}
            elif any(x in content for x in ["funding", "raised", "acquisition", "opening", "growth"]):
                pulse = {"sentiment": "positive", "event": "Rapid Expansion", "strategy": "Scaling & Automation"}
            elif "ceo" in content or "leadership" in content:
                pulse = {"sentiment": "neutral", "event": "Leadership Change", "strategy": "Culture Alignment"}
        except Exception:
            pass
        return pulse

    @staticmethod
    async def get_recruiter_info(company: str, job_title: str) -> Dict[str, str]:
        """
        🕵️ RECRUITER SNIPER: Extracts specific recruiter names and LinkedIn profiles.
        """
        try:
            results = await asyncio.to_thread(_safe_ddgs_search, f"{company} {job_title} recruiter linkedin", 3)
            if results:
                best = results[0]
                name_raw = best['title'].split("-")[0].split("|")[0].strip()
                return {"name": name_raw, "url": best['href']}
        except Exception:
            pass
        return {
            "name": "Talent Acquisition Manager",
            "url": f"https://www.linkedin.com/search/results/people/?keywords={company}%20recruiter"
        }

    @staticmethod
    async def get_culture_values(company: str) -> str:
        """
        🧬 CULTURE HARVESTER: Extracts specific mission-critical keywords.
        """
        try:
            results = await asyncio.to_thread(_safe_ddgs_search, f"{company} mission values culture", 3)
            if results:
                return f"Values Found: {' '.join([r.get('body', '')[:100] for r in results if r.get('body')])}"
        except Exception:
            pass
        return "Innovation, Excellence, Customer Focus."

    @staticmethod
    async def get_competitor_disruption(company: str) -> str:
        """
        🦈 PREDATOR RECON: Finds recent failures of direct rivals.
        """
        try:
            results = await asyncio.to_thread(_safe_ddgs_search, f"{company} top competitors", 2)
            rival = "a top competitor"
            if results: rival = results[0]['title'].split()[0]
            fail_res = await asyncio.to_thread(_safe_ddgs_search, f"{rival} layoff or failure or lawsuit 2024", 1)
            if fail_res:
                return f"{rival} recently faced: {fail_res[0]['title']}"
        except Exception:
            pass
        return "Competitors are currently struggling with operational inertia."

    @staticmethod
    async def get_internal_lingo(company: str) -> str:
        """
        🗣️ INTERNALL LINGO: Extracts company-specific behavioral jargon.
        """
        try:
            results = await asyncio.to_thread(_safe_ddgs_search, f"site:glassdoor.com \"{company}\" interview questions culture", 3)
            if results:
                return f"Lingo Tags: {' '.join([r.get('body', '')[:50] for r in results if r.get('body')])}"
        except Exception:
            pass
        return "Growth mindset, Customer excellence."

    @staticmethod
    async def get_leadership_team(company: str) -> str:
        """
        👔 LEADERSHIP RECON: Finds executive team names.
        """
        try:
            results = await asyncio.to_thread(_safe_ddgs_search, f"{company} leadership team executive officers", 3)
            if results:
                return f"Leadership: {' '.join([r.get('title', '')[:100] for r in results if r.get('title')])}"
        except Exception:
            pass
        return "Executive Leadership Team"

class PlatformDiscovery:
    """[👑 ARCHITECT OF DESTINY] Discovers new job boards, apps, and groups automatically."""
    
    DISCOVERY_QUERIES = [
        'أهم منصات التوظيف العالمية 2024 2025',
        'Telegram "job" recruitment groups worldwide',
        'WhatsApp "recruitment" groups link global',
        'best niche job boards for remote "Operations"',
        '"new recruitment app" worldwide mobile',
        'site:facebook.com "jobs group" global 2024',
        'site:linkedin.com "hiring groups" worldwide',
        'أفضل مجموعات الواتساب للوظائف العالمية',
        'Telegram "HR" global groups list',
        'remote job boards Europe USA Canada Australia'
    ]

    @staticmethod
    async def run_discovery_cycle():
        """Searches for new recruitment platforms and logs them for review."""
        logging.info("🌐 OMNICRAWLER: Initiating Platform Discovery Protocol...")
        discovered = []
        try:
            for query in PlatformDiscovery.DISCOVERY_QUERIES:
                logging.info(f"🔎 Scanning for new platforms: {query[:40]}...")
                results = await asyncio.to_thread(_safe_ddgs_search, query, 20)
                for res in results:
                    url = res.get('href')
                    if url:
                        if ".il" in url.lower() or "israel" in url.lower(): continue
                        await db_manager.client.add_discovered_link(url, source=f"Discovery: {query}")
                        discovered.append(url)
                await asyncio.sleep(5)
        except Exception as e:
            logging.error(f"❌ Platform Discovery Error: {e}")
        
        logging.info(f"🌐 Discovery Complete: {len(discovered)} potential platforms found.")
        return discovered

class OmniCrawler:
    """Multi-spider protocol for discovering job targets across the web."""
    
    # 100% SOVEREIGN SOCIAL QUERIES - Network Engineering focused
    SOCIAL_QUERIES = [
        'site:linkedin.com/posts "hiring" "Network Engineer" UAE',
        'site:linkedin.com/posts "looking for" "IT Infrastructure" Dubai',
        'site:twitter.com "hiring" "Network Engineer" Lebanon',
        'site:linkedin.com/posts "recruitment" "Senior Network Engineer" Gulf'
    ]
    
    # 🔥 IT-SPECIFIC JOB BOARDS (Not on LinkedIn/Indeed - exclusive jobs!)
    IT_JOB_BOARDS = [
        # Global IT boards
        {"name": "Dice.com", "url": "https://www.dice.com/jobs?q=network+engineer&location=UAE", "type": "it_board"},
        {"name": "Jobserve IT", "url": "https://www.jobserve.com/gb/en/Job-Search/?shid=network-engineer", "type": "it_board"},
        {"name": "TechFetch", "url": "https://www.techfetch.com/job/network-engineer-jobs.aspx", "type": "it_board"},
        {"name": "ClearanceJobs", "url": "https://www.clearancejobs.com/jobs?q=network+engineer", "type": "it_board"},
        {"name": "Stack Overflow Jobs", "url": "https://stackoverflow.com/jobs?q=network+engineer", "type": "it_board"},
        # Middle East IT boards
        {"name": "Bayt Network Engineer", "url": "https://www.bayt.com/en/uae/jobs/network-engineer-jobs/", "type": "it_board"},
        {"name": "Naukrigulf Network", "url": "https://www.naukrigulf.com/network-engineer-jobs", "type": "it_board"},
        {"name": "GulfTalent IT", "url": "https://www.gulftalent.com/jobs/it-technology/network-engineer", "type": "it_board"},
        # Lebanon specific
        {"name": "Daleel Madani IT", "url": "https://www.daleel-madani.org/civil-society-directory/jobs?field_job_category=IT", "type": "it_board"},
        {"name": "HireLebanese IT", "url": "https://www.hireleb.com/jobs/it-technology", "type": "it_board"},
    ]

    def __init__(self, ai_agent: Optional[OmniIntelligence] = None):
        self.ai_agent = ai_agent or OmniIntelligence()
        from core.db_client import get_db
        self.db = get_db()
        self.patrol = get_patrol(self.ai_agent, self.db)
        from core.runtime_helpers import get_proxy_mesh
        self.proxy_mesh = get_proxy_mesh()

    def _extract_snippet_emails(self, title: str, snippet: str) -> Optional[str]:
        """Check snippet for emails before visiting URL"""
        all_text = f"{title} {snippet}"
        emails = list(set(re.findall(EMAIL_REGEX, all_text)))
        valid_emails = [e for e in emails if not any(b in e.lower() for b in BAD_EMAILS)]
        
        if valid_emails:
            return valid_emails[0]
        return None

    def _extract_person_name(self, title: str, snippet: str) -> Optional[str]:
        """SOCIAL RECON: Extract potential Hiring Manager / CEO names from snippet"""
        prompt = (
            f"Identify the most likely 'person_name' (e.g. HR Manager, CEO, Founder) from this context. "
            f"Return only the name or 'Unknown'. JSON: {{'person_name': '...'}}\n"
            f"Context: {title} | {snippet}"
        )
        try:
            data = self.ai_agent._extract_json_robustly(prompt)
            name = data.get("person_name", "Unknown")
            return name if name != "Unknown" else None
        except Exception:
            return None

    def _extract_company_info(self, title: str, snippet: str, content: str = "") -> dict:
        """[🎯 FIXED] Extract company and job title using fast regex parsing (AI prompt was broken)."""
        # Use the fast deterministic extractor — no AI call needed for this step
        result = _extract_company_from_title(title)
        if result.get("company") and result["company"].lower() not in ("unknown", "none", ""):
            return result
        
        # Fallback: try snippet for 'at CompanyName' pattern
        if snippet:
            match = re.search(r'\bat\s+([A-Z][\w\s&]+?)(?:\s*[,.|]|\s+is\s|\s+we\s)', snippet)
            if match:
                result["company"] = match.group(1).strip()
        
        if not result.get("company"):
            result["company"] = "Unknown"
        if not result.get("job_title"):
            result["job_title"] = title
        return result

    def calculate_market_priority(self, company: str, job_title: str, location: str, mission_type: str = "standard") -> float:
        """[👑 INFINITY] Calculates the 'Strike Priority' for market arbitrage."""
        score = 10.0
        
        # 🌏 Regional Weighting
        loc_lower = location.lower()
        if any(x in loc_lower for x in ["dubai", "uae", "emirates", "riyadh", "saudi", "qatar", "doha"]):
            score += 15.0 # High value regions
        elif any(x in loc_lower for x in ["london", "uk", "british", "europe"]):
            score += 10.0
            
        # 🏹 Seniority Weighting
        title_lower = job_title.lower()
        if any(x in title_lower for x in ["director", "vp", "chief", "head", "executive"]):
            score += 20.0
        elif "manager" in title_lower:
            score += 10.0
            
        # 🕵️ Mission Weighting (Ghost Jobs)
        if mission_type == "PRE_HIRING_SIGNAL":
            score += 30.0 # Absolute priority for pre-hiring signals
            
        return score

    def _create_job_entry(self, company: str, job_title: str, email: str, url: str, snippet: str, platform: str = "omni", person_name: str = None, mission_type: str = "standard", location: str = "Global Focus") -> dict:
        """Factory method to create standardized job entry with Social Recon data and INFINITY Priority."""
        priority = self.calculate_market_priority(company, job_title, location, mission_type)
        return {
            "company_name": company,
            "email": email,
            "hiring_manager": person_name,
            "location": location,
            "salary": "0",
            "job_title": job_title,
            "description": snippet[:500] if snippet else "",
            "link": url,
            "platform": platform,
            "mission_type": mission_type,
            "priority_score": priority
        }

    async def hunt_expansion_signals(self) -> list:
        """
        [🌏 MULTIVERSE READY]
        Finds companies showing 'Pre-hiring' signals (funding, new office, executive hire).
        These are 'Ghost Jobs' – targets that need a professional before they post an ad.
        """
        logging.info("🕵️ MULTIVERSE: Hunting for pre-hiring expansion signals...")
        leads = []
        try:
            queries = [
                'site:crunchbase.com "raised funding" 2024',
                'site:globenewswire.com "new headquarters" 2024',
                'startup "received seed funding" "Riyadh"',
                'company "expanding office" "Dubai"',
                '"new office opening" "London" 2024'
            ]
            for query in queries:
                results = await asyncio.to_thread(_safe_ddgs_search, query, 5)
                for r in results:
                    company_match = re.search(r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)', r['title'])
                    if company_match:
                        company = company_match.group(1)
                        # Don't guess email — leads without real emails get filtered downstream
                        leads.append({
                            "company_name": company,
                            "job_title": "Senior Network Engineer",
                            "email": None,
                            "description": r['body'],
                            "link": r['href'],
                            "mission_type": "PRE_HIRING_SIGNAL",
                            "location": "Global Focus",
                            "platform": "expansion_recon"
                        })
        except Exception as e:
            logging.error(f"Expansion Hunt Failed: {e}")
        return leads

    async def hunt_the_web(self) -> list:
        """
        GHOST OPS: Search queries for maximum discovery with anti-detection headers.
        """
        logging.info("🕵️‍♂️ OMNI-CRAWLER MAX: Initiating Maximum Batch Reconnaissance...")
        
        # 🌏 MULTIVERSE: Pre-hiring Expansion Signals
        expansion_leads = await self.hunt_expansion_signals()
        
        # GHOST RECON: Deep Discovery Operators
        # 100% SOVEREIGN PROTOCOL: Unified board and social recon hunt.
        # SINGULARITY PROTOCOL: News-based predictive recon.
        queries = [
            # LinkedIn Deep Recon (Worldwide)
            'site:linkedin.com/jobs "Network Engineer" "remote" "apply to"',
            'site:linkedin.com/jobs "IT Infrastructure Manager" USA UK Europe',
            'site:linkedin.com/pulse "hiring" "Network Engineer" "email" worldwide',
            'site:linkedin.com/posts "we are hiring" "Network Engineer" "remote"',
            
            # Global remote jobs
            'site:weworkremotely.com "Network Engineer" "apply"',
            'site:remoteok.com "Network" "hiring"',
            'site:flexjobs.com "IT Infrastructure" "remote"',
            
            # High intent worldwide keywords
            '"Senior Network Engineer" "visa sponsorship" "relocation" worldwide',
            '"Network Administrator" "remote" "employment" "email"',
            '"IT Infrastructure Engineer" Europe "sponsorship" "email"',
            '"Network Security Engineer" "Global" "employment pack"',
            '"Systems Administrator" "remote" "relocation package"',
            '"Network Consultant" "remote" "sponsorship"',
            '"IT Manager" "Global" "relocation"',
            '"NOC Engineer" "remote" "visa sponsorship"',
            '"Cisco Network Engineer" "Global" "employment visa"',
            '"Network Engineer" "Global" "careers@"',
            '"IT Director" Europe "relocation"',
            '"Network Administrator" "remote" "apply now"',
            '"Telecom Engineer" "Global" "sponsorship"',

            # [🇸🇦 KSA & 🇦🇪 UAE SURGE]
            'site:linkedin.com/jobs "Network Engineer" Riyadh "apply"',
            'site:linkedin.com/jobs "IT Manager" Dubai "hiring"',
            'site:linkedin.com/posts "hiring" "Network Engineer" Saudi Arabia',
            'site:linkedin.com/posts "IT Infrastructure" "UAE" "careers@"',
            '"Senior Network Engineer" "NEOM" "recruitment" "email"',
            '"Network Engineer" "Riyadh Air" "apply"',
            '"IT Infrastructure" "Dubai Future Foundation" "careers"',
            
            # [🇪🇺 EUROPEAN REMOTE EXPANSION]
            'site:linkedin.com/jobs "Network Engineer" Berlin "remote" "apply"',
            'site:linkedin.com/jobs "IT Manager" Amsterdam "remote"',
            'site:linkedin.com/posts "hiring" "Remote" Europe "Network Engineer"',
            'site:linkedin.com/posts "IT Infrastructure" "Remote" Germany',
            '"Network Engineer" "London" "remote" "visa"',
            '"Senior Network Engineer" "Zurich" "remote" "hiring"',
            
            # Regional Strike Queries
            '"Network Engineer" "Dubai" "hiring" "email"',
            '"IT Manager" "Saudi Arabia" "remote" "apply"',
            '"Network Administrator" "Abu Dhabi" "visa sponsorship"',
            '"Systems Administrator" "Qatar" "recruitment" "email"',
            '"Regional IT Manager" "Gulf" "employment"',
        ]
        
        # 🕸️ MULTIVERSE: Deep-Web Reconnaissance
        DEEP_WEB_QUERIES = [
            'site:t.me "Network Engineer" "remote" "send CV"',
            'site:t.me "IT Infrastructure" "Global" "hiring"',
            'site:discord.com/channels "startup" "Network Engineer" "hiring"',
            'site:docs.google.com "Job Board" "Global" "Network Engineer"',
            'site:pastebin.com "hiring" "Global" "careers@"',
            'site:notion.site "Open Roles" "Network Engineer" "remote"',
            'site:github.com "awesome-jobs" "Worldwide" "IT Infrastructure"'
        ]
        
        queries = queries + self.SOCIAL_QUERIES + MarketOracle.EXPANSION_QUERIES + DEEP_WEB_QUERIES
        
        batch_queries = random.sample(queries, min(len(queries), 8))  # Max 8 queries to prevent OOM
        discovered_jobs = []
        user_agent = random.choice(USER_AGENTS)
        
        try:
            if DDGS is None:
                logging.warning("DuckDuckGo search unavailable; OmniCrawler skipped.")
                return []
            for search_query in batch_queries:
                if _get_deep_dive_count() >= 200:
                    logging.warning("🛑 Scrape cap reached (200 limit for memory safety).")
                    break
                    
                logging.info(f"🔍 Ghost-Spider [{user_agent[:15]}...]: {search_query[:50]}...")
                
                try:
                    def sync_search():
                        # [🕵️ PHASE RESILIENCE: PROXY FAILOVER GRID]
                        primary_proxy = os.getenv("PROXY_URL")
                        # Use Shadow Grid as primary failover
                        shadow_proxy = self.proxy_mesh.get_next_sync()
                        failover_proxies = [
                            shadow_proxy,
                            None  # Direct fallback (removed dead hardcoded proxy 72.10.252.134)
                        ]
                        
                        proxies_to_try = [primary_proxy] + failover_proxies
                        for proxy in proxies_to_try:
                            try:
                                res = _safe_ddgs_search(search_query, max_results=8, proxy=proxy, headers={"User-Agent": user_agent}, region='wt-wt', timeout=20)
                                if res:
                                    return res
                            except Exception as e:
                                logging.warning(f"Proxy Failure ({proxy}): {e}. Rotating to failover...")
                                continue
                        return []
                    results = await asyncio.to_thread(sync_search)
                except Exception as ddg_err:
                    logging.warning(f"DDG Search Grid Collapse: {ddg_err}")
                    results = []
                
                # [🛡️ RATE-LIMIT FIX]: Delay between queries to avoid 429 from Brave/DDG
                await asyncio.sleep(random.uniform(3, 7))
                if not results:
                    continue
                
                logging.info(f"📊 Found {len(results)} potential targets")
                
                for res in results:
                    if _get_deep_dive_count() >= 200:
                        break
                    
                    url = res.get('href', '')
                    url_lower = url.lower()
                    
                    # [🚫 SOVEREIGN EXCLUSION]: Skip Israel-related results
                    if ".il" in url_lower or "israel" in url_lower:
                        continue
                    
                    # [🧊 DOMAIN COOLING]: Respect Hive-Mind blacklist
                    domain = urlparse(url).netloc.replace("www.", "")
                    if domain and self.db:
                        if await self.db.is_globally_blacklisted(domain):
                            logging.debug(f"🧊 COOLING: Skipping blacklisted domain {domain}")
                            continue
                    
                    # [🎯 JOB GATE]: Skip non-job URLs entirely — this is the primary noise filter
                    if not _is_valid_job_url(url_lower):
                        logging.debug(f"🚫 NOISE FILTERED: {url[:60]}")
                        continue
                        
                    title = res.get('title', '')
                    snippet = res.get('body', '')
                    
                    if not url or not title:
                        continue
                    
                    # [🎯 TITLE GATE]: Skip results whose title looks like a generic webpage
                    JUNK_TITLE_KEYWORDS = [
                        'youtube', 'wikipedia', 'reddit', 'whatsapp', 'instagram', 'facebook',
                        'download', 'télécharger', 'herunterladen', '下载', 'скачать',
                        'login', 'sign in', 'register', 'create account', 'help center',
                        'speed test', 'internet speed', 'how to', 'what is', 'best pizza',
                        'pornhub', 'xnxx', 'adult forum', 'порно',
                    ]
                    if any(junk in title.lower() for junk in JUNK_TITLE_KEYWORDS):
                        logging.debug(f"🚫 JUNK TITLE: {title[:60]}")
                        continue
                    
                    # ORACLE SNIPER: Check snippet for email
                    target_email = self._extract_snippet_emails(title, snippet)
                    is_guessed = False
                    
                    if not target_email:
                        # RUSSIAN RECON: Pattern guessing from domain — ONLY for real job domains
                        guesses = PatternRecon.guess_hr_emails(url)
                        if guesses:
                            target_email = guesses[0]  # Take hr@ pattern
                            is_guessed = True

                    if target_email:
                        tag = "recon" if is_guessed else "oracle"
                        logging.info(f"✨ {tag.upper()}: Email {'guessed' if is_guessed else 'found'}: {target_email}")
                        
                        # SOCIAL RECON: Deep Identity Harvesting
                        person_name = self._extract_person_name(title, snippet)
                        if person_name:
                            logging.info(f"👤 SOCIAL IDENTITY DISCOVERED: {person_name}")

                        intel = self._extract_company_info(title, snippet)
                        company = intel.get("company", "").strip()
                        
                        # [🎯 COMPANY GATE]: Only save if we extracted a real company name
                        if not company or company.lower() in ("unknown", "none", "target node", ""):
                            logging.debug(f"🚫 NO COMPANY: Skipping lead for '{title[:50]}'")
                            continue
                        
                        job = self._create_job_entry(
                            company,
                            intel.get("job_title", title),
                            target_email,
                            url,
                            snippet,
                            tag,
                            person_name=person_name
                        )
                        job['is_guessed'] = is_guessed
                        discovered_jobs.append(job)
                        logging.info(f"✅ LEAD QUALIFIED: {company} | {intel.get('job_title', title)[:40]}")
                        continue
                    
                    # 🧬 SINGULARITY: Early Intent / Founding Strike
                    # If we detect a growth intent but no email, launch a Recon Surge for the CEO
                    if MarketOracle.detect_intent(title, snippet):
                        domain = urlparse(url).netloc.replace("www.", "")
                        if domain:
                            logging.info(f"🧬 GROWTH SIGNAL DETECTED: {domain}. Launching Founding Strike Recon...")
                            ceo_emails = await self.recon_surge(domain.split('.')[0])
                            if ceo_emails:
                                job = self._create_job_entry(
                                    domain.split('.')[0].capitalize(),
                                    "Founding Operations Partner",
                                    ceo_emails[0],
                                    url,
                                    snippet,
                                    "founding_strike"
                                )
                                job['mission_type'] = "Founding_Strike"
                                discovered_jobs.append(job)
                                continue
                    
                    # Deep recon for high-value URLs
                    if any(k in url.lower() for k in ['careers', 'jobs', 'vacancy', 'hiring']):
                        try:
                            time.sleep(random.uniform(1, 3))
                            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                            response = fetch_page(url, headers=headers)
                            
                            if response.status_code == 200:
                                content = response.text
                                
                                # 🛠️ SINGULARITY: AI-Driven Self-Healing
                                # If typical extraction yields nothing, trigger the Healer
                                emails = list(set(re.findall(EMAIL_REGEX, content)))
                                valid_emails = [e for e in emails if not any(b in e.lower() for b in BAD_EMAILS)]
                                
                                if not valid_emails:
                                    logging.info("🧬 SELF-HEAL: No email found in content. Analyzing structure...")
                                    selectors = await self.patrol.get_selectors(url)
                                    # Attempt AI-based repair if we have nothing
                                    if not selectors.get("repaired") and len(content) > 500:
                                        await self.patrol.auto_repair(url, content[:3000])
                                
                                if valid_emails:
                                    target_email = valid_emails[0]
                                else:
                                    # 🛡️ DNS CHECK before guessing
                                    domain = urllib.parse.urlparse(url).netloc.replace("www.", "")
                                    import socket
                                    try:
                                        socket.getaddrinfo(domain, None)
                                        target_email = f"hr@{domain}"
                                    except (socket.gaierror, OSError):
                                        continue  # Domain doesn't exist, skip
                                    
                                logging.info(f"🎯 Target Acquired: {target_email}")
                                intel = self._extract_company_info(title, snippet, content[:1500])
                                discovered_jobs.append(self._create_job_entry(
                                    intel.get("company", "Unknown"),
                                    intel.get("job_title", title),
                                    target_email,
                                    url,
                                    snippet,
                                    "omni"
                                ))
                                _increment_deep_dive()
                            else:
                                # Fallback for blocked sites — skip guessing, no DNS check possible
                                continue
                        except Exception as e:
                            logging.debug(f"Scan failed: {e}")
                            continue
                            
        except Exception as e:
            logging.error(f"Omni-Crawler error: {e}")
        final_leads = expansion_leads + discovered_jobs
        
        # Persist leads to the cloud DB so they appear in the HUD queue immediately
        try:
            from core.db_manager import db_manager
            # [💎 DEDUPLICATION]: Avoid spamming the DB with duplicate URLs in the same cycle
            seen_urls = set()
            for l in final_leads:
                job_url = l.get("url") or l.get("link")
                if not job_url or job_url in seen_urls:
                    continue
                seen_urls.add(job_url)
                
                # ✅ FIX: STOP using "Target Node". If unknown, try to extract from domain.
                company = l.get("company_name")
                if not company or company.lower() in ("unknown", "none", "target node", ""):
                    # Extract from domain (e.g. https://google.com/jobs -> Google)
                    try:
                        domain = urlparse(job_url).netloc.replace("www.", "").split(".")[0]
                        if len(domain) > 2:
                            l["company_name"] = domain.capitalize()
                            logging.info(f"🧬 RECOVERY: Deduced company '{l['company_name']}' from URL.")
                        else:
                            continue # Still too garbage, skip
                    except Exception:
                        continue # Skip unextractable leads
                        
                await db_manager.save_potential_lead(l, score=90)
        except Exception as e:
            logging.debug(f"Failed to persist omni-crawler leads: {e}")
            
        logging.info(f"🏁 Omni-Crawler MAX Complete: {len(final_leads)} total targets discovered")
        return final_leads

    async def hunt_registered_platforms(self) -> list:
        """
        [👑 UNIVERSAL HUNTER] Iterates through the registry and extracts jobs from ALL discovered platforms.
        """
        # Built-in platforms always available (no DB needed)
        BUILTIN_PLATFORMS = [
            {"name": "LinkedIn", "url": "https://www.linkedin.com/jobs"},
            {"name": "Bayt", "url": "https://www.bayt.com"},
            {"name": "GulfTalent", "url": "https://www.gulftalent.com"},
            {"name": "Naukrigulf", "url": "https://www.naukrigulf.com"},
            {"name": "Indeed Middle East", "url": "https://ae.indeed.com"},
            {"name": "Dubizzle Jobs", "url": "https://dubai.dubizzle.com"},
            {"name": "Daleel Madani", "url": "https://www.daleel-madani.org"},
        ]
        
        # Also get any DB-registered platforms
        db_platforms = await db_manager.client.get_active_platforms()
        platforms = BUILTIN_PLATFORMS + (db_platforms or [])
        
        all_leads = []
        if not platforms:
            logging.info("🛰️ No custom platforms registered yet. Sticking to deep-web hunting.")
            return []
            
        logging.info(f"🌐 SOVEREIGN HUNT: Preparing to strike {len(platforms)} custom platforms...")

        all_leads = []
        # Process platforms sequentially (not parallel) to avoid task explosion
        for platform in platforms:
            domain = urlparse(platform['url']).netloc
            logging.info(f"🎯 Striking Platform: {platform['name']} ({domain})")

            # Only 1 query per platform to reduce load
            q = f'site:{domain} "Network Engineer" OR "IT Manager" Lebanon OR Dubai hiring'
            try:
                results = await asyncio.wait_for(
                    asyncio.to_thread(_safe_ddgs_search, q, 5),
                    timeout=15
                )
                for r in results:
                    company_name = "Unknown"
                    try:
                        company_name = domain.split(".")[0].capitalize()
                    except:
                        pass
                    all_leads.append({
                        "company_name": company_name,
                        "job_title": r.get('title', 'Network Engineer'),
                        "url": r.get('href', ''),
                        "email": None,
                        "source": platform['name']
                    })
            except (asyncio.TimeoutError, Exception):
                pass
            await asyncio.sleep(2)

        return all_leads

    async def recon_surge(self, company_name: str) -> list:
        """
        COSMIC SELF-HEALING: Targeted deep-search for alternative decision makers.
        """
        logging.info(f"🧬 OmniCrawler: Launching Recon Surge for {company_name}...")
        targets = [
            f'"{company_name}" CEO email',
            f'"{company_name}" Operations Manager contact',
            f'"{company_name}" HR Director email recruiters',
            f'site:linkedin.com/in "{company_name}" Founder'
        ]
        
        found_emails = []
        
        for query in targets:
            try:
                results = await asyncio.to_thread(_safe_ddgs_search, query, 5, proxy=os.getenv("PROXY_URL"))
                for res in results:
                    email = self._extract_snippet_emails(res['title'], res['body'])
                    if email: found_emails.append(email)
            except Exception:
                continue
            
            if found_emails: break
            
        # Fallback to PatternRecon if search fails
        if not found_emails:
            try:
                results = await asyncio.to_thread(_safe_ddgs_search, f'"{company_name}" official website', 1, proxy=os.getenv("PROXY_URL"))
                if results:
                    domain_url = results[0].get('link') or results[0].get('href')
                    found_emails = PatternRecon.guess_hr_emails(domain_url)
            except Exception:
                pass
                
        return list(set(found_emails))

    async def resolve_manager_name(self, company: str, job_title: str) -> str:
        """
        🕵️ IDENTITY HARVESTER: Finds specific hiring names via public recon.
        """
        query = f"VP Operations or HR Director {company} name"
        try:
            results = await asyncio.to_thread(_safe_ddgs_search, query, 3)
            if results:
                text = " ".join([r['body'] for r in results])
                match = re.search(r"([A-Z][a-z]+ [A-Z][a-z]+)", text)
                if match:
                    found_name = match.group(1)
                    logging.info(f"🕵️ IDENTITY FOUND: {found_name} at {company}")
                    return found_name
        except Exception:
            pass
        return None

    async def scrape_via_mirror(self, url: str) -> str:
        """
        👻 THE GHOST MIRROR: Scrapes via Archive.org or Google Cache if blocked.
        """
        logging.info(f"👻 MIRROR-SCRAPE: Attempting archive rescue for {url}...")
        try:
            archive_url = f"https://web.archive.org/web/{url}"
            session = await self.ai_agent._get_session()
            response = await session.get(archive_url, timeout=10)
            if response.status_code == 200:
                from core.scrapers.scraper import _parse_html_for_pdf
                return _parse_html_for_pdf(response.text)
        except Exception:
            pass
        return None
