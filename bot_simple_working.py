#!/usr/bin/env python3
"""
🚀 SIMPLE WORKING BOT - NO CONFLICTS
Fixed for Windows Unicode issues.
"""

import os
import sys
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

# Add core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

print("=" * 70)
print("STARTING SIMPLE WORKING BOT")
print("=" * 70)
print(f"Token: {TOKEN[:20]}...")
print(f"Chat ID: {CHAT_ID}")
print()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Import components
try:
    from core.db_client import RealityShapingDB
    from core.ai_agent import OmniIntelligence
except ImportError:
    from db_client import RealityShapingDB
    from ai_agent import OmniIntelligence

db = RealityShapingDB()
ai = OmniIntelligence()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start"""
    await update.message.reply_text(
        "🚀 **Bot Online!**\n\n"
        "Commands:\n"
        "/menu - Main menu\n"
        "/stats - Statistics\n"
        "/test_email - Send test email"
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /menu"""
    keyboard = [
        [InlineKeyboardButton("📊 Stats", callback_data="stats")],
        [InlineKeyboardButton("📧 Test Email", callback_data="test_email")],
        [InlineKeyboardButton("🚀 Send 1 Application", callback_data="send_one")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎯 **Main Menu**", reply_markup=reply_markup)

async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats"""
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
    """Handle /test_email"""
    await update.message.reply_text("📧 Sending test email...")
    try:
        from core.smtp_engine import send_test_email
        result = await asyncio.to_thread(send_test_email, 'samsalameh.cv@gmail.com')
        if result:
            await update.message.reply_text("✅ Test email sent!")
        else:
            await update.message.reply_text("❌ Failed to send")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "stats":
        try:
            s = await db.get_stats()
            msg = (
                f"📊 **Statistics**\n\n"
                f"Total Strikes: {s.get('total_strikes', 0)}\n"
                f"Recon Rows: {s.get('recon_rows', 0)}"
            )
            await query.edit_message_text(msg)
        except Exception as e:
            await query.edit_message_text(f"❌ Error: {e}")
    
    elif query.data == "test_email":
        await query.edit_message_text("📧 Sending test email...")
        try:
            from core.smtp_engine import send_test_email
            result = await asyncio.to_thread(send_test_email, 'samsalameh.cv@gmail.com')
            if result:
                await query.edit_message_text("✅ Test email sent successfully!")
            else:
                await query.edit_message_text("❌ Failed to send test email")
        except Exception as e:
            await query.edit_message_text(f"❌ Error: {e}")
    
    elif query.data == "send_one":
        await query.edit_message_text("🚀 Sending 1 application...")
        try:
            from core.smtp_engine import send_strike
            
            # Get one qualified lead
            qualified = await db.get_qualified_leads()
            if not qualified or len(qualified) == 0:
                await query.edit_message_text("⚠️ No qualified leads found. Run /scrape first.")
                return
            
            lead = qualified[0]
            result = await asyncio.to_thread(send_strike, lead)
            
            if result:
                # Update status (might need to await or call a wrapper)
                # db.update_lead_status(lead['url'], 'sent')
                await query.edit_message_text(
                    f"✅ Application sent!\n\n"
                    f"Company: {lead.get('company_name', 'Unknown')}\n"
                    f"Job: {lead.get('job_title', 'Unknown')}"
                )
            else:
                await query.edit_message_text("❌ Failed to send application")
        except Exception as e:
            await query.edit_message_text(f"❌ Error: {e}")

async def main():
    """Start bot"""
    print("Starting bot...")
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("stats", stats_cmd))
    app.add_handler(CommandHandler("test_email", test_email_cmd))
    app.add_handler(CallbackQueryHandler(handle_button))
    
    await app.initialize()
    await app.start()
    await app.bot.delete_webhook(drop_pending_updates=True)
    
    print("=" * 70)
    print("✅ BOT IS RUNNING!")
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
