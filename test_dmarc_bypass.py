import requests
from core import config

api_key = getattr(config, 'BREVO_API_KEY', None)
print(f"Testing with API Key: {api_key[:10]}...")

payload = {
    "sender": {"name": "Sam Salameh", "email": "a974ef001@smtp-brevo.com"},
    "to": [{"email": "sam.dev1@hotmail.com"}],
    "subject": "Test DMARC Bypass",
    "htmlContent": "<p>Test</p>",
    "replyTo": {"email": "sam.dev1@hotmail.com", "name": "Sam Salameh"}
}

response = requests.post(
    "https://api.brevo.com/v3/smtp/email",
    headers={"api-key": api_key, "Content-Type": "application/json", "Accept": "application/json"},
    json=payload
)
print("Status Code:", response.status_code)
print("Response:", response.text)
