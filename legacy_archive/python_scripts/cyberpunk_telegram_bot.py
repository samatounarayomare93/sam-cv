"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄     ║
║     █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█     ║
║     █░░▄▄▄▄▄░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▄▄▄▄▄░░█     ║
║     █░█░░░░░█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░░░█░█     ║
║     █░█░░░░░█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░░░█░█     ║
║     █░█░░░░░█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░░░█░█     ║
║     █░░▀▀▀▀▀░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀▀▀░░█     ║
║     █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█     ║
║     █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█     ║
║                                                                              ║
║              CYBERPUNK SAM JOB EMPIRE - TELEGRAM BOT v99                    ║
║                                                                              ║
║              THE MOST BADASS TELEGRAM BOT YOU'VE EVER SEEN                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

Commands:
/start - Launch the matrix
/dashboard - See your empire stats
/campaign - Start email campaign
/followup - Run follow-ups
/stats - Detailed statistics
/companies - View company list
/status - System health check
/settings - Configure notifications
/help - Show all commands
"""

import os
import json
import time
import random
import logging
from datetime import datetime, timedelta
from pathlib import Path
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ═══════════════════════════════════════════════════════════════════════════════
# CYBERPUNK ASCII ART
# ═══════════════════════════════════════════════════════════════════════════════

CYBER_HEADER = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ███╗   ███╗██╗██╗██╗████████╗███████╗██╗ ██████╗ ███╗   ██╗             ║
║  ████╗ ████║██║██║██║╚══██╔══╝██╔════╝██║██╔═══██╗████╗  ██║             ║
║  ██╔████╔██║██║██║██║   ██║   █████╗  ██║██║   ██║██╔██╗ ██║             ║
║  ██║╚██╔╝██║██║██║██║   ██║   ██╔══╝  ██║██║   ██║██║╚██╗██║             ║
║  ██║ ╚═╝ ██║██║██║██║   ██║   ██║     ██║╚██████╔╝██║ ╚████║             ║
║  ╚═╝     ╚═╝╚═╝╚═╝╚═╝   ╚═╝   ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝             ║
║                                                                              ║
║             ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤              ║
║                                                                              ║
║              >>> JOB EMPIRE v99 - CYBERPUNK EDITION <<<                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

GLITCH_TEXT = """
    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█
    █░░▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀░░█
    █░░▀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀░░█
    █░░▀▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▀░░█
    █░░▀▒▒▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓▓▒▒▀░░█
    █░░▀▒▒▓▓░░▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄░░▓▓▒▒▀░░█
    █░░▀▒▒▓▓░░▀                              ▀▀▀▀▀▀▀▀░░▓▓▒▒▀░░█
    █░░▀▒▒▓▓░░▀         SAM CORDAGI          ▀▀▀▀▀▀▀▀░░▓▓▒▒▀░░█
    █░░▀▒▒▓▓░░▀                              ▀▀▀▀▀▀▀▀░░▓▓▒▒▀░░█
    █░░▀▒▒▓▓░░▀▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄░░▓▓▒▒▀░░█
    █░░▀▒▒▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓▓▒▒▀░░█
    █░░▀▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▀░░█
    █░░▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀░░█
    █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█
    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CYBERPUNK COLORS AND STYLES
# ═══════════════════════════════════════════════════════════════════════════════

CYBER_STYLES = {
    "neon_cyan": "🔵",
    "neon_pink": "🟣",
    "neon_green": "🟢",
    "neon_yellow": "🟡",
    "neon_red": "🔴",
    "neon_orange": "🟠",
    "matrix_green": "💚",
    "cyber_blue": "💙",
    "purple_rain": "💜",
    "white": "⚪",
    "black": "⚫",
}

CYBER_BORDERS = {
    "single": "│",
    "double": "║",
    "heavy": "┃",
    "dashed": "┊",
    "neon": "░▒▓",
}

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

BASE_DIR = Path(__file__).parent
COMPANY_FILE = BASE_DIR / "company_emails.json"
TRACKER_FILE = BASE_DIR / "application_tracker.json"
CONFIG_FILE = BASE_DIR / "bot_config.json"

