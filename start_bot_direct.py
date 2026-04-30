#!/usr/bin/env python3
"""
🚀 DIRECT TELEGRAM BOT START
Bypasses leadership system for local testing
"""

import sys
import os
import asyncio
import logging
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [BOT] %(levelname)s - %(message)s"
)

# Add core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

load_dotenv()

print("=" * 70)
print("🚀 STARTING TELEGRAM BOT (DIRECT MODE)")
print("=" * 70)

# Check environment variables
token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

if not token:
    print("❌ TELEGRAM_BOT_TOKEN not found in .env!")
    sys.exit(1)

if not chat_id:
    print("❌ TELEGRAM_CHAT_ID not found in .env!")
    sys.exit(1)

print(f"\n✅ Token: {token[:20]}...")
print(f"✅ Chat ID: {chat_id}")

# Import bot components
try:
    from telegram import Update
    from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
    from core.db_client import RealityShapingDB
    from core.ai_agent import OmniIntelligence
    
    print("\n🔧 Initializing components...")
    db = RealityShapingDB()
    ai = OmniIntelligence()
    
    print("✅ Components initialized!")
    
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
            stats = db.get_stats()
            msg = (
                f"📊 **Statistics**\n\n"
                f"Total Leads: {stats.get('total', 0)}\n"
                f"Qualified: {stats.get('qualified', 0)}\n"
                f"Sent: {stats.get('sent', 0)}\n"
                f"Pending: {stats.get('pending', 0)}"
            )
            await update.message.reply_text(msg)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
    
    async def test_email_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /test_email command"""
        await update.message.reply_text("📧 Sending test email...")
        try:
            from core.smtp_engine import send_test_email
            result = send_test_email('samsalameh.cv@gmail.com')
            if result:
                await update.message.reply_text("✅ Test email sent successfully!")
            else:
                await update.message.reply_text("❌ Failed to send test email")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
    
    async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "stats":
            try:
                stats = db.get_stats()
                msg = (
                    f"📊 **Statistics**\n\n"
                    f"Total Leads: {stats.get('total', 0)}\n"
                    f"Qualified: {stats.get('qualified', 0)}\n"
                    f"Sent: {stats.get('sent', 0)}\n"
                    f"Pending: {stats.get('pending', 0)}"
                )
                await query.edit_message_text(msg)
            except Exception as e:
                await query.edit_message_text(f"❌ Error: {e}")
        
        elif query.data == "test_email":
            await query.edit_message_text("📧 Sending test email...")
            try:
                from core.smtp_engine import send_test_email
                result = send_test_email('samsalameh.cv@gmail.com')
                if result:
                    await query.edit_message_text("✅ Test email sent successfully!")
                else:
                    await query.edit_message_text("❌ Failed to send test email")
            except Exception as e:
                await query.edit_message_text(f"❌ Error: {e}")
        
        else:
            await query.edit_message_text(f"⚠️ Command '{query.data}' not implemented yet")
    
    async def main():
        """Start the bot"""
        print("\n🚀 Starting Telegram bot...")
        
        # Build application
        app = ApplicationBuilder().token(token).build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("menu", menu))
        app.add_handler(CommandHandler("stats", stats))
        app.add_handler(CommandHandler("test_email", test_email_cmd))
        app.add_handler(CallbackQueryHandler(handle_callback))
        
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
        print("   /menu - To see the main menu")
        print("   /stats - To view statistics")
        print("   /test_email - To send a test email")
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
    
    # Run the bot
    asyncio.run(main())
    
except KeyboardInterrupt:
    print("\n\n⚠️ Bot stopped by user")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
