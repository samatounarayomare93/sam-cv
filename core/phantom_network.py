import os
import logging
import asyncio
import re
import random
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from dotenv import load_dotenv

# Absolute path imports (for Render/Local parity)
try:
    from core.db_client import RealityShapingDB
    from core.ai_agent import OmniIntelligence
except ImportError:
    from db_client import RealityShapingDB
    from ai_agent import OmniIntelligence

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [PHANTOM] %(levelname)s - %(message)s")

class PhantomNetwork:
    """[🕵️ PROJECT CHRONOS: PHANTOM NETWORK]
    Omnipresent userbot layer for proactive recruiter outreach and mass-infiltration.
    """
    
    def __init__(self):
        self.api_id = os.getenv("TELEGRAM_API_ID")
        self.api_hash = os.getenv("TELEGRAM_API_HASH")
        self.session_string = os.getenv("TELEGRAM_SESSION_STRING")
        self.db = RealityShapingDB()
        self.ai = OmniIntelligence()
        self.client = None
        
        # Target keywords for recruitment detection
        self.keywords = ["hiring", "urgent", "recruiting", "recruitment", "vacancy", "looking for", "vacancy", "تطلب", "توظيف"]
        
        # Target Groups (Usernames or IDs)
        # @LebanonJobs, @RecruitDubai, etc.
        self.target_groups = os.getenv("PHANTOM_TARGET_GROUPS", "").split(",")

    async def generate_phantom_pitch(self, recruiter_name: str, group_post: str) -> str:
        """Generates a high-velocity personalized pitch based on the recruitment post."""
        prompt = f"""
        [TACTICAL DIRECTIVE: PHANTOM OUTREACH]
        Recruiter Name: {recruiter_name}
        Context (Post): {group_post}
        
        Generate a concise, high-impact Telegram DM (Direct Message).
        Tone: Professional, HR-savvy, proactive.
        Goal: Offer HR Operations & Recruitment Automation services.
        Constraint: Maximum 280 characters. No generic fluff.
        Arabic/English bilingual if relevant.
        """
        pitch = await self.ai.generate_content(prompt)
        return pitch.strip()

    async def handle_new_post(self, event):
        """Analyzes group messages for recruitment opportunities."""
        text = event.message.message.lower()
        
        if any(kw in text for kw in self.keywords):
            sender = await event.get_sender()
            username = getattr(sender, 'username', None)
            user_id = getattr(sender, 'id', None)
            
            if not username and not user_id: return
            
            # Prevent double-contacting the same user in 24h
            # if await self.db.is_recent_outreach(username or user_id): return
            
            logging.info(f"🎯 PHANTOM SIGNAL: Candidate found in {event.chat.title} (User: {username})")
            
            # Generate and send DM
            try:
                recruiter_name = getattr(sender, 'first_name', 'Recruiter')
                pitch = await self.generate_phantom_pitch(recruiter_name, text)
                
                # Zero-Width Shadow Tracking ID
                strike_id = f"PHANTOM_{user_id}"
                final_pitch = self.ai.encode_shadow_id(pitch, strike_id)
                
                # Send DM
                await self.client.send_message(sender, final_pitch)
                logging.info(f"✅ PHANTOM DISPATCH: DM sent to {username or user_id}")
                
                # Log to DB
                # await self.db.log_userbot_outreach(username or str(user_id), event.chat.title, final_pitch)
                
                # Anti-Ban Cooling
                await asyncio.sleep(random.randint(60, 300))
                
            except Exception as e:
                logging.error(f"❌ PHANTOM FAULT: Failed outreach to {username}: {e}")

    async def ignite(self):
        """Starts the Phantom Network service."""
        if not self.api_id or not self.api_hash or not self.session_string:
            logging.error("❌ PHANTOM CRITICAL: Missing MTProto credentials (API_ID/API_HASH/SESSION_STRING).")
            return

        logging.info("👻 INITIATING PHANTOM NETWORK (MTProto v2.0)...")
        self.client = TelegramClient(StringSession(self.session_string), self.api_id, self.api_hash)
        
        @self.client.on(events.NewMessage(chats=self.target_groups))
        async def incoming_handler(event):
            await self.handle_new_post(event)

        await self.client.start()
        logging.info("✅ PHANTOM NETWORK ACTIVE. Monitoring HR Pulse nodes.")
        await self.client.run_until_disconnected()

if __name__ == "__main__":
    import random
    phantom = PhantomNetwork()
    asyncio.run(phantom.ignite())