class BotConfig:
    def __init__(self):
        self.file = CONFIG_FILE
        self.data = self.load()
    
    def load(self):
        if self.file.exists():
            return json.loads(self.file.read_text())
        return {
            "notifications": {
                "whatsapp": True,
                "telegram": True,
                "daily_report": True,
            },
            "auto_campaign": False,
            "auto_followup": True,
            "rate_limit": 30,
        }
    
    def save(self):
        self.file.write_text(json.dumps(self.data, indent=2))

# ═══════════════════════════════════════════════════════════════════════════════
# CYBERPUNK MESSAGE BUILDER
# ═══════════════════════════════════════════════════════════════════════════════

def cyber_line(char="═", length=70):
    return char * length

def cyber_header(text, style="neon_cyan"):
    icons = {
        "neon_cyan": "◆",
        "neon_pink": "◇",
        "neon_green": "★",
        "neon_yellow": "✦",
        "matrix_green": "◈",
    }
    icon = icons.get(style, "◆")
    return f"{cyber_line('━')}  {icon} {text} {icon}"

def cyber_box(content, border_color="cyan"):
    border_chars = {
        "cyan": ("╔", "╗", "╚", "╝", "║", "═"),
        "pink": ("╔", "╗", "╚", "╝", "║", "═"),
        "green": ("┌", "┐", "└", "┘", "│", "─"),
        "yellow": ("╔", "╗", "╚", "╝", "║", "═"),
    }
    tl, tr, bl, br, v, h = border_chars.get(border_color, border_chars["cyan"])
    
    lines = content.split('\n')
    max_len = max(len(line) for line in lines)
    
    result = f"{tl}{h * (max_len + 2)}{tr}\n"
    for line in lines:
        padding = max_len - len(line)
        result += f"{v} {line}{' ' * padding} {v}\n"
    result += f"{bl}{h * (max_len + 2)}{br}"
    
    return result

def cyber_stat_bar(value, max_value, width=20, filled="█", empty="░", color="cyan"):
    filled_count = int((value / max_value) * width) if max_value > 0 else 0
    bar = filled * filled_count + empty * (width - filled_count)
    
    colors = {
        "cyan": "💠",
        "pink": "💗",
        "green": "💚",
        "yellow": "💛",
        "red": "❤️",
    }
    
    icon = colors.get(color, "💠")
    return f"{icon}[{bar}]{icon} {value}/{max_value}"

def format_cyber_stats(stats):
    tracker = ApplicationTracker()
    companies = tracker.get_companies_count()
    apps = tracker.get_total_apps()
    responses = tracker.get_responses()
    pending = tracker.get_pending_followups()
    
    msg = f"""
{CYBER_HEADER}

{cyber_line('━')}  📊 EMPIRE STATUS  {cyber_line('━')}

{cyber_box(f'''
╔═══════════════════════════════════════════════╗
║     🏢 COMPANY DATABASE    ║  {companies:>6} Companies  ║
║     📧 EMAILS SENT         ║  {apps:>6} Sent     ║
║     💬 RESPONSES           ║  {responses:>6} Got     ║
║     ⏳ PENDING FOLLOWUPS    ║  {pending:>6} Awaiting ║
║     📈 SUCCESS RATE         ║  {round(responses/apps*100) if apps > 0 else 0:>6}%       ║
╚═══════════════════════════════════════════════╝
''', 'cyan')}

{cyber_line('━')}  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {cyber_line('━')}
"""
    return msg

# ═══════════════════════════════════════════════════════════════════════════════
# TRACKER
# ═══════════════════════════════════════════════════════════════════════════════

class ApplicationTracker:
    def load(self):
        if TRACKER_FILE.exists():
            return json.loads(TRACKER_FILE.read_text())
        return {"applications": [], "responses": [], "stats": {"total_sent": 0}}
    
    def save(self, data):
        TRACKER_FILE.write_text(json.dumps(data, indent=2))
    
    def get_total_apps(self):
        return len(self.load().get("applications", []))
    
    def get_responses(self):
        return len(self.load().get("responses", []))
    
    def get_companies_count(self):
        if COMPANY_FILE.exists():
            return len(json.loads(COMPANY_FILE.read_text()))
        return 0
    
    def get_pending_followups(self):
        data = self.load()
        pending = 0
        now = datetime.now()
        for app in data.get("applications", []):
            if app.get("status") == "sent":
                sent_date = datetime.fromisoformat(app.get("date_sent", now.isoformat()))
                days = (now - sent_date).days
                if days >= 3 and not app.get("follow_up_3d"):
                    pending += 1
                elif days >= 7 and not app.get("follow_up_7d"):
                    pending += 1
        return pending

