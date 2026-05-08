#!/usr/bin/env python3
"""
🚀 DIRECT TELEGRAM BOT START
Bypasses leadership system for local testing
Fixed for Windows Unicode issues.
"""

import sys
import os
import asyncio
import logging
from dotenv import load_dotenv

# [🛡️ WINDOWS UTF-8 FIX]
if sys.platform == 'win32':
    import io
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [BOT] %(levelname)s - %(message)s"
)

# Add core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

load_dotenv()

print("=" * 70)
print("STARTING TELEGRAM BOT (DIRECT MODE)")
print("=" * 70)

# Check environment variables
token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

if not token:
    print("ERROR: TELEGRAM_BOT_TOKEN not found in .env!")
    sys.exit(1)

if not chat_id:
    print("ERROR: TELEGRAM_CHAT_ID not found in .env!")
    sys.exit(1)

print(f"\n[OK] Token: {token[:20]}...")
print(f"[OK] Chat ID: {chat_id}")

# Import bot components
try:
    from telegram import Update
    from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
    from core.db_client import RealityShapingDB
    from core.ai_agent import OmniIntelligence
    
    print("\n[INFO] Initializing components...")
    db = RealityShapingDB()
    ai = OmniIntelligence()
    
    print("[OK] Components initialized!")
    
    # Create simple command handlers
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        await update.message.reply_text(
            "🚀 **Sam's Job Bot is Online!**\n\n"
            "Available commands:\n"
            "/menu - Main menu\n"
            "/stats - View statistics\n"
            "/scrape - Find new jobs\n"
            "/qualify - Qualify leads\n"
            "/strike - Send applications\n"
            "/test_email - Send test email"
        )
    
    async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /menu command"""
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        
        keyboard = [
            [InlineKeyboardButton("📊 Stats", callback_data="stats")],
            [InlineKeyboardButton("🔍 Scrape Jobs", callback_data="scrape")],
            [InlineKeyboardButton("✅ Qualify Leads", callback_data="qualify")],
            [InlineKeyboardButton("🚀 Send Applications", callback_data="strike")],
            [InlineKeyboardButton("📧 Test Email", callback_data="test_email")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🎯 **Main Menu**\n\nChoose an action:",
            reply_markup=reply_markup
        )
    
    async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        try:
            s = await db.get_stats()
            msg = (
                f"📊 **Statistics**\n\n"
                f"Total Strikes: {s.get('total_strikes', 0)}\n"
                f"Recon Rows: {s.get('recon_rows', 0)}"
            )
            await update.message.reply_text(msg)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
    
    async def test_email_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /test_email command"""
        await update.message.reply_text("📧 Sending test email...")
        try:
            from core.smtp_engine import send_test_email
            result = await asyncio.to_thread(send_test_email, 'samsalameh.cv@gmail.com')
            if result:
                await update.message.reply_text("✅ Test email sent successfully!")
            else:
                await update.message.reply_text("❌ Failed to send test email")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
    
    # ... (other handlers)
    
    async def main():
        """Start the bot"""
        print("\n[INFO] Starting Telegram bot...")
        
        # Build application
        app = ApplicationBuilder().token(token).build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("menu", menu))
        app.add_handler(CommandHandler("stats", stats))
        app.add_handler(CommandHandler("test_email", test_email_cmd))
        
        print("[OK] Bot handlers registered")
        print("[INFO] Connecting to Telegram...")
        
        # Initialize and start
        await app.initialize()
        await app.start()
        
        # Delete webhook to use polling
        await app.bot.delete_webhook(drop_pending_updates=True)
        
        print("=" * 70)
        print("✅ BOT IS NOW RUNNING!")
        print("=" * 70)
        
        # Start polling
        await app.updater.start_polling(drop_pending_updates=True)
        
        # Keep running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n[INFO] Stopping bot...")
            await app.updater.stop()
            await app.stop()
            await app.shutdown()
            print("[OK] Bot stopped")
    
    # Run the bot
    if __name__ == "__main__":
        asyncio.run(main())
    
except Exception as e:
    print(f"\n[ERROR] ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
