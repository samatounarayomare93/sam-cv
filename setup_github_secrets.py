"""
Setup GitHub Secrets for the deploy workflow.
Run this ONCE to add all secrets to GitHub repo.
"""
import requests, os, base64, json
from dotenv import load_dotenv
load_dotenv()

GITHUB_PAT = os.getenv('GITHUB_PAT', '')
REPO = 'samatounarayomare93/sam-cv'

headers = {
    'Authorization': f'token {GITHUB_PAT}',
    'Accept': 'application/vnd.github.v3+json',
    'X-GitHub-Api-Version': '2022-11-28'
}

# Get repo public key for secret encryption
r = requests.get(f'https://api.github.com/repos/{REPO}/actions/secrets/public-key', headers=headers, timeout=10)
if r.status_code != 200:
    print(f"Failed to get public key: {r.status_code} - {r.text[:200]}")
    exit(1)

pub_key_data = r.json()
pub_key_id = pub_key_data['key_id']
pub_key_b64 = pub_key_data['key']

# Encrypt secret using libsodium (PyNaCl)
try:
    from nacl import encoding, public
    def encrypt_secret(public_key_b64: str, secret_value: str) -> str:
        pk = public.PublicKey(public_key_b64.encode("utf-8"), encoding.Base64Encoder())
        sealed_box = public.SealedBox(pk)
        encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
        return base64.b64encode(encrypted).decode("utf-8")
    HAS_NACL = True
except ImportError:
    HAS_NACL = False
    print("⚠️ PyNaCl not installed. Installing...")
    import subprocess
    subprocess.run(['.sovereign_runtime/python.exe', '-m', 'pip', 'install', 'PyNaCl', '-q'])
    from nacl import encoding, public
    def encrypt_secret(public_key_b64: str, secret_value: str) -> str:
        pk = public.PublicKey(public_key_b64.encode("utf-8"), encoding.Base64Encoder())
        sealed_box = public.SealedBox(pk)
        encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
        return base64.b64encode(encrypted).decode("utf-8")

def set_secret(name: str, value: str):
    if not value:
        print(f"  ⏭️  {name}: SKIPPED (empty)")
        return
    encrypted = encrypt_secret(pub_key_b64, value)
    r = requests.put(
        f'https://api.github.com/repos/{REPO}/actions/secrets/{name}',
        headers=headers,
        json={'encrypted_value': encrypted, 'key_id': pub_key_id},
        timeout=10
    )
    if r.status_code in (201, 204):
        masked = value[:6] + '...' if len(value) > 6 else '***'
        print(f"  ✅ {name}: {masked}")
    else:
        print(f"  ❌ {name}: HTTP {r.status_code} - {r.text[:100]}")

print("=" * 55)
print("SETTING GITHUB SECRETS FOR DEPLOY WORKFLOW")
print("=" * 55)

secrets = {
    # Render Account 2
    'RENDER_API_KEY_ACC2':      'rnd_m4ozEoc4nQYOT16Omj0U9QGd3pra',
    'RENDER_SERVICE_ID_ACC2':   'srv-d80th10g4nts738vk7b0',
    # Database
    'SUPABASE_URL':             os.getenv('SUPABASE_URL', ''),
    'SUPABASE_KEY':             os.getenv('SUPABASE_KEY', ''),
    # AI
    'GROQ_API_KEY':             os.getenv('GROQ_API_KEY', ''),
    'GEMINI_API_KEY':           os.getenv('GEMINI_API_KEY', ''),
    'OPENROUTER_API_KEY':       os.getenv('OPENROUTER_API_KEY', ''),
    'DEEPSEEK_API_KEY':         os.getenv('DEEPSEEK_API_KEY', ''),
    'HUGGINGFACE_API_KEY':      os.getenv('HUGGINGFACE_API_KEY', ''),
    # Telegram
    'TELEGRAM_BOT_TOKEN':       os.getenv('TELEGRAM_BOT_TOKEN', ''),
    'TELEGRAM_CHAT_ID':         os.getenv('TELEGRAM_CHAT_ID', ''),
    'TELEGRAM_API_ID':          os.getenv('TELEGRAM_API_ID', ''),
    'TELEGRAM_API_HASH':        os.getenv('TELEGRAM_API_HASH', ''),
    'TELEGRAM_SESSION_STRING':  os.getenv('TELEGRAM_SESSION_STRING', ''),
    # Email
    'GMAIL_SMTP_USER':          os.getenv('GMAIL_SMTP_USER', ''),
    'GMAIL_APP_PASSWORD':       os.getenv('GMAIL_APP_PASSWORD', ''),
    'ZOHO_SMTP_USER':           os.getenv('ZOHO_SMTP_USER', ''),
    'ZOHO_APP_PASSWORD':        os.getenv('ZOHO_APP_PASSWORD', ''),
    'ZOHO_SMTP_USER_2':         os.getenv('ZOHO_SMTP_USER_2', ''),
    'ZOHO_APP_PASSWORD_2':      os.getenv('ZOHO_APP_PASSWORD_2', ''),
    'BREVO_API_KEY':            os.getenv('BREVO_API_KEY', ''),
    'BREVO_SMTP_LOGIN':         os.getenv('BREVO_SMTP_LOGIN', ''),
    'BREVO_SMTP_PASSWORD':      os.getenv('BREVO_SMTP_PASSWORD', ''),
    'RESEND_API_KEY':           os.getenv('RESEND_API_KEY', ''),
}

for name, value in secrets.items():
    set_secret(name, value)

print(f"\n✅ Done! {len(secrets)} secrets configured.")
print("\nNow push the deploy.yml and it will auto-sync env vars on every deploy.")
