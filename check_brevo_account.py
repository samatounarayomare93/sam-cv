import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('BREVO_API_KEY')
headers = {'api-key': api_key}

# Check account status
r = requests.get('https://api.brevo.com/v3/account', headers=headers)
data = r.json()
print("Account:", data.get('email'))
print("Plan:", data.get('plan'))
print("Company:", data.get('companyName'))

# Check if account is blocked
print("\nFull response:")
import json
print(json.dumps(data, indent=2))
