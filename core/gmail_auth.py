import os.path
import logging
import json
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    """
    ☁️ CLOUD-SAFE Gmail Authentication
    Supports both local file (token.json) and cloud environment variable (GMAIL_TOKEN_JSON)
    """
    creds = None
    
    # ☁️ CLOUD PRIORITY: Check environment variable first
    token_env = os.getenv("GMAIL_TOKEN_JSON")
    if token_env:
        try:
            # Decode from base64 if needed
            if token_env.startswith("eyJ"):  # Looks like base64
                token_json = base64.b64decode(token_env).decode('utf-8')
            else:
                token_json = token_env
            
            token_data = json.loads(token_json)
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)
            logging.info("✅ Gmail credentials loaded from environment variable")
        except Exception as e:
            logging.warning(f"⚠️ Failed to load Gmail token from env var: {e}")
    
    # LOCAL FALLBACK: Check token.json file
    if not creds and os.path.exists('token.json'):
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            logging.info("✅ Gmail credentials loaded from token.json file")
        except Exception as e:
            logging.warning(f"⚠️ Failed to load Gmail token from file: {e}")
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                logging.info("✅ Gmail token refreshed successfully")
                
                # ☁️ CLOUD: Save refreshed token back to env var (for next restart)
                if token_env:
                    # Note: Can't update env var at runtime, but log for manual update
                    logging.info("💡 Gmail token refreshed. Update GMAIL_TOKEN_JSON env var with:")
                    logging.info(base64.b64encode(creds.to_json().encode()).decode())
            except Exception as e:
                logging.error(f"❌ Gmail token refresh failed: {e}")
                creds = None
        else:
            # Need fresh authentication
            if not os.path.exists('credentials.json'):
                logging.error("❌ credentials.json not found. Gmail API unavailable.")
                return None
            
            # [🛡️ CLOUD SAFETY]: Never run an interactive server in a headless/cloud environment
            is_headless = os.getenv("RENDER") or os.getenv("RAILWAY") or os.getenv("HEROKU")
            if is_headless:
                logging.error("❌ GMAIL AUTH REJECTED: Interactive login is blocked on Cloud.")
                logging.error("💡 To fix: Run bot locally once to generate token, then add to Render:")
                logging.error("   1. Run locally: python main_bot.py")
                logging.error("   2. Complete Gmail OAuth")
                logging.error("   3. Copy token.json content")
                logging.error("   4. Base64 encode: base64 token.json")
                logging.error("   5. Add to Render env var: GMAIL_TOKEN_JSON=<base64_string>")
                return None

            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0, access_type='offline', prompt='consent')
                
                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
                
                logging.info("✅ Gmail authentication completed. Token saved to token.json")
                logging.info("💡 For cloud deployment, add this to Render env vars:")
                logging.info(f"   GMAIL_TOKEN_JSON={base64.b64encode(creds.to_json().encode()).decode()}")
            except Exception as e:
                logging.error(f"❌ Gmail authentication failed: {e}")
                return None
    
    if not creds:
        logging.error("❌ Gmail authentication failed completely")
        return None
    
    try:
        return build('gmail', 'v1', credentials=creds)
    except Exception as e:
        logging.error(f"❌ Failed to build Gmail service: {e}")
        return None
