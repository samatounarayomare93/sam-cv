"""
🤖 MULTI-AI FALLBACK CHAIN (100% FREE)
Never run out of AI capacity - automatic failover across 5+ free providers

Chain: Groq → Gemini → Hugging Face → Together AI → Perplexity
Total capacity: 20,000+ requests/day (FREE)
"""

import logging
import os
import time
from typing import Optional, Dict, Any, List
import json

# Provider configurations
PROVIDERS = [
    {
        "name": "groq",
        "display_name": "Groq",
        "daily_limit": 14400,
        "rpm_limit": 30,
        "enabled": bool(os.getenv("GROQ_API_KEY")),
        "priority": 1
    },
    {
        "name": "gemini",
        "display_name": "Google Gemini",
        "daily_limit": 86400,  # 60 req/min * 1440 min
        "rpm_limit": 60,
        "enabled": bool(os.getenv("GEMINI_API_KEY")),
        "priority": 2
    },
    {
        "name": "huggingface",
        "display_name": "Hugging Face",
        "daily_limit": 10000,  # Conservative estimate
        "rpm_limit": 10,
        "enabled": bool(os.getenv("HUGGINGFACE_API_KEY")),
        "priority": 3
    },
    {
        "name": "together",
        "display_name": "Together AI",
        "daily_limit": 86400,
        "rpm_limit": 60,
        "enabled": bool(os.getenv("TOGETHER_API_KEY")),
        "priority": 4
    },
    {
        "name": "perplexity",
        "display_name": "Perplexity",
        "daily_limit": 120,  # 5 req/hour * 24 hours
        "rpm_limit": 1,
        "enabled": bool(os.getenv("PERPLEXITY_API_KEY")),
        "priority": 5
    }
]


