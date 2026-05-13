import sys
import os
import asyncio
import logging

# Set up paths
sys.path.append(os.getcwd())

async def verify_system():
    print("--- INITIATING SOVEREIGN VERIFICATION ---")
    
    try:
        from core.db_manager import db_manager
        print("[OK] DatabaseManager: LOADED")
        
        from core.ai_agent import OmniIntelligence
        ai = OmniIntelligence()
        print("[OK] OmniIntelligence: LOADED")
        
        from core.main_bot import AlphaOrchestrator
        bot = AlphaOrchestrator()
        print("[OK] AlphaOrchestrator: LOADED")
        
        print("\n--- TESTING EVOLUTIONARY WEIGHTS ---")
        weights = await db_manager.get_variant_performance()
        print(f"Weights: {weights}")
        
        print("\n--- ENGINES STATUS ---")
        stats = await db_manager.get_stats()
        print(f"Stats: {stats}")
        
        print("\n=== VERIFICATION COMPLETE: ALL SYSTEMS NOMINAL. ===")
        return True
    except Exception as e:
        print(f"❌ VERIFICATION FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(verify_system())
