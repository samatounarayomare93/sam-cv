#!/usr/bin/env python3
"""
🚀 SOVEREIGN TELEGRAM BOT - FULL FEATURED
Complete implementation with all commands and premium features.
Fixed for Windows Unicode issues.
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv

# [🛡️ WINDOWS UTF-8 FIX]
if sys.platform == 'win32':
    import io
    # Reconfigure stdout/stderr to use UTF-8
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        # Fallback for older python
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [BOT] %(levelname)s - %(message)s"
)

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

print("=" * 70)
print("🚀 SOVEREIGN TELEGRAM BOT")
print("=" * 70)
print(f"Token: {TOKEN[:20]}...")
print(f"Chat ID: {CHAT_ID}")
print()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Import components
try:
    from core.db_client import RealityShapingDB
    from core.ai_agent import OmniIntelligence
    from core import smtp_engine
except ImportError:
    # If core is not in path or nested
    from db_client import RealityShapingDB
    from ai_agent import OmniIntelligence
    import smtp_engine

db = RealityShapingDB()
ai = OmniIntelligence()

# ============================================================================
# COMMAND HANDLERS
# ============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start"""
    keyboard = [
        [InlineKeyboardButton("📊 Stats", callback_data="stats"),
         InlineKeyboardButton("🖥️ Status", callback_data="status")],
        [InlineKeyboardButton("📧 Test Email", callback_data="test_email"),
         InlineKeyboardButton("🧪 Test Strike", callback_data="test_strike")],
        [InlineKeyboardButton("🛑 Kill Switch", callback_data="kill"),
         InlineKeyboardButton("🟢 Resume", callback_data="resume")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👑 **PROJECT CHRONOS: SOVEREIGN V2**\n\n"
        "Welcome, Master. The automation swarm is operational.\n\n"
        "**System Status:** 🟢 Online\n"
        "**Target:** 1500 apps/day\n\n"
        "Choose an action:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /menu"""
    keyboard = [
        [InlineKeyboardButton("📊 Statistics", callback_data="stats"),
         InlineKeyboardButton("🖥️ Cloud Status", callback_data="status")],
        [InlineKeyboardButton("📧 Quick Test", callback_data="test_email"),
         InlineKeyboardButton("🧪 Manual Strike", callback_data="test_strike")],
        [InlineKeyboardButton("📜 System Logs", callback_data="logs"),
         InlineKeyboardButton("📋 View Leads", callback_data="leads")],
        [InlineKeyboardButton("🛑 STOP ALL", callback_data="kill"),
         InlineKeyboardButton("🟢 RESUME", callback_data="resume")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎮 **SOVEREIGN COMMAND CENTER**\n\nChoose an action:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats"""
    try:
        s = await db.get_stats()
        msg = (
            f"📊 **MISSION STATISTICS**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🚀 **Total Strikes:** `{s.get('total_strikes', 0)}` (Emails sent)\n"
            f"🎯 **Leads Found:** `{s.get('recon_rows', 0)}` (Job discovery)\n"
            f"💻 **Mode:** `ULTRA-MAXIMUM`\n"
            f"━━━━━━━━━━━━━━━"
        )
        await update.message.reply_text(msg, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"❌ **Stats Error:** `{e}`")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status"""
    try:
        health = db.get_system_health()
        msg = (
            f"🖥️ **SYSTEM TELEMETRY**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🧠 **AI Intelligence:** {health.get('ai', '🟢 Active')}\n"
            f"👤 **API Access:** {health.get('access', '🟢 Verified')}\n"
            f"🔌 **Cloud Sync:** {health.get('persistence', '🟢 Online')}\n"
            f"🕒 **Uptime:** `{health.get('uptime', 'N/A')}`\n"
            f"━━━━━━━━━━━━━━━"
        )
        await update.message.reply_text(msg, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"❌ **Status Error:** `{e}`")

async def test_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /test_email - Quick test to default email"""
    target = os.getenv("TEST_RECEIVER_EMAIL", "samsalameh.cv@gmail.com")
    
    # Check if update has message or callback_query
    msg = update.message if update.message else update.callback_query.message
    
    status_msg = await msg.reply_text(f"🧪 **INITIATING QUICK TEST STRIKE...**\nTarget: `{target}`\n_Generating high-fidelity CV & Cover Letter..._", parse_mode='Markdown')
    try:
        success = await asyncio.to_thread(smtp_engine.send_test_email, target)
        if success:
            await status_msg.edit_text(f"✅ **TEST STRIKE DELIVERED!**\nTarget: `{target}`\n\nCheck your inbox for the premium dark-themed design.", parse_mode='Markdown')
        else:
            await status_msg.edit_text(f"❌ **TEST STRIKE FAILED**\nCheck server logs. Brevo or Gmail might be blocking.", parse_mode='Markdown')
    except Exception as e:
        await status_msg.edit_text(f"💥 **ERROR:** `{e}`", parse_mode='Markdown')

async def test_strike(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /test_strike - Prompt for email"""
    msg = update.message if update.message else update.callback_query.message
    
    context.user_data['state'] = 'WAITING_TEST_EMAIL'
    await msg.reply_text(
        "🧪 **MANUAL TEST STRIKE**\n\n"
        "Please enter the **target email address** where you want to receive the premium application simulation.\n\n"
        "💡 _Example: your personal Gmail address_",
        parse_mode='Markdown'
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages for states"""
    state = context.user_data.get('state')
    user_text = update.message.text.strip()
    
    if state == 'WAITING_TEST_EMAIL':
        if '@' not in user_text:
            await update.message.reply_text("❌ **Invalid Email.** Please enter a valid email address.")
            return
        
        context.user_data['state'] = None
        status_msg = await update.message.reply_text(f"🚀 **LAUNCHING PREMIUM STRIKE TO:** `{user_text}`...", parse_mode='Markdown')
        try:
            success = await asyncio.to_thread(smtp_engine.send_test_email, user_text)
            if success:
                await status_msg.edit_text(f"✅ **STRIKE SUCCESS!**\n\nThe premium application package has been delivered to `{user_text}`.", parse_mode='Markdown')
            else:
                await status_msg.edit_text(f"⚠️ **STRIKE FAILED**\nDelivery chain failed. Check Brevo/Gmail credentials.", parse_mode='Markdown')
        except Exception as e:
            await status_msg.edit_text(f"💥 **ERROR:** `{e}`", parse_mode='Markdown')

async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /kill"""
    msg = update.message if update.message else update.callback_query.message
    try:
        await db.activate_kill_switch(True)
        await msg.reply_text("🛑 **SYSTEM OVERRIDE: KILL SWITCH ACTIVATED**\nAll autonomous cycles frozen.", parse_mode='Markdown')
    except Exception as e:
        await msg.reply_text(f"❌ **Error:** `{e}`")

async def resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /resume"""
    msg = update.message if update.message else update.callback_query.message
    try:
        await db.activate_kill_switch(False)
        await msg.reply_text("🟢 **COMMAND: SWARM RE-ACTIVATED**\nOperations resumed successfully.", parse_mode='Markdown')
    except Exception as e:
        await msg.reply_text(f"❌ **Error:** `{e}`")

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "stats":
        await stats(update, context)
    elif query.data == "status":
        await status(update, context)
    elif query.data == "test_email":
        await test_email(update, context)
    elif query.data == "test_strike":
        await test_strike(update, context)
    elif query.data == "kill":
        await kill(update, context)
    elif query.data == "resume":
        await resume(update, context)
    elif query.data == "leads":
        leads = await db.get_pending_leads(limit=10)
        if not leads:
            await query.message.reply_text("📋 No pending leads in queue.")
            return
        msg = "📋 **PENDING LEADS (TOP 10):**\n"
        for i, l in enumerate(leads, 1):
            msg += f"{i}. {l.get('company_name', 'Unknown')} - {l.get('job_title', 'Unknown')}\n"
        await query.message.reply_text(msg, parse_mode='Markdown')

async def main():
    """Start bot"""
    print("🚀 Initializing Sovereign Dashboard...")
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("test_email", test_email))
    app.add_handler(CommandHandler("test_strike", test_strike))
    app.add_handler(CommandHandler("kill", kill))
    app.add_handler(CommandHandler("resume", resume))
    
    # Add callback and message handlers
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Set bot commands in UI
    commands = [
        BotCommand("start", "🚀 Start System"),
        BotCommand("menu", "📱 Main Menu"),
        BotCommand("stats", "📊 Stats"),
        BotCommand("status", "🖥️ Status"),
        BotCommand("test_strike", "🧪 Test Email"),
        BotCommand("kill", "🛑 Kill Switch"),
        BotCommand("resume", "🟢 Resume")
    ]
    
    await app.initialize()
    await app.bot.set_my_commands(commands)
    await app.start()
    
    # Clear webhooks to ensure polling works
    await app.bot.delete_webhook(drop_pending_updates=True)
    
    print("=" * 70)
    print("✅ SOVEREIGN BOT IS ONLINE!")
    print("=" * 70)
    print("Check Telegram to interact.")
    
    await app.updater.start_polling(drop_pending_updates=True)
    
    try:
        # Keep running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping bot...")
        await app.updater.stop()
        await app.stop()
        await app.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"💥 CRITICAL ERROR: {e}")
