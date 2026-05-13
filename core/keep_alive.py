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
        loop = asyncio.get_event_loop()
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
    """Runs the aiohttp web server synchronously inside the daemon thread."""
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
        web.run_app(app, host=host, port=port, handle_signals=False, access_log=None)
    except OSError as e:
        if e.errno == 10048:
            logging.warning(f"⚠️ [CLOUD-ALIVE] Port {port} already in use. Skipping locally.")
        else:
            logging.error(f"⚠️ [CLOUD-ALIVE] Fatal Crash: {e}")
    except Exception as e:
        logging.error(f"⚠️ [CLOUD-ALIVE] Fatal Crash: {e}")


def _self_ping_loop():
    """[IMMORTALITY]: Pings every 8 minutes to prevent Render from sleeping.
    On failure: retries every 2 minutes (fixed interval, NOT exponential backoff).
    Render sleeps after 15 min of inactivity — 8 min ping keeps it awake forever.
    """
    url = os.environ.get("RENDER_EXTERNAL_URL", "").strip()
    if not url or not url.startswith("https://"):
        url = "https://sam-bot-v2.onrender.com"

    logging.info(f"🛰️ [SELF-PING] Target: {url}")
    logging.info(f"🛡️ [IMMORTALITY] Pinging every 8 min — Render will NEVER sleep.")

    # Wait 30s for server to start before first ping
    time.sleep(30)

    ping_count = 0
    fail_count = 0
    start_time = time.time()

    while True:
        try:
            r = requests.get(url, timeout=20)
            ping_count += 1
            fail_count = 0
            uptime_hours = (time.time() - start_time) / 3600
            logging.info(
                f"💓 [HEARTBEAT #{ping_count}] Status: {r.status_code} | "
                f"Uptime: {uptime_hours:.1f}h"
            )
            time.sleep(480)   # 8 minutes between successful pings
        except Exception as e:
            fail_count += 1
            logging.warning(f"⚠️ [HEARTBEAT] Ping failed ({fail_count}): {e}")
            time.sleep(120)   # 2 minutes on failure — keep trying!


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
    logging.info("🛡️ [IMMORTALITY] Self-ping every 8 min — bot runs 24/7.")
    logging.info("💡 [TIP] Add https://sam-bot-v2.onrender.com to UptimeRobot.com for extra reliability (free)")
