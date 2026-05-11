"""
Deep diagnostic for every API key - shows exact error and fix
"""
import os, sys, requests, json
from dotenv import load_dotenv
load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 65)
print("🔍 DEEP API DIAGNOSTIC")
print("=" * 65)

results = {}

# ── 1. GROQ ───────────────────────────────────────────────────
print("\n⚡ GROQ:")
key = os.getenv("GROQ_API_KEY", "")
if not key:
    print("  ❌ NOT SET")
    results["Groq"] = ("❌", "Not set", "Add GROQ_API_KEY to .env")
else:
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": "llama-3.3-70b-versatile",
                  "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 3},
            timeout=15
        )
        d = r.json()
        if r.status_code == 200:
            resp = d["choices"][0]["message"]["content"]
            usage = d.get("usage", {})
            print(f"  ✅ Working! Response: {resp}")
            print(f"  📊 Tokens used this call: {usage.get('total_tokens', 0)}")
            # Check rate limit headers
            remaining = r.headers.get("x-ratelimit-remaining-requests", "?")
            reset = r.headers.get("x-ratelimit-reset-requests", "?")
            print(f"  📊 Requests remaining: {remaining}")
            print(f"  ⏰ Reset in: {reset}")
            results["Groq"] = ("✅", "Working", f"Remaining: {remaining}")
        elif r.status_code == 429:
            err = d.get("error", {}).get("message", "")
            print(f"  ⚠️ RATE LIMITED: {err[:80]}")
            results["Groq"] = ("⚠️", "Rate limited", "Wait or get new key")
        elif r.status_code == 401:
            print(f"  ❌ INVALID KEY: {d.get('error', {}).get('message', '')[:80]}")
            results["Groq"] = ("❌", "Invalid key", "Get new key from console.groq.com")
        else:
            print(f"  ❌ HTTP {r.status_code}: {str(d)[:100]}")
            results["Groq"] = ("❌", f"HTTP {r.status_code}", str(d)[:60])
    except Exception as e:
        print(f"  ❌ Error: {e}")
        results["Groq"] = ("❌", str(e)[:60], "Check internet connection")

# ── 2. GEMINI ─────────────────────────────────────────────────
print("\n💎 GEMINI:")
key = os.getenv("GEMINI_API_KEY", "")
if not key:
    print("  ❌ NOT SET")
    results["Gemini"] = ("❌", "Not set", "Get free key: makersuite.google.com/app/apikey")
else:
    try:
        r = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}",
            json={"contents": [{"parts": [{"text": "Say OK"}]}]},
            timeout=15
        )
        d = r.json()
        if d.get("candidates"):
            resp = d["candidates"][0]["content"]["parts"][0]["text"]
            print(f"  ✅ Working! Response: {resp[:20]}")
            results["Gemini"] = ("✅", "Working", "")
        else:
            err = d.get("error", {}).get("message", "")
            code = d.get("error", {}).get("code", r.status_code)
            if "quota" in err.lower() or code == 429:
                print(f"  ⚠️ QUOTA EXCEEDED: {err[:80]}")
                print(f"  💡 Fix: Get new key from different Google account")
                print(f"  🔗 makersuite.google.com/app/apikey")
                results["Gemini"] = ("⚠️", "Quota exceeded", "Get new key from different Google account")
            elif "API_KEY_INVALID" in err or code == 400:
                print(f"  ❌ INVALID KEY")
                results["Gemini"] = ("❌", "Invalid key", "Get new key: makersuite.google.com/app/apikey")
            else:
                print(f"  ❌ Error {code}: {err[:80]}")
                results["Gemini"] = ("❌", err[:60], "")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        results["Gemini"] = ("❌", str(e)[:60], "")

# ── 3. DEEPSEEK ───────────────────────────────────────────────
print("\n🔵 DEEPSEEK:")
key = os.getenv("DEEPSEEK_API_KEY", "")
if not key:
    print("  ❌ NOT SET")
    print("  💡 Free: platform.deepseek.com/api_keys")
    results["DeepSeek"] = ("❌", "Not set", "platform.deepseek.com/api_keys")
