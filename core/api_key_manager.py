"""
API Key Manager — stores/retrieves API keys from Supabase system_settings.
Keys stored in DB override env vars, allowing live updates from Telegram.
"""
import os
import logging
import requests
from typing import Optional, Dict, Tuple

# ── All manageable API keys ───────────────────────────────────────────────────
API_KEY_REGISTRY: Dict[str, Dict] = {
    # AI Providers
    "GROQ_API_KEY": {
        "label": "Groq AI",
        "icon": "⚡",
        "category": "AI",
        "free_info": "14,400 req/day FREE",
        "signup": "console.groq.com/keys",
        "test_url": "https://api.groq.com/openai/v1/chat/completions",
        "quota_warning": 12000,   # warn when daily usage > this
    },
    "DEEPSEEK_API_KEY": {
        "label": "DeepSeek AI",
        "icon": "🔵",
        "category": "AI",
        "free_info": "Free tier + cheap paid",
        "signup": "platform.deepseek.com/api_keys",
        "test_url": "https://api.deepseek.com/chat/completions",
    },
    "OPENROUTER_API_KEY": {
        "label": "OpenRouter",
        "icon": "🌐",
        "category": "AI",
        "free_info": "Free models (no credits needed)",
        "signup": "openrouter.ai/keys",
        "test_url": "https://openrouter.ai/api/v1/chat/completions",
    },
    "TOGETHER_API_KEY": {
        "label": "Together AI",
        "icon": "🤝",
        "category": "AI",
        "free_info": "$25 free credit on signup",
        "signup": "api.together.xyz",
        "test_url": "https://api.together.xyz/v1/chat/completions",
    },
    "HUGGINGFACE_API_KEY": {
        "label": "HuggingFace",
        "icon": "🤗",
        "category": "AI",
        "free_info": "Free unlimited",
        "signup": "huggingface.co/settings/tokens",
        "test_url": "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3",
    },
    "GEMINI_API_KEY": {
        "label": "Google Gemini",
        "icon": "💎",
        "category": "AI",
        "free_info": "1,500 req/day FREE",
        "signup": "makersuite.google.com/app/apikey",
        "test_url": "GEMINI_SPECIAL",
    },
    # Email Providers
    "RESEND_API_KEY": {
        "label": "Resend Email",
        "icon": "📧",
        "category": "Email",
        "free_info": "100/day FREE",
        "signup": "resend.com",
        "test_url": "https://api.resend.com/domains",
    },
    "BREVO_API_KEY": {
        "label": "Brevo Email",
        "icon": "📨",
        "category": "Email",
        "free_info": "300/day FREE",
        "signup": "app.brevo.com",
        "test_url": "https://api.brevo.com/v3/account",
    },
    # Infrastructure
    "RENDER_API_KEY": {
        "label": "Render Deploy",
        "icon": "☁️",
        "category": "Infra",
        "free_info": "Free tier",
        "signup": "dashboard.render.com",
        "test_url": None,
    },
    "GITHUB_PAT": {
        "label": "GitHub Token",
        "icon": "🐙",
        "category": "Infra",
        "free_info": "Free",
        "signup": "github.com/settings/tokens",
        "test_url": "https://api.github.com/user",
    },
}

# DB key prefix to avoid collision with other settings
_DB_PREFIX = "apikey:"


