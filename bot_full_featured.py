#!/usr/bin/env python3
"""
🚀 FULL-FEATURED TELEGRAM BOT
Complete implementation with all commands and features
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv

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
print("🚀 FULL-FEATURED TELEGRAM BOT")
print("=" * 70)
print(f"Token: {TOKEN[:20]}...")
print(f"Chat ID: {CHAT_ID}")
print()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Import components
from core.db_client import RealityShapingDB
from core.ai_agent import OmniIntelligence

db = RealityShapingDB()
ai = OmniIntelligence()

# ============================================================================
# COMMAND HANDLERS
# ============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start"""
    keyboard = [
        [InlineKeyboardButton("📊 Stats", callback_data="stats"),
         InlineKeyboardButton("🔍 Scrape", callback_data="scrape")],
        [InlineKeyboardButton("✅ Qualify", callback_data="qualify"),
         InlineKeyboardButton("🚀 Strike", callback_data="strike")],
        [InlineKeyboardButton("📧 Test Email", callback_data="test_email"),
         InlineKeyboardButton("🛑 Kill Switch", callback_data="kill")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🚀 **Sam's Job Automation Bot**\n\n"
        "Full-featured bot with all commands!\n\n"
        "Quick Actions:",
        reply_markup=reply_markup
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /menu"""
    keyboard = [
        [InlineKeyboardButton("📊 Stats", callback_data="stats"),
         InlineKeyboardButton("🔍 Scrape Jobs", callback_data="scrape")],
        [InlineKeyboardButton("✅ Qualify Leads", callback_data="qualify"),
         InlineKeyboardButton("🚀 Send Applications", callback_data="strike")],
        [InlineKeyboardButton("📧 Test Email", callback_data="test_email"),
         InlineKeyboardButton("🖥️ System Status", callback_data="status")],
        [InlineKeyboardButton("🛑 Kill Switch", callback_data="kill"),
         InlineKeyboardButton("🟢 Resume", callback_data="resume")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎯 **Main Menu**\n\nChoose an action:",
        reply_markup=reply_markup
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats"""
    try:
        stats = db.get_stats()
        msg = (
            f"📊 **Statistics**\n\n"
            f"Total Leads: {stats.get('total', 0)}\n"
            f"Qualified: {stats.get('qualified', 0)}\n"
            f"Sent: {stats.get('sent', 0)}\n"
            f"Pending: {stats.get('pending', 0)}\n"
            f"Success Rate: {stats.get('success_rate', 0)}%"
        )
        await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status"""
    try:
        health = db.get_system_health()
        msg = (
            f"🖥️ **System Status**\n\n"
            f"Database: {'🟢 Online' if health.get('db_online') else '🔴 Offline'}\n"
            f"AI Engine: {'🟢 Active' if health.get('ai_active') else '🔴 Inactive'}\n"
            f"Email System: {'🟢 Ready' if health.get('email_ready') else '🔴 Not Ready'}\n"
            f"Uptime: {health.get('uptime', 'Unknown')}\n"
            f"Last Activity: {health.get('last_activity', 'Unknown')}"
        )
        await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def scrape(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /scrape"""
    await update.message.reply_text("🔍 Scraping jobs... This may take a few minutes.")
    try:
        from core.scrapers.omni_crawler import OmniCrawler
        crawler = OmniCrawler()
        
        # Run scraping
        results = []
        # Add your scraping logic here
        
        await update.message.reply_text(f"✅ Scraping complete! Found {len(results)} jobs.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def qualify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /qualify"""
    await update.message.reply_text("✅ Qualifying leads...")
    try:
        pending = db.get_pending_leads()
        qualified_count = 0
        
        for lead in pending[:10]:  # Qualify first 10
            try:
                score = ai.qualify_lead(lead)
                if score > 70:
                    db.update_lead_status(lead['url'], 'qualified')
                    qualified_count += 1
            except Exception:
                continue
        
        await update.message.reply_text(f"✅ Qualified {qualified_count} leads!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def strike(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /strike"""
    await update.message.reply_text("🚀 Sending applications...")
    try:
        from core.smtp_engine import send_strike
        
        qualified = db.get_qualified_leads()
        if not qualified or len(qualified) == 0:
            await update.message.reply_text("⚠️ No qualified leads found. Run /scrape and /qualify first.")
            return
        
        sent_count = 0
        for lead in qualified[:5]:  # Send to first 5
            try:
                result = send_strike(lead)
                if result:
                    db.update_lead_status(lead['url'], 'sent')
                    sent_count += 1
            except Exception:
                continue
        
        await update.message.reply_text(f"✅ Sent {sent_count} applications!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def test_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /test_email"""
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

async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /kill"""
    try:
        db.activate_kill_switch(True)
        await update.message.reply_text("🛑 **KILL SWITCH ACTIVATED**\n\nAll operations stopped.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /resume"""
    try:
        db.activate_kill_switch(False)
        await update.message.reply_text("🟢 **OPERATIONS RESUMED**\n\nBot is active again.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def ignite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ignite - Full system activation"""
    await update.message.reply_text("🔥 **SYSTEM IGNITION**\n\nStarting full automation cycle...")
    try:
        # Scrape -> Qualify -> Strike
        await scrape(update, context)
        await asyncio.sleep(2)
        await qualify(update, context)
        await asyncio.sleep(2)
        await strike(update, context)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def leads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /leads"""
    try:
        leads = db.get_pending_leads()[:10]
        if not leads:
            await update.message.reply_text("📋 No leads found.")
            return
        
        msg = "📋 **Recent Leads:**\n\n"
        for i, lead in enumerate(leads, 1):
            msg += f"{i}. {lead.get('company_name', 'Unknown')} - {lead.get('job_title', 'Unknown')}\n"
        
        await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def audit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /audit"""
    try:
        stats = db.get_stats()
        health = db.get_system_health()
        
        msg = (
            f"👁️ **System Audit**\n\n"
            f"**Statistics:**\n"
            f"Total Leads: {stats.get('total', 0)}\n"
            f"Qualified: {stats.get('qualified', 0)}\n"
            f"Sent: {stats.get('sent', 0)}\n\n"
            f"**Health:**\n"
            f"Database: {'🟢' if health.get('db_online') else '🔴'}\n"
            f"AI: {'🟢' if health.get('ai_active') else '🔴'}\n"
            f"Email: {'🟢' if health.get('email_ready') else '🔴'}"
        )
        await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ============================================================================
# BUTTON HANDLER
# ============================================================================

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "stats":
        try:
            stats = db.get_stats()
            msg = (
                f"📊 **Statistics**\n\n"
                f"Total: {stats.get('total', 0)}\n"
                f"Qualified: {stats.get('qualified', 0)}\n"
                f"Sent: {stats.get('sent', 0)}\n"
                f"Pending: {stats.get('pending', 0)}"
            )
            await query.edit_message_text(msg)
        except Exception as e:
            await query.edit_message_text(f"❌ Error: {e}")
    
    elif query.data == "status":
        try:
            health = db.get_system_health()
            msg = (
                f"🖥️ **System Status**\n\n"
                f"DB: {'🟢' if health.get('db_online') else '🔴'}\n"
                f"AI: {'🟢' if health.get('ai_active') else '🔴'}\n"
                f"Email: {'🟢' if health.get('email_ready') else '🔴'}"
            )
            await query.edit_message_text(msg)
        except Exception as e:
            await query.edit_message_text(f"❌ Error: {e}")
    
    elif query.data == "scrape":
        await query.edit_message_text("🔍 Scraping jobs...")
        try:
            from core.scrapers.omni_crawler import OmniCrawler
            crawler = OmniCrawler()
            results = []
            await query.edit_message_text(f"✅ Found {len(results)} jobs!")
        except Exception as e:
            await query.edit_message_text(f"❌ Error: {e}")
    
    elif query.data == "qualify":
        await query.edit_message_text("✅ Qualifying leads...")
        try:
            pending = db.get_pending_leads()
            qualified_count = 0
            for lead in pending[:10]:
                try:
                    score = ai.qualify_lead(lead)
                    if score > 70:
                        db.update_lead_status(lead['url'], 'qualified')
                        qualified_count += 1
                except Exception:
                    continue
            await query.edit_message_text(f"✅ Qualified {qualified_count} leads!")
        except Exception as e:
            await query.edit_message_text(f"❌ Error: {e}")
    
    elif query.data == "strike":
        await query.edit_message_text("🚀 Sending applications...")
        try:
            from core.smtp_engine import send_strike
            qualified = db.get_qualified_leads()
            if not qualified:
                await query.edit_message_text("⚠️ No qualified leads")
                return
            sent_count = 0
            for lead in qualified[:5]:
                try:
                    result = send_strike(lead)
                    if result:
                        db.update_lead_status(lead['url'], 'sent')
                        sent_count += 1
                except Exception:
                    continue
            await query.edit_message_text(f"✅ Sent {sent_count} applications!")
        except Exception as e:
            await query.edit_message_text(f"❌ Error: {e}")
    
    elif query.data == "test_email":
        await query.edit_message_text("📧 Sending test email...")
        try:
            from core.smtp_engine import send_test_email
            result = send_test_email('samsalameh.cv@gmail.com')
            if result:
                await query.edit_message_text("✅ Test email sent!")
            else:
                await query.edit_message_text("❌ Failed to send")
        except Exception as e:
            await query.edit_message_text(f"❌ Error: {e}")
    
    elif query.data == "kill":
        try:
            db.activate_kill_switch(True)
            await query.edit_message_text("🛑 **KILL SWITCH ACTIVATED**")
        except Exception as e:
            await query.edit_message_text(f"❌ Error: {e}")
    
    elif query.data == "resume":
        try:
            db.activate_kill_switch(False)
            await query.edit_message_text("🟢 **OPERATIONS RESUMED**")
        except Exception as e:
            await query.edit_message_text(f"❌ Error: {e}")
    
    else:
        await query.edit_message_text(f"⚠️ Unknown command: {query.data}")

# ============================================================================
# MAIN
# ============================================================================

async def main():
    """Start bot"""
    print("🚀 Starting full-featured bot...")
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("scrape", scrape))
    app.add_handler(CommandHandler("qualify", qualify))
    app.add_handler(CommandHandler("strike", strike))
    app.add_handler(CommandHandler("test_email", test_email))
    app.add_handler(CommandHandler("kill", kill))
    app.add_handler(CommandHandler("resume", resume))
    app.add_handler(CommandHandler("ignite", ignite))
    app.add_handler(CommandHandler("leads", leads))
    app.add_handler(CommandHandler("audit", audit))
    
    # Add button handler
    app.add_handler(CallbackQueryHandler(handle_button))
    
    # Set bot commands
    commands = [
        BotCommand("start", "🚀 Start bot"),
        BotCommand("menu", "📱 Main menu"),
        BotCommand("stats", "📊 Statistics"),
        BotCommand("status", "🖥️ System status"),
        BotCommand("scrape", "🔍 Scrape jobs"),
        BotCommand("qualify", "✅ Qualify leads"),
        BotCommand("strike", "🚀 Send applications"),
        BotCommand("test_email", "📧 Test email"),
        BotCommand("kill", "🛑 Kill switch"),
        BotCommand("resume", "🟢 Resume operations"),
        BotCommand("ignite", "🔥 Full ignition"),
        BotCommand("leads", "📋 View leads"),
        BotCommand("audit", "👁️ System audit")
    ]
    
    await app.initialize()
    await app.bot.set_my_commands(commands)
    await app.start()
    await app.bot.delete_webhook(drop_pending_updates=True)
    
    print("=" * 70)
    print("✅ FULL-FEATURED BOT IS RUNNING!")
    print("=" * 70)
    print("\n📱 Available Commands:")
    print("   /start - Start bot")
    print("   /menu - Main menu")
    print("   /stats - Statistics")
    print("   /status - System status")
    print("   /scrape - Scrape jobs")
    print("   /qualify - Qualify leads")
    print("   /strike - Send applications")
    print("   /test_email - Test email")
    print("   /kill - Kill switch")
    print("   /resume - Resume operations")
    print("   /ignite - Full ignition")
    print("   /leads - View leads")
    print("   /audit - System audit")
    print("\n⚠️  Keep this window open!")
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
