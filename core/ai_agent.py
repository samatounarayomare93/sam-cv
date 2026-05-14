import re
import asyncio
import logging
import os
import json
import time
import warnings
from typing import Dict, Any, Tuple, Optional, List
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
try:
    from google import genai
    _HAS_GENAI = True
except (ImportError, Exception):
    genai = None
    _HAS_GENAI = False
import aiohttp
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [OMNI-AGENTS] %(levelname)s - %(message)s")

class OmniIntelligence:
    _instance = None
    _session: httpx.AsyncClient = None
    _lock: asyncio.Lock = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        
        self.gemini_key = os.getenv("GEMINI_API_KEY")

        # ── Multi-key Groq rotation: GROQ_API_KEY, GROQ_API_KEY_2, GROQ_API_KEY_3 ...
        _groq_keys = []
        for _i in range(1, 10):
            _suffix = "" if _i == 1 else f"_{_i}"
            _k = os.getenv(f"GROQ_API_KEY{_suffix}", "")
            if _k:
                _groq_keys.append(_k)
        self._groq_keys: list = _groq_keys          # all available keys
        self._groq_key_index: int = 0               # current rotation index
        self.groq_key: str = _groq_keys[0] if _groq_keys else ""  # active key
        self.groq_timeout = aiohttp.ClientTimeout(total=30, connect=10)
        self.cv_content = self._load_cv()
        
        # MAXIMUM POWER: Faster timeout for 429 detection
        self.gemini_timeout = 15
        
        self.primary_engine = "gemini" if self.gemini_key else None
        if self.primary_engine == "gemini":
            try:
                if not _HAS_GENAI or genai is None:
                    raise ImportError("google-genai not installed")
                self.client = genai.Client(api_key=self.gemini_key, http_options={'api_version': 'v1beta'})
                # Try gemini-2.0-flash first (lower quota usage), fall back to 2.5-flash
                self.model_id = 'gemini-2.0-flash'
                logging.info("PRIMARY INTELLIGENCE: Gemini 2.0 Flash Online (genai-SDK).")
            except Exception as e:
                import traceback
                error_detail = traceback.format_exc()
                logging.error(f"GEMINI ACTIVATION FAILURE: {e}\n{error_detail}")
                self.primary_engine = None

        # If Gemini unavailable, use Groq as primary
        if self.primary_engine is None and self.groq_key:
            self.primary_engine = "groq"
            logging.info("PRIMARY INTELLIGENCE: Groq llama-3.3-70b-versatile (Gemini unavailable).")
        elif self.primary_engine is None:
            logging.info("🛰️ SOVEREIGN PROTOCOL: Apex-Static Engine Initialized.")
    
    def _next_groq_key(self) -> str:
        """Round-robin rotate through all available Groq API keys."""
        if not self._groq_keys:
            return ""
        key = self._groq_keys[self._groq_key_index % len(self._groq_keys)]
        self._groq_key_index = (self._groq_key_index + 1) % len(self._groq_keys)
        self.groq_key = key  # keep self.groq_key in sync
        return key

    def _mark_groq_key_exhausted(self):
        """Mark current key as rate-limited and rotate to next one immediately."""
        if len(self._groq_keys) > 1:
            exhausted = self._groq_keys[self._groq_key_index % len(self._groq_keys)]
            logging.warning(f"⏳ [AI] Groq key #{self._groq_key_index % len(self._groq_keys) + 1} rate-limited — rotating to next key")
            self._groq_key_index = (self._groq_key_index + 1) % len(self._groq_keys)
            self.groq_key = self._groq_keys[self._groq_key_index]
        else:
            logging.warning("⏳ [AI] Groq rate limited — cooling down 60s")
            self._groq_cooldown_until = time.time() + 60

    async def _get_session(self) -> httpx.AsyncClient:
        """Always return a fresh session bound to the current event loop."""
        # Always create fresh — avoids 'Event loop is closed' after restart
        if self._session is not None:
            try:
                if not self._session.is_closed:
                    # Verify it's bound to the current loop
                    current_loop = asyncio.get_running_loop()
                    return self._session
            except Exception:
                pass
            # Session is dead — close and recreate
            try:
                await self._session.aclose()
            except Exception:
                pass
            self._session = None

        is_render = os.getenv("RENDER") is not None
        proxy = None
        if not is_render:
            try:
                from core.runtime_helpers import ProxyMesh
                pm = ProxyMesh()
                proxy = await pm.get_next()
            except Exception:
                proxy = None

        self._session = httpx.AsyncClient(
            timeout=30,
            follow_redirects=True,
            proxy=proxy
        )
        return self._session
    
    async def _get_lock(self) -> asyncio.Lock:
        """Get async lock — always bound to current event loop."""
        try:
            current_loop = asyncio.get_running_loop()
            if self._lock is not None:
                lock_loop = getattr(self._lock, '_loop', None)
                if lock_loop is None or lock_loop is current_loop:
                    return self._lock
            # Create fresh lock for current loop
            self._lock = asyncio.Lock()
        except RuntimeError:
            self._lock = asyncio.Lock()
        return self._lock
    
    async def close(self):
        """Graceful cleanup"""
        if self._session:
            try:
                await self._session.aclose()
            except Exception:
                pass
            self._session = None

    def _load_cv(self) -> str:
        """Loads the candidate's CV/Profile to provide ground truth for the AI."""
        # 1. Try profile.json first (Dynamic Mode)
        profile_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "profile.json")
        if os.path.exists(profile_path):
            try:
                import json
                with open(profile_path, 'r', encoding='utf-8') as f:
                    p = json.load(f)
                    # Convert JSON to a readable text summary for the AI
                    summary = f"Candidate Name: {p.get('candidate', {}).get('name')}\n"
                    summary += f"Title: {p.get('candidate', {}).get('title')}\n"
                    summary += f"Skills: {', '.join(p.get('skills', []))}\n"
                    summary += f"Summary: {p.get('summary')}\n"
                    summary += "Experience:\n"
                    for exp in p.get('experience', []):
                        summary += f"- {exp.get('role')} at {exp.get('company')} ({exp.get('period')})\n"
                    return summary
            except Exception as e:
                logging.error(f"Failed to load profile.json: {e}")

        # 2. Fallback to Sam's HTML CV (Legacy Mode)
        cv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Sam_Salameh_CV.html")
        if os.path.exists(cv_path):
            try:
                with open(cv_path, 'r', encoding='utf-8') as f:
                    return f.read()[:5000] # Cap to prevent context bloat
            except Exception as e:
                logging.error(f"Failed to load CV: {e}")
        
        return "Senior Network Engineer with 15+ years experience in Cisco, MikroTik, Ubiquiti, Fortinet, TCP/IP, VPN, Firewalls, and IT Infrastructure."

    def _extract_json_robustly(self, text: str) -> Dict[str, Any]:
        """Uses regex to pull JSON out of potential AI conversational padding."""
        try:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group())
            return json.loads(text)
        except Exception:
            return {}

    def encode_shadow_id(self, text: str, strike_id: str) -> str:
        """
        [🕵️ APEX DEITY: SHADOW TRACKING]
        Encodes a strike ID into the text using Zero-Width Unicode characters.
        Survives copy-paste, plain-text conversion, and AI re-summarization.
        """
        # Header: \u200D (ZWJ), Binary Payload: \u200B (0) / \u200C (1), Footer: \u200D (ZWJ)
        binary_id = ''.join(format(ord(c), '08b') for c in strike_id[:8]) # Encodes first 8 chars
        payload = binary_id.replace('0', '\u200B').replace('1', '\u200C')
        shadow_sig = f"\u200D{payload}\u200D"
        
        # Inject after the first sentence or at the very beginning
        pts = text.split('.', 1)
        if len(pts) > 1:
            return f"{pts[0]}.{shadow_sig}{pts[1]}"
        return f"{shadow_sig}{text}"

    def decode_shadow_id(self, text: str) -> str:
        """
        [🕵️ APEX DEITY: SHADOW RECOVERY]
        Extracts and decodes the hidden strike ID from a text body.
        Used to track viral spread of applications in recruiter systems.
        """
        match = re.search(r'\u200D([\u200B\u200C]+)\u200D', text)
        if not match: return ""
        
        payload = match.group(1).replace('\u200B', '0').replace('\u200C', '1')
        chars = [chr(int(payload[i:i+8], 2)) for i in range(0, len(payload), 8)]
        return "".join(chars)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10), reraise=True)
    async def analyze_job(self, job_title: str, description: str, variant_weights: Optional[Dict] = None, person_name: Optional[str] = None, location: str = "Global", news_headline: str = None, company_values: str = None, competitor_fail: str = None, internal_lingo: str = None, executive_names: str = None, peer_inspiration: str = None, oracle_pulse: Dict = None) -> Tuple:
        """
        [🌌 TRANSCENDENCE READY]
        Analyzes a job with Social Infiltration and Meta-Strategy Selection.
        [🚀 ZERO-COST OPTIMIZATION] Integrated AI caching for 60% API savings.
        """
        
        # 🚀 ZERO-COST: Check cache first
        try:
            from core.ai_cache import get_cached_analysis, save_analysis_to_cache
            
            cached = get_cached_analysis(job_title, description, person_name or "")
            if cached:
                analysis = cached.get("analysis", {})
                return (
                    analysis.get("is_relevant", False),
                    analysis.get("reason", ""),
                    analysis.get("cover_letter_body", ""),
                    analysis.get("extracted_salary", "0"),
                    analysis.get("lead_score", 0),
                    analysis.get("competitive_advantage", ""),
                    analysis.get("keywords", []),
                    analysis.get("culture_persona", "Modern"),
                    analysis.get("psychological_variant", "EMPATHETIC"),
                    analysis.get("personality_archetype", "VISIONARY_TECH"),
                    analysis.get("highlights", [])
                )
        except Exception as e:
            logging.debug(f"Cache check failed: {e}")
        
        # Determine the target variant based on evolutionary weights if provided
        target_variant = "EMPATHETIC"
        if variant_weights:
            # Simple weighted choice
            variants = list(variant_weights.keys())
            weights = list(variant_weights.values())
            import random
            target_variant = random.choices(variants, weights=weights, k=1)[0]
            logging.info(f"🧬 EVOLUTIONARY CHOICE: Selected '{target_variant}' based on performance weights.")

        # Dialect & Persona Detection logic
        target_dialect = "American English"
        target_persona = "Modern"
        
        loc_str = (location or "Global").lower()
        uk_gulf_locs = ["dubai", "uae", "abu dhabi", "qatar", "lebanon", "beirut", "gulf", "uk", "london", "emirates"]
        if any(l in loc_str for l in uk_gulf_locs):
            target_dialect = "British English"
            if any(l in loc_str for l in ["lebanon", "beirut", "dubai", "uae", "abu dhabi"]):
                target_persona = "Phoenician" # Regional Mastery (Phase: PHOENIX)

        # 🌌 TRANSCENDENCE: Pre-calculate Meta-Strategy based on job context
        meta_strategy = "THE_LOYALIST"
        desc_lower = (description or "").lower()
        if any(k in desc_lower for k in ['fast-paced', 'startup', 'disrupt', 'growth', 'vibrant']):
            meta_strategy = "THE_CHALLENGER"
        elif any(k in desc_lower for k in ['corporate', 'compliance', 'structured', 'rigid', 'process']):
            meta_strategy = "THE_ARCHITECT"

        system_prompt = f"""
        You are an elite Technical Recruiter writing a job application for Sam Salameh.
        
        [SAM'S BACKGROUND — READ EVERY WORD]
        Name: Sam Salameh | Senior Network Engineer | Beirut, Lebanon
        Phone: +961 70 841 1009 | Email: samsalameh.cv@gmail.com
        LinkedIn: https://www.linkedin.com/in/sam-salameh
        Available: Immediately — open to relocation (UAE, KSA, Qatar, Europe)
        
        EXPERIENCE (15+ years):
        - Deployed enterprise networks for 20+ clients (ISPs, banks, universities) — 99.9% uptime SLA
        - Reduced security incidents by 100% via FortiGate/Cisco ASA firewall hardening
        - Configured site-to-site IPSec VPN tunnels for 50+ branch offices
        - Installed 500+ km fiber optic cabling with OTDR testing and fusion splicing
        - Managed 8 concurrent enterprise projects simultaneously
        - Trained 15+ junior network engineers on Cisco and MikroTik platforms
        - Deployed MikroTik CHR for ISP billing serving 10,000+ subscribers
        - Achieved <1 hour MTTR on all critical network incidents over 13-year career
        
        CERTIFICATIONS (Active):
        - Cisco CCNA — Routing & Switching
        - Fortinet NSE — Network Security Expert
        - MikroTik MTCNA — Certified Network Associate
        - Ubiquiti UBWA — Wireless Administrator
        
        TECHNICAL SKILLS:
        - Routing/Switching: Cisco IOS/IOS-XE, MikroTik RouterOS, OSPF, BGP, EIGRP, STP, VLANs
        - Security: FortiGate, Cisco ASA, IPSec VPN, SSL VPN, ACLs, NAT, IDS/IPS, 802.1X
        - Wireless: Ubiquiti UniFi, AirMax, 802.11ac/ax, Point-to-Point microwave
        - Monitoring: PRTG, SolarWinds, Nagios, Zabbix, Wireshark, NetFlow, SNMP
        - Infrastructure: Fiber optic (SM/MM), structured cabling (Cat5e/6/6A), rack installation
        - Automation: Python scripting, Ansible basics, Netmiko, NAPALM
        
        LANGUAGES: Arabic (Native), English (Fluent), French (Intermediate)
        {self.cv_content}
        
        [JOB DETAILS]
        Title: {job_title}
        Company Location/Region: {location}
        Description: {description[:2500]}
        
        [INTELLIGENCE CONTEXT]
        Recent Company News: {news_headline if news_headline else "No recent news."}
        Market Sentiment: {oracle_pulse.get('sentiment', 'neutral') if oracle_pulse else 'neutral'}
        Strategic Context: {oracle_pulse.get('event', 'Stable Operations') if oracle_pulse else 'Stable Operations'}
        Hiring Manager: {person_name if person_name else "Hiring Team"}
        
        [YOUR MISSION]
        
        STEP 1 — RELEVANCE CHECK:
        Is this role relevant for Sam? RELEVANT = Network Engineer, IT Infrastructure, Systems Admin, 
        Network Security, IT Manager, NOC Engineer, Telecom Engineer, Cisco/MikroTik/Fortinet/Ubiquiti roles.
        NOT RELEVANT = HR, Accounting, Medical, Driving, Cooking, Sales (non-technical), etc.
        
        STEP 2 — SALARY CHECK:
        - Lebanon jobs: must be ≥ $1,500/month
        - Outside Lebanon (Gulf, Europe, Remote): must be ≥ $4,000/month  
        - If salary hidden: Senior/Manager/Director/Lead titles → PASS automatically
        
        STEP 3 — LEAD SCORE (0-100):
        Score based on: technical skill match, seniority match, location preference, salary.
        
        STEP 4 — WRITE THE COVER LETTER BODY (3 paragraphs, HTML format):
        
        PARAGRAPH 1 — THE HOOK (2-3 sentences):
        - If news headline exists: OPEN with it. "Given [Company Name]'s [news detail], I felt compelled to reach out..."
        - Otherwise: Open with a bold, specific statement about Sam's most relevant achievement for THIS role.
        - Mention the specific job title and company name.
        - Use dialect: {target_dialect}
        
        PARAGRAPH 2 — THE PROOF (3-4 sentences):
        - List 2-3 SPECIFIC technical achievements matching this job's requirements.
        - Use exact numbers: "20+ enterprise clients", "99.9% uptime", "50+ VPN tunnels", "500+ km fiber"
        - Mention the SPECIFIC technologies from the job description that Sam knows.
        - Reference Sam's certifications if relevant (CCNA, NSE, MTCNA, UBWA).
        - Apply the {target_variant} psychological approach:
          * AGGRESSIVE: "I will deliver X% improvement in Y weeks"
          * ANALYTICAL: "My track record shows: 99.9% uptime, <1hr MTTR, 100% security incident reduction"
          * EMPATHETIC: "I understand the challenges your team faces with [specific issue from JD]"
          * VISIONARY: "I see an opportunity to transform your network infrastructure into..."
        
        PARAGRAPH 3 — THE CLOSE (2-3 sentences):
        - Express genuine interest in THIS specific company/role.
        - If company values provided ({company_values}): mirror their exact language.
        - End with a confident call to action.
        - Sign off: "Best regards,\\nSam Salameh\\nSenior Network Engineer\\n+961 70 841 1009 | samsalameh.cv@gmail.com\\nhttps://www.linkedin.com/in/sam-salameh"
        
        HUMAN MARKERS (mandatory — bypass AI detectors):
        - Vary sentence length (mix short punchy sentences with longer ones)
        - Use one specific detail from the job description to prove you read it carefully
        - Avoid: "Moreover", "Furthermore", "In conclusion", "I am writing to"
        - Use natural transitions: "Truth be told,", "What excites me most is", "Here's what I bring:"
        
        STEP 5 — HIGHLIGHTS (3 context-specific bullets for the email):
        Each highlight should be specific to THIS job's requirements, not generic.
        
        STEP 6 — ATS KEYWORDS: Extract 15+ keywords from the job description.
        
        Reply in STRICT JSON (no markdown, no explanation outside JSON):
        {{
            "is_relevant": true,
            "salary_match": "PASS",
            "reason": "Strong match — Cisco/Fortinet expertise aligns perfectly",
            "lead_score": 88,
            "culture_persona": "Corporate",
            "personality_archetype": "VISIONARY_TECH",
            "psychological_variant": "{target_variant}",
            "competitive_advantage": "15+ years enterprise network engineering with CCNA/NSE/MTCNA certifications and proven 99.9% uptime delivery",
            "extracted_salary": "0",
            "keywords": ["Cisco", "FortiGate", "OSPF", "BGP", "VPN", "Network Security"],
            "highlights": [
                {{"title": "ENTERPRISE DELIVERY", "desc": "Deployed networks for 20+ enterprise clients achieving 99.9% uptime SLA across ISPs, banks, and universities."}},
                {{"title": "SECURITY EXPERTISE", "desc": "Reduced security incidents by 100% through FortiGate/Cisco ASA hardening and IPSec VPN for 50+ branch offices."}},
                {{"title": "CERTIFIED ENGINEER", "desc": "Active CCNA, Fortinet NSE, MikroTik MTCNA, and Ubiquiti UBWA certifications with 15+ years hands-on experience."}}
            ],
            "cover_letter_body": "<p>Dear {person_name if person_name else 'Hiring Team'},</p><p>[Paragraph 1]</p><p>[Paragraph 2]</p><p>[Paragraph 3]</p><p>Best regards,<br>Sam Salameh<br>Senior Network Engineer<br>+961 70 841 1009 | samsalameh.cv@gmail.com<br>https://www.linkedin.com/in/sam-salameh</p>"
        }}
        """
        
        try:
            # 1. Primary Engine Attempt (Gemini or Groq)
            if self.primary_engine == "groq":
                # Groq is primary (Gemini unavailable/quota exceeded)
                try:
                    return await self._fallback_groq(system_prompt, job_title, news_headline, company_values, competitor_fail, internal_lingo, executive_names, peer_inspiration)
                except Exception as e:
                    logging.warning(f"⚠️ Groq primary failed: {e}. Using static fallback.")
                    return self._apex_static_fallback(job_title, news_headline, executive_names, location=location)

            if self.primary_engine == "gemini":
                try:
                    response = await self.client.aio.models.generate_content(
                        model=self.model_id,
                        contents=system_prompt
                    )
                except Exception as gemini_err:
                    err_str = str(gemini_err)
                    # Detect permanent key suspension — no point retrying, go straight to Groq
                    if "CONSUMER_SUSPENDED" in err_str or "has been suspended" in err_str:
                        logging.warning("⚠️ Gemini key suspended. Disabling Gemini for this session and falling back to Groq.")
                        self.primary_engine = None  # Don't try again this session
                    elif "PERMISSION_DENIED" in err_str or "403" in err_str:
                        logging.warning(f"⚠️ Gemini permission error: {err_str[:120]}. Falling back to Groq.")
                        self.primary_engine = None
                    elif "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "quota" in err_str.lower():
                        logging.warning(f"⚠️ Gemini quota exhausted. Switching to Groq as primary for this session.")
                        self.primary_engine = "groq" if self.groq_key else None
                        # Fall through to Groq below
                    else:
                        logging.error(f"⚡ Gemini failure: {err_str[:120]}. Falling back to Groq.")
                    # Fall through to Groq below
                else:
                    data = self._extract_json_robustly(response.text)
                    
                    cover_letter = data.get("cover_letter_body", "")
                    score = data.get("lead_score", 0)
                    
                    if data.get("is_relevant") and cover_letter:
                        # [🕵️ PHASE SINGULARITY: REGIONAL PARITY OVERRIDE]
                        # If we have a specific regional persona (e.g. Phoenician), enforce it.
                        persona = target_persona if target_persona != "Modern" else data.get("culture_persona", "Modern")
                        
                        # Sector Reflection Loop (If Groq is available)
                        if self._groq_keys and score > 85:
                            try:
                                logging.info("🧠 REFLECTION TRIGGERED: Groq is critiquing the draft...")
                                cover_letter = await self.reflect_on_outreach(cover_letter, job_title)
                            except: pass
                    
                    # --- PHASE MULTIVERSE: THE GHOST PASS ---
                    if score >= 90:
                        try:
                            logging.info(f"🕵️ GHOST-PASS: Auditing high-value strike...")
                            cover_letter = await self.ghost_pass(cover_letter, job_title)
                        except: pass
                        
                    result = (
                        data.get("is_relevant", False),
                        data.get("reason", "Analyzed via Gemini-Flash"),
                        cover_letter,
                        data.get("extracted_salary", "0"),
                        score,
                        data.get("competitive_advantage", "Proven Operations expert."),
                        data.get("keywords", []),
                        target_persona if target_persona != "Modern" else data.get("culture_persona", "Modern"),
                        data.get("psychological_variant", target_variant),
                        data.get("personality_archetype", "VISIONARY_TECH"),
                        data.get("highlights", [])
                    )
                    
                    # 🚀 ZERO-COST: Save to cache
                    try:
                        from core.ai_cache import save_analysis_to_cache
                        save_analysis_to_cache(job_title, description, person_name or "", {
                            "is_relevant": result[0],
                            "reason": result[1],
                            "cover_letter_body": result[2],
                            "extracted_salary": result[3],
                            "lead_score": result[4],
                            "competitive_advantage": result[5],
                            "keywords": result[6],
                            "culture_persona": result[7],
                            "psychological_variant": result[8],
                            "personality_archetype": result[9],
                            "highlights": result[10]
                        })
                    except Exception as e:
                        logging.debug(f"Cache save failed: {e}")
                    
                    return result
            
            # 2. Secondary Engine Attempt (Groq)
            if self._groq_keys:
                try:
                    return await self._fallback_groq(system_prompt, job_title, news_headline, company_values, competitor_fail, internal_lingo, executive_names, peer_inspiration)
                except Exception as e:
                    logging.warning(f"🛡️ HIVE-MIND FALLBACK: Groq failed ({e}). Escalating to Apex Static Engine.")
                
        except Exception as e:
            logging.error(f"⚡ Intelligence Failure: {e}. Pivoting to Apex Static Fallback.")
        
        return self._apex_static_fallback(job_title, news_headline, executive_names, location=location)

    async def reflect_on_outreach(self, letter: str, job_title: str) -> str:
        """Chinese-style Multi-Model Reflection: Using Groq to critique and improve the draft."""
        prompt = f"""
        Role: Strict Hiring Manager.
        Task: Critique this cover letter for a {job_title} role. 
        Letter: {letter}
        
        Critique points:
        - Does it sound too robotic?
        - Are there metrics?
        - Is the 'Sovereign' tone achieved?
        
        Return ONLY the improved, high-impact HTML version of the letter.
        """
        try:
            session = await self._get_session()
            active_key = self._next_groq_key()
            headers = {"Authorization": f"Bearer {active_key}", "Content-Type": "application/json"}
            data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt[:8000]}]}
            
            response = await session.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
            if response.status_code == 200:
                res = response.json()
                return res['choices'][0]['message']['content'].strip()
        except Exception:
            pass
        return letter

    async def ghost_pass(self, letter: str, job_title: str) -> str:
        """
        ADVERSARIAL DISCRIMINATOR: The 'Bot-Hunter' pass.
        Ensures the text passes as 100% human by purging AI patterns.
        """
        prompt = f"""
        Role: A cynical, elite Recruiter who HATES AI-generated cover letters.
        Task: Analyze this letter for a {job_title} role and identify "AI markers" (e.g., over-processed rhythmic structure, generic adjectives, lack of grit).
        Letter: {letter}
        
        Instruction: 
        1. Critically audit the text. If it sounds 'perfect', it is a failure.
        2. Rewrite the letter so it sounds like it was written by a stressed, high-performing human professional who is busy but brilliant. 
        3. Inject 'Human Grit': use direct, bold statements.
        4. Vary the sentence complexity. Some short. Some long.
        5. Purge corporate 'fluff' words like 'synergy', 'leverage', or 'delve'. 
        6. Ensure it is 100% UNIDENTIFIABLE by AI detectors like GPTZero or Originality.ai.
        7. Maintain HTML formatting for paragraph breaks.
        """
        try:
            # Shift to high-intelligence model for the Ghost-Pass
            if self._groq_keys:
                active_key = self._next_groq_key()
                headers = {"Authorization": f"Bearer {active_key}", "Content-Type": "application/json"}
                data = {
                    "model": "llama-3.3-70b-versatile", 
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.5 # Add entropy
                }
                session = await self._get_session()
                response = await session.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
                if response.status_code == 200:
                    res = response.json()
                    return res['choices'][0]['message']['content'].strip()
        except Exception as e:
            logging.error(f"⚠️ Ghost-Pass Failed (API): {e}")
        
        # 🛡️ SOVEREIGN FALLBACK: Local Heuristic Scrub
        # If API is dead, we manually purge common 'AI Signatures'
        return self._heuristic_scrub(letter)

    def _heuristic_scrub(self, letter: str) -> str:
        """Purges common AI fingerprints using deterministic regex patterns."""
        signatures = [
            (r"I hope this (email|letter) finds you well", "Truth be told,"),
            (r"In summary,", "At the end of the day,"),
            (r"Furthermore,", "More importantly,"),
            (r"Moreover,", "Beyond that,"),
            (r"delve into", "address"),
            (r"a proven track record", "real-world experience"),
            (r"highly motivated", "ready"),
            (r"leverag(e|ing) synergies", "driving results"),
            (r"passionate about", "focused on"),
            (r"utilizing my expertise", "using what I know"),
            (r"In conclusion,", "Finally,"),
            (r"dynamic and fast-paced", "active"),
            (r"cutting-edge", "modern")
        ]
        
        scrubbed = letter
        for pattern, replacement in signatures:
            scrubbed = re.sub(pattern, replacement, scrubbed, flags=re.IGNORECASE)
        
        # Micro-Entropy injection: Shuffle punctuation jitter
        if random.random() > 0.8:
            scrubbed = scrubbed.replace("!", ".").replace("...", ".")

        return scrubbed

    def _select_meta_strategy(self, archetype: str) -> str:
        """🌌 TRANSCENDENCE: Selects the optimal psychological strike profile."""
        if archetype in ['CHAOTIC_STARTUP', 'VISIONARY_TECH']:
            return 'THE_CHALLENGER'
        elif archetype in ['RIGID_CORPORATE']:
            return 'THE_ARCHITECT'
        return 'THE_LOYALIST'

    def _apex_static_fallback(self, job_title: str, news_headline: str = None, executive_names: str = None, location: str = "Global") -> tuple:
        """[👑 APEX DEITY] Elite Procedural Engine - Network Engineer Specialist."""
        is_uk = any(x in location.lower() for x in ["dubai", "london", "uk", "emirates", "qatar", "riyadh", "beirut", "lebanon"])
        org = "organisation" if is_uk else "organization"
        specialise = "specialise" if is_uk else "specialize"

        # Smart variant rotation based on job title and location
        title_lower = job_title.lower()
        if any(k in title_lower for k in ['security', 'firewall', 'fortinet', 'noc', 'cyber']):
            variant = "ANALYTICAL"
        elif any(k in title_lower for k in ['manager', 'director', 'head', 'lead', 'architect']):
            variant = "VISIONARY"
        elif any(k in title_lower for k in ['engineer', 'administrator', 'specialist', 'consultant']):
            variant = random.choice(["AGGRESSIVE", "EMPATHETIC"])
        else:
            variant = random.choice(["AGGRESSIVE", "EMPATHETIC", "ANALYTICAL", "VISIONARY"])

        # ELITE NETWORK ENGINEER TEMPLATE REPOSITORY
        templates = [
            # T1: The Technical Authority (Analytical/Aggressive)
            f"""<p>Dear Hiring Team,</p>
            <p>I am writing to express my strong interest in the <b>{job_title}</b> position at your {org}. With over 15 years of hands-on experience designing, implementing, and managing enterprise-grade network infrastructure, I bring a proven track record of delivering zero-downtime environments across complex multi-site deployments.</p>
            <p>My expertise spans <b>Cisco IOS/CCNP, MikroTik RouterOS, Fortinet FortiGate, and Ubiquiti UniFi</b> platforms. I have successfully deployed BGP/OSPF routing protocols, configured IPSec/SSL VPN solutions, and managed fiber optic installations for ISPs and enterprise clients across Lebanon and the GCC region.</p>
            <p>What sets me apart is my ability to translate complex network challenges into reliable, scalable solutions — achieving 99.9% uptime across all managed environments. I am confident I can bring this same level of excellence to your team.</p>
            <p>I have attached my CV for your review. I would welcome the opportunity to discuss how my technical background aligns with your infrastructure goals.</p>""",

            # T2: The Problem Solver (Empathetic/Direct)
            f"""<p>Dear Hiring Manager,</p>
            <p>I came across the <b>{job_title}</b> opportunity and immediately recognized the alignment with my 15+ years of network engineering experience. I {specialise} in building resilient network infrastructure that keeps businesses running — no matter what.</p>
            <p>Throughout my career, I have managed enterprise networks for 20+ clients including ISPs, educational institutions, and corporate environments. My core strengths include <b>network security hardening</b> (Fortinet/Cisco ASA), <b>wireless network design</b> (Ubiquiti/Cisco), and <b>structured cabling & fiber optic</b> installations.</p>
            <p>I hold certifications in <b>Cisco CCNA, Fortinet NSE, MikroTik MTCNA, and Ubiquiti UBWA</b> — and I continuously update my skills to stay ahead of evolving network threats and technologies.</p>
            <p>I would be delighted to bring this expertise to your {org}. Please find my CV attached, and I look forward to connecting.</p>""",

            # T3: The Results Driver (Aggressive/Visionary)
            f"""<p>To the {job_title} Hiring Team,</p>
            <p>Networks are the backbone of every modern business — and I have spent 15+ years making sure that backbone never breaks. I am a Senior Network Engineer with deep expertise in <b>Cisco, MikroTik, Fortinet, and Ubiquiti</b> platforms, and a reputation for delivering infrastructure that performs under pressure.</p>
            <p>My recent work includes designing and deploying enterprise networks for 20+ clients, implementing VPN solutions that reduced security incidents by 100%, and conducting network audits that achieved 99.9% uptime SLAs. I bring both the technical depth and the strategic mindset to elevate your network operations.</p>
            <p>I am not just looking for a job — I am looking for an {org} where I can make a measurable impact on network reliability, security, and performance. Based on what I know about your operations, I believe that {org} is exactly that place.</p>
            <p>My CV is attached. Let's discuss how I can contribute to your infrastructure goals.</p>""",

            # T4: The Trusted Expert (Empathetic/Analytical) - for Lebanon/GCC
            f"""<p>Dear Hiring Team,</p>
            <p>I am a Senior Network Engineer based in Beirut, Lebanon, with 15+ years of experience delivering enterprise-grade network solutions across Lebanon and the GCC region. I am reaching out regarding the <b>{job_title}</b> position, which closely matches my technical background and career aspirations.</p>
            <p>My expertise includes full-lifecycle network management: from initial design and hardware procurement through deployment, configuration, and ongoing maintenance. I am proficient in <b>Cisco IOS (CCNA certified), MikroTik RouterOS (MTCNA certified), Fortinet FortiGate (NSE certified)</b>, and Ubiquiti UniFi systems.</p>
            <p>I have a strong track record of providing 24/7 technical support for critical infrastructure, resolving complex connectivity issues with under 1-hour MTTR, and training technical teams on best practices. I am available for relocation and hold a valid passport.</p>
            <p>I would be honored to bring my expertise to your team. Please review my attached CV and let me know if you would like to schedule a technical interview.</p>"""
        ]

        body = random.choice(templates)

        # Inject personalized news if exists
        if news_headline:
            body = body.replace("<p>Dear Hiring Team,</p>",
                f"<p>Dear Hiring Team,</p><p>I noted your recent development regarding <b>{news_headline}</b> — this reinforces my belief that your {org} is exactly where I want to contribute my network engineering expertise.</p>")
            body = body.replace("<p>Dear Hiring Manager,</p>",
                f"<p>Dear Hiring Manager,</p><p>Your recent news about <b>{news_headline}</b> caught my attention and prompted me to reach out immediately.</p>")

        # Inject executive name if available
        if executive_names:
            exec_name = executive_names if isinstance(executive_names, str) else str(executive_names)
            if exec_name and exec_name != "Hiring Manager":
                body = body.replace("Dear Hiring Team,", f"Dear {exec_name},")
                body = body.replace("Dear Hiring Manager,", f"Dear {exec_name},")

        highlights = [
            {
                "title": "01. NETWORK INFRASTRUCTURE",
                "desc": "15+ years designing and managing enterprise networks: Cisco, MikroTik, Fortinet, Ubiquiti — achieving 99.9% uptime across all deployments."
            },
            {
                "title": "02. SECURITY & VPN",
                "desc": "Expert in network security hardening, firewall configuration (FortiGate/Cisco ASA), and VPN deployment (IPSec/SSL) — reducing security incidents by 100%."
            },
            {
                "title": "03. CERTIFIED PROFESSIONAL",
                "desc": "Cisco CCNA | Fortinet NSE | MikroTik MTCNA | Ubiquiti UBWA — continuously updated certifications with hands-on enterprise experience."
            }
        ]

        return (
            True, "Sovereign Elite Fallback (Network Engineer Engine)",
            body.strip(),
            "0", 87,
            "Senior Network Engineer with 15+ years enterprise experience — Cisco, MikroTik, Fortinet certified.",
            ["Network Engineering", "Cisco", "MikroTik", "Fortinet", "VPN", "Security", "Infrastructure"],
            "Modern", variant, "VISIONARY_TECH",
            highlights
        )

    def encode_shadow_text(self, text: str) -> str:
        """
        [🕵️ PHASE SHADOW: HOMOGLYPH STEALTH]
        Replaces specific characters with visually identical Unicode homoglyphs.
        Bypasses automated LinkedIn keyword filters for outreach.
        """
        # Mapping for subtle character substitution
        homoglyphs = {
            'a': 'а', # Cyrillic
            'e': 'е', # Cyrillic
            'o': 'о', # Cyrillic
            'p': 'р', # Cyrillic
            'c': 'с', # Cyrillic
            'y': 'у'  # Cyrillic
        }
        
        encoded = ""
        # Randomly replace 30% of eligible characters to maximize stealth with zero detection
        for char in text:
            if char.lower() in homoglyphs and random.random() < 0.3:
                # Keep case
                replacement = homoglyphs[char.lower()]
                encoded += replacement.upper() if char.isupper() else replacement
            else:
                encoded += char
        return encoded

    async def structural_query(self, prompt: str) -> Dict[str, Any]:
        """
        [🕵️ PHASE OMEGA: STRUCTURAL INTELLIGENCE]
        Performs deep structural analysis of code/HTML for self-healing and regeneration.
        Uses Groq (Llama-3-70b) for maximum parsing performance.
        """
        if not self._groq_keys:
            logging.error("SENTINEL FAILURE: Groq API Key required for structural analysis.")
            return {}

        # Respect cooldown windows to avoid hammering APIs after hard failures.
        now = time.time()
        access_cooldown_until = getattr(self, '_groq_access_cooldown_until', 0)
        if now < access_cooldown_until:
            return {}

        active_key = self._next_groq_key()
        headers = {"Authorization": f"Bearer {active_key}", "Content-Type": "application/json"}
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": f"Respond in JSON format only.\n\n{prompt[:4000]}"}],
            "response_format": {"type": "json_object"},
            "temperature": 0.0
        }

        # Gentle baseline pacing so background loops don't burn quota.
        await asyncio.sleep(0.35)

        for attempt in range(3):
            try:
                session = await self._get_session()
                response = await session.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=data
                )

                if response.status_code == 200:
                    try:
                        content = response.json()['choices'][0]['message']['content']
                        return json.loads(content)
                    except Exception:
                        parsed = self._extract_json_robustly(response.text)
                        return parsed if isinstance(parsed, dict) else {}

                if response.status_code == 429:
                    # Back off for one minute when rate-limited.
                    self._groq_cooldown_until = time.time() + 60
                    logging.warning("⏳ GROQ RATE LIMITED in structural_query — cooldown 60s")
                    return {}

                if response.status_code in (401, 403):
                    # Access denial is often network/egress-policy related; reset client and retry.
                    if attempt < 2:
                        try:
                            if self._session and not self._session.is_closed:
                                await self._session.aclose()
                        except Exception:
                            pass
                        self._session = None
                        await asyncio.sleep(0.8 + (attempt * 0.7))
                        continue

                    # Avoid noisy repeated failures in hot loops.
                    self._groq_access_cooldown_until = time.time() + 120
                    logging.error(f"Structural Query Failed ({response.status_code}): {response.text[:200]}")
                    return {}

                if response.status_code in (500, 502, 503, 504) and attempt < 2:
                    await asyncio.sleep(0.7 + (attempt * 0.8))
                    continue

                logging.error(f"Structural Query Failed ({response.status_code}): {response.text[:200]}")
                return {}

            except Exception as e:
                if attempt < 2:
                    try:
                        if self._session and not self._session.is_closed:
                            await self._session.aclose()
                    except Exception:
                        pass
                    self._session = None
                    await asyncio.sleep(0.6 + (attempt * 0.8))
                    continue
                logging.error(f"Structural Query connection error: {e}")

        return {}

    async def _fallback_groq(self, prompt: str, job_title: str, news_headline: str = None, company_values: str = None, competitor_fail: str = None, internal_lingo: str = None, executive_names: str = None, peer_inspiration: str = None) -> Tuple[bool, str, str, str, int, str, list, str, str, str, list]:
        """
        Multi-provider AI fallback chain (all 100% free):
        1. Groq (llama-3.3-70b) — 14,400 req/day
        2. DeepSeek (deepseek-chat) — 500 req/day free
        3. OpenRouter (free models) — unlimited free tier
        4. Together AI (free models) — 60 req/min free
        5. Static fallback
        """
        # ── Helper: parse AI JSON response ───────────────────────────────────
        def _parse_response(content: str):
            parsed = json.loads(content)
            return (
                parsed.get("is_relevant", False),
                parsed.get("reason", "AI decision"),
                parsed.get("cover_letter_body", ""),
                parsed.get("extracted_salary", "0"),
                parsed.get("lead_score", 0),
                parsed.get("competitive_advantage", "Senior Network Engineer — Cisco CCNA, Fortinet NSE, MikroTik MTCNA certified with 15+ years enterprise experience."),
                parsed.get("keywords", []),
                parsed.get("culture_persona", "Modern"),
                parsed.get("psychological_variant", "EMPATHETIC"),
                parsed.get("personality_archetype", "VISIONARY_TECH"),
                parsed.get("highlights", [])
            )

        session = await self._get_session()

        # ── 1. GROQ (primary free AI) — rotates across all keys ─────────────
        if self._groq_keys:
            # Check if ALL Groq keys are in cooldown
            groq_cooldown_until = getattr(self, '_groq_cooldown_until', 0)
            if time.time() < groq_cooldown_until:
                logging.debug("⏳ [AI] Groq in cooldown — skipping to DeepSeek")
            else:
                # Try each key once before giving up on Groq entirely
                for _attempt_key in range(len(self._groq_keys)):
                    active_key = self._next_groq_key()
                    try:
                        response = await session.post(
                            "https://api.groq.com/openai/v1/chat/completions",
                            headers={"Authorization": f"Bearer {active_key}", "Content-Type": "application/json"},
                            json={"model": "llama-3.3-70b-versatile",
                                  "messages": [{"role": "user", "content": prompt[:12000]}],
                                  "response_format": {"type": "json_object"}, "temperature": 0.3}
                        )
                        if response.status_code == 200:
                            key_num = self._groq_keys.index(active_key) + 1
                            logging.info(f"✅ [AI] Groq responded (key #{key_num})")
                            return _parse_response(response.json()['choices'][0]['message']['content'])
                        elif response.status_code == 429:
                            self._mark_groq_key_exhausted()
                            # Try next key immediately
                            continue
                        else:
                            logging.warning(f"⚠️ [AI] Groq HTTP {response.status_code}")
                            break
                    except Exception as e:
                        logging.warning(f"⚠️ [AI] Groq error: {e}")
                        if self._session:
                            try: await self._session.aclose()
                            except: pass
                            self._session = None
                            session = await self._get_session()
                        break

        # ── 2. DEEPSEEK (free tier: 500 req/day, very smart) ─────────────────
        deepseek_key = os.getenv("DEEPSEEK_API_KEY", "")
        if deepseek_key:
            try:
                logging.info("🔄 [AI] Trying DeepSeek...")
                response = await session.post(
                    "https://api.deepseek.com/chat/completions",
                    headers={"Authorization": f"Bearer {deepseek_key}", "Content-Type": "application/json"},
                    json={"model": "deepseek-chat",
                          "messages": [{"role": "user", "content": prompt[:12000]}],
                          "response_format": {"type": "json_object"}, "temperature": 0.3}
                )
                if response.status_code == 200:
                    logging.info("✅ [AI] DeepSeek responded")
                    return _parse_response(response.json()['choices'][0]['message']['content'])
                else:
                    logging.warning(f"⚠️ [AI] DeepSeek HTTP {response.status_code}: {response.text[:100]}")
            except Exception as e:
                logging.warning(f"⚠️ [AI] DeepSeek error: {e}")

        # ── 3. OPENROUTER (free models: meta-llama, mistral, etc.) ───────────
        openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
        if openrouter_key:
            # Current free models on OpenRouter (updated May 2026)
            free_models = [
                "openrouter/free",                              # Auto-selects best free model
                "google/gemma-4-26b-a4b-it:free",              # Google Gemma 4 (fast)
                "qwen/qwen3-next-80b-a3b-instruct:free",       # Qwen3 (smart)
                "nvidia/nemotron-3-nano-30b-a3b:free",         # Nvidia (reliable)
                "liquid/lfm-2.5-1.2b-instruct:free",           # Liquid (lightweight)
            ]
            for model in free_models:
                try:
                    short_name = model.split('/')[1][:25] if '/' in model else model[:25]
                    logging.info(f"🔄 [AI] Trying OpenRouter ({short_name})...")
                    response = await session.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers={"Authorization": f"Bearer {openrouter_key}",
                                 "Content-Type": "application/json",
                                 "HTTP-Referer": "https://sam-bot-v2.onrender.com",
                                 "X-Title": "Sam Job Automator"},
                        json={"model": model,
                              "messages": [{"role": "user", "content": prompt[:8000]}],
                              "temperature": 0.3,
                              "max_tokens": 2000}
                    )
                    if response.status_code == 200:
                        resp_data = response.json()
                        content = resp_data.get('choices', [{}])[0].get('message', {}).get('content', '')
                        if not content:
                            continue
                        try:
                            return _parse_response(content)
                        except Exception:
                            match = re.search(r'\{.*\}', content, re.DOTALL)
                            if match:
                                try:
                                    return _parse_response(match.group())
                                except Exception:
                                    pass
                        logging.warning(f"⚠️ [AI] OpenRouter {short_name}: could not parse JSON")
                    elif response.status_code in (404, 429):
                        logging.warning(f"⚠️ [AI] OpenRouter {short_name}: HTTP {response.status_code}, trying next")
                        continue
                    else:
                        logging.warning(f"⚠️ [AI] OpenRouter {short_name}: HTTP {response.status_code}")
                except Exception as e:
                    logging.warning(f"⚠️ [AI] OpenRouter error: {str(e)[:60]}")
                    continue

        # ── 4. TOGETHER AI (free tier: 60 req/min) ───────────────────────────
        together_key = os.getenv("TOGETHER_API_KEY", "")
        if together_key:
            try:
                logging.info("🔄 [AI] Trying Together AI...")
                response = await session.post(
                    "https://api.together.xyz/v1/chat/completions",
                    headers={"Authorization": f"Bearer {together_key}", "Content-Type": "application/json"},
                    json={"model": "meta-llama/Llama-3-8b-chat-hf",
                          "messages": [{"role": "user", "content": prompt[:8000]}],
                          "temperature": 0.3, "max_tokens": 2000}
                )
                if response.status_code == 200:
                    content = response.json()['choices'][0]['message']['content']
                    try:
                        return _parse_response(content)
                    except Exception:
                        match = re.search(r'\{.*\}', content, re.DOTALL)
                        if match:
                            return _parse_response(match.group())
                    logging.warning("⚠️ [AI] Together AI: could not parse JSON")
                else:
                    logging.warning(f"⚠️ [AI] Together AI HTTP {response.status_code}")
            except Exception as e:
                logging.warning(f"⚠️ [AI] Together AI error: {e}")

        # ── 5. HUGGING FACE (free inference API) ─────────────────────────────
        hf_key = os.getenv("HUGGINGFACE_API_KEY", "")
        if hf_key:
            # Try multiple HF models (some may be loading/unavailable)
            hf_models = [
                "mistralai/Mistral-7B-Instruct-v0.2",
                "HuggingFaceH4/zephyr-7b-beta",
                "microsoft/DialoGPT-medium",
            ]
            for hf_model in hf_models:
                try:
                    logging.info(f"🔄 [AI] Trying HuggingFace ({hf_model.split('/')[-1][:20]})...")
                    simple_prompt = f"Analyze this job for a Senior Network Engineer and return JSON with is_relevant(bool), lead_score(0-100), cover_letter_body(string). Job: {prompt[:2000]}"
                    response = await session.post(
                        f"https://api-inference.huggingface.co/models/{hf_model}",
                        headers={"Authorization": f"Bearer {hf_key}", "Content-Type": "application/json"},
                        json={"inputs": simple_prompt, "parameters": {"max_new_tokens": 800, "temperature": 0.3, "return_full_text": False}}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        if isinstance(data, list) and data:
                            content = data[0].get("generated_text", "")
                        elif isinstance(data, dict):
                            content = data.get("generated_text", str(data))
                        else:
                            content = str(data)
                        match = re.search(r'\{.*\}', content, re.DOTALL)
                        if match:
                            try:
                                return _parse_response(match.group())
                            except Exception:
                                pass
                        logging.warning(f"⚠️ [AI] HuggingFace {hf_model}: could not parse response")
                    elif response.status_code == 503:
                        logging.warning(f"⚠️ [AI] HuggingFace {hf_model}: model loading, trying next")
                        continue
                    else:
                        logging.warning(f"⚠️ [AI] HuggingFace {hf_model}: HTTP {response.status_code}")
                except Exception as e:
                    logging.warning(f"⚠️ [AI] HuggingFace error: {str(e)[:60]}")
                    continue

        # ── 6. Static fallback (always works) ────────────────────────────────
        logging.warning("⚠️ [AI] All providers failed — using static fallback")
        return self._apex_static_fallback(job_title, news_headline)

    async def generate_decoy_persona(self, job_title: str, company: str) -> Dict[str, str]:
        """
        🇷🇺 THE MOSCOW TRICK: Generates a decoy persona to shift recruiter baseline.
        One decoy is 'Overqualified/Arrogant', one is 'Passionate/Inexperienced'.
        This makes Sam (the 'Balanced Professional') the inevitable choice.
        """
        types = [
            {"type": "OVERQUALIFIED", "trait": "demands 2x salary, extremely rigid"},
            {"type": "JUNIOR_CHAOS", "trait": "high energy but lacks any relevant experience"}
        ]
        chosen = random.choice(types)
        
        prompt = f"""
        Create a fake job applicant persona for: {job_title} at {company}.
        The persona type is: {chosen['type']} ({chosen['trait']}).
        Return JSON:
        {{
            "name": "Full Name",
            "background": "Short bio",
            "fatal_flaw": "The reason they will be rejected in favor of a balanced candidate"
        }}
        """
        
        try:
            if self.primary_engine == "gemini":
                response = await self.client.aio.models.generate_content(
                    model=self.model_id,
                    contents=prompt
                )
                return self._extract_json_robustly(response.text)
        except Exception:
            pass
            
        return {
            "name": "Alex Rivars",
            "background": "Former Director at a failed startup.",
            "fatal_flaw": "Demands remote work from a private island."
        }

    async def generate_decoy_letter(self, persona: Dict[str, str], job_title: str, company: str) -> str:
        """
        Generates a cover letter that subtly highlights the decoy's flaw.
        """
        prompt = f"""
        Write a short cover letter for {persona['name']} applying for {job_title} at {company}.
        Bio: {persona['background']}
        Fatal Flaw to subtly include: {persona['fatal_flaw']}
        Make it look realistic but slightly 'off' compared to a perfect candidate.
        """
        try:
            if self.primary_engine == "gemini":
                response = await self.client.aio.models.generate_content(
                    model=self.model_id,
                    contents=prompt
                )
                return response.text
        except Exception:
            pass
        return f"Dear Hiring Manager, I am {persona['name']} and I want this job at {company}."

    async def generate_cheat_sheet(self, company_name: str, job_title: str) -> str:
        """Generates a high-velocity tactical prep guide for a specific job."""
        prompt = f"""
        TARGET: {company_name} - {job_title}
        MISSION: Prepare Sam Salameh (Senior Network Engineer, male) for a high-stakes interview.
        
        OUTPUT:
        1. 'Predator Positioning': How to frame his background to make them feel they NEED him.
        2. '3 Psychological Hooks': Questions he should ask to expose their pain points.
        3. 'The Closer': A 1-sentence closing statement that guarantees a follow-up.
        
        Keep it elite, short, and data-driven. Use HTML <b> and <i> tags.
        """
        try:
            if self.primary_engine == "gemini":
                response = await self.client.aio.models.generate_content(
                    model=self.model_id,
                    contents=prompt
                )
                return response.text.strip()
            elif self._groq_keys:
                # Fix: use key rotation instead of direct self.groq_key
                session = await self._get_session()
                active_key = self._next_groq_key()
                headers = {"Authorization": f"Bearer {active_key}", "Content-Type": "application/json"}
                resp = await session.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json={"model": "llama-3.3-70b-versatile",
                          "messages": [{"role": "user", "content": prompt}],
                          "max_tokens": 500}
                )
                if resp.status_code == 200:
                    return resp.json()['choices'][0]['message']['content'].strip()
                return "Oracle is silent."
        except Exception as e:
            return f"Error in tactical extraction: {e}"
        return "Intelligence Retrieval Failed."


# Singleton instance
_ai_instance = None

def get_ai_agent() -> OmniIntelligence:
    global _ai_instance
    if _ai_instance is None:
        _ai_instance = OmniIntelligence()
    return _ai_instance

if __name__ == "__main__":
    async def test():
        ai = OmniIntelligence()
        # analyze_job returns 11 values: (is_relevant, reason, cover_letter, salary, score, advantage, keywords, persona, variant, archetype, highlights)
        rel, reason, body, salary, score, advantage, keywords, persona, variant, archetype, highlights = await ai.analyze_job("Senior HR Manager", "We need a leader.")
        print(f"Relevant? {rel}")
        print(f"Reason: {reason}")
        print(f"Salary: {salary}")
        print(f"Score: {score}")
        await ai.close()
    
    asyncio.run(test())
