import requests

api_key = 'sp_apikey_7705735ac00012975c4457e04b5e2b631f2f1bf2e7be618f8019ece27395d485'
headers = {'Authorization': f'Bearer {api_key}'}

# Check user info
r = requests.get('https://api.sendpulse.com/user/info', headers=headers, timeout=10)
print('user/info:', r.status_code, r.text[:200])

# Check balance
r2 = requests.get('https://api.sendpulse.com/user/balance/email', headers=headers, timeout=10)
print('balance/email:', r2.status_code, r2.text[:200])

# Check if they have a different email endpoint
r3 = requests.get('https://api.sendpulse.com/smtp/emails?limit=5', headers=headers, timeout=10)
print('smtp/emails:', r3.status_code, r3.text[:200])
