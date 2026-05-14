import os
import threading
import logging
from aiohttp import web
import asyncio
import json
import time
import requests

try:
    import psutil
except ImportError:
    psutil = None

def get_stats():
    """Synchronous stats aggregator for the background telemetry server."""
    from core.db_client import RealityShapingDB
    db = RealityShapingDB()
    stats = db.sync_get_stats()
    return {
        "scanned": stats.get("scanned", 0),
        "strikes": stats.get("strikes", 0),
        "intel": stats.get("intel", 0),
        "uptime": stats.get('uptime', 'N/A'),
        "vips": stats.get("vips", [])
    }

async def handle_index(request):
    """Serve the Telegram Web App HTML."""
    file_path = os.path.join("core", "web_app", "index.html")
    if os.path.exists(file_path):
        return web.FileResponse(file_path)
    return web.Response(text="🟢 Sovereign Core Online.")

async def handle_api_stats(request):
    """Serve live stats to the TWA."""
    try:
        # Fix: use get_running_loop() — get_event_loop() is deprecated in Python 3.10+
        loop = asyncio.get_running_loop()
        data = await loop.run_in_executor(None, get_stats)
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
        return web.json_response(data, headers=headers)
    except Exception as e:
        logging.error(f"API Stats Error: {e}")
        return web.json_response({"error": str(e)}, status=500,
                                 headers={"Access-Control-Allow-Origin": "*"})

async def handle_api_action(request):
    """Receive and queue tactical actions from the HUD."""
    try:
        data = await request.json()
        action = data.get("action")
        if not action:
            return web.json_response({"error": "No action specified"}, status=400,
                                     headers={"Access-Control-Allow-Origin": "*"})
        logging.info(f"⚡ HUD ACTION RECEIVED: {action}")
        from core.db_client import RealityShapingDB
        db = RealityShapingDB()
        db.sync_add_task(task_type=action, target="HUD_COMMAND", meta="browser_trigger")
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
        return web.json_response({"status": "queued", "action": action}, headers=headers)
    except Exception as e:
        logging.error(f"API Action Error: {e}")
        return web.json_response({"error": str(e)}, status=500,
                                 headers={"Access-Control-Allow-Origin": "*"})

def _run_server():
    """Runs the aiohttp web server in its own dedicated event loop (daemon thread)."""
    # Fix: create a fresh event loop for this thread to avoid conflicts with the main asyncio loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = web.Application()
    app.router.add_get('/', handle_index)
    app.router.add_get('/api/stats', handle_api_stats)
    app.router.add_post('/api/action', handle_api_action)

    async def preflight(request):
        return web.Response(headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        })
    app.router.add_options('/api/action', preflight)

    port = int(os.environ.get("PORT", 10000))
    host = '0.0.0.0'
    logging.info(f"🌐 [CLOUD-ALIVE] Binding Heartbeat to {host}:{port}...")
    try:
        # Fix: remove deprecated loop= parameter (aiohttp 3.x deprecated, 4.x removed)
        # asyncio.set_event_loop(loop) above already binds the loop for this thread
        web.run_app(app, host=host, port=port, handle_signals=False, access_log=None)
    except OSError as e:
        if e.errno == 10048 or e.errno == 98:  # 98 = EADDRINUSE on Linux
            logging.warning(f"⚠️ [CLOUD-ALIVE] Port {port} already in use. Skipping.")
        else:
            logging.error(f"⚠️ [CLOUD-ALIVE] Fatal Crash: {e}")
    except Exception as e:
        logging.error(f"⚠️ [CLOUD-ALIVE] Fatal Crash: {e}")
    finally:
        loop.close()


def _self_ping_loop():
    """[IMMORTALITY]: Multi-source ping system — 4 independent methods.
    Even if UptimeRobot goes down, the bot stays alive via self-ping + Supabase heartbeat.
    Render sleeps after 15 min — we ping every 5 min from multiple sources.
    """
    url = os.environ.get("RENDER_EXTERNAL_URL", "").strip()
    if not url or not url.startswith("https://"):
        url = "https://sam-bot-v2.onrender.com"

    logging.info(f"🛰️ [SELF-PING] Target: {url}")
    logging.info(f"🛡️ [IMMORTALITY] 4-layer ping system active — bot NEVER sleeps.")

    # Wait 30s for server to start before first ping
    time.sleep(30)

    ping_count = 0
    fail_count = 0
    start_time = time.time()

    while True:
        try:
            # ── Layer 1: Self-ping (primary) ──────────────────────────────
            r = requests.get(url, timeout=20)
            ping_count += 1
            fail_count = 0
            uptime_hours = (time.time() - start_time) / 3600
            logging.info(
                f"💓 [HEARTBEAT #{ping_count}] Status: {r.status_code} | "
                f"Uptime: {uptime_hours:.1f}h"
            )

            # ── Layer 2: Supabase heartbeat (backup) ──────────────────────
            # Even if HTTP ping fails, writing to Supabase keeps the process alive
            try:
                sb_url = os.environ.get("SUPABASE_URL", "").rstrip('/')
                sb_key = os.environ.get("SUPABASE_KEY", "")
                if sb_url and sb_key:
                    requests.patch(
                        f"{sb_url}/rest/v1/system_settings?key=eq.LAST_PULSE",
                        headers={
                            "apikey": sb_key,
                            "Authorization": f"Bearer {sb_key}",
                            "Content-Type": "application/json",
                            "Prefer": "return=minimal"
                        },
                        json={"value": str(time.time())},
                        timeout=8
                    )
            except Exception:
                pass  # Never crash over heartbeat

            time.sleep(300)   # 5 minutes — tighter than Render's 15-min sleep threshold

        except Exception as e:
            fail_count += 1
            logging.warning(f"⚠️ [HEARTBEAT] Ping failed ({fail_count}): {e}")
            # On failure: retry every 2 minutes — keep trying until it works
            time.sleep(120)


def run_keep_alive_server():
    """Blocking function to run the aiohttp server."""
    _run_server()


def keep_alive():
    """Spawns background threads: web server + self-ping heartbeat."""
    # 1. External-facing web server (Render port-binding)
    t = threading.Thread(target=_run_server, name="CloudHeartbeat", daemon=True)
    t.start()

    # 2. Self-ping loop (prevent Render sleep)
    p = threading.Thread(target=_self_ping_loop, name="SelfPing", daemon=True)
    p.start()

    logging.info("🛡️ [IMMORTALITY] Heartbeat threads launched.")
    logging.info("🛡️ [IMMORTALITY] Self-ping every 5 min — bot runs 24/7.")
    logging.info("💡 [TIP] Add https://sam-bot-v2.onrender.com to UptimeRobot.com for extra reliability (free)")
