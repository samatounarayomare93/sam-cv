import os
import re
import time
import subprocess
import logging
import requests
from typing import Optional
from google import genai
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [PROTOCOL GENESIS] - %(message)s")

# ZERO-COST REQUIREMENT: Uses Gemini Free Tier
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None
# Model for 2.0-flash-exp (or whichever is current)
MODEL_ID = 'gemini-2.0-flash-exp'

LOG_PATHS = ["logs/engine.log", "logs/dashboard.log", "logs/out.txt"]
TARGET_APP_SCRIPT = "run.py"

def find_latest_traceback(log_path: str) -> Optional[str]:
    """Scans the end of a log file for Python Tracebacks."""
    if not os.path.exists(log_path):
        return None
        
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Scan bottom 100 lines for Traceback
        traceback_str = ""
        in_traceback = False
        
        for line in lines[-100:]:
            if "Traceback (most recent call last)" in line:
                in_traceback = True
                traceback_str = line
            elif in_traceback:
                traceback_str += line
                if not line.startswith(" ") and traceback_str.count("\n") > 2:
                    break 
                    
        return traceback_str if in_traceback else None
    except Exception as e:
        logging.error(f"Error reading log: {e}")
        return None

def extract_file_and_line(traceback_str: str):
    """Extracts the exact Python file and line number that crashed."""
    match = re.search(r'File "([^"]+\.py)", line (\d+)', traceback_str)
    if match:
        return match.group(1), int(match.group(2))
    return None, None

def get_failed_function_source(filepath: str, line_num: int):
    """Pulls the 50 lines around the crashing line."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        start = max(0, line_num - 25)
        end = min(len(lines), line_num + 25)
        
        return "".join(lines[start:end]), lines
    except Exception as e:
        logging.error(f"Error reading source file: {e}")
        return None, None

def rewrite_code_with_llm(traceback_str: str, source_code: str) -> Optional[str]:
    """Asks Gemini to fix the specific function based on the traceback."""
    logging.info("🧠 Submitting traceback to God-Tier Intelligence for rewriting...")
    
    prompt = f"""
    You are an elite Python Architect tasked with self-healing a live server.
    
    The system crashed with this Traceback:
    ```
    {traceback_str}
    ```
    
    Here is the source code around the crash:
    ```python
    {source_code}
    ```
    
    OUTPUT INSTRUCTIONS:
    1. Fix the bug in the code.
    2. Respond with ONLY the fully corrected code snippet. No markdown, just raw code.
    3. Ensure indentation is perfectly preserved.
    """
    
    try:
        if not client:
            logging.error("No GEMINI_API_KEY provided. Cannot rewrite code.")
            return None
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )
        text = response.text.replace('```python', '').replace('```', '').strip()
        return text
    except Exception as e:
        logging.error(f"LLM Fix Generation Error: {e}")
        return None

def notify_user(message: str):
    """Sends a notification to the Sovereign Leader via Telegram."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, data={
            "chat_id": chat_id,
            "text": f"🧬 <b>PROTOCOL GENESIS:</b>\n{message}",
            "parse_mode": "HTML"
        })
    except Exception as e:
        logging.error(f"Notification Error: {e}")

def stage_patch(filepath: str, original_snippet: str, new_snippet: str):
    """Stages the LLM patch for the Sovereign to review."""
    os.makedirs("staged_patches", exist_ok=True)
    patch_id = int(time.time())
    patch_file = f"staged_patches/fix_{patch_id}.py"
    
    try:
        with open(patch_file, 'w', encoding='utf-8') as pf:
            pf.write(f"# SOURCE: {filepath}\n")
            pf.write(f"# --- PROPOSED PATCH ---\n")
            pf.write(new_snippet)
            
        logging.info(f"✅ Neural Patch Staged: {patch_file}. Review via /repair in Telegram.")
        
        # Optional: Auto-Update database task
        try:
            from core.db_client import RealityShapingDB
            db = RealityShapingDB()
            import asyncio
            asyncio.run(db.save_task({
                "type": "GENESIS_PATCH",
                "target": filepath,
                "message": f"Neural patch staged at {patch_file}. Click /repair to initiate application."
            }))
        except: pass
        
        notify_user(f"Critical failure detected in <code>{os.path.basename(filepath)}</code>. Neural patch staged and ready for verification.")
        
    except Exception as e:
        logging.error(f"Failed to stage patch: {e}")

def run_genesis_loop():
    """Main Event Loop for Autonomous self-improvement."""
    logging.info("🧬 Protocol Genesis Active: Monitoring core logs for failures...")
    while True:
        for log in LOG_PATHS:
            tb = find_latest_traceback(log)
            if tb:
                logging.error(f"💥 Critical Failure Detected in {log}!")
                file_path, line_num = extract_file_and_line(tb)
                
                if file_path and os.path.exists(file_path):
                    logging.info(f"Targeting root cause: {file_path} @ Line {line_num}")
                    source_snippet, all_lines = get_failed_function_source(file_path, line_num)
                    
                    if source_snippet:
                        fixed_code = rewrite_code_with_llm(tb, source_snippet)
                        if fixed_code:
                            stage_patch(file_path, source_snippet, fixed_code)
                            # Clear the log so we don't fix it twice
                            open(log, 'w').close()
                            time.sleep(30) 
        time.sleep(10)

if __name__ == "__main__":
    run_genesis_loop()
