import os
import logging
import asyncio
import sqlite3
from typing import Dict, Any, List, Optional
import aiohttp
from .db_client import RealityShapingDB

class DatabaseManager:
    """
    The Alpha & Omega Unified Database Layer.
    Provides both Async and Sync interfaces to the Sovereign Intelligence Vault.
    Consolidates logic from legacy database.py and modern db_client.py.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = RealityShapingDB()
        return cls._instance

    @property
    def db(self):
        """[👑 ALIAS] Backward compatibility for legacy code."""
        return self.client

    # --- ASYNC INTERFACE (Native) ---

    async def is_duplicate(self, identifier: str) -> bool:
        return await self.client.is_duplicate(identifier)

    async def log_application(self, lead: Dict[str, Any]) -> bool:
        return await self.client.log_application(lead)

    async def save_potential_lead(self, lead_data: Dict[str, Any], score: int = 0):
        await self.client.save_potential_lead(lead_data, score)

    async def get_pending_leads(self, limit: int = 10) -> List[Dict]:
        return await self.client.get_pending_leads(limit)

    async def get_variant_performance(self) -> Dict[str, float]:
        return await self.client.get_variant_performance()

    async def get_stats(self) -> Dict[str, Any]:
        return await self.client.get_stats()

    async def check_kill_switch(self) -> bool:
        val = await self.client.get_settings("kill_switch")
        return str(val).lower() == "true"

    # --- SYNC WRAPPERS (For Scrapers/Legacy) ---

    def sync_is_duplicate(self, identifier: str) -> bool:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # This is tricky if called from a thread, usually works
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    return asyncio.run_coroutine_threadsafe(self.is_duplicate(identifier), loop).result()
            return asyncio.run(self.is_duplicate(identifier))
        except Exception:
            # Absolute fallback to local SQLite
            return self.client._is_dup_locally(identifier)

    def sync_save_potential_lead(self, lead_data: Dict[str, Any], score: int = 0):
        """[👑 ROBUST-BRIDGE]: Synchronously trigger an async lead save with failover."""
        try:
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = None

            if loop and loop.is_running():
                asyncio.run_coroutine_threadsafe(self.save_potential_lead(lead_data, score), loop)
            else:
                # No loop running in this thread, use a one-off run
                asyncio.run(self.save_potential_lead(lead_data, score))
        except Exception as e:
            logging.debug(f"⚠️ Sync Bridge Bypass: {e}")
            # Fallback to absolute local shadow if cloud bridge collapses
            self.client._log_locally(lead_data)

# Singleton handle
db_manager = DatabaseManager()

def get_db():
    return db_manager
