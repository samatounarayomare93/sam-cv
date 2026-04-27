from telethon import TelegramClient
from telethon.sessions import StringSession
import os

def ignite_session():
    print("""
    [🕵️ PROJECT CHRONOS: SESSION GENERATION PROTOCOL]
    -------------------------------------------------
    This will generate the TELEGRAM_SESSION_STRING required 
    for the Phantom Network to run on the Render cloud.
    """)
    
    # User Inputs
    api_id = input("Enter your TELEGRAM_API_ID: ").strip()
    api_hash = input("Enter your TELEGRAM_API_HASH: ").strip()

    if not api_id or not api_hash:
        print("❌ Error: API_ID and API_HASH are mandatory.")
        return

    # Create client with temporary in-memory session
    client = TelegramClient(StringSession(), int(api_id), api_hash)

    async def main():
        await client.start()
        print("\n✅ Authentication Successful!")
        print("-" * 50)
        print("YOUR TELEGRAM_SESSION_STRING (Copy the entire line below):")
        print("-" * 50)
        print(client.session.save())
        print("-" * 50)
        print("\n⚠️  IMPORTANT: Keep this string SECRET. Anyone with it can control your account.")
        print("Now, paste this into your Render Environment Variables as 'TELEGRAM_SESSION_STRING'.")

    with client:
        client.loop.run_until_complete(main())

if __name__ == "__main__":
    ignite_session()