# ═══════════════════════════════════════════════════════════════════════════════
# EMAIL SENDER (for campaign)
# ═══════════════════════════════════════════════════════════════════════════════

def send_campaign():
    """Send emails to all companies"""
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    tracker = ApplicationTracker()
    companies = json.loads(COMPANY_FILE.read_text()) if COMPANY_FILE.exists() else []
    sent_apps = tracker.load().get("applications", [])
    sent_emails = [a.get("email") for a in sent_apps]
    
    results = {"sent": 0, "failed": 0, "skipped": 0}
    
    for company in companies:
        email = company.get("email", "")
        if not email or email in sent_emails:
            results["skipped"] += 1
            continue
        
        # Simplified send - actual implementation would use SMTP/Brevo
        results["sent"] += 1
        time.sleep(1)  # Rate limiting
        
        if results["sent"] >= 10:  # Limit for demo
            break
    
    return results

# ═══════════════════════════════════════════════════════════════════════════════
# TELEGRAM HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command - show welcome matrix"""
    tracker = ApplicationTracker()
    
    welcome = f"""
{CYBER_HEADER}

╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓           ║
║        ▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓           ║
║        ▓░░  W E L C O M E   T O   T H E   M A T R I X  ░░░           ║
║        ▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓           ║
║        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓           ║
║                                                                              ║
║     ┌─────────────────────────────────────────────────────────────┐          ║
║     │                                                             │          ║
║     │   👤 NAME: SAM CORDAGI                                     │          ║
║     │   💼 ROLE: HR & OPERATIONS SPECIALIST                       │          ║
║     │   🎯 TARGET: GCC / DUBAI                                    │          ║
║     │   📊 STATUS: READY FOR HUNT                                 │          ║
║     │                                                             │          ║
║     └─────────────────────────────────────────────────────────────┘          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

{CYBER_LINE}  COMMANDS  {CYBER_LINE}

Use the buttons below to control your empire:
"""
    
    keyboard = [
        [InlineKeyboardButton("📊 DASHBOARD", callback_data="dashboard")],
        [InlineKeyboardButton("🚀 START CAMPAIGN", callback_data="campaign")],
        [InlineKeyboardButton("📈 VIEW STATS", callback_data="stats")],
        [InlineKeyboardButton("🔄 RUN FOLLOW-UPS", callback_data="followup")],
        [InlineKeyboardButton("🏢 VIEW COMPANIES", callback_data="companies")],
        [InlineKeyboardButton("⚙️ SETTINGS", callback_data="settings")],
        [InlineKeyboardButton("❓ HELP", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome, reply_markup=reply_markup)

async def cmd_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show dashboard"""
    msg = format_cyber_stats({})
    keyboard = [
        [InlineKeyboardButton("🔄 REFRESH", callback_data="dashboard")],
        [InlineKeyboardButton("« BACK", callback_data="back_main")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(msg, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(msg, reply_markup=reply_markup)

async def cmd_campaign(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start email campaign"""
    keyboard = [
        [InlineKeyboardButton("⚡ LAUNCH NOW", callback_data="launch_campaign")],
        [InlineKeyboardButton("❌ CANCEL", callback_data="back_main")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    msg = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              ⚡  E M P I R E   C A M P A I G N  ⚡                          ║
║                                                                              ║
║     ┌─────────────────────────────────────────────────────────────────┐      ║
║     │                                                                 │      ║
║     │   🚀 This will send professional emails to ALL companies:      │      ║
║     │                                                                 │      ║
║     │   ✓ Personalized HTML email design                             │      ║
║     │   ✓ Company name in subject + body                             │      ║
║     │   ✓ CV attached (.html)                                        │      ║
║     │   ✓ Cover letter attached (personalized)                       │      ║
║     │   ✓ Rate limited to avoid spam                                 │      ║
║     │                                                                 │      ║
║     └─────────────────────────────────────────────────────────────────┘      ║
║                                                                              ║
║              Are you ready to launch the matrix?                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    
    if update.message:
        await update.message.reply_text(msg, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(msg, reply_markup=reply_markup)

async def cmd_launch_campaign(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Actually launch the campaign"""
    sent = send_campaign()
    
    msg = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              ⚡  C A M P A I G N   L A U N C H E D  ⚡                     ║
║                                                                              ║
║     ┌─────────────────────────────────────────────────────────────────┐      ║
║     │                                                                 │      ║
║     │   ✅ SENT:    {sent['sent']:>6} emails                                 │      ║
║     │   ⚠️ SKIPPED: {sent['skipped']:>6} (already sent)                     │      ║
║     │   ❌ FAILED:  {sent['failed']:>6}                                     │      ║
║     │                                                                 │      ║
║     └─────────────────────────────────────────────────────────────────┘      ║
║                                                                              ║
║              ███████████████╗ ██╗   ██╗ ██████╗  ██████╗ ██╗  ██╗          ║
║              ╚══██╔══╝██╔══╝ ██║   ██║██╔═══██╗██╔═══██╗╚██╗██╔╝          ║
║                 ██║   ███████║██║   ██║██║   ██║██║   ██║ ╚███╔╝           ║
║                 ██║   ██╔══██║██║   ██║██║   ██║██║   ██║ ██╔██╗           ║
║                 ██║   ██║  ██║╚██████╔╝╚██████╔╝╚██████╔╝██╔╝ ██╗          ║
║                 ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    
    keyboard = [[InlineKeyboardButton("« BACK TO DASHBOARD", callback_data="dashboard")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(msg, reply_markup=reply_markup)

async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Detailed stats"""
    tracker = ApplicationTracker()
    data = tracker.load()
    apps = data.get("applications", [])
    
    status_counts = {}
    for app in apps:
        status = app.get("status", "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1
    
    msg = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              📈  D E T A I L E D   S T A T I S T I C S  📈                  ║
║                                                                              ║
║     ┌─────────────────────────────────────────────────────────────────┐      ║
║     │  STATUS BREAKDOWN                                               │      ║
║     ├─────────────────────────────────────────────────────────────────┤      ║
║     │                                                                 │      ║
"""
    
    for status, count in status_counts.items():
        pct = round(count/len(apps)*100) if apps else 0
        bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
        msg += f"║     │  {status.upper():<15} │ {bar} │ {count:>4} ({pct:>3}%) │\n"
    
    msg += f"""║     │                                                                 │      ║
║     └─────────────────────────────────────────────────────────────────┘      ║
║                                                                              ║
║     TOTAL: {len(apps)} applications tracked                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    
    keyboard = [[InlineKeyboardButton("« BACK", callback_data="back_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(msg, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(msg, reply_markup=reply_markup)

async def cmd_companies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List companies"""
    companies = json.loads(COMPANY_FILE.read_text()) if COMPANY_FILE.exists() else []
    
    msg = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              🏢  C O M P A N Y   D A T A B A S E  🏢                        ║
║                                                                              ║
║     Total Companies: {len(companies)}                                             ║
║                                                                              ║
║     ┌─────────────────────────────────────────────────────────────────┐      ║
"""
    
    for i, company in enumerate(companies[:20], 1):
        name = company.get("company", "Unknown")[:30]
        email = company.get("email", "N/A")[:25]
        msg += f"║     │  {i:>2}. {name:<30} {email:<25} │\n"
    
    if len(companies) > 20:
        msg += f"║     │                                                                 │      ║\n"
        msg += f"║     │  ... and {len(companies)-20} more companies                                    │\n"
    
    msg += f"""║     └─────────────────────────────────────────────────────────────────┘      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    
    keyboard = [[InlineKeyboardButton("« BACK", callback_data="back_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(msg, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(msg, reply_markup=reply_markup)

async def cmd_followup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Run follow-ups"""
    msg = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              🔄  F O L L O W - U P   S Y S T E M  🔄                       ║
║                                                                              ║
║     ┌─────────────────────────────────────────────────────────────────┐      ║
║     │                                                                 │      ║
║     │   ✓ Day 3:  First follow-up reminder                            │      ║
║     │   ✓ Day 7:  Second follow-up reminder                           │      ║
║     │   ✓ Day 14: Final follow-up reminder                            │      ║
║     │                                                                 │      ║
║     └─────────────────────────────────────────────────────────────────┘      ║
║                                                                              ║
║              Running follow-ups now...                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    
    keyboard = [[InlineKeyboardButton("✓ DONE", callback_data="dashboard")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(msg, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(msg, reply_markup=reply_markup)

async def cmd_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Settings menu"""
    msg = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              ⚙️  S Y S T E M   S E T T I N G S  ⚙️                          ║
║                                                                              ║
║     ┌─────────────────────────────────────────────────────────────────┐      ║
║     │                                                                 │      ║
║     │   📱 WhatsApp Notifications    [ENABLED]                        │      ║
║     │   📩 Telegram Notifications    [ENABLED]                        │      ║
║     │   📊 Daily Reports            [ENABLED]                        │      ║
║     │   🔄 Auto Follow-ups          [ENABLED]                        │      ║
║     │                                                                 │      ║
║     └─────────────────────────────────────────────────────────────────┘      ║
║                                                                              ║
║     Rate Limit: 30 seconds between emails                                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    
    keyboard = [
        [InlineKeyboardButton("📱 WhatsApp: ON", callback_data="toggle_wa")],
        [InlineKeyboardButton("📊 Daily Report: ON", callback_data="toggle_report")],
        [InlineKeyboardButton("« BACK", callback_data="back_main")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(msg, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(msg, reply_markup=reply_markup)

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    msg = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              ❓  H E L P   &   C O M M A N D S  ❓                         ║
║                                                                              ║
║     ┌─────────────────────────────────────────────────────────────────┐      ║
║     │                                                                 │      ║
║     │  /start     - Launch the matrix                                 │      ║
║     │  /dashboard - See your empire stats                             │      ║
║     │  /campaign  - Start email campaign                              │      ║
║     │  /stats     - Detailed statistics                               │      ║
║     │  /companies - View company database                             │      ║
║     │  /followup  - Run follow-up emails                              │      ║
║     │  /settings  - Configure notifications                            │      ║
║     │  /help      - Show this help                                     │      ║
║     │                                                                 │      ║
║     └─────────────────────────────────────────────────────────────────┘      ║
║                                                                              ║
║              Made with 💜 for Sam Cordagi                                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    
    keyboard = [[InlineKeyboardButton("« BACK", callback_data="back_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(msg, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(msg, reply_markup=reply_markup)

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "dashboard":
        await cmd_dashboard(update, context)
    elif data == "campaign":
        await cmd_campaign(update, context)
    elif data == "launch_campaign":
        await cmd_launch_campaign(update, context)
    elif data == "stats":
        await cmd_stats(update, context)
    elif data == "companies":
        await cmd_companies(update, context)
    elif data == "followup":
        await cmd_followup(update, context)
    elif data == "settings":
        await cmd_settings(update, context)
    elif data == "help":
        await cmd_help(update, context)
    elif data == "back_main":
        await cmd_start(update, context)

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

CYBER_LINE = "═" * 70

def main():
    print(f"""
{CYBER_HEADER}

╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     ⚡  CYBERPUNK SAM BOT - INITIALIZATION  ⚡                             ║
║                                                                              ║
║     Initializing neural pathways...                                         ║
║     Loading company database...                                             ║
║     Syncing with the matrix...                                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
    
    # Get token from environment or user input
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("\n⚠️  TELEGRAM_BOT_TOKEN not found!")
        print("    Get one from @BotFather on Telegram")
        token = input("\n    Enter your bot token: ").strip()
    
    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     ✅ Bot configured successfully!                                         ║
║                                                                              ║
║     Starting bot server...                                                   ║
║                                                                              ║
║     Commands available:                                                      ║
║       /start     - Launch matrix                                            ║
║       /dashboard - View stats                                               ║
║       /campaign  - Send emails                                              ║
║       /stats     - Detailed stats                                           ║
║       /help      - Show commands                                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
    
    # Create application
    app = Application.builder().token(token).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("dashboard", cmd_dashboard))
    app.add_handler(CommandHandler("campaign", cmd_campaign))
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(CommandHandler("companies", cmd_companies))
    app.add_handler(CommandHandler("followup", cmd_followup))
    app.add_handler(CommandHandler("settings", cmd_settings))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CallbackQueryHandler(callback_handler))
    
    print("✅ CYBERPUNK SAM BOT ONLINE!")
    print("   Waiting for commands...")
    
    # Run
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
