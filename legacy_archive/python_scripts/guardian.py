import logging
import time
import os
from datetime import datetime
import telebot # Needs: pip install pyTelegramBotAPI
import database
import config
from dotenv import load_dotenv

# ==========================================
# 🛰️ PROJECT CHRONOS // GUARDIAN LISTENER
# ==========================================
# This script is designed to run 24/7 on a free cloud host (Koyeb, Railway, etc.)
# It provides millisecond response times to the Master's status requests.
# ==========================================

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

# Initialize Telegram Guardian
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MASTER_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TOKEN or not MASTER_ID:
    logging.critical("❌ GUARDIAN OFFLINE: Secrets missing (TELEGRAM_BOT_TOKEN/CHAT_ID).")
    exit(1)

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def get_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(KeyboardButton("📊 Live Status"), KeyboardButton("🧠 Interview Prep"))
    markup.row(KeyboardButton("📚 System Help"), KeyboardButton("🛑 Emergency Stop"))
    markup.row(KeyboardButton("🟢 Resume Engine"))
    markup.row(KeyboardButton("💓 Check Pulse"))
    return markup

@bot.message_handler(func=lambda message: str(message.chat.id) == str(MASTER_ID))
def handle_master_commands(message):
    text = message.text
    
    if text == "💓 Check Pulse":
        logging.info("💓 Pulse Request Received.")
        # Get the Pulse
        mins, time_str = database.get_last_heartbeat()
        
        # Check infrastructure
        healthy, msg, _ = database.verify_infrastructure()
        
        status_icon = "🟢" if mins < 45 else "🔴"
        status_text = "SYSTEM ONLINE" if mins < 45 else "SYSTEM OFFLINE"
        health_icon = "✅" if healthy else "⚠️"
        
        current_time = datetime.now().strftime("%I:%M %p")
        
        response = (
            f"{status_icon} <b>{status_text}</b>\n\n"
            f"📅 <b>Local Time:</b> {current_time}\n"
            f"💓 <b>Last Pulse:</b> {time_str} ({mins} mins ago)\n"
            f"{health_icon} <b>Health:</b> {msg}\n"
            f"📝 <i>Ready for commands, Master.</i>"
        )
        bot.reply_to(message, response, parse_mode='HTML', reply_markup=get_keyboard())

    elif text == "📊 Live Status":
        stats = database.get_global_stats()
        bot.reply_to(message, 
            f"📊 <b>CURRENT DB INTELLIGENCE</b>\n\n"
            f"📍 Leads: {stats['leads']}\n"
            f"🎯 Apps: {stats['applications']}\n"
            f"🚀 Sync: ACTIVE",
            reply_markup=get_keyboard()
        )

if __name__ == "__main__":
    logging.info("🚀 Project Chronos Guardian is now Watching... (24/7 Mode)")
    while True:
        try:
            bot.polling(non_stop=True, timeout=60)
        except Exception as e:
            logging.error(f"⚠️ Guardian Connection Flap: {e}")
            time.sleep(10)
