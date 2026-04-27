"""
AI Agent Module - Intelligent Job Analysis
Uses Gemini and Groq for AI-powered job matching and cover letter generation.
"""
import logging
import config
import re
import database

# Lazy import to avoid circular dependency
def _get_uplink():
    try:
        import uplink
        return uplink
    except ImportError:
        return None

# ==========================================
# 🧠 AI RECONNAISSANCE (Gemini)
# ==========================================
class GeminiAgent:
    def __init__(self, api_key=None):
        # Zero-investment mode should not import or initialize paid AI paths.
        if getattr(config, 'ZERO_INVESTMENT_MODE', False) or not getattr(config, 'USE_AI_ANALYSIS', False):
            self.gemini_pool = []
            self.groq_pool = []
            self.current_gemini_idx = 0
            self.current_groq_idx = 0
            self.enabled = False
            self.groq_enabled = False
            return

        # 💎 LOAD POOLS FROM VAULT
        self.gemini_pool = self._load_pool("GEMINI_KEY_POOL", api_key or config.GEMINI_API_KEY)
        self.groq_pool = self._load_pool("GROQ_KEY_POOL", config.GROQ_API_KEY)
        
        self.current_gemini_idx = 0
        self.current_groq_idx = 0
        
        self._init_gemini()
        self.groq_enabled = len(self.groq_pool) > 0
        
    def _load_pool(self, secret_name, default_key):
        """Retrieves and parses a CSV pool of keys from Supabase."""
        raw = database.get_secret(secret_name)
        # Fallback for single legacy secret names
        if not raw:
            fallback_name = "GROQ_API_KEY" if "GROQ" in secret_name else "GEMINI_API_KEY"
            raw = database.get_secret(fallback_name)
            
        if not raw and default_key:
            return [default_key]
        if raw:
            return [k.strip() for k in raw.split(",") if k.strip()]
        return []

    def _init_gemini(self):
        """Initializes Gemini with the current key from the pool."""
        self.enabled = False
        if self.current_gemini_idx < len(self.gemini_pool):
            try:
                import google.generativeai as genai
                key = self.gemini_pool[self.current_gemini_idx]
                genai.configure(api_key=key)
                self.model = genai.GenerativeModel('gemini-2.0-flash')
                self.enabled = True
                logging.info(f"🧠 Gemini Key #{self.current_gemini_idx+1} linked (Pool: {len(self.gemini_pool)}).")
            except Exception as e:
                logging.error(f"🧠 Gemini Init Failed for Key #{self.current_gemini_idx+1}: {e}")
                self.rotate_gemini()

    def rotate_gemini(self):
        """Moves to the next key in the Gemini pool."""
        self.current_gemini_idx += 1
        if self.current_gemini_idx < len(self.gemini_pool):
            logging.warning(f"🔄 Rotating to Gemini Key #{self.current_gemini_idx+1}...")
            self._init_gemini()
        else:
            logging.error("💀 Gemini Pool Exhausted.")
            self.enabled = False

    def notify_failure(self, error):
        """Sends a one-time Telegram alert when the ENTIRE AI System dies."""
        if getattr(self, '_notified', False): return
        if not database.check_system_flag("ai_error", "notified"):
            uplink = _get_uplink()
            if not self.enabled and not self.groq_enabled:
                if uplink:
                    uplink.send_message(f"🆘 <b>ALL AI POOLS EXHAUSTED</b>\n🛡️ Status: [ACTIVATING PROCEDURAL FALLBACK]")
                database.set_system_flag("ai_error", "notified")
        self._notified = True

    def call_groq(self, prompt, model="llama3-70b-8192"):
        """Iterates through Groq pool to fulfill the mission."""
        import requests
        import json
        
        while self.current_groq_idx < len(self.groq_pool):
            key = self.groq_pool[self.current_groq_idx]
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"} if "JSON" in prompt else None,
                "temperature": 0.5
            }
            
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=20)
                if response.status_code == 200:
                    return response.json()['choices'][0]['message']['content']
                elif response.status_code == 429:
                    logging.warning(f"🔄 Groq Key #{self.current_groq_idx+1} Quota hit. Rotating...")
                    self.current_groq_idx += 1
                else:
                    logging.error(f"🧠 Groq Error ({response.status_code}): {response.text}")
                    self.current_groq_idx += 1
            except Exception as e:
                logging.error(f"🧠 Groq Connection Error: {e}")
                self.current_groq_idx += 1
        
        self.groq_enabled = False
        return None

    def get_procedural_fallback(self, reason):
        """Emergency keyword-based engine when all AI brains are offline."""
        fallback_html = """
        <div style="background-color: #2b2b36; padding: 30px; border-radius: 8px; color: #e0e0e0; font-family: Arial, sans-serif;">
            <p>I am a dedicated HR & Operations Professional writing to express my strong interest in joining your team. I thrive on bringing structure, efficiency, and excellence to fast-paced environments.</p>
            <ul style="color: #e0e0e0; padding-left: 20px;">
                <li style="margin-bottom: 10px;"><b>Operational Excellence:</b> Proven track record in streamlining processes, managing resources, and ensuring seamless day-to-day operations.</li>
                <li style="margin-bottom: 10px;"><b>Human Resources & Coordination:</b> Extensive experience handling full-cycle recruitment, employee relations, and policy deployment.</li>
            </ul>
            <p style="border-left: 4px solid #ff00ff; padding-left: 15px; font-style: italic; color: #aaaaaa; margin-top: 20px;">
                "True efficiency is not just about doing things right, but about building systems that make it impossible to do them wrong."
            </p>
        </div>
        """
        return True, reason, fallback_html, "0"

    def analyze_job(self, title, description="", is_warmup=False):
        if not self.enabled and not self.groq_enabled:
            return self.get_procedural_fallback("AI Pools Empty.")
        
        prompt = f"""
        Analyze this job opportunity and write a high-impact HTML cover letter.
        TARGET ROLE: {title}
        JOB DESCRIPTION: {description[:3000]}
        
        Output ONLY a JSON string:
        {{
            "decision": "apply" or "skip",
            "reason": "Brief reason for decision",
            "estimated_salary": "The estimated annual salary as a number",
            "cover_letter_html": "The HTML content here (professional, tailored, matching job language)"
        }}
        """
        
        # 1. Primary Pool (Gemini)
        if self.enabled:
            try:
                response = self.model.generate_content(prompt)
                return self._parse_ai_output(response.text)
            except Exception as e:
                err_str = str(e).lower()
                if ("429" in err_str or "exhausted" in err_str) and not is_warmup:
                    logging.warning("🧠 Gemini Quota Hit. Attempting failover rotation...")
                    self.rotate_gemini()
                    return self.analyze_job(title, description, is_warmup=True)
                else:
                    logging.error(f"🧠 Gemini Engine Failure: {e}")
                    self.enabled = False 

        # 2. Secondary Pool (Groq)
        if self.groq_enabled:
            logging.info("🧠 Failover: Engaging Groq Pool.")
            response_text = self.call_groq(prompt)
            if response_text:
                return self._parse_ai_output(response_text)

        # 3. Procedural Fallback
        self.notify_failure("All AI exhausted.")
        return self.get_procedural_fallback("All AI engines REACHED LIMIT.")

    def _parse_ai_output(self, raw_text):
        """Standardized parsing for both Gemini and Groq outputs."""
        import json
        try:
            # Robust extraction using Regex
            match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            json_str = match.group(0) if match else raw_text
            data = json.loads(json_str)
            
            decision = data.get("decision", "skip") == "apply"
            return decision, data.get("reason", ""), data.get("cover_letter_html", ""), str(data.get("estimated_salary", "0"))
        except Exception as e:
            logging.error(f"🧠 AI Parse Error: {e}")
            return self.get_procedural_fallback(f"AI Output Mismatch: {str(e)}")

    def generate_interview_prep(self, company_name):
        if not self.enabled and not self.groq_enabled:
            return "❌ <b>AI Systems Offline.</b> Please update Vault."
            
        prompt = f"Provide a strategic interview preparation dossier for: {company_name}."
        
        # 1. Primary Attempt (Gemini)
        if self.enabled:
            try:
                response = self.model.generate_content(prompt)
                return response.text.replace('```html', '').replace('```', '').strip()
            except Exception as exc:
                logging.debug(f"Interview prep Gemini attempt failed: {exc}")

        # 2. Secondary Attempt (Groq)
        if self.groq_enabled:
            res = self.call_groq(prompt)
            if res: return res
            
        logging.warning("AI interview prep fell back after all model attempts failed.")
        return "❌ <b>Intelligence Gathering Failed.</b> All AI pools exhausted."
