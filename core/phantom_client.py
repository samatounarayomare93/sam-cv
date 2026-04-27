import os
import logging
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from dotenv import load_dotenv

load_dotenv()

class PhantomClient:
    """Advanced UserBot client for Phantom Outreach and Ghost Networking."""
    
    def __init__(self, api_id=None, api_hash=None, session_string=None):
        self.api_id = api_id or os.getenv("TELEGRAM_API_ID")
        self.api_hash = api_hash or os.getenv("TELEGRAM_API_HASH")
        self.session_string = session_string or os.getenv("TELEGRAM_SESSION_STRING")
        self.client = None
        
        if not self.api_id or not self.api_hash:
            logging.warning("⚠️ PHANTOM CLIENT: Missing API ID/Hash. Outreach disabled.")

    async def start(self):
        """Initializes the client using a session string or existing file."""
        if not self.api_id or not self.api_hash:
            return False
            
        try:
            # Use StringSession for cloud-native persistence (Render-friendly)
            self.client = TelegramClient(
                StringSession(self.session_string) if self.session_string else 'phantom_ghost', 
                self.api_id, 
                self.api_hash
            )
            await self.client.connect()
            return True
        except Exception as e:
            logging.error(f"❌ PHANTOM CLIENT FAIL: {e}")
            return False

    async def get_session_string(self):
        """Returns the exported session string for persistence."""
        if self.client and self.client.is_connected():
            return self.client.session.save()
        return None

    async def send_ghost_message(self, target_username, message):
        """Sends a high-stealth message from the user account."""
        if not self.client or not await self.client.is_user_authorized():
            return False
        try:
            await self.client.send_message(target_username, message)
            return True
        except Exception as e:
            logging.error(f"⚠️ GHOST STRIKE FAIL: {e}")
            return False

    async def disconnect(self):
        if self.client:
            await self.client.disconnect()

    async def run_watchdog(self):
        """Continuously polls the database for 'phantom_outreach' missions."""
        from core.db_client import get_db
        db = get_db()
        
        logging.info("👻 PHANTOM WATCHDOG: Monitoring mission queue...")
        
        # We only start the client if we actually have tasks to perform
        while True:
            try:
                # 1. Check for pending Phantom tasks
                tasks = await db.get_pending_tasks(task_type="phantom_outreach", limit=1)
                
                if tasks:
                    task = tasks[0]
                    target = task.get('target')
                    meta = task.get('meta') or "PHANTOM STRIKE"
                    
                    logging.info(f"🎯 PHANTOM ASSIGNMENT: Targeting {target}...")
                    
                    # 2. Ensure client is connected
                    if not self.client or not await self.client.is_user_authorized():
                        success = await self.start()
                        if not success:
                            logging.error("❌ PHANTOM CRITICAL: Link inactive. Aborting mission.")
                            await asyncio.sleep(60)
                            continue

                    # 3. Execute outreach
                    sent = await self.send_ghost_message(target, meta)
                    if sent:
                        await db.mark_task_completed(task['id'])
                        logging.info(f"✅ PHANTOM SUCCESS: Target {target} neutralized.")
                    else:
                        logging.error(f"⚠️ PHANTOM FAIL: Transmission to {target} failed.")
                
            except Exception as e:
                logging.error(f"⚠️ PHANTOM WATCHDOG FAULT: {e}")
            
            # Anti-Ban / Resource Protection Delay (60s)
            await asyncio.sleep(60)