class MultiAIFallback:
    """Intelligent AI provider fallback with automatic retry."""
    
    def __init__(self):
        self.providers = [p for p in PROVIDERS if p["enabled"]]
        self.usage = {}
        self.last_request_time = {}
        
        if not self.providers:
            logging.error("❌ NO AI PROVIDERS CONFIGURED!")
        else:
            logging.info(f"✅ {len(self.providers)} AI providers available")
    
    def _can_use_provider(self, provider: Dict) -> bool:
        """Check if provider is available (not rate limited)."""
        provider_name = provider["name"]
        
        # Check daily limit
        today = time.strftime("%Y-%m-%d")
        usage_key = f"{provider_name}_{today}"
        current_usage = self.usage.get(usage_key, 0)
        
        if current_usage >= provider["daily_limit"]:
            logging.warning(f"⚠️ {provider['display_name']} daily limit reached")
            return False
        
        # Check rate limit (requests per minute)
        last_request = self.last_request_time.get(provider_name, 0)
        time_since_last = time.time() - last_request
        min_interval = 60.0 / provider["rpm_limit"]
        
        if time_since_last < min_interval:
            wait_time = min_interval - time_since_last
            logging.debug(f"⏳ Rate limit: waiting {wait_time:.1f}s for {provider['display_name']}")
            time.sleep(wait_time)
        
        return True
    
    def _record_usage(self, provider_name: str):
        """Record API usage for provider."""
        today = time.strftime("%Y-%m-%d")
        usage_key = f"{provider_name}_{today}"
        self.usage[usage_key] = self.usage.get(usage_key, 0) + 1
        self.last_request_time[provider_name] = time.time()
    
    def _call_groq(self, prompt: str, model: str = "llama-3.3-70b-versatile") -> Optional[str]:
        """Call Groq API."""
        try:
            from groq import Groq
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logging.error(f"Groq API error: {e}")
            return None
    
    def _call_gemini(self, prompt: str) -> Optional[str]:
        """Call Google Gemini API."""
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            # [🛡️ FIX 2026-05-07]: gemini-2.0-flash-exp deprecated → use gemini-2.5-flash
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            
            return response.text
            
        except Exception as e:
            logging.error(f"Gemini API error: {e}")
            return None
    
    def _call_huggingface(self, prompt: str) -> Optional[str]:
        """Call Hugging Face Inference API."""
        try:
            import requests
            
            api_key = os.getenv("HUGGINGFACE_API_KEY")
            if not api_key:
                return None
            
            # Use free inference API
            API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
            headers = {"Authorization": f"Bearer {api_key}"}
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 2000,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            }
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "")
            
            return None
            
        except Exception as e:
            logging.error(f"Hugging Face API error: {e}")
            return None
    
    def _call_together(self, prompt: str) -> Optional[str]:
        """Call Together AI API."""
        try:
            import requests
            
            api_key = os.getenv("TOGETHER_API_KEY")
            if not api_key:
                return None
            
            url = "https://api.together.xyz/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 2000,
                "temperature": 0.7
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            logging.error(f"Together AI error: {e}")
            return None
    
    def _call_perplexity(self, prompt: str) -> Optional[str]:
        """Call Perplexity API."""
        try:
            import requests
            
            api_key = os.getenv("PERPLEXITY_API_KEY")
            if not api_key:
                return None
            
            url = "https://api.perplexity.ai/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "llama-3.1-sonar-small-128k-online",
                "messages": [{"role": "user", "content": prompt}]
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            logging.error(f"Perplexity API error: {e}")
            return None
    
    def generate(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        """
        Generate AI response with automatic fallback.
        
        Tries each provider in priority order until success.
        
        Args:
            prompt: The prompt to send to AI
            max_retries: Maximum retry attempts per provider
        
        Returns:
            Generated text or None if all providers fail
        """
        for provider in self.providers:
            if not self._can_use_provider(provider):
                continue
            
            provider_name = provider["name"]
            logging.info(f"🤖 Trying {provider['display_name']}...")
            
            for attempt in range(max_retries):
                try:
                    # Call appropriate provider
                    if provider_name == "groq":
                        result = self._call_groq(prompt)
                    elif provider_name == "gemini":
                        result = self._call_gemini(prompt)
                    elif provider_name == "huggingface":
                        result = self._call_huggingface(prompt)
                    elif provider_name == "together":
                        result = self._call_together(prompt)
                    elif provider_name == "perplexity":
                        result = self._call_perplexity(prompt)
                    else:
                        result = None
                    
                    if result:
                        self._record_usage(provider_name)
                        logging.info(f"✅ Success with {provider['display_name']}")
                        return result
                    
                except Exception as e:
                    logging.warning(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)  # Exponential backoff
            
            logging.warning(f"❌ {provider['display_name']} failed after {max_retries} attempts")
        
        logging.error("❌ ALL AI PROVIDERS FAILED!")
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get usage statistics for all providers."""
        today = time.strftime("%Y-%m-%d")
        stats = {
            "date": today,
            "providers": {},
            "total_requests": 0
        }
        
        for provider in self.providers:
            provider_name = provider["name"]
            usage_key = f"{provider_name}_{today}"
            used = self.usage.get(usage_key, 0)
            
            stats["providers"][provider["display_name"]] = {
                "used": used,
                "limit": provider["daily_limit"],
                "remaining": provider["daily_limit"] - used,
                "enabled": provider["enabled"]
            }
            
            stats["total_requests"] += used
        
        return stats


# Global instance
_fallback = None


def get_ai_fallback() -> MultiAIFallback:
    """Get global AI fallback instance."""
    global _fallback
    if _fallback is None:
        _fallback = MultiAIFallback()
    return _fallback


def generate_with_fallback(prompt: str) -> Optional[str]:
    """Generate AI response with automatic fallback."""
    return get_ai_fallback().generate(prompt)


def get_ai_stats() -> Dict[str, Any]:
    """Get AI usage statistics."""
    return get_ai_fallback().get_stats()


# Example usage
if __name__ == "__main__":
    fallback = MultiAIFallback()
    
    print("🤖 Multi-AI Fallback System")
    print("=" * 50)
    
    # Test prompt
    test_prompt = "Write a professional email subject line for a job application to a tech company."
    
    print(f"\n📝 Test prompt: {test_prompt}")
    print("\n🔄 Attempting generation...")
    
    result = fallback.generate(test_prompt)
    
    if result:
        print(f"\n✅ Success!")
        print(f"📄 Result: {result[:200]}...")
    else:
        print("\n❌ All providers failed")
    
    # Show stats
    print("\n📊 Usage Statistics:")
    stats = fallback.get_stats()
    for provider, data in stats["providers"].items():
        print(f"  {provider}: {data['used']}/{data['limit']} requests")
