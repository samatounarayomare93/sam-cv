"""
PHANTOM IGNITION: Secret Injection Script
Pushes local .env credentials to Supabase Secret Vault (system_secrets table).
"""
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def ignite_vault():
    url = os.getenv("SUPABASE_URL", "").rstrip('/')
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") # Use Service Role for injection
    if not key:
        key = os.getenv("SUPABASE_KEY")
        
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }

    secrets = {
        "TELEGRAM_SESSION_STRING": os.getenv("TELEGRAM_SESSION_STRING"),
        "SUPABASE_URL": os.getenv("SUPABASE_URL"),
        "SUPABASE_KEY": os.getenv("SUPABASE_KEY"),
        "SUPABASE_SERVICE_ROLE_KEY": os.getenv("SUPABASE_SERVICE_ROLE_KEY"),
        "RENDER_EXTERNAL_URL": os.getenv("RENDER_EXTERNAL_URL", "https://sam-job-automator.onrender.com"),
        "BREVO_API_KEY": os.getenv("BREVO_API_KEY"),
        "GMAIL_APP_PASSWORD": os.getenv("GMAIL_APP_PASSWORD"),
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
        "OPENROUTER_API_KEY": os.getenv("OPENROUTER_API_KEY")
    }

    print("IGNITING CLOUD SECRET VAULT...")
    
    for k, v in secrets.items():
        if not v:
            print(f"Skipping {k} (empty)")
            continue
            
        payload = {"key": k, "value": v}
        endpoint = f"{url}/rest/v1/system_secrets"
        
        # Test if key exists to decide between POST and PATCH (or just use resolution=merge-duplicates)
        r = requests.post(endpoint, headers=headers, data=json.dumps(payload))
        
        if r.status_code in [200, 201, 204]:
            print(f"Vaulted: {k}")
        else:
            print(f"Failed to vault {k}: {r.status_code} - {r.text}")

if __name__ == "__main__":
    ignite_vault()
