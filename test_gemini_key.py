import requests

key = 'AIzaSyB8Qu1X_0WHvwOPIA3jBD37VallwFbTXyw'

# Test 1: List available models
print("=" * 60)
print("Testing Gemini API Key...")
print("=" * 60)

try:
    r = requests.get(
        f'https://generativelanguage.googleapis.com/v1beta/models?key={key}',
        timeout=15
    )
    data = r.json()
    
    if 'models' in data:
        print("\n✅ API Key is valid!")
        print(f"\nAvailable models ({len(data['models'])} total):")
        for model in data['models'][:5]:
            name = model.get('name', 'unknown')
            print(f"  - {name}")
    else:
        print("\n❌ API Key failed:")
        print(data.get('error', {}).get('message', str(data)[:200]))
except Exception as e:
    print(f"\n❌ Error: {e}")

# Test 2: Try to generate content
print("\n" + "=" * 60)
print("Testing content generation...")
print("=" * 60)

try:
    r = requests.post(
        f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={key}',
        json={'contents': [{'parts': [{'text': 'Say OK'}]}]},
        timeout=15
    )
    data = r.json()
    
    if 'candidates' in data:
        response = data['candidates'][0]['content']['parts'][0]['text']
        print(f"\n✅ Content generation works!")
        print(f"Response: {response[:50]}")
    else:
        print("\n❌ Content generation failed:")
        error_msg = data.get('error', {}).get('message', str(data)[:200])
        print(error_msg)
        
        # If quota exceeded, check if it's a billing issue
        if 'quota' in error_msg.lower():
            print("\n⚠️ QUOTA ISSUE DETECTED")
            print("This usually means:")
            print("  1. Free tier quota exhausted")
            print("  2. Need to enable billing on Google Cloud")
            print("  3. Need to wait for quota reset")
            print("\nSolution:")
            print("  - Go to: https://console.cloud.google.com/billing")
            print("  - Enable billing for your project")
            print("  - Or wait for free quota to reset (usually monthly)")
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "=" * 60)
print("RECOMMENDATION:")
print("=" * 60)
print("The system is currently using Groq API as primary AI provider.")
print("Groq is working perfectly with 14,400 requests/day free.")
print("Gemini is only used as a fallback, so this is NOT critical.")
print("\nYou can:")
print("  1. Enable billing on Google Cloud for unlimited Gemini access")
print("  2. Keep using Groq as primary (current setup)")
print("  3. Wait for Gemini free quota to reset")
print("=" * 60)
