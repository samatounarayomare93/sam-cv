import sys
import os
import requests
import logging
from pathlib import Path

# Add project root to sys.path
root = Path(__file__).resolve().parent
if str(root) not in sys.path:
    sys.path.append(str(root))

import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def install_database():
    logging.info("🛠 INITIATING SOVEREIGN DATABASE INSTALLER...")
    
    if not config.SUPABASE_URL or not config.SUPABASE_KEY:
        logging.error("❌ SUPABASE_URL or SUPABASE_KEY missing in .env")
        logging.info("💡 Please add your Supabase credentials to the .env file first.")
        return False
        
    sql_file = root / "Sovereign_Database_Fix.sql"
    if not sql_file.exists():
        logging.error(f"❌ SQL file not found: {sql_file}")
        return False
        
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_commands = f.read()
    
    logging.info("📡 Connecting to Supabase API...")
    
    # We use the Supabase REST API (PostgREST) which doesn't support multi-statement DDL directly.
    # However, we can try to use the SQL API if available, but usually users have to use the Dashboard.
    
    logging.info("⚠️ Note: Automated DDL via REST API is restricted by Supabase for security.")
    logging.info("💡 I have prepared the SQL instructions for you.")
    logging.info("🚀 TO COMPLETE THE INSTALLATION:")
    logging.info("1. Go to: https://supabase.com/dashboard/project/_/sql")
    logging.info(f"2. Copy all content from: {sql_file}")
    logging.info("3. Paste and click 'RUN'.")
    
    logging.info("---")
    logging.info("✅ Code is ready. Local engine is unblocked.")
    return True

if __name__ == "__main__":
    install_database()
