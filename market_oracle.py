import os
import time
import asyncio
import logging
import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning, module='ddgs')
warnings.filterwarnings('ignore', message='.*duckduckgo_search.*')
warnings.filterwarnings('ignore', message='.*has been renamed.*')
logging.getLogger("ddgs").setLevel(logging.CRITICAL)
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [MARKET ORACLE] - %(message)s")

# ZERO-COST REQUIREMENT: Uses Gemini Free Tier
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

async def scrape_expansion_news() -> list:
    """100% Free Web Scraper for MENA/Global expansion news."""
    logging.info("🔮 ORACLE: Scanning global news streams for HR expansion events...")
    queries = [
        '"opening new office" "HR" (UAE OR Qatar OR Dubai OR Riyadh)',
        '"expanding operations" "human resources" MENA',
        '"startup funding" "hiring" "HR Director" EMEA'
    ]
    
    results = []
    try:
        def perform_search():
            all_r = []
            with DDGS() as ddgs:
                for q in queries:
                    all_r.extend(list(ddgs.news(q, max_results=2)))
                    time.sleep(1) # Gentle throttling
            return all_r
            
        results = await asyncio.to_thread(perform_search)
    except Exception as e:
        logging.error(f"DDGS Critical Error: {e}")
    
    return results

async def draft_whitepaper_pitch(news_item: dict):
    """Uses Gemini Free Tier to draft a custom HR Infrastructure Pitch."""
    company_context = news_item.get('title', '') + " - " + news_item.get('body', '')
    url = news_item.get('url', '')
    
    logging.info(f"✍️ ORACLE: Drafting Alpha Pitch for: {news_item.get('title')[:50]}...")
    
    prompt = f"""
    You are the Ultimate HR Operations Architect.
    
    A company was just featured in the news:
    Context: "{company_context}"
    Article Link: {url}
    
    Write an extremely aggressive, high-converting cold-email drafted to their CEO or HR Director.
    Pitch a custom "HR Infrastructure & Automation Whitepaper" for their exact expansion phase.
    Do not use generic greetings. Be confident, data-driven, and short (under 150 words).
    """
    
    try:
        response = await asyncio.to_thread(model.generate_content, prompt)
        pitch = response.text.strip()
        
        # OMNISCIENT SYNC: Save to central database as a high-priority lead
        try:
            from core.db_client import RealityShapingDB
            db = RealityShapingDB()
            await db.save_task({
                "type": "ORACLE_LEAD",
                "target": news_item.get('title', 'Unknown Enterprise'),
                "meta": f"Source: {url}\n\nDraft:\n{pitch}",
                "status": "PENDING"
            })
            logging.info(f"👑 HIVE-MIND: Oracle lead [{news_item.get('title')[:20]}] synchronized to Central Command.")
        except Exception as db_e:
            logging.error(f"Failed to sync Oracle lead to DB: {db_e}")
            
    except Exception as e:
        logging.error(f"LLM Drafting Error: {e}")

async def run_oracle(headless=True):
    """Main Oracle Event Loop"""
    news_items = await scrape_expansion_news()
    
    if not news_items:
        logging.warning("No high-value expansion events detected in this cycle.")
        return

    logging.info(f"Detected {len(news_items)} expansion events. Processing top strikes...")
    
    for item in news_items[:3]:
        await draft_whitepaper_pitch(item)
        await asyncio.sleep(5)

if __name__ == "__main__":
    logging.info("🔮 PRE-COGNITIVE MARKET ORACLE (OSINT) INITIALIZED 🔮")
    asyncio.run(run_oracle(headless=False))
