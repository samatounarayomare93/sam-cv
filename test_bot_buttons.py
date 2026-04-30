#!/usr/bin/env python3
"""
Test if bot is receiving button clicks
"""

import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    print(f"✅ BUTTON CLICKED: {query.data}")
    await query.answer()
    await query.edit_message_text(f"✅ Button '{query.data}' was clicked!")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    await app.initialize()
    await app.start()
    await app.bot.delete_webhook(drop_pending_updates=True)
    
    print("✅ Listening for button clicks...")
    print("Press Ctrl+C to stop")
    
    await app.updater.start_polling(drop_pending_updates=True)
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