else:
    try:
        r = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": "deepseek-chat",
                  "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 3},
            timeout=15
        )
        d = r.json()
        if r.status_code == 200:
            resp = d["choices"][0]["message"]["content"]
            print(f"  ✅ Working! Response: {resp[:20]}")
            results["DeepSeek"] = ("✅", "Working", "")
        elif r.status_code == 402:
            print(f"  ⚠️ INSUFFICIENT BALANCE: Need to add credits")
            results["DeepSeek"] = ("⚠️", "No balance", "Add credits at platform.deepseek.com")
        elif r.status_code == 401:
            print(f"  ❌ INVALID KEY")
            results["DeepSeek"] = ("❌", "Invalid key", "Get new key: platform.deepseek.com/api_keys")
        else:
            print(f"  ❌ HTTP {r.status_code}: {str(d)[:100]}")
            results["DeepSeek"] = ("❌", f"HTTP {r.status_code}", str(d)[:60])
    except Exception as e:
        print(f"  ❌ Error: {e}")
        results["DeepSeek"] = ("❌", str(e)[:60], "")

# ── 4. OPENROUTER ─────────────────────────────────────────────
print("\n🌐 OPENROUTER:")
key = os.getenv("OPENROUTER_API_KEY", "")
if not key:
    print("  ❌ NOT SET")
    print("  💡 Free: openrouter.ai/keys (no credit card needed)")
    results["OpenRouter"] = ("❌", "Not set", "openrouter.ai/keys - FREE no credit card")
else:
    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                     "HTTP-Referer": "https://sam-job-automator.onrender.com"},
            json={"model": "meta-llama/llama-3.1-8b-instruct:free",
                  "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 3},
            timeout=15
        )
        d = r.json()
        if r.status_code == 200:
            resp = d["choices"][0]["message"]["content"]
            print(f"  ✅ Working! Response: {resp[:20]}")
            results["OpenRouter"] = ("✅", "Working", "")
        elif r.status_code == 401:
            print(f"  ❌ INVALID KEY")
            results["OpenRouter"] = ("❌", "Invalid key", "Get new key: openrouter.ai/keys")
        else:
            print(f"  ❌ HTTP {r.status_code}: {str(d)[:100]}")
            results["OpenRouter"] = ("❌", f"HTTP {r.status_code}", str(d)[:60])
    except Exception as e:
        print(f"  ❌ Error: {e}")
        results["OpenRouter"] = ("❌", str(e)[:60], "")

# ── 5. TOGETHER AI ────────────────────────────────────────────
print("\n🤝 TOGETHER AI:")
key = os.getenv("TOGETHER_API_KEY", "")
if not key:
    print("  ❌ NOT SET")
    print("  💡 Free $25 credit: api.together.xyz")
    results["Together"] = ("❌", "Not set", "api.together.xyz - $25 free credit")
else:
    try:
        r = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": "meta-llama/Llama-3-8b-chat-hf",
                  "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 3},
            timeout=15
        )
        d = r.json()
        if r.status_code == 200:
            resp = d["choices"][0]["message"]["content"]
            print(f"  ✅ Working! Response: {resp[:20]}")
            results["Together"] = ("✅", "Working", "")
        else:
            print(f"  ❌ HTTP {r.status_code}: {str(d)[:100]}")
            results["Together"] = ("❌", f"HTTP {r.status_code}", str(d)[:60])
    except Exception as e:
        print(f"  ❌ Error: {e}")
        results["Together"] = ("❌", str(e)[:60], "")

# ── 6. HUGGINGFACE ────────────────────────────────────────────
print("\n🤗 HUGGINGFACE:")
key = os.getenv("HUGGINGFACE_API_KEY", "")
if not key:
    print("  ❌ NOT SET")
    print("  💡 Free: huggingface.co/settings/tokens")
    results["HuggingFace"] = ("❌", "Not set", "huggingface.co/settings/tokens - FREE")
else:
    try:
        r = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3",
            headers={"Authorization": f"Bearer {key}"},
            json={"inputs": "Say OK", "parameters": {"max_new_tokens": 5}},
            timeout=20
        )
        if r.status_code == 200:
            d = r.json()
            text = d[0].get("generated_text", "") if isinstance(d, list) else str(d)
            print(f"  ✅ Working! Response: {text[:30]}")
            results["HuggingFace"] = ("✅", "Working", "")
        elif r.status_code == 503:
            print(f"  ⚠️ Model loading (try again in 20s)")
            results["HuggingFace"] = ("⚠️", "Model loading", "Try again in 20 seconds")
        elif r.status_code == 401:
            print(f"  ❌ INVALID KEY")
            results["HuggingFace"] = ("❌", "Invalid key", "Get new key: huggingface.co/settings/tokens")
        else:
            print(f"  ❌ HTTP {r.status_code}: {r.text[:100]}")
            results["HuggingFace"] = ("❌", f"HTTP {r.status_code}", r.text[:60])
    except Exception as e:
        print(f"  ❌ Error: {e}")
        results["HuggingFace"] = ("❌", str(e)[:60], "")

