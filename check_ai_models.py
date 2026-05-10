"""Check available AI models and test them."""
import requests, os
from dotenv import load_dotenv
load_dotenv()

groq_key = os.getenv('GROQ_API_KEY')
gemini_key = os.getenv('GEMINI_API_KEY')

# Check Groq models
print("=== GROQ MODELS ===")
r = requests.get('https://api.groq.com/openai/v1/models',
    headers={'Authorization': f'Bearer {groq_key}'}, timeout=10)
models = r.json().get('data', [])
for m in sorted(models, key=lambda x: x.get('id', '')):
    mid = m['id']
    print(f"  {mid}")

# Test Groq with correct model
print("\n=== GROQ TEST ===")
for model in ['llama-3.3-70b-versatile', 'llama3-70b-8192', 'mixtral-8x7b-32768']:
    try:
        r = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={'Authorization': f'Bearer {groq_key}', 'Content-Type': 'application/json'},
            json={'model': model, 'messages': [{'role': 'user', 'content': 'Say OK in 2 words'}], 'max_tokens': 10},
            timeout=15
        )
        data = r.json()
        if 'choices' in data:
            reply = data['choices'][0]['message']['content']
            print(f"  ✅ {model}: '{reply}'")
        else:
            err = data.get('error', {}).get('message', str(data))[:60]
            print(f"  ❌ {model}: {err}")
    except Exception as e:
        print(f"  ❌ {model}: {e}")

# Test Gemini models
print("\n=== GEMINI TEST ===")
for model in ['gemini-2.0-flash', 'gemini-2.5-flash', 'gemini-1.5-flash']:
    try:
        r = requests.post(
            f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={gemini_key}',
            json={'contents': [{'parts': [{'text': 'Say OK'}]}]},
            timeout=15
        )
        data = r.json()
        if 'candidates' in data:
            reply = data['candidates'][0]['content']['parts'][0]['text'][:30]
            print(f"  ✅ {model}: '{reply}'")
        else:
            err = data.get('error', {}).get('message', str(data))[:80]
            print(f"  ❌ {model}: {err}")
    except Exception as e:
        print(f"  ❌ {model}: {e}")
