"""Check Gmail API token status"""
import base64, json, os
from dotenv import load_dotenv
load_dotenv()

token_env = os.getenv('GMAIL_TOKEN_JSON', '')
if token_env:
    try:
        decoded = base64.b64decode(token_env).decode()
        data = json.loads(decoded)
        has_refresh = bool(data.get('refresh_token'))
        expiry = data.get('expiry', '?')
        print(f'Gmail token: PRESENT')
        print(f'Has refresh_token: {has_refresh}')
        print(f'Expiry: {expiry}')
        if has_refresh:
            print('Status: OK - will auto-refresh')
        else:
            print('Status: WARNING - no refresh token, may expire')
    except Exception as e:
        print(f'Gmail token: ERROR - {e}')
else:
    print('Gmail token: NOT SET in env (GMAIL_TOKEN_JSON missing)')
    if os.path.exists('token.json'):
        print('token.json: EXISTS locally')
        with open('token.json') as f:
            data = json.load(f)
        print(f'Has refresh_token: {bool(data.get("refresh_token"))}')
    else:
        print('token.json: NOT FOUND')