# ── 7. RESEND ─────────────────────────────────────────────────
print("\n📧 RESEND:")
key = os.getenv("RESEND_API_KEY", "")
if not key:
    print("  ❌ NOT SET")
    results["Resend"] = ("❌", "Not set", "resend.com - 100/day FREE")
else:
    try:
        r = requests.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"from": "Sam Salameh <onboarding@resend.dev>",
                  "to": ["samsalameh.cv@gmail.com"],
                  "subject": "✅ Resend Test",
                  "html": "<p>Test</p>"},
            timeout=15
        )
        d = r.json()
        if d.get("id"):
            print(f"  ✅ Working! Email sent: {d['id'][:20]}...")
            results["Resend"] = ("✅", "Working", "")
        else:
            print(f"  ❌ Failed: {str(d)[:100]}")
            results["Resend"] = ("❌", str(d)[:60], "")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        results["Resend"] = ("❌", str(e)[:60], "")

# ── 8. BREVO ──────────────────────────────────────────────────
print("\n📨 BREVO:")
key = os.getenv("BREVO_API_KEY", "")
if not key:
    print("  ❌ NOT SET")
    results["Brevo"] = ("❌", "Not set", "app.brevo.com - 300/day FREE")
else:
    try:
        r = requests.get(
            "https://api.brevo.com/v3/account",
            headers={"api-key": key},
            timeout=10
        )
        d = r.json()
        if r.status_code == 200:
            credits = next((p.get("credits", 0) for p in d.get("plan", [])
                           if p.get("type") == "free"), 0)
            email = d.get("email", "")
            print(f"  ✅ Valid key! Account: {email}")
            print(f"  📊 Credits remaining: {credits}")
            if credits == 0:
                print(f"  ⚠️ CREDITS EXHAUSTED - emails won't send via Brevo")
                print(f"  💡 Fix: Create new Brevo account or wait for monthly reset")
                results["Brevo"] = ("⚠️", f"Credits=0 (exhausted)", "Create new account at app.brevo.com")
            else:
                results["Brevo"] = ("✅", f"Working ({credits} credits)", "")
        else:
            print(f"  ❌ HTTP {r.status_code}: {str(d)[:100]}")
            results["Brevo"] = ("❌", f"HTTP {r.status_code}", "")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        results["Brevo"] = ("❌", str(e)[:60], "")

# ── SUMMARY ───────────────────────────────────────────────────
print("\n" + "=" * 65)
print("📊 SUMMARY")
print("=" * 65)

working = []
broken = []
missing = []

for name, (icon, status, fix) in results.items():
    if icon == "✅":
        working.append(name)
        print(f"  ✅ {name}: {status}")
    elif icon == "⚠️":
        broken.append(name)
        print(f"  ⚠️ {name}: {status}")
        if fix:
            print(f"     💡 Fix: {fix}")
    else:
        missing.append(name)
        print(f"  ❌ {name}: {status}")
        if fix:
            print(f"     💡 Fix: {fix}")

print(f"\n✅ Working: {len(working)} — {', '.join(working) if working else 'None'}")
print(f"⚠️ Issues:  {len(broken)} — {', '.join(broken) if broken else 'None'}")
print(f"❌ Missing: {len(missing)} — {', '.join(missing) if missing else 'None'}")

print("\n" + "=" * 65)
print("🎯 PRIORITY ACTIONS:")
print("=" * 65)

if "OpenRouter" in missing:
    print("\n1. 🌐 Add OpenRouter (FREE, no credit card):")
    print("   → openrouter.ai/keys")
    print("   → /setkey OPENROUTER_API_KEY sk-or-xxx")

if "HuggingFace" in missing:
    print("\n2. 🤗 Add HuggingFace (FREE, unlimited):")
    print("   → huggingface.co/settings/tokens")
    print("   → /setkey HUGGINGFACE_API_KEY hf_xxx")

if "Gemini" in broken:
    print("\n3. 💎 Fix Gemini (quota exceeded):")
    print("   → Create new Google account")
    print("   → makersuite.google.com/app/apikey")
    print("   → /setkey GEMINI_API_KEY AIza_xxx")

print("=" * 65)
