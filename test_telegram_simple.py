#!/usr/bin/env python3
"""
Simple Telegram Bot Test
"""

import os
import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

print("=" * 70)
print("🤖 SIMPLE TELEGRAM BOT TEST")
print("=" * 70)
print(f"\n✅ Token: {TOKEN[:20]}...")
print(f"✅ Chat ID: {CHAT_ID}")
print()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        "✅ Bot is working!\n\n"
        "Available commands:\n"
        "/start - This message\n"
        "/test - Test response\n"
        "/ping - Check if bot is alive"
    )

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /test command"""
    await update.message.reply_text("✅ Test successful! Bot is responding.")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ping command"""
    await update.message.reply_text("🏓 Pong! Bot is alive and running.")

async def main():
    """Start the bot"""
    print("🚀 Starting bot...")
    
    # Build application
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(CommandHandler("ping", ping))
    
    print("✅ Bot handlers registered")
    print("📡 Connecting to Telegram...")
    
    # Initialize and start
    await app.initialize()
    await app.start()
    
    # Delete webhook to use polling
    await app.bot.delete_webhook(drop_pending_updates=True)
    
    print("=" * 70)
    print("✅ BOT IS NOW RUNNING!")
    print("=" * 70)
    print("\n📱 Open Telegram and send:")
    print("   /start - To see available commands")
    print("   /test - To test the bot")
    print("   /ping - To check if bot is alive")
    print("\n⚠️  Keep this window open!")
    print("   Press Ctrl+C to stop the bot")
    print("=" * 70)
    print()
    
    # Start polling
    await app.updater.start_polling(drop_pending_updates=True)
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Stopping bot...")
        await app.updater.stop()
        await app.stop()
        await app.shutdown()
        print("✅ Bot stopped")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Bot stopped by user")
