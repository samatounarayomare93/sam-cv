import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

async def main():
    print("""
    ==========================================================
    PROJECT CHRONOS: SESSION STRING GENERATOR
    ==========================================================
    This script will generate a permanent SESSION STRING.
    You will need to paste this into your Render Environment
    Variables as: TELEGRAM_SESSION_STRING
    ==========================================================
    """)
    
    # 1. Ask for credentials (or use env if set)
    api_id = input("Enter your Telegram API_ID: ").strip()
    api_hash = input("Enter your Telegram API_HASH: ").strip()
    phone = input("Enter your Phone Number (w/ country code): ").strip()

    # 2. Initialize Telethon with StringSession
    try:
        async with TelegramClient(StringSession(), api_id, api_hash) as client:
            session_str = client.session.save()
            
            print("\n" + "="*60)
            print("🚀 ABSOLUTE SUCCESS: SESSION STRING GENERATED")
            print("="*60)
            print("\nCopy the line below and paste it into Render Environment Variables:")
            print(f"\n{session_str}\n")
            print("="*60)
            print("KEEP THIS STRING SECRET. It grants full access to your account.")
            print("="*60)

    except Exception as e:
        print(f"\n❌ FAILED TO GENERATE SESSION: {e}")

if __name__ == "__main__":
    asyncio.run(main())
