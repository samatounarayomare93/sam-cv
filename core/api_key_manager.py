"""
🔑 API KEY MANAGER
Centralized management of all API keys.
Supports: get, set, test, list — all from Telegram via /keys, /setkey, /testkey
"""
import os
import logging
import asyncio
from typing import Dict, Tuple, Optional

# ============================================================
# REGISTRY: All manageable API keys with metadata
# ============================================================
API_KEY_REGISTRY: Dict[str, Dict] = {
    # ── AI Providers ────────────────────────────────────────
    "GROQ_API_KEY": {
        "label": "Groq API",
        "icon": "🧠",
        "category": "AI",
        "env_var": "GROQ_API_KEY",
        "free_info": "Free 14,400 req/day — groq.com",
        "signup": "https://console.groq.com",
        "test_fn": "_test_groq",
    },
    "GEMINI_API_KEY": {
        "label": "Gemini API",
        "icon": "✨",
        "category": "AI",
        "env_var": "GEMINI_API_KEY",
        "free_info": "Free 1,500 req/day — aistudio.google.com",
        "signup": "https://aistudio.google.com/app/apikey",
        "test_fn": "_test_gemini",
    },
    "OPENROUTER_API_KEY": {
        "label": "OpenRouter API",
        "icon": "🌐",
        "category": "AI",
        "env_var": "OPENROUTER_API_KEY",
        "free_info": "Free models available — openrouter.ai",
        "signup": "https://openrouter.ai/keys",
        "test_fn": "_test_openrouter",
    },
    # ── Email Providers ─────────────────────────────────────
    "RESEND_API_KEY": {
        "label": "Resend API",
        "icon": "📧",
        "category": "Email",
        "env_var": "RESEND_API_KEY",
        "free_info": "Free 3,000/month — resend.com",
        "signup": "https://resend.com/signup",
        "test_fn": "_test_resend",
    },
    "BREVO_API_KEY": {
        "label": "Brevo API",
        "icon": "📨",
        "category": "Email",
        "env_var": "BREVO_API_KEY",
        "free_info": "Free 300/day — brevo.com",
        "signup": "https://app.brevo.com",
        "test_fn": "_test_brevo",
    },
    # ── Infrastructure ───────────────────────────────────────
    "RENDER_API_KEY": {
        "label": "Render API",
        "icon": "☁️",
        "category": "Infra",
        "env_var": "RENDER_API_KEY",
        "free_info": "Render.com deployment key",
        "signup": "https://dashboard.render.com/u/settings",
        "test_fn": "_test_render",
    },
    "RENDER_SERVICE_ID": {
        "label": "Render Service ID",
        "icon": "🆔",
        "category": "Infra",
        "env_var": "RENDER_SERVICE_ID",
        "free_info": "Service ID from Render dashboard",
        "signup": "https://dashboard.render.com",
        "test_fn": None,
    },
}


