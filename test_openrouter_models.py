import os, requests
from dotenv import load_dotenv
load_dotenv()

key = os.getenv('OPENROUTER_API_KEY', '')
if not key:
    print('No OpenRouter key set')
else:
    print(f"Testing OpenRouter key: {key[:20]}...")
    models = [
        'meta-llama/llama-3.2-3b-instruct:free',
        'meta-llama/llama-3.1-8b-instruct:free',
        'mistralai/mistral-7b-instruct:free',
        'google/gemma-2-9b-it:free',
        'microsoft/phi-3-mini-128k-instruct:free',
    ]
    for m in models:
        try:
            r = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {key}',
                    'Content-Type': 'application/json',
                    'HTTP-Referer': 'https://sam-bot-v2.onrender.com'
                },
                json={'model': m, 'messages': [{'role': 'user', 'content': 'Say OK'}], 'max_tokens': 5},
                timeout=15
            )
            if r.status_code == 200:
                resp = r.json().get('choices', [{}])[0].get('message', {}).get('content', '')
                print(f"  OK: {m.split('/')[-1][:30]} -> {resp[:20]}")
            else:
                print(f"  FAIL {r.status_code}: {m.split('/')[-1][:30]} -> {r.text[:60]}")
        except Exception as e:
            print(f"  ERROR: {m.split('/')[-1][:30]} -> {str(e)[:50]}")
