#!/usr/bin/env python3
"""
Test bot polling directly
"""

import os
import asyncio
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

print("=" * 70)
print("🧪 TESTING BOT POLLING")
print("=" * 70)

async def handle_any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle any message"""
    print(f"✅ RECEIVED MESSAGE: {update.message.text}")
    await update.message.reply_text(f"✅ Bot received: {update.message.text}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start"""
    print("✅ RECEIVED /start")
    await update.message.reply_text("✅ Bot is working!")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_any_message))
    
    await app.initialize()
    await app.start()
    await app.bot.delete_webhook(drop_pending_updates=True)
    
    print("✅ Bot started - Send /start to test")
    print("=" * 70)
    
    await app.updater.start_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