class APIKeyManager:
    """Manages API keys stored in Supabase, with env var fallback."""

    def __init__(self):
        self.supa_url = os.getenv("SUPABASE_URL", "").rstrip("/")
        self.supa_key = os.getenv("SUPABASE_KEY", "")
        self._cache: Dict[str, str] = {}

    def _headers(self) -> Dict:
        return {
            "apikey": self.supa_key,
            "Authorization": f"Bearer {self.supa_key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }

    # ── Read ──────────────────────────────────────────────────────────────────
    def get(self, key_name: str) -> str:
        """Get API key: DB value overrides env var."""
        # 1. Check in-memory cache first
        if key_name in self._cache:
            return self._cache[key_name]

        # 2. Try Supabase
        try:
            db_key = f"{_DB_PREFIX}{key_name}"
            r = requests.get(
                f"{self.supa_url}/rest/v1/system_settings?key=eq.{db_key}&select=value",
                headers=self._headers(), timeout=5
            )
            if r.status_code == 200:
                data = r.json()
                if data and data[0].get("value"):
                    val = data[0]["value"]
                    self._cache[key_name] = val
                    # Also inject into os.environ so all code picks it up
                    os.environ[key_name] = val
                    return val
        except Exception:
            pass

        # 3. Fall back to env var
        return os.getenv(key_name, "")

    # ── Write ─────────────────────────────────────────────────────────────────
    def set(self, key_name: str, value: str) -> Tuple[bool, str]:
        """Save API key to Supabase and update env var immediately."""
        if key_name not in API_KEY_REGISTRY:
            return False, f"Unknown key: {key_name}"

        db_key = f"{_DB_PREFIX}{key_name}"
        try:
            # Upsert into system_settings
            r = requests.post(
                f"{self.supa_url}/rest/v1/system_settings",
                headers={**self._headers(), "Prefer": "resolution=merge-duplicates,return=representation"},
                json={"key": db_key, "value": value},
                timeout=10
            )
            if r.status_code in (200, 201):
                # Update cache and env
                self._cache[key_name] = value
                os.environ[key_name] = value
                # Clear singleton AI agent so it re-initializes with new key
                try:
                    from core.ai_agent import OmniIntelligence
                    OmniIntelligence._instance = None
                except Exception:
                    pass
                return True, f"✅ {key_name} saved and active immediately"
            else:
                return False, f"DB error: {r.status_code} — {r.text[:100]}"
        except Exception as e:
            return False, f"Error: {e}"

    # ── Delete ────────────────────────────────────────────────────────────────
    def delete(self, key_name: str) -> Tuple[bool, str]:
        """Remove key from DB (falls back to env var)."""
        db_key = f"{_DB_PREFIX}{key_name}"
        try:
            r = requests.delete(
                f"{self.supa_url}/rest/v1/system_settings?key=eq.{db_key}",
                headers=self._headers(), timeout=10
            )
            self._cache.pop(key_name, None)
            return True, f"✅ {key_name} removed from DB (env var still active if set)"
        except Exception as e:
            return False, f"Error: {e}"

    # ── Status ────────────────────────────────────────────────────────────────
    def get_all_status(self) -> Dict[str, Dict]:
        """Return status of all registered keys."""
        result = {}
        for key_name, info in API_KEY_REGISTRY.items():
            val = self.get(key_name)
            source = "none"
            if val:
                db_key = f"{_DB_PREFIX}{key_name}"
                try:
                    r = requests.get(
                        f"{self.supa_url}/rest/v1/system_settings?key=eq.{db_key}&select=value",
                        headers=self._headers(), timeout=3
                    )
                    if r.status_code == 200 and r.json():
                        source = "db"
                    else:
                        source = "env"
                except Exception:
                    source = "env"

            result[key_name] = {
                **info,
                "value": val,
                "has_key": bool(val),
                "source": source,
                "masked": f"{val[:8]}...{val[-4:]}" if val and len(val) > 12 else ("SET" if val else "NOT SET"),
            }
        return result

    # ── Quick test ────────────────────────────────────────────────────────────
    async def test_key(self, key_name: str) -> Tuple[bool, str]:
        """Quick live test of a specific API key."""
        import httpx
        val = self.get(key_name)
        if not val:
            return False, "No key set"

        info = API_KEY_REGISTRY.get(key_name, {})
        test_url = info.get("test_url")

        if not test_url:
            return True, "Key set (no test available)"

        try:
            async with httpx.AsyncClient(timeout=8) as client:
                if test_url == "GEMINI_SPECIAL":
                    r = await client.post(
                        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={val}",
                        json={"contents": [{"parts": [{"text": "Say OK"}]}]}
                    )
                    d = r.json()
                    if d.get("candidates"):
                        return True, "Working ✅"
                    err = d.get("error", {}).get("message", "")
                    if "quota" in err.lower():
                        return False, "Quota exceeded ⚠️"
                    return False, err[:60]

                elif key_name == "GROQ_API_KEY":
                    r = await client.post(test_url,
                        headers={"Authorization": f"Bearer {val}", "Content-Type": "application/json"},
                        json={"model": "llama-3.3-70b-versatile",
                              "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 3})
                    if r.status_code == 200:
                        return True, "Working ✅"
                    if r.status_code == 429:
                        return False, "Rate limited ⚠️"
                    return False, f"HTTP {r.status_code}"

                elif key_name == "DEEPSEEK_API_KEY":
                    r = await client.post(test_url,
                        headers={"Authorization": f"Bearer {val}", "Content-Type": "application/json"},
                        json={"model": "deepseek-chat",
                              "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 3})
                    return (True, "Working ✅") if r.status_code == 200 else (False, f"HTTP {r.status_code}")

                elif key_name == "OPENROUTER_API_KEY":
                    r = await client.post(test_url,
                        headers={"Authorization": f"Bearer {val}", "Content-Type": "application/json",
                                 "HTTP-Referer": "https://sam-job-automator.onrender.com"},
                        json={"model": "meta-llama/llama-3.1-8b-instruct:free",
                              "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 3})
                    return (True, "Working ✅") if r.status_code == 200 else (False, f"HTTP {r.status_code}")

                elif key_name == "RESEND_API_KEY":
                    r = await client.get(test_url,
                        headers={"Authorization": f"Bearer {val}"})
                    return (True, "Working ✅") if r.status_code in (200, 401) else (False, f"HTTP {r.status_code}")

                elif key_name == "BREVO_API_KEY":
                    r = await client.get(test_url, headers={"api-key": val})
                    if r.status_code == 200:
                        credits = next((p.get("credits", 0) for p in r.json().get("plan", [])
                                        if p.get("type") == "free"), 0)
                        return True, f"Working ✅ ({credits} credits left)"
                    return False, f"HTTP {r.status_code}"

                elif key_name == "GITHUB_PAT":
                    r = await client.get(test_url,
                        headers={"Authorization": f"token {val}", "Accept": "application/vnd.github.v3+json"})
                    if r.status_code == 200:
                        return True, f"Working ✅ ({r.json().get('login', '')})"
                    return False, f"HTTP {r.status_code}"

                else:
                    return True, "Key set (no test available)"

        except Exception as e:
            return False, f"Error: {str(e)[:50]}"


# ── Singleton ─────────────────────────────────────────────────────────────────
_manager: Optional[APIKeyManager] = None

def get_key_manager() -> APIKeyManager:
    global _manager
    if _manager is None:
        _manager = APIKeyManager()
    return _manager


def get_api_key(key_name: str) -> str:
    """Convenience function — use this everywhere instead of os.getenv for API keys."""
    return get_key_manager().get(key_name)
