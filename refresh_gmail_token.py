import os
import sys
import logging

# Ensure we can import from core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.gmail_auth import get_gmail_service

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    print("\n" + "="*50)
    print("GMAIL TOKEN REFRESHER - PROJECT CHRONOS")
    print("="*50)
    print("\nThis script will open a browser to refresh your Gmail token.")
    print("Once you log in, it will save a fresh 'token.json' file.")
    print("After that, you just need to push the new token to Render.\n")
    
    try:
        # Force os.environ['RENDER'] to None to allow local server
        if 'RENDER' in os.environ:
            del os.environ['RENDER']
            
        print("🚀 Requesting fresh token from Google...")
        service = get_gmail_service()
        
        if service:
            print("\n✅ SUCCESS: 'token.json' has been refreshed!")
            print("Next steps:")
            print("1. Run: git add token.json")
            print("2. Run: git commit -m 'Refresh Gmail Token'")
            print("3. Run: git push origin main")
            print("\nThen your bot on Render will have 100% Inbox delivery power!")
        else:
            print("\n❌ FAILED: Could not initialize Gmail service.")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    main()
