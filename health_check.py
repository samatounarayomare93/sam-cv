import os
import sys
import json
import sqlite3
from datetime import datetime

def check_file(path, description):
    exists = os.path.exists(path)
    status = "?" if exists else "?"
    print(f"  {status} {description}: {path}")
    return exists

def check_env_var(name):
    value = os.getenv(name, "")
    status = "? SET" if value else "? MISSING"
    masked = value[:5] + "***" if value and "KEY" in name else value
    print(f"  {status} {name}: {masked}")
    return bool(value)

print("---------------------------------------------------------------")
print("  ?? PROJECT CHRONOS - HEALTH CHECK")
print("---------------------------------------------------------------")

# 1. Check critical files
print("\n?? CRITICAL FILES:")
critical = [
    ("run.py", "Main entry point"),
    ("core/main_bot.py", "Main bot engine"),
    ("core/ai_agent.py", "AI engine"),
    ("core/smtp_engine.py", "Email engine"),
    ("core/db_client.py", "Database client"),
    ("core/telegram_dashboard.py", "Telegram bot"),
    (".env", "Environment variables"),
    ("profile.json", "Profile data"),
    ("Sam_Salameh_CV.html", "CV file"),
    ("requirements.txt", "Dependencies"),
]
all_critical = all(check_file(f, d) for f, d in critical)

# 2. Check environment variables
print("\n?? REQUIRED ENVIRONMENT VARIABLES:")
required = [
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
    "GEMINI_API_KEY",
    "GROQ_API_KEY",
    "SUPABASE_URL",
    "SUPABASE_KEY",
]
all_env = all(check_env_var(v) for v in required)

# 3. Check email providers
print("\n?? EMAIL PROVIDERS (at least one needed):")
email_providers = [
    ("GMAIL_SMTP_USER", "Gmail"),
    ("BREVO_SMTP_LOGIN", "Brevo"),
    ("ZOHO_SMTP_USER", "Zoho"),
    ("RESEND_API_KEY", "Resend"),
    ("YAHOO_SMTP_USER", "Yahoo"),
    ("OUTLOOK_USER", "Outlook"),
]
email_count = sum(1 for e, _ in email_providers if os.getenv(e))
for env, name in email_providers:
    check_env_var(env)
print(f"\n  ?? Total email providers configured: {email_count}")

# 4. Check database
print("\n??? DATABASE:")
try:
    conn = sqlite3.connect("sam_ultimate.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"  ? SQLite database accessible ({len(tables)} tables)")
    conn.close()
except Exception as e:
    print(f"  ?? SQLite: {e}")

# 5. Check logs
print("\n?? LOGS:")
if os.path.exists("logs"):
    log_files = os.listdir("logs")
    print(f"  ? Log directory exists ({len(log_files)} files)")
else:
    print("  ?? Log directory not found")

# 6. Summary
print("\n---------------------------------------------------------------")
if all_critical and all_env and email_count > 0:
    print("  ? ALL SYSTEMS GO - READY TO LAUNCH")
elif all_critical and email_count > 0:
    print("  ?? MOSTLY READY - Some API keys missing (bot will use fallbacks)")
else:
    print("  ? MISSING CRITICAL COMPONENTS - Check errors above")
print("---------------------------------------------------------------")

if __name__ == "__main__":
    pass
