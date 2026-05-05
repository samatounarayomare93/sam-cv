#!/usr/bin/env python
"""
launch_sam.py - Unified entry point for Project Chronos on Render.
Delegates entirely to run.py which handles everything correctly:
- Single asyncio event loop (no threading conflicts)
- Proper keep-alive / port binding
- Telegram polling with correct event loop management
- All fixes for asyncio.Lock, semaphore, and polling errors
"""

import sys
import os

# Ensure core modules are importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Simply run the unified swarm orchestrator
import run
import asyncio

if __name__ == "__main__":
    try:
        asyncio.run(run.main())
    except KeyboardInterrupt:
        pass
