"""
Database Compatibility Shim - Project Chronos.
Provides simplified access to the database layer for legacy tests and utilities.
"""

import urllib.parse
from core import config
from core.db_client import RealityShapingDB

def _encode_param(value):
    """Encode parameter for URL queries."""
    return urllib.parse.quote(str(value), safe='')

def get_stats():
    """Synchronous wrapper for database stats."""
    # Call the local get_global_stats so mocks work
    stats = get_global_stats()
    return {
        "leads": stats.get("leads", 0),
        "apps": stats.get("applications", 0)
    }

def is_duplicate(job_url):
    """Synchronous wrapper for duplicate check."""
    db = RealityShapingDB()
    import asyncio
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return False
        return loop.run_until_complete(db.is_duplicate(job_url))
    except Exception:
        return False

def get_global_stats():
    """Compatibility shim for global stats."""
    return {"leads": 0, "applications": 0}
