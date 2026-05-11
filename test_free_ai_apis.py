"""
Test all free AI APIs and show which ones work.
Run this after adding API keys to .env
"""
import os, requests, json
from dotenv import load_dotenv
load_dotenv()

TEST_PROMPT = '{"is_relevant": true, "lead_score": 85, "reason": "test"}'
QUESTION = f'Return this exact JSON: {TEST_PROMPT}'

print("="*60)
print("🧠 FREE AI APIs TEST")
print("="*60)

# ── 1. Groq ───────────────────────────────────────────────────
print("\n1. GROQ (14,400 req/day FREE):")
key = os.getenv("GROQ_API_KEY","")
if key:
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": "llama-3.3-70b-versatile",
                  "messages": [{"role":"user","content":"Say OK"}], "max_tokens": 5},
            timeout=15)
        d = r.json()
        if d.get("choices"):
            print(f"  ✅ Working! Response: {d['choices'][0]['message']['content']}")
            # Show remaining quota
            usage = d.get("usage",{})
            print(f"     Tokens used: {usage.get('total_tokens',0)}")
        else:
            print(f"  ❌ Failed: {str(d)[:80]}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
else:
    print("  ⚠️ No key set")

# ── 2. DeepSeek ───────────────────────────────────────────────
print("\n2. DEEPSEEK (Free tier available):")
print("   Get key: https://platform.deepseek.com/api_keys")
key = os.getenv("DEEPSEEK_API_KEY","")
if key:
    try:
        r = requests.post("https://api.deepseek.com/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": "deepseek-chat",
                  "messages": [{"role":"user","content":"Say OK"}], "max_tokens": 5},
            timeout=15)
        d = r.json()
        if d.get("choices"):
            print(f"  ✅ Working! Response: {d['choices'][0]['message']['content']}")
        else:
            print(f"  ❌ Failed: {str(d)[:80]}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
else:
    print("  ⚠️ No key — add DEEPSEEK_API_KEY to .env")
    print("     Free: $5 credit on signup (no card needed)")

# ── 3. OpenRouter ─────────────────────────────────────────────
print("\n3. OPENROUTER (Free models, no credits needed):")
print("   Get key: https://openrouter.ai/keys")
key = os.getenv("OPENROUTER_API_KEY","")
if key:
    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                     "HTTP-Referer": "https://sam-job-automator.onrender.com"},
            json={"model": "meta-llama/llama-3.1-8b-instruct:free",
                  "messages": [{"role":"user","content":"Say OK"}], "max_tokens": 5},
            timeout=15)
        d = r.json()
        if d.get("choices"):
            print(f"  ✅ Working! Response: {d['choices'][0]['message']['content']}")
        else:
            print(f"  ❌ Failed: {str(d)[:80]}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
else:
    print("  ⚠️ No key — add OPENROUTER_API_KEY to .env")
    print("     Free: unlimited free models (llama, mistral, gemma)")

# ── 4. Together AI ────────────────────────────────────────────
print("\n4. TOGETHER AI (Free $25 credit on signup):")
print("   Get key: https://api.together.xyz/settings/api-keys")
key = os.getenv("TOGETHER_API_KEY","")
if key:
    try:
        r = requests.post("https://api.together.xyz/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": "meta-llama/Llama-3-8b-chat-hf",
                  "messages": [{"role":"user","content":"Say OK"}], "max_tokens": 5},
            timeout=15)
        d = r.json()
        if d.get("choices"):
            print(f"  ✅ Working! Response: {d['choices'][0]['message']['content']}")
        else:
            print(f"  ❌ Failed: {str(d)[:80]}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
else:
    print("  ⚠️ No key — add TOGETHER_API_KEY to .env")
    print("     Free: $25 credit on signup")

# ── 5. HuggingFace ────────────────────────────────────────────
print("\n5. HUGGING FACE (Free inference API):")
print("   Get key: https://huggingface.co/settings/tokens")
key = os.getenv("HUGGINGFACE_API_KEY","")
if key:
    try:
        r = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3",
            headers={"Authorization": f"Bearer {key}"},
            json={"inputs": "Say OK in one word", "parameters": {"max_new_tokens": 10}},
            timeout=20)
        if r.status_code == 200:
            d = r.json()
            text = d[0].get("generated_text","") if isinstance(d,list) else str(d)
            print(f"  ✅ Working! Response: {text[:50]}")
        else:
            print(f"  ❌ HTTP {r.status_code}: {r.text[:80]}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
else:
    print("  ⚠️ No key — add HUGGINGFACE_API_KEY to .env")
    print("     Free: unlimited (rate limited)")

print("\n" + "="*60)
print("📋 HOW TO ADD FREE KEYS:")
print("="*60)
print("""
1. OpenRouter (BEST - truly free models):
   → https://openrouter.ai/keys
   → Sign up free, get key
   → Add to .env: OPENROUTER_API_KEY=sk-or-...

2. DeepSeek (BEST quality, cheap):
   → https://platform.deepseek.com/api_keys
   → Sign up, get $5 free credit
   → Add to .env: DEEPSEEK_API_KEY=sk-...

3. HuggingFace (truly free, no credit card):
   → https://huggingface.co/settings/tokens
   → Create token (read access)
   → Add to .env: HUGGINGFACE_API_KEY=hf_...

4. Together AI ($25 free credit):
   → https://api.together.xyz/settings/api-keys
   → Sign up, get $25 credit
   → Add to .env: TOGETHER_API_KEY=...

After adding keys, run:
  .sovereign_runtime\\python.exe sync_env_to_render.py
""")
