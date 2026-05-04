import resend
import os
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv('RESEND_API_KEY')

print(f"API Key: {resend.api_key[:20]}...")

try:
    r = resend.Emails.send({
        "from": "Sam Salameh <onboarding@resend.dev>",
        "to": ["samsalameh.cv@gmail.com"],
        "subject": "✅ Test Email - Resend Working!",
        "html": "<h1>✅ Resend is working!</h1><p>This email was sent via Resend API. If you see this, emails will now arrive in your inbox!</p>"
    })
    print("SUCCESS:", r)
except Exception as e:
    print("FAILED:", e)
