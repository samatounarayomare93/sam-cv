#!/usr/bin/env python3
"""
🚀 FINAL FIXED BOT - ALL WORKING
"""

import os
import sys
import asyncio
import logging
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

print("=" * 70)
print("🚀 FINAL FIXED BOT")
print("=" * 70)
print(f"Token: {TOKEN[:20]}...")
print(f"Chat ID: {CHAT_ID}")
print()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

from core.db_client import RealityShapingDB
from core.ai_agent import OmniIntelligence

db = RealityShapingDB()
ai = OmniIntelligence()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start"""
    await update.message.reply_text(
        "🚀 **Sam's Job Bot - FIXED VERSION**\n\n"
        "Commands:\n"
        "/menu - Main menu\n"
        "/stats - Statistics\n"
        "/test_email - Send test email\n"
        "/send_one - Send 1 application"
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /menu"""
    keyboard = [
        [InlineKeyboardButton("📊 Stats", callback_data="stats")],
        [InlineKeyboardButton("📧 Test Email", callback_data="test_email")],
        [InlineKeyboardButton("🚀 Send 1 App", callback_data="send_one")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎯 **Main Menu**", reply_markup=reply_markup)

async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats"""
    try:
        stats = await db.get_stats()
        msg = (
            f"📊 **Statistics**\n\n"
            f"Total: {stats.get('total', 0)}\n"
            f"Qualified: {stats.get('qualified', 0)}\n"
            f"Sent: {stats.get('sent', 0)}\n"
            f"Pending: {stats.get('pending', 0)}"
        )
        await update.message.reply_text(msg)
    except Exception as e:
        logging.error(f"Stats error: {e}")
        await update.message.reply_text(f"❌ Error: {e}")

async def test_email_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /test_email"""
    await update.message.reply_text("📧 Sending test email...")
    try:
        from core.smtp_engine import send_test_email
        result = send_test_email('samsalameh.cv@gmail.com')
        if result:
            await update.message.reply_text("✅ Test email sent!")
        else:
            await update.message.reply_text("❌ Failed to send")
    except Exception as e:
        logging.error(f"Test email error: {e}")
        await update.message.reply_text(f"❌ Error: {e}")

async def send_one_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /send_one - Send 1 application"""
    await update.message.reply_text("🚀 Sending 1 application...")
    try:
        from core.smtp_engine import send_strike
        
        # Get pending leads (these are qualified leads ready to send)
        pending = await db.get_pending_leads(limit=1)
        
        if not pending or len(pending) == 0:
            await update.message.reply_text("⚠️ No pending leads found.")
            return
        
        lead = pending[0]
        
        # Send application
        result = send_strike(lead)
        
        if result:
            # Update status to sent
            await db.update_lead_status(lead.get('url', ''), 'sent')
            await update.message.reply_text(
                f"✅ Application sent!\n\n"
                f"Company: {lead.get('company_name', 'Unknown')}\n"
                f"Job: {lead.get('job_title', 'Unknown')}"
            )
        else:
            await update.message.reply_text("❌ Failed to send application")
    except Exception as e:
        logging.error(f"Send one error: {e}")
        await update.message.reply_text(f"❌ Error: {e}")

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    
    try:
        if query.data == "stats":
            stats = await db.get_stats()
            msg = (
                f"📊 **Statistics**\n\n"
                f"Total: {stats.get('total', 0)}\n"
                f"Qualified: {stats.get('qualified', 0)}\n"
                f"Sent: {stats.get('sent', 0)}\n"
                f"Pending: {stats.get('pending', 0)}"
            )
            await query.edit_message_text(msg)
        
        elif query.data == "test_email":
            await query.edit_message_text("📧 Sending test email...")
            from core.smtp_engine import send_test_email
            result = send_test_email('samsalameh.cv@gmail.com')
            if result:
                await query.edit_message_text("✅ Test email sent successfully!")
            else:
                await query.edit_message_text("❌ Failed to send test email")
        
        elif query.data == "send_one":
            await query.edit_message_text("🚀 Sending 1 application...")
            from core.smtp_engine import send_strike
            
            pending = await db.get_pending_leads(limit=1)
            
            if not pending or len(pending) == 0:
                await query.edit_message_text("⚠️ No pending leads found.")
                return
            
            lead = pending[0]
            result = send_strike(lead)
            
            if result:
                await db.update_lead_status(lead.get('url', ''), 'sent')
                await query.edit_message_text(
                    f"✅ Application sent!\n\n"
                    f"Company: {lead.get('company_name', 'Unknown')}\n"
                    f"Job: {lead.get('job_title', 'Unknown')}"
                )
            else:
                await query.edit_message_text("❌ Failed to send application")
        
        else:
            await query.edit_message_text(f"⚠️ Unknown: {query.data}")
    
    except Exception as e:
        logging.error(f"Button handler error: {e}")
        await query.edit_message_text(f"❌ Error: {e}")

async def main():
    """Start bot"""
    print("🚀 Starting bot...")
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("stats", stats_cmd))
    app.add_handler(CommandHandler("test_email", test_email_cmd))
    app.add_handler(CommandHandler("send_one", send_one_cmd))
    app.add_handler(CallbackQueryHandler(handle_button))
    
    await app.initialize()
    await app.start()
    await app.bot.delete_webhook(drop_pending_updates=True)
    
    print("=" * 70)
    print("✅ BOT IS RUNNING!")
    print("=" * 70)
    print("📱 Commands:")
    print("   /menu - Main menu")
    print("   /stats - Statistics")
    print("   /test_email - Send test email")
    print("   /send_one - Send 1 application")
    print("=" * 70)
    
    await app.updater.start_polling(drop_pending_updates=True)
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Bot stopped")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
