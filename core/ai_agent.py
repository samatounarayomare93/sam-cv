import re
import asyncio
import logging
import os
import json
import warnings
from typing import Dict, Any, Tuple, Optional, List
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google import genai
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
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.groq_timeout = aiohttp.ClientTimeout(total=30, connect=10)
        self.cv_content = self._load_cv()
        
        # MAXIMUM POWER: Faster timeout for 429 detection
        self.gemini_timeout = 15
        
        self.primary_engine = "gemini" if self.gemini_key else None
        if self.primary_engine == "gemini":
            try:
                self.client = genai.Client(api_key=self.gemini_key, http_options={'api_version': 'v1alpha'})
                self.model_id = 'gemini-2.0-flash'
                logging.info("PRIMARY INTELLIGENCE: Gemini Online (genai-SDK).")
            except Exception as e:
                import traceback
                error_detail = traceback.format_exc()
                logging.error(f"GEMINI ACTIVATION FAILURE: {e}\n{error_detail}")
                self.primary_engine = None
        else:
            logging.info("🛰️ SOVEREIGN PROTOCOL: Apex-Static Engine Initialized.")
        
        if self.groq_key:
            logging.info("GROQ FALLBACK: Available and armed.")
    
    async def _get_session(self) -> httpx.AsyncClient:
        """[👑 FIX] Direct session for AI API calls. Groq/Gemini are globally accessible from Render.
        Free proxies were CAUSING the 400 errors by mangling the request.
        Only use proxy when running locally (e.g. Lebanon where Groq may be blocked)."""
        if self._session is None or self._session.is_closed:
            is_render = os.getenv("RENDER") is not None
            proxy = None
            
            if not is_render:
                # Only use proxy when running locally (not on Render)
                from core.runtime_helpers import ProxyMesh
                pm = ProxyMesh()
                proxy = await pm.get_next()
                max_nodes = pm.active_nodes
                attempts = 0
                while proxy is None and attempts < max_nodes:
                    proxy = await pm.get_next()
                    attempts += 1
                if proxy:
                    logging.info(f"🌐 AI-PROXY: Tunneling through {proxy.split('@')[-1] if '@' in proxy else 'secure-node'}")
            else:
                logging.info("🌐 AI-DIRECT: Render detected — using direct connection to AI APIs (no proxy)")
            
            self._session = httpx.AsyncClient(
                timeout=30,
                follow_redirects=True,
                proxy=proxy
            )
        return self._session
    
    async def _get_lock(self) -> asyncio.Lock:
        """Get async lock for thread-safe operations"""
        if self._lock is None:
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
        You are an elite Technical Recruiter evaluating a job for Sam Salameh.
        
        [SAM'S REAL BACKGROUND (GROUND TRUTH - READ CAREFULLY)]
        - Senior Network Engineer with 15+ years of progressive experience
        - Expert in: Cisco IOS, MikroTik RouterOS, Ubiquiti UniFi, Fortinet FortiGate
        - Skills: TCP/IP, VLAN, Routing & Switching, QoS, Network Security
        - Infrastructure: Fiber Optic, Structured Cabling, Wireless Networks
        - Security: Firewalls, VPN (IPSec, SSL), Access Control, Intrusion Detection
        - Tools: Wireshark, SolarWinds, PRTG, Nagios, Cacti
        - Education: B3 Information Technology - Dekwene Technical School 2016
        - Languages: English (Fluent), Arabic (Native), French (Intermediate)
        - Location: Beirut, Lebanon
        - Target: Network Engineering / IT Infrastructure / IT Management roles
        {self.cv_content}
        
        [JOB DETAILS]
        Title: {job_title}
        Description: {description[:2000]}
        
        [👑 APEX DEITY: ORACLE PULSE]
        Recent News Headline: {news_headline if news_headline else "No recent news found."}
        Market Sentiment: {oracle_pulse.get('sentiment', 'neutral') if oracle_pulse else 'neutral'}
        Strategic Context: {oracle_pulse.get('event', 'Stable') if oracle_pulse else 'Stable'}
        Recommended Narrative Pivot: {oracle_pulse.get('strategy', 'Standard') if oracle_pulse else 'Standard'}
        
        [MISSION]
        1. Evaluate relevance: Does Sam have at least 60% match for this role?
           - RELEVANT: Network Engineer, IT Infrastructure, Systems Admin, Network Security, IT Manager, NOC Engineer, Telecom Engineer, Cisco/MikroTik/Fortinet roles
           - NOT RELEVANT: HR, Recruitment, Accounting, Medical, Driving, Cooking, etc.
        2. **SALARY THRESHOLD (MANDATORY)**:
           - If the job is in LEBANON: Salary must be at least **$1,500/month**. Reject if below.
           - If the job is OUTSIDE LEBANON (Remote, Worldwide, USA, Gulf, etc.): Salary must be at least **$4,000/month**. Reject if below.
           - If salary is not explicitly mentioned: 
              - If the Job Title contains 'Senior', 'Manager', 'Director', 'Head of', 'Lead', assume salary MEETS threshold.
              - DO NOT reject high-level roles just because the salary is hidden.
        3. Assign a 'Lead Score' (0-100).
        4. Generate 'Competitive Advantage' summary (2-3 sentences) focused on Sam's NETWORK ENGINEERING skills.
        5. Generate a persuasive 3-paragraph cover letter body mentioning:
           - Specific technologies Sam knows (Cisco, MikroTik, Fortinet, etc.)
           - Specific achievements (20+ enterprise clients, VPN implementations, etc.)
           - Why Sam is perfect for THIS specific role
           - SALUTATION: Use 'Dear {person_name if person_name else "Hiring Team"}'.
           
           - 🚨 APEX OPENING (MANDATORY): If a news headline is found, you MUST start the very first sentence of paragraph 1 by referencing it. Do not be generic. Example: "Given [Company Name]'s recent pivot toward [News Detail], I felt compelled to reach out."
           - ⚔️ THE RUSSIAN TRICK: Frame Sam's application as a "Strategic Defection" from a top global industry rival. Do not just apply; position her as bringing "Insider Excellence" and "Competitor Success Blueprints" to the target. Use words like 'Strategic pivot' and 'Competitive edge'.
           - 🏮 THE CHINESE TRICK (Sun Tzu): Adopt the principle of "winning without fighting." Frame Sam's arrival as the missing piece that completes the puzzle—total harmony and effortless efficiency. Use terms like 'seamless integration', 'holistic alignment', and 'supreme excellence'.
           - 🦅 THE USA TRICK (Hyper-Scale): Mirror the "Silicon Valley" mentality of aggressive growth and absolute market saturation. Frame Sam as a 'Multiplier' who doesn't just manage but scales operations at 10x velocity. Use power words like 'Growth-Hacking', 'Hyper-Scale', and 'Disruptive Efficiency'.
           - 🌍 THE PHOENICIAN TRICK (MENA Protocol): For targets in Lebanon or UAE, adopt the "Relationship First" approach. Focus on loyalty, operational resilience in volatile markets, and the value of a trusted, versatile partner. Use terms like 'Stewardship', 'High-Trust Partnership', and 'Unwavering Reliability'.
           - 🧬 CULTURE-CLONING: If company values are provided ({company_values}), MIRROR their specific jargon and mission-statement keywords. If they value 'Radical Candor', use that exact term. Be a cultural clone.
           - 🦈 PREDATOR STRIKE: If a competitor failure is identified ({competitor_fail}), subtly contrast Sam's success patterns with that specific failure to prove why the target needs her expertise to avoid similar pitfalls.
           - 🌌 THE ETERNAL STRATEGY: You MUST adopt the **Meta-Strategy** assigned:
             - `THE_CHALLENGER`: Be assertive, industry-disrupting, and performance-obsessed. (Startups/Visionary Tech)
             - `THE_ARCHITECT`: Be system-first, structural, and meticulously organized. (Corporate/Rigid)
             - `THE_LOYALIST`: Focus on cultural roots, long-term impact, and team service. (Family Office/Mission Driven)

           - 🔮 ORACLE PIVOT: Use the 'Recommended Narrative Pivot' ({oracle_pulse.get('strategy', 'Standard') if oracle_pulse else 'Standard'}) to frame Sam's core value:
             - If 'Efficiency & Stability': Focus on her ability to audit, cut costs, and restore process integrity during restructuring.
             - If 'Scaling & Automation': Focus on her ability to build high-velocity systems and manage hyper-growth.

           - 🎯 BOARDROOM SNIPER: If executive names are provided ({executive_names}), mention one as an "Inspiration" or reference their recent public stance.
           - 🗣️ INSIDER LINGO: If internal lingo is provided ({internal_lingo}), seamlessly weave 1-2 of these industry/company terms into the narrative.
        5. Extract 20+ high-impact 'ATS Keywords' from the job description.
        
        [HUMAN SIGNATURE - GOD-TIER BYPASS]
        - To bypass AI detectors, inject subtle 'Human Markers':
          - Vary sentence length significantly (the 'staccato' effect).
          - Use occasional colloquial but professional transitions (e.g., "Truth be told," or "On a more personal note,").
          - Avoid overly repetitive 'GPT' structures (e.g., 'Moreover', 'Furthermore').
          - Insert a specific detail from the job description to prove high-level recon.
          - Add a subtle, intentional typo (e.g., 'ops' instead of 'operations') in a non-critical area to mimic human drafting.
        
        6. Detect 'culture_persona': 'Corporate' (Formal), 'Startup' (Bold), or 'Modern' (Balanced).
        
        [🕵️ SINGULARITY: ARCHETYPE DYNAMICS]
        7. Classify the company into one of 5 **Archetypes**: 
           - 'CHAOTIC_STARTUP': Use high-velocity, disruptive language.
           - 'RIGID_CORPORATE': Use meticulous, metric-heavy, indirect Phrasing.
           - 'VISIONARY_TECH': Focus on future-proofing and scaling.
           - 'FAMILY_OFFICE': Focus on loyalty, tradition, and safe-hands.
           - 'MISSION_DRIVEN': Focus on empathy, impact, and collective good.
        8. **Vocab-Sync**: Mirror the vocabulary density and informality level found in the Job Details. If they use 'we', use 'we'. If they use 'The Candidate', use formal 3rd person.

        9. The target tone variant for this strike is: **{target_variant}**.
        10. The assigned **Meta-Strategy** is: **{meta_strategy}**.
           - 'AGGRESSIVE': High confidence, risk-taking ("I will drive a 40% efficiency gain").
           - 'EMPATHETIC': Rapport-driven, safe ("I admire the team culture you've built").
           - 'ANALYTICAL': Cold hard facts, data-heavy ("Managed $5M budget, achieved 99% SLA").
        Draft the cover_letter_body STRICTLY matching the **Archetype**, the **target_variant**, and the **Meta-Strategy**.
        
        [🌏 MULTIVERSE: DIALECT SYNC]
        Enforce the following English dialect based on the target region ({location}):
        - If Dubai/Gulf/UK/Europe: Use **British English** (e.g., 'organisation', 'authorised', 'programme', 'summarise').
        - If USA/General: Use **American English** (e.g., 'organization', 'authorized', 'program', 'summarize').
        - Current Target Dialect: **{target_dialect}**.
        
        Reply in strict JSON mapping:
        {{
            "is_relevant": true,
            "salary_valuation": "Estimated/Actual salary amount",
            "salary_match": "PASS/FAIL",
            "reason": "Brief strategic reason (mention salary if it failed)",
            "lead_score": 85,
            "semantic_fit_analysis": {{
                "technical_skills": 90,
                "experience_level": 85,
                "cultural_alignment": 80,
                "bilingual_advantage": "High (Arabic context detected)"
            }},
            "culture_persona": "Startup",
            "personality_archetype": "CHAOTIC_STARTUP",
            "psychological_variant": "{target_variant}",
            "competitive_advantage": "...",
            "extracted_salary": "0",
            "keywords": ["Skill1", "Skill2", ...],
            "highlights": [
                {{"title": "01. NAME", "desc": "Context-specific high-level achievement or skill."}},
                {{"title": "02. NAME", "desc": "Context-specific high-level achievement or skill."}},
                {{"title": "03. NAME", "desc": "Context-specific high-level achievement or skill."}}
            ],
            "cover_letter_body": "HTML formatted body text..."
        }}
        """
        
        try:
            # 1. Primary Engine Attempt (Gemini)
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
                        if self.groq_key and score > 85:
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
            if self.groq_key:
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
            headers = {"Authorization": f"Bearer {self.groq_key}", "Content-Type": "application/json"}
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
            if self.groq_key:
                headers = {"Authorization": f"Bearer {self.groq_key}", "Content-Type": "application/json"}
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

    def _apex_static_fallback(self, job_title: str, news_headline: str = None, executive_names: str = None, location: str = "Global") -> Tuple[bool, str, str, str, int, str, list, str, str, str]:
        """[👑 APEX DEITY] Elite Procedural Engine (Non-AI Human-Equivalent)."""
        is_uk = any(x in location.lower() for x in ["dubai", "london", "uk", "emirates", "qatar", "riyadh"])
        org = "organisation" if is_uk else "organization"
        prog = "programme" if is_uk else "program"
        specialise = "specialise" if is_uk else "specialize"
        
        # ELITE TEMPLATE REPOSITORY
        templates = [
            # T1: The Strategic Defector (Aggressive/Analytical)
            f"""<p>Dear Hiring Team,</p>
            <p>I am reaching out regarding the {job_title} role at your {org}. My decision to move is a <b>Strategic Defection</b> from top-tier industry rivals; I am looking to bring my success blueprints to an elite team with your specific market trajectory.</p>
            <p>With 15+ years in Operations & HR Management, I {specialise} in creating high-velocity, metric-driven environments. I am not looking for a vacancy; I am looking to drive a competitive pivot for your team through a comprehensive automation {prog}.</p>
            <p>I have attached my CV which details my history of streamlining complex workflows. Are you free for a 15-minute briefing on Tuesday?</p>""",
            
            # T2: The Growth Multiplier (Scaling/Visionary)
            f"""<p>To the {job_title} Hiring Manager,</p>
            <p>I have been tracking your firm's growth for some time. It is clear that scaling at your current velocity requires more than administration—it requires an <b>Operational Multiplier</b>.</p>
            <p>I specialize in building the "Engine Room" that allows leadership to focus on vision while I handle the structural integrity of the {org}. I bring a 10x mentality to talent acquisition and process automation.</p>
            <p>My background in managing teams of 50+ and budgets exceeding $5M makes me the ideal partner for your next phase of expansion.</p>""",
            
            # T3: The Direct Human (Grit/Bold)
            f"""<p>Dear Hiring Team,</p>
            <p>Truth be told, I don't believe in long-winded applications. You need someone who can step into the {job_title} role and deliver process excellence from Day 1. That is exactly what I do.</p>
            <p>I have spent my career purging operational inefficiency and building high-trust HR {prog}s. I am looking for a challenge that rewards bold decision-making and structural precision.</p>
            <p>If you are looking for 'safe' and 'generic', I am not your candidate. If you are looking for 'Elite' and 'Effective', let's talk.</p>"""
        ]
        
        body = random.choice(templates)
        # Inject personalized news if exists
        if news_headline:
            body = body.replace("<p>Dear Hiring Team,</p>", f"<p>Dear Hiring Team,</p><p>Given your recent news regarding <b>{news_headline}</b>, I felt compelled to reach out.</p>")

        highlights = [
            {"title": "01. OPERATIONS LIFECYCLE", "desc": "Proven expertise in managing high-volume recruitment logistics and payroll synchronization with 100% data integrity."},
            {"title": "02. SERVICE & RETENTION", "desc": "A track record of resolving complex technical and billing inquiries while maintaining strict SLA compliance."},
            {"title": "03. WORKFLOW OPTIMIZATION", "desc": "Experience in standardizing onboarding templates and operational diagnostics to significantly reduce overhead."}
        ]

        return (
            True, "Sovereign Elite Fallback (Procedural Engine)",
            body.strip(),
            "0", 85, "Elite Operations Professional.", ["Operations", "Strategy", "HR", "Efficiency"],
            "Modern", "AGGRESSIVE", "VISIONARY_TECH",
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
        if not self.groq_key:
            logging.error("SENTINEL FAILURE: Groq API Key required for structural analysis.")
            return {}

        headers = {"Authorization": f"Bearer {self.groq_key}", "Content-Type": "application/json"}
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt[:10000]}],  # Truncate for Groq context window
            "response_format": {"type": "json_object"},
            "temperature": 0.0 # High precision
        }
        
        try:
            session = await self._get_session()
            response = await session.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                return json.loads(content)
            logging.error(f"Structural Query Failed ({response.status_code}): {response.text}")
        except Exception as e:
            logging.error(f"Structural Query connection error: {e}")
        
        return {}

    async def _fallback_groq(self, prompt: str, job_title: str, news_headline: str = None, company_values: str = None, competitor_fail: str = None, internal_lingo: str = None, executive_names: str = None, peer_inspiration: str = None) -> Tuple[bool, str, str, str, int, str, list, str, str, str, list]:
        """Exponential backoff Groq with full JSON support and session reuse"""
        headers = {
            "Authorization": f"Bearer {self.groq_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.3-70b-versatile", # Using 70b specifically for fallback for higher intelligence
            "messages": [{"role": "user", "content": prompt[:12000]}],  # [👑 FIX: Truncate to avoid 400 context overflow]
            "response_format": {"type": "json_object"},
            "temperature": 0.3
        }
        
        max_retries = 2
        base_delay = 1
        
        for attempt in range(max_retries):
            try:
                session = await self._get_session()
                response = await session.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=data
                )
                if response.status_code == 200:
                    res_json = response.json()
                    content = res_json['choices'][0]['message']['content']
                    parsed = json.loads(content)
                    return (
                        parsed.get("is_relevant", False),
                        parsed.get("reason", "Groq fallback decision"),
                        parsed.get("cover_letter_body", ""),
                        parsed.get("extracted_salary", "0"),
                        parsed.get("lead_score", 0),
                        parsed.get("competitive_advantage", "Proven Operations expert."),
                        parsed.get("keywords", []),
                        parsed.get("culture_persona", "Modern"),
                        parsed.get("psychological_variant", "EMPATHETIC"),
                        parsed.get("personality_archetype", "VISIONARY_TECH"),
                        parsed.get("highlights", [])  # 11th value — required by analyze_job caller
                    )
                elif response.status_code == 429:
                    delay = base_delay * (2 ** attempt)
                    logging.warning(f"⏳ GROQ RATE LIMITED - Retrying in {delay}s...")
                    await asyncio.sleep(delay)
                else:
                    error_body = response.text[:300] if hasattr(response, 'text') else 'No body'
                    logging.error(f"❌ GROQ HTTP {response.status_code}: {error_body}")
                    break
            except asyncio.TimeoutError:
                logging.warning(f"⏳ GROQ TIMEOUT - Attempt {attempt + 1}")
                await asyncio.sleep(1)
            except Exception as e:
                resp_code = locals().get('response', None)
                resp_code = resp_code.status_code if resp_code and hasattr(resp_code, 'status_code') else 'N/A'
                logging.error(f"❌ GROQ FAILURE: {resp_code} — {str(e)[:200]}")
                # Reset session on failure so next attempt uses a fresh connection
                if self._session:
                    try: await self._session.aclose()
                    except: pass
                    self._session = None
                break
        
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
        MISSION: Prepare Sam Salameh for a high-stakes interview.
        
        OUTPUT:
        1. 'Predator Positioning': How to frame her background to make them feel they NEED her.
        2. '3 Psychological Hooks': Questions she should ask to expose their pain points.
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
            elif self.groq_key:
                data = await self.ai.structural_query(prompt)
                return data.get("reply_message", "Oracle is silent.")
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
        rel, reason, body, salary = await ai.analyze_job("Senior HR Manager", "We need a leader.")
        print(f"Relevant? {rel}")
        print(f"Reason: {reason}")
        print(f"Salary: {salary}")
        await ai.close()
    
    asyncio.run(test())