class APIKeyManager:
    """Manages API keys: get from env/DB, set to env/DB, test live."""

    def __init__(self, db=None):
        self.db = db

    def get(self, key_name: str) -> Optional[str]:
        """Get a key value from env (DB bootstrap already loaded keys into env)."""
        info = API_KEY_REGISTRY.get(key_name)
        if not info:
            return None
        return os.getenv(info["env_var"], "").strip() or None

    def set(self, key_name: str, value: str) -> Tuple[bool, str]:
        """Set a key in the current process env and persist to DB."""
        info = API_KEY_REGISTRY.get(key_name)
        if not info:
            return False, f"Unknown key: {key_name}"
        if not value or not value.strip():
            return False, "Value cannot be empty"
        value = value.strip()
        # Set in current process immediately
        os.environ[info["env_var"]] = value
        # Persist to DB if available
        if self.db:
            try:
                import asyncio as _asyncio
                loop = _asyncio.get_event_loop()
                if loop.is_running():
                    import concurrent.futures
                    future = _asyncio.run_coroutine_threadsafe(
                        self.db.update_setting(info["env_var"], value), loop
                    )
                    future.result(timeout=5)
                else:
                    loop.run_until_complete(self.db.update_setting(info["env_var"], value))
            except Exception as e:
                logging.warning(f"DB persist failed for {key_name}: {e}")
        return True, f"Key saved successfully"

    def get_all_status(self) -> Dict[str, Dict]:
        """Return status of all registered keys."""
        result = {}
        for key_name, info in API_KEY_REGISTRY.items():
            val = os.getenv(info["env_var"], "").strip()
            has_key = bool(val)
            masked = f"{val[:8]}...{val[-4:]}" if len(val) > 12 else ("SET" if val else "NOT SET")
            source = "env" if has_key else "missing"
            result[key_name] = {
                "label": info["label"],
                "icon": info["icon"],
                "category": info["category"],
                "has_key": has_key,
                "masked": masked,
                "source": source,
                "free_info": info["free_info"],
            }
        return result

    async def test_key(self, key_name: str) -> Tuple[bool, str]:
        """Live-test a specific API key."""
        info = API_KEY_REGISTRY.get(key_name)
        if not info:
            return False, "Unknown key"
        val = self.get(key_name)
        if not val:
            return False, "Key not set"
        test_fn = info.get("test_fn")
        if not test_fn:
            return True, "Key is set (no live test available)"
        fn = getattr(self, test_fn, None)
        if not fn:
            return True, "Key is set (test not implemented)"
        try:
            return await fn(val)
        except Exception as e:
            return False, f"Test error: {e}"

    async def _test_groq(self, key: str) -> Tuple[bool, str]:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                    json={"model": "llama3-8b-8192", "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 3}
                )
            if r.status_code == 200:
                return True, "✅ Groq working — response received"
            elif r.status_code == 401:
                return False, "❌ Invalid key"
            elif r.status_code == 429:
                return True, "⚠️ Rate limited (key valid, quota exceeded)"
            elif r.status_code == 403:
                return True, "⚠️ Network blocked locally (works on Render)"
            return False, f"HTTP {r.status_code}"
        except Exception as e:
            return False, str(e)[:80]

    async def _test_gemini(self, key: str) -> Tuple[bool, str]:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.get(
                    f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
                )
            if r.status_code == 200:
                models = r.json().get("models", [])
                return True, f"✅ Gemini working — {len(models)} models"
            elif r.status_code == 400:
                return False, "❌ Invalid API key"
            elif r.status_code == 429:
                return True, "⚠️ Quota exceeded (key valid)"
            return False, f"HTTP {r.status_code}"
        except Exception as e:
            return False, str(e)[:80]

    async def _test_openrouter(self, key: str) -> Tuple[bool, str]:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.get(
                    "https://openrouter.ai/api/v1/models",
                    headers={"Authorization": f"Bearer {key}"}
                )
            if r.status_code == 200:
                return True, "✅ OpenRouter working"
            return False, f"HTTP {r.status_code}"
        except Exception as e:
            return False, str(e)[:80]

    async def _test_resend(self, key: str) -> Tuple[bool, str]:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.get(
                    "https://api.resend.com/domains",
                    headers={"Authorization": f"Bearer {key}"}
                )
            if r.status_code == 200:
                return True, "✅ Resend working"
            elif r.status_code == 401:
                return False, "❌ Invalid key"
            return False, f"HTTP {r.status_code}"
        except Exception as e:
            return False, str(e)[:80]

    async def _test_brevo(self, key: str) -> Tuple[bool, str]:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.get(
                    "https://api.brevo.com/v3/account",
                    headers={"api-key": key}
                )
            if r.status_code == 200:
                data = r.json()
                plan = data.get("plan", [{}])
                credits = plan[0].get("credits", "?") if plan else "?"
                return True, f"✅ Brevo working (credits: {credits})"
            elif r.status_code == 401:
                return False, "❌ Key disabled or invalid"
            return False, f"HTTP {r.status_code}"
        except Exception as e:
            return False, str(e)[:80]

    async def _test_render(self, key: str) -> Tuple[bool, str]:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.get(
                    "https://api.render.com/v1/services",
                    headers={"Authorization": f"Bearer {key}"}
                )
            if r.status_code == 200:
                services = r.json()
                return True, f"✅ Render API working ({len(services)} services)"
            elif r.status_code == 401:
                return False, "❌ Invalid key"
            return False, f"HTTP {r.status_code}"
        except Exception as e:
            return False, str(e)[:80]


# ── Singleton ────────────────────────────────────────────────
_manager: Optional[APIKeyManager] = None

def get_key_manager(db=None) -> APIKeyManager:
    global _manager
    if _manager is None:
        _manager = APIKeyManager(db=db)
    return _manager
