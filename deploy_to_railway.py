"""
Deploy to Railway.app - Free alternative to Render with no build minutes limit.
Railway gives $5 free credit/month which is enough for a small bot.

Steps:
1. Create Railway account
2. Get Railway token
3. Deploy via Railway CLI or API
"""
import os, requests, json
from dotenv import load_dotenv
load_dotenv()

railway_token = os.getenv('RAILWAY_TOKEN', '')

if not railway_token:
    print("="*60)
    print("RAILWAY DEPLOYMENT GUIDE")
    print("="*60)
    print("""
To deploy on Railway (FREE, no build minutes limit):

STEP 1: Create account
  → railway.app
  → Sign up with GitHub (same account)
  → Free $5 credit/month

STEP 2: Get token
  → railway.app/account/tokens
  → Create new token
  → Copy it

STEP 3: Add to .env
  RAILWAY_TOKEN=your_token_here

STEP 4: Run this script again
  .sovereign_runtime\\python.exe deploy_to_railway.py

OR use Railway CLI:
  npm install -g @railway/cli
  railway login
  railway init
  railway up
""")
else:
    print("Railway token found! Deploying...")
    # Railway GraphQL API
    headers = {
        'Authorization': f'Bearer {railway_token}',
        'Content-Type': 'application/json'
    }
    
    # Create project
    query = """
    mutation {
      projectCreate(input: {name: "sam-cv-bot"}) {
        id
        name
      }
    }
    """
    r = requests.post(
        'https://backboard.railway.app/graphql/v2',
        headers=headers,
        json={'query': query},
        timeout=30
    )
    print(f"Status: {r.status_code}")
    print(r.json())
