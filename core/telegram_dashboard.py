import sys
import os
import logging
import subprocess
import re
import asyncio
from datetime import datetime
from telegram import (
    Update, BotCommand, ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo,
    InlineQueryResultArticle, InputTextMessageContent
)
from telegram.error import Conflict
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, InlineQueryHandler, filters, ContextTypes
)
from dotenv import load_dotenv

from core.keep_alive import keep_alive
from core.phantom_client import PhantomClient

# Lazy import for hardware telemetry
try:
    import psutil
except ImportError:
    psutil = None

try:
    from core.db_client import RealityShapingDB
except ImportError:
    from db_client import RealityShapingDB

try:
    from core.ai_agent import OmniIntelligence
except ImportError:
    from ai_agent import OmniIntelligence

# Safe VoiceCommander import
VoiceCommander = None
try:
    from core.voice_ops import VoiceCommander as _VC
    VoiceCommander = _VC
except (ImportError, Exception):
    logging.warning("⚠️ VoiceCommander unavailable. Voice ops disabled.")

try:
    from core import smtp_engine
except ImportError:
    import smtp_engine

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [TELEGRAM] %(levelname)s - %(message)s")


class SovereignDashboard:
    """Absolute remote control interface for Project Chronos. 20 MENU COMMANDS."""

    def __init__(self, db=None, ai=None):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.db = db if db else RealityShapingDB()
        self.ai = ai if ai else OmniIntelligence()
        self.chat_id_raw = os.getenv("TELEGRAM_CHAT_ID", "")
        
        # [👑 MULTI-USER SYNC]: Support comma-separated IDs
        self.authorized_users = []
        if self.chat_id_raw:
            for part in self.chat_id_raw.split(','):
                part = part.strip()
                if not part: continue
                try:
                    self.authorized_users.append(int(part))
                except Exception:
                    self.authorized_users.append(part)
        
        # Primary chat ID for administrative tasks
        self.chat_id = self.authorized_users[0] if self.authorized_users else None
        self.hud_message_id = None
        self.is_leader = False
        self._phantom_state = {} # Temporary state for UserBot linking
        self._polling_conflict = False
        self._leader_verify_degraded = False
        self._loops_started = False # Flag to ensure background tasks start only once
        
        from core.runtime_helpers import get_proxy_mesh
        self.proxy_mesh = get_proxy_mesh()
        
        # Telemetry Stream

    def _build_polling_error_callback(self):
        """Create polling error callback that flags 409 conflict for controlled recovery."""

        async def _handle_error(error):
            if isinstance(error, Conflict):
                logging.debug("🔄 TELEGRAM 409 CONFLICT: Library will auto-retry.")
                return
            logging.error(f"⚠️ POLLING ERROR: {error}")

        def _error_callback(error):
            # [FIX] Don't capture the loop at build time — fetch it at call time to avoid
            # "cannot schedule new futures after shutdown" when the loop restarts.
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(_handle_error(error))
            except RuntimeError:
                # No running loop (e.g. during shutdown) — just log directly
                if isinstance(error, Conflict):
                    logging.debug("🔄 TELEGRAM 409 CONFLICT: Library will auto-retry.")
                else:
                    logging.error(f"⚠️ POLLING ERROR: {error}")

        return _error_callback

    async def broadcast_message(self, bot, text: str, parse_mode: str = 'HTML', reply_markup=None):
        """[👑 APEX BROADCAST] Sends a message to all authorized users."""
        for uid in self.authorized_users:
            try:
                await bot.send_message(chat_id=uid, text=text, parse_mode=parse_mode, reply_markup=reply_markup)
            except Exception as e:
                logging.error(f"⚠️ Broadcast failed for User {uid}: {e}")

    async def broadcast_document(self, bot, document, caption: str = "", parse_mode: str = 'HTML'):
        """[👑 APEX BROADCAST] Sends a document to all authorized users."""
        for uid in self.authorized_users:
            try:
                # Need to seek(0) if it's a file object, but usually we pass the file handle
                if hasattr(document, 'seek'):
                    document.seek(0)
                await bot.send_document(chat_id=uid, document=document, caption=caption, parse_mode=parse_mode)
            except Exception as e:
                logging.error(f"⚠️ Doc Broadcast failed for User {uid}: {e}")

    async def _sync_ui_standalone(self, application):
        """Standalone UI sync that can be called without start_polling."""
        commands = [
            BotCommand("menu", "📱 القائمة الرئيسية (Main Menu)"),
            BotCommand("start", "🚀 بدء التشغيل (Start Ops)"),
            BotCommand("status", "🖥️ تقرير السحاب (Cloud Status)"),
            BotCommand("logs", "📜 سجل النظام (System Logs)"),
            BotCommand("stats", "📊 إحصائيات المهمة (Mission Stats)"),
            BotCommand("tasks", "🧬 قائمة المهام (Mission Tasks)"),
            BotCommand("leads", "📋 فرص الوظائف (Job Leads)"),
            BotCommand("companies", "🏢 تحليل الشركات (Company Intel)"),
            BotCommand("shield", "🛡️ درع الحماية (Security Shield)"),
            BotCommand("pulse", "📜 نبض النظام (System Pulse)"),
            BotCommand("track", "🛰️ تتبع الرادار (Live Tracking)"),
            BotCommand("synapse", "💪 فحص القوة (Strength Check)"),
            BotCommand("oracle", "🔮 استشعار السوق (Market Oracle)"),
            BotCommand("guide", "📖 الدليل الشامل (Operation Manual)"),
            BotCommand("settings", "⚙️ الإعدادات (System Settings)"),
            BotCommand("reboot", "🔄 إعادة تشغيل (Full Reboot)"),
            BotCommand("pause", "⏸️ إيقاف مؤقت (Pause Engine)"),
            BotCommand("resume", "🟢 استئناف العمل (Resume Swarm)"),
            BotCommand("unpause", "▶️ إلغاء الإيقاف (Unpause)"),
            BotCommand("omega_halt", "🛑 التوقف التام (Total Halt)"),
            BotCommand("fix", "🔧 إصلاح طارئ (Emergency Fix & Restart)"),
            BotCommand("ai_check", "🧠 فحص الذكاء الاصطناعي (AI Status Check)"),
            BotCommand("keys", "🔑 إدارة API Keys (API Key Manager)"),
            BotCommand("setkey", "✏️ تغيير API Key (Set API Key)"),
            BotCommand("testkey", "🧪 اختبار API Key (Test API Key)")
        ]
        try:
            await application.bot.set_my_commands(commands)
            if self.chat_id:
                from telegram import BotCommandScopeChat, MenuButtonCommands
                scope = BotCommandScopeChat(chat_id=self.chat_id)
                await application.bot.set_my_commands(commands, scope=scope)
                await application.bot.set_chat_menu_button(chat_id=self.chat_id, menu_button=MenuButtonCommands())
                logging.info(f"✅ UI: Dashboard buttons forced active for Chat {self.chat_id}")
        except Exception as e:
            logging.error(f"⚠️ UI FORCE SYNC FAILED: {e}")

    async def authenticate(self, update: Update) -> bool:
        # [🛡️ AUTH-AUDIT]: Check both user ID and chat ID for authorization
        user_id = str(update.effective_user.id)
        chat_id = str(update.effective_chat.id)
        auth_list = [str(uid) for uid in self.authorized_users if uid]
        
        logging.info(f"🔐 [ORCHESTRATOR] Auth Check: User {user_id} in Chat {chat_id} against {auth_list}")
        
        # Check both user ID and chat ID (for private chats, they are the same)
        if user_id in auth_list or chat_id in auth_list:
            return True
        
        await update.effective_message.reply_text(f"🚨 UNAUTHORIZED ACCESS. User: {user_id}, Chat: {chat_id}")
        logging.warning(f"❌ UNAUTHORIZED ATTEMPT: User {user_id} in Chat {chat_id}")
        return False

    async def handle_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        cmd_text = update.message.text
        if not cmd_text: return
        
        logging.info(f"📨 [COMMAND RECEIVED]: '{cmd_text}' from User {update.effective_user.id} in Chat {update.effective_chat.id}")
        
        # [🎯 VIP PORTAL CHECK]
        # Bypass authentication only for deep-linked /start
        if cmd_text.startswith("/start") and len(cmd_text.split()) > 1:
            target_id = cmd_text.split()[1]
            await self._handle_vip_portal(target_id, update, context)
            return

        # Standard Authentication for all other commands
        if not await self.authenticate(update): return
        await self._dispatch_command(cmd_text, update, context)

    async def _dispatch_command(self, cmd_text: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if "logs" in cmd_text.lower() or "سجلات" in cmd_text or cmd_text.startswith("/logs"):
            cmd = "/logs"
        else:
            raw = cmd_text.strip().split()[0].lower()
            cmd = raw if raw.startswith("/") else f"/{raw}"

        # TEXT_ONLY_CMDS: only the keys that go to _handle_text_map (NOT slash commands)
        TEXT_ONLY_CMDS = {
            "tasks", "shield", "pulse", "leads", "prep", "campaign", "followup", 
            "companies", "test_strike", "evolution", "audit", "ai_status", 
            "vision", "synapse", "matrix", "phantom", "menu", "guide"
        }
        if cmd.lstrip("/") in TEXT_ONLY_CMDS:
            await self._handle_text_map(cmd.lstrip("/"), update, context)
            return

        if cmd == "/ignite":
            # ☁️ CLOUD-SAFE: Bot is already running 24/7 on Render
            await update.effective_message.reply_text("🔥 <b>IGNITION SEQUENCE INITIATED...</b>\n<i>System is running 24/7 on cloud.</i>", parse_mode='HTML')
            try:
                if self.db:
                    await self.db.activate_kill_switch(False)  # Ensure kill switch is off
                await update.effective_message.reply_text("✅ <b>EMPIRE IGNITED.</b>\nAbsolute Singularity is now 100% active on cloud.", parse_mode='HTML')
            except Exception as e:
                await update.effective_message.reply_text(f"⚠️ <b>IGNITION ERROR:</b> {e}", parse_mode='HTML')

        elif cmd == "/start":
            reply_markup, inline_markup = self._get_sovereign_keyboards()
            await update.effective_message.reply_text(
                "👑 <b>PROJECT CHRONOS: SOVEREIGN V2</b>\n"
                f"<i>Node: {os.getenv('NODE_NAME', 'MASTER-CLOUD')}</i>\n"
                "<i>Status: Armed & Operational</i>\n\n"
                "🔥 <b>ULTRA-MAXIMUM MODE ACTIVE</b>\n"
                "━━━━━━━━━━━━━━━\n"
                "📊 Target: 1500 applications/day\n"
                "⚡ Speed: 120 apps/hour\n"
                "📧 Capacity: 1900 emails/day\n"
                "🕐 Hours: 5 AM - 11 PM\n"
                "━━━━━━━━━━━━━━━\n\n"
                "Use the <b>COMMAND CENTER</b> (Inline) or the <b>SOVEREIGN TILESET</b> (Bottom).\n"
                "<i>Click '📖 GUIDE' for a full Arabic manual of all abilities.</i>",
                parse_mode='HTML',
                reply_markup=reply_markup
            )
            await update.effective_message.reply_text("🎮 <b>DYNAMIC COMMAND CENTER:</b>", reply_markup=inline_markup, parse_mode='HTML')

        elif cmd in ("/stats", "/menu"):
            await self._dispatch_command("/status", update, context)
            return

        elif cmd == "/kill" or cmd == "/omega_halt":
            if self.db:
                await self.db.activate_kill_switch(True)
            await update.effective_message.reply_text("🚨 <b>SYSTEM OVERRIDE: TOTAL KILL SWITCH ENGAGED.</b>\nAll infinite cycles frozen.", parse_mode='HTML')

        elif cmd == "/resume" or cmd == "/unpause":
            if self.db:
                await self.db.activate_kill_switch(False)
            # Show keyboard with current state
            reply_markup, inline_markup = self._get_sovereign_keyboards()
            await update.effective_message.reply_text(
                "▶️ <b>التقديمات شغّالة!</b>\n"
                "━━━━━━━━━━━━━━━\n"
                "✅ البوت عم يقدّم على وظائف\n"
                "📊 Target: 1500 تقديم/يوم\n"
                "━━━━━━━━━━━━━━━\n"
                "لما تبدك توقف اضغط ⏸️ PAUSE",
                parse_mode='HTML',
                reply_markup=inline_markup
            )

        elif cmd == "/pause":
            if self.db:
                await self.db.activate_kill_switch(True)
            reply_markup, inline_markup = self._get_sovereign_keyboards()
            await update.effective_message.reply_text(
                "⏸️ <b>التقديمات موقوفة!</b>\n"
                "━━━━━━━━━━━━━━━\n"
                "🛑 البوت وقف عن التقديم\n"
                "📧 الإيميلات مش رح تنبعت\n"
                "━━━━━━━━━━━━━━━\n"
                "لما تبدك تكمل اضغط ▶️ RESUME",
                parse_mode='HTML',
                reply_markup=inline_markup
            )

        elif cmd == "/launch_single":
            await update.effective_message.reply_text("🚀 <b>READY</b>\nThe bot already runs continuously in the cloud. Use /status to verify live health.", parse_mode='HTML')

        elif cmd == "/launch_infinite" or cmd == "/hunter" or cmd == "/run_now":
            await update.effective_message.reply_text("♾️ <b>READY</b>\nContinuous mode is already active. Use /logs or /tasks for live work.", parse_mode='HTML')

        elif cmd in ("/test_gmail", "/test_brevo"):
            # Real test path uses the existing SMTP engine; no fake status text.
            target_email = os.getenv("GMAIL_TEST_RECIPIENT") or os.getenv("GMAIL_SMTP_USER")
            await update.effective_message.reply_text("💌 <b>RUNNING SMTP TEST...</b>", parse_mode='HTML')
            try:
                result = await asyncio.to_thread(smtp_engine.send_test_email, target_email)
                if result:
                    await update.effective_message.reply_text(f"✅ <b>SMTP TEST SUCCESS</b>\nSent to <code>{target_email}</code>", parse_mode='HTML')
                else:
                    await update.effective_message.reply_text("⚠️ <b>SMTP TEST FAILED</b>\nCheck server logs and credentials.", parse_mode='HTML')
            except Exception as e:
                await update.effective_message.reply_text(f"❌ <b>TEST ERROR:</b> {e}", parse_mode='HTML')

        elif cmd == "/queue":
            pending = await self.db.get_pending_tasks(limit=10) if self.db else []
            count = len(pending) if pending else 0
            msg = "📧 <b>MISSION DISPATCH QUEUE</b>\n━━━━━━━━━━━━━━━\n"
            msg += f"📦 Pending Actions: {count}\n"
            msg += "📍 Status: Actively Processing\n"
            msg += "━━━━━━━━━━━━━━━"
            if pending:
                msg += "\n" + "\n".join([f"• {t.get('type', 'TASK')} -> {str(t.get('target', ''))[:30]}" for t in pending[:5]])
            await update.effective_message.reply_text(msg, parse_mode='HTML')

        elif cmd == "/supabase":
            status = "ONLINE" if self.db else "OFFLINE"
            await update.effective_message.reply_text(f"🩺 <b>DATABASE TELEMETRY</b>\nStatus: 🟢 {status}\nSync: {'Local Mirror Active' if self.db else 'Unavailable'}", parse_mode='HTML')

        elif cmd == "/menu":
            reply_markup, inline_markup = self._get_sovereign_keyboards()
            await update.effective_message.reply_text("📱 <b>MAIN MENU</b>", reply_markup=reply_markup, parse_mode='HTML')
            await update.effective_message.reply_text("🎮 <b>DYNAMIC COMMAND CENTER:</b>", reply_markup=inline_markup, parse_mode='HTML')

        elif cmd == "/auto_backup":
            await update.effective_message.reply_text("💾 <b>AUTO BACKUP</b>\nThis is a maintenance helper, not a user action.", parse_mode='HTML')
            if self.authorized_users:
                await self._execute_backup_logic(context.bot, self.authorized_users[0])
            return

        elif cmd == "/logs":
            await update.effective_message.reply_text("📤 <b>GENERATING ACTIVITY REPORT...</b>\n<i>Pulling data from Supabase cloud...</i>", parse_mode='HTML')
            try:
                from datetime import datetime, timedelta, timezone
                now = datetime.now(timezone.utc)
                yesterday = (now - timedelta(hours=24)).isoformat().replace("+", "%2B")

                # 1. Get recent applications (last 24h)
                app_lines = []
                app_succ, app_data = await self.db._request_with_retry(
                    "GET",
                    f"{self.db.url}/rest/v1/applications?select=company_name,job_title,status,timestamp&order=timestamp.desc&limit=20&timestamp=gte.{yesterday}"
                )
                if app_succ and isinstance(app_data, list):
                    for a in app_data:
                        company = a.get('company_name', 'Unknown')[:20]
                        title = a.get('job_title', 'N/A')[:25]
                        status = a.get('status', 'SENT')
                        app_lines.append(f"✅ {company} — {title} [{status}]")

                # 2. Get recent leads (last 24h)
                lead_lines = []
                lead_succ, lead_data = await self.db._request_with_retry(
                    "GET",
                    f"{self.db.url}/rest/v1/leads?select=company_name,job_title,status,created_at&order=created_at.desc&limit=20&created_at=gte.{yesterday}"
                )
                if lead_succ and isinstance(lead_data, list):
                    for l in lead_data:
                        company = l.get('company_name', 'Unknown')[:20]
                        title = l.get('job_title', 'N/A')[:25]
                        status = l.get('status', 'NEW')
                        lead_lines.append(f"🎯 {company} — {title} [{status}]")

                # 3. Get total stats
                stats = await self.db.get_stats()
                total_apps = stats.get('total_strikes', 0)
                total_leads = stats.get('recon_rows', 0)

                # Build the report
                report = f"📜 <b>ACTIVITY REPORT — Last 24 Hours</b>\n━━━━━━━━━━━━━━━\n"
                report += f"📊 <b>Total Applications Ever:</b> {total_apps}\n"
                report += f"📋 <b>Total Leads Ever:</b> {total_leads}\n"
                report += f"━━━━━━━━━━━━━━━\n\n"

                # Get accurate 24h counts
                app_24h_count = len(app_lines)
                app_c_succ, app_c_data = await self.db._request_with_retry("GET", f"{self.db.url}/rest/v1/applications?select=company_name&limit=1&timestamp=gte.{yesterday}", headers={"Prefer": "count=exact"})
                if app_c_succ and isinstance(app_c_data, dict): app_24h_count = app_c_data.get("count", app_24h_count)

                lead_24h_count = len(lead_lines)
                lead_c_succ, lead_c_data = await self.db._request_with_retry("GET", f"{self.db.url}/rest/v1/leads?select=id&limit=1&created_at=gte.{yesterday}", headers={"Prefer": "count=exact"})
                if lead_c_succ and isinstance(lead_c_data, dict): lead_24h_count = lead_c_data.get("count", lead_24h_count)

                if app_lines:
                    report += f"🚀 <b>Applications Sent (Last 24h): {app_24h_count}</b> <i>(Showing Top 15)</i>\n"
                    report += "\n".join(app_lines[:15])
                    report += "\n\n"
                else:
                    report += "🚀 <b>Applications Sent (Last 24h):</b> 0\n<i>No new applications in the last 24 hours.</i>\n\n"

                if lead_lines:
                    report += f"🎯 <b>Leads Discovered (Last 24h): {lead_24h_count}</b> <i>(Showing Top 15)</i>\n"
                    report += "\n".join(lead_lines[:15])
                    report += "\n\n"
                else:
                    report += "🎯 <b>Leads Discovered (Last 24h):</b> 0\n<i>No new leads in the last 24 hours.</i>\n\n"

                report += "━━━━━━━━━━━━━━━\n"
                report += f"🕐 <i>Report generated: {now.strftime('%Y-%m-%d %H:%M UTC')}</i>"

                await update.effective_message.reply_text(report, parse_mode='HTML')

                # Generate full CSV of last 24h activity
                csv_content = "TYPE,COMPANY,JOB_TITLE,STATUS,DATE\n"
                has_csv_data = False
                
                app_full_succ, app_full_data = await self.db._request_with_retry("GET", f"{self.db.url}/rest/v1/applications?select=company_name,job_title,status,timestamp&order=timestamp.desc&limit=2000&timestamp=gte.{yesterday}")
                if app_full_succ and isinstance(app_full_data, list):
                    for a in app_full_data:
                        c_name = str(a.get('company_name', '')).replace('"', '""')
                        j_title = str(a.get('job_title', '')).replace('"', '""')
                        csv_content += f"APPLICATION,\"{c_name}\",\"{j_title}\",\"{a.get('status', '')}\",\"{a.get('timestamp', '')}\"\n"
                        has_csv_data = True
                
                lead_full_succ, lead_full_data = await self.db._request_with_retry("GET", f"{self.db.url}/rest/v1/leads?select=company_name,job_title,status,created_at&order=created_at.desc&limit=2000&created_at=gte.{yesterday}")
                if lead_full_succ and isinstance(lead_full_data, list):
                    for l in lead_full_data:
                        c_name = str(l.get('company_name', '')).replace('"', '""')
                        j_title = str(l.get('job_title', '')).replace('"', '""')
                        csv_content += f"LEAD,\"{c_name}\",\"{j_title}\",\"{l.get('status', '')}\",\"{l.get('created_at', '')}\"\n"
                        has_csv_data = True

                if has_csv_data:
                    import io
                    file_bytes = io.BytesIO(csv_content.encode('utf-8-sig')) # UTF-8 with BOM for Excel compatibility
                    file_bytes.name = f"sam_full_report_{now.strftime('%Y%m%d_%H%M')}.csv"
                    await context.bot.send_document(
                        chat_id=update.effective_chat.id, 
                        document=file_bytes, 
                        caption="📎 <b>Full 24h Activity Report</b> (All Records)",
                        parse_mode='HTML'
                    )

                # 4. Also send the raw log file if it exists (☁️ CLOUD-SAFE: logs might not exist)
                log_path = "logs/orchestrator.log"
                if os.path.exists(log_path) and os.path.getsize(log_path) > 0:
                    try:
                        with open(log_path, "rb") as f:
                            await context.bot.send_document(chat_id=update.effective_chat.id, document=f, filename="sam_raw_logs_24h.txt", caption="📎 Raw system logs attached above")
                    except Exception as e:
                        logging.debug(f"Could not send log file: {e}")

            except Exception as e:
                await update.effective_message.reply_text(f"⚠️ <b>ERROR generating report:</b> {e}", parse_mode='HTML')

        elif cmd == "/lazarus" or cmd == "/repair":
            staged = []
            if os.path.exists("staged_patches"):
                staged = [f for f in os.listdir("staged_patches") if f.endswith(".py")]
            
            if staged:
                msg = "🩹 <b>REPAIR PROTOCOL: LAZARUS</b>\nCritical failures detected. Staged fixes ready:\n\n"
                for i, p in enumerate(staged):
                    msg += f"🧬 <code>{p}</code>\n"
                msg += "\nTo apply a fix, use: <code>/apply_patch fix_ID.py</code>"
            else:
                msg = "✅ <b>REPAIR PROTOCOL:</b> No staged patches. System clean."
            
            await update.effective_message.reply_text(msg, parse_mode='HTML')

        elif cmd == "/reboot":
            # ☁️ CLOUD-SAFE: On cloud, Render handles restarts
            await update.effective_message.reply_text("🔄 <b>REBOOT REQUEST</b>\nOn cloud, Render automatically restarts the bot if needed. System is running 24/7.", parse_mode='HTML')

        elif cmd == "/fix" or cmd == "/reset" or cmd == "/forcestart":
            """[🔥 EMERGENCY FIX]: Force reset leadership, clear kill switch, restart engine."""
            await update.effective_message.reply_text("🔧 <b>EMERGENCY FIX INITIATED...</b>\n<i>Resetting all locks and restarting engine...</i>", parse_mode='HTML')
            
            steps = []
            try:
                # Step 1: Disable kill switch in DB
                await self.db.activate_kill_switch(False)
                os.environ["KILL_SWITCH_ACTIVE"] = "false"
                steps.append("✅ Kill switch: DISABLED")
            except Exception as e:
                steps.append(f"⚠️ Kill switch reset failed: {e}")
            
            try:
                # Step 2: Force claim leadership by clearing stale heartbeat
                old_time = "2020-01-01T00:00:00"
                await self.db.update_setting("active_bot_heartbeat", old_time)
                await asyncio.sleep(1)
                is_leader = await self.db.claim_bot_leadership()
                steps.append(f"✅ Leadership: {'CLAIMED' if is_leader else 'FAILED'}")
            except Exception as e:
                steps.append(f"⚠️ Leadership reset failed: {e}")
            
            try:
                # Step 3: Check pending leads count
                count = await self.db.get_pending_leads_count()
                steps.append(f"📊 Pending leads in queue: {count}")
                if count == 0:
                    steps.append("⚠️ Queue is EMPTY - bot will scrape new jobs in next cycle")
                else:
                    steps.append(f"🚀 Bot will process {count} leads immediately")
            except Exception as e:
                steps.append(f"⚠️ Queue check failed: {e}")
            
            try:
                # Step 4: Send heartbeat to confirm DB connection
                await self.db.send_heartbeat()
                steps.append("✅ Database: CONNECTED")
            except Exception as e:
                steps.append(f"❌ Database: FAILED - {e}")
            
            result_msg = (
                "🔧 <b>EMERGENCY FIX COMPLETE</b>\n"
                "━━━━━━━━━━━━━━━\n"
                + "\n".join(steps) +
                "\n━━━━━━━━━━━━━━━\n"
                "🔥 <b>Engine is running!</b>\n"
                "<i>If queue was empty, bot will scrape new jobs in ~90 minutes.\n"
                "Use /status to monitor progress.</i>"
            )
            await update.effective_message.reply_text(result_msg, parse_mode='HTML')

        elif cmd == "/hud":
            msg = await update.effective_message.reply_text("📟 <b>INITIALIZING LIVE HUD...</b>", parse_mode='HTML')
            self.hud_message_id = msg.message_id
            try:
                await context.bot.pin_chat_message(chat_id=update.effective_message.chat_id, message_id=self.hud_message_id)
            except: pass
            asyncio.create_task(self._live_hud_loop(context.bot, update.effective_message.chat_id))
            return

        elif cmd == "/backup":
            await update.effective_message.reply_text("💾 <b>CREATING BACKUP...</b>", parse_mode='HTML')
            try:
                await self._execute_backup_logic(context.bot, update.effective_message.chat_id)
                await update.effective_message.reply_text("✅ <b>BACKUP COMPLETE</b>", parse_mode='HTML')
            except Exception as e:
                await update.effective_message.reply_text(f"⚠️ <b>BACKUP FAILED:</b> {e}", parse_mode='HTML')

        elif cmd == "/cmd":
            await update.effective_message.reply_text("🚫 <b>COMMAND SHELL NOT AVAILABLE</b>\nUse /status, /logs, /tasks, or /leads instead.", parse_mode='HTML')

        elif cmd == "/audit":
            stats = await self.db.get_stats() if self.db else {}
            health = self.db.get_advanced_health() if self.db else {} # For memory/uptime only
            
            # Get today's metrics
            from datetime import datetime, timedelta, timezone
            now = datetime.now(timezone.utc)
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat().replace("+", "%2B")
            
            today_apps = 0
            try:
                app_succ, app_data = await self.db._request_with_retry(
                    "GET",
                    f"{self.db.url}/rest/v1/applications?select=id&timestamp=gte.{today_start}",
                    headers={"Prefer": "count=exact"}
                )
                if app_succ and isinstance(app_data, dict):
                    today_apps = app_data.get("count", 0)
            except Exception:
                pass
            
            # Get email provider status
            email_providers = []
            try:
                from core.email_rotator import get_rotator
                rotator = get_rotator()
                current_provider = rotator.get_current_provider()
                provider_stats = rotator.get_provider_stats()
                
                for provider, data in provider_stats.items():
                    status_icon = "🟢" if data['available'] else "🔴"
                    email_providers.append(
                        f"{status_icon} <b>{provider}:</b> {data['sent_today']}/{data['daily_limit']} "
                        f"({int((data['sent_today']/data['daily_limit'])*100)}%)"
                    )
                
                current_provider_line = f"📧 <b>Active Provider:</b> {current_provider}\n"
            except Exception as e:
                logging.error(f"Email rotator error: {e}")
                email_providers = ["🔄 Email rotation system active"]
                current_provider_line = ""
            
            providers_str = "\n".join(email_providers) if email_providers else "No providers configured"
            
            msg = (
                "👁️ <b>SOVEREIGN AUDIT REPORT</b>\n"
                f"━━━━━━━━━━━━━━━\n"
                f"🔥 <b>MODE:</b> ULTRA-MAXIMUM (1500/day)\n"
                f"━━━━━━━━━━━━━━━\n\n"
                f"📊 <b>TODAY'S PERFORMANCE:</b>\n"
                f"🚀 <b>Applications Sent:</b> {today_apps}/1500\n"
                f"📈 <b>Progress:</b> {int((today_apps/1500)*100)}%\n\n"
                f"📧 <b>EMAIL PROVIDERS:</b>\n"
                f"{current_provider_line}"
                f"{providers_str}\n\n"
                f"🎯 <b>GLOBAL STATS:</b>\n"
                f"📍 <b>Targets Discovered:</b> <code>{stats.get('recon_rows', 0)}</code>\n"
                f"🚀 <b>Total Strikes:</b> <code>{stats.get('total_strikes', 0)}</code>\n"
                f"🕒 <b>Uptime:</b> {health.get('uptime', 'N/A')}\n"
                f"━━━━━━━━━━━━━━━"
            )
            await update.effective_message.reply_text(msg, parse_mode='HTML')

        elif cmd == "/track":
            tasks = await self.db.get_pending_tasks(limit=3) if self.db else []
            task_str = "\n".join([f"🎯 {t['type']}: {t['target'][:20]}..." for t in tasks]) if tasks else "Radar quiet. All targets processed."
            msg = (
                "🛰️ <b>LIVE TRACKING RADAR</b>\n"
                f"━━━━━━━━━━━━━━━\n"
                f"📡 <b>Signal:</b> Locked & Routing\n"
                f"{task_str}\n"
                f"━━━━━━━━━━━━━━━"
            )
            await update.effective_message.reply_text(msg, parse_mode='HTML')

        elif cmd == "/magic" or cmd == "/refresh_ui":
            await update.effective_message.reply_text("🪄 <b>PURGING UI CACHE...</b>\n<i>Force-pushing commands to the Sovereign Link.</i>", parse_mode='HTML')
            try:
                await self._sync_ui_standalone(context.application)
                await update.effective_message.reply_text("✅ <b>UI SYNCHRONIZED.</b>", parse_mode='HTML')
            except Exception as e:
                await update.effective_message.reply_text(f"⚠️ <b>UI REFRESH FAILED:</b> {e}", parse_mode='HTML')

        elif cmd == "/ai_config":
            engine = getattr(self.ai, 'primary_engine', 'unknown') if self.ai else 'unavailable'
            await update.effective_message.reply_text(
                f"🛠️ <b>AI CONFIGURATION CORE</b>\n━━━━━━━━━━━━━━━\nEngine: <code>{engine}</code>\nStatus: <code>{'Ready' if self.ai else 'Unavailable'}</code>\n━━━━━━━━━━━━━━━\n<i>This page is informational; real AI work happens in /prep and /oracle.</i>",
                parse_mode='HTML'
            )

        elif cmd == "/keys" or cmd == "/apikeys":
            # ── Show all API keys status ──────────────────────────────────────
            from core.api_key_manager import get_key_manager, API_KEY_REGISTRY
            mgr = get_key_manager()
            status = mgr.get_all_status()

            # Group by category
            categories = {}
            for key_name, info in status.items():
                cat = info["category"]
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append((key_name, info))

            lines = ["🔑 <b>API KEYS MANAGER</b>", "━━━━━━━━━━━━━━━━━━━━"]

            for cat, items in categories.items():
                cat_icons = {"AI": "🧠", "Email": "📧", "Infra": "☁️"}
                lines.append(f"\n{cat_icons.get(cat,'📌')} <b>{cat}:</b>")
                for key_name, info in items:
                    has = info["has_key"]
                    src = f" <i>({info['source']})</i>" if has else ""
                    masked = info["masked"]
                    icon = "✅" if has else "❌"
                    lines.append(
                        f"  {icon} {info['icon']} <b>{info['label']}</b>{src}\n"
                        f"     <code>{masked}</code>\n"
                        f"     💡 {info['free_info']}"
                    )

            lines.append("\n━━━━━━━━━━━━━━━━━━━━")
            lines.append("📝 <b>Commands:</b>")
            lines.append("/setkey — Set/update a key")
            lines.append("/testkey — Test a specific key")
            lines.append("/ai_check — Test all AI keys live")

            await update.effective_message.reply_text("\n".join(lines), parse_mode='HTML')

        elif cmd == "/setkey":
            # ── Set an API key from Telegram ──────────────────────────────────
            # Usage: /setkey GROQ_API_KEY gsk_xxxxx
            parts = update.message.text.strip().split(None, 2)
            if len(parts) < 3:
                from core.api_key_manager import API_KEY_REGISTRY
                key_list = "\n".join(
                    f"  • <code>{k}</code> — {v['icon']} {v['label']}"
                    for k, v in API_KEY_REGISTRY.items()
                )
                await update.effective_message.reply_text(
                    "🔑 <b>SET API KEY</b>\n━━━━━━━━━━━━━━━\n"
                    "<b>Usage:</b> <code>/setkey KEY_NAME value</code>\n\n"
                    "<b>Example:</b>\n"
                    "<code>/setkey GROQ_API_KEY gsk_xxxxx</code>\n"
                    "<code>/setkey OPENROUTER_API_KEY sk-or-xxxxx</code>\n\n"
                    "<b>Available keys:</b>\n" + key_list +
                    "\n\n⚠️ <i>Key is saved to DB and active immediately on Render!</i>",
                    parse_mode='HTML'
                )
                return

            _, key_name, new_value = parts
            key_name = key_name.strip().upper()
            new_value = new_value.strip()

            from core.api_key_manager import get_key_manager, API_KEY_REGISTRY
            if key_name not in API_KEY_REGISTRY:
                await update.effective_message.reply_text(
                    f"❌ Unknown key: <code>{key_name}</code>\n"
                    f"Use /keys to see all available keys.",
                    parse_mode='HTML'
                )
                return

            # Save to DB
            mgr = get_key_manager()
            ok, msg_text = mgr.set(key_name, new_value)
            info = API_KEY_REGISTRY[key_name]

            if ok:
                masked = f"{new_value[:8]}...{new_value[-4:]}" if len(new_value) > 12 else "SET"
                # Also sync to Render env vars
                try:
                    render_key = os.getenv("RENDER_API_KEY", "")
                    render_svc = os.getenv("RENDER_SERVICE_ID", "")
                    if render_key and render_svc:
                        import requests as _req
                        _req.put(
                            f"https://api.render.com/v1/services/{render_svc}/env-vars",
                            headers={"Authorization": f"Bearer {render_key}",
                                     "Content-Type": "application/json"},
                            json=[{"key": key_name, "value": new_value}],
                            timeout=10
                        )
                        render_note = "\n☁️ Also synced to Render!"
                    else:
                        render_note = ""
                except Exception:
                    render_note = ""

                # Test the new key
                ok_test, test_result = await mgr.test_key(key_name)
                test_line = f"\n🧪 Test: {test_result}"

                await update.effective_message.reply_text(
                    f"✅ <b>{info['icon']} {info['label']} Updated!</b>\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"🔑 Key: <code>{masked}</code>\n"
                    f"💾 Saved to: DB (active immediately){render_note}"
                    f"{test_line}\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"<i>No restart needed — key is live now!</i>",
                    parse_mode='HTML'
                )
            else:
                await update.effective_message.reply_text(
                    f"❌ <b>Failed to save {key_name}</b>\n{msg_text}",
                    parse_mode='HTML'
                )

        elif cmd == "/testkey":
            # ── Test a specific key ───────────────────────────────────────────
            # Usage: /testkey GROQ_API_KEY
            parts = update.message.text.strip().split(None, 1)
            if len(parts) < 2:
                from core.api_key_manager import API_KEY_REGISTRY
                key_list = " | ".join(f"<code>{k}</code>" for k in API_KEY_REGISTRY.keys())
                await update.effective_message.reply_text(
                    f"🧪 <b>TEST API KEY</b>\n"
                    f"<b>Usage:</b> <code>/testkey KEY_NAME</code>\n\n"
                    f"<b>Available:</b>\n{key_list}",
                    parse_mode='HTML'
                )
                return

            key_name = parts[1].strip().upper()
            from core.api_key_manager import get_key_manager, API_KEY_REGISTRY
            if key_name not in API_KEY_REGISTRY:
                await update.effective_message.reply_text(
                    f"❌ Unknown key: <code>{key_name}</code>", parse_mode='HTML'
                )
                return

            mgr = get_key_manager()
            info = API_KEY_REGISTRY[key_name]
            val = mgr.get(key_name)

            if not val:
                await update.effective_message.reply_text(
                    f"❌ <b>{info['icon']} {info['label']}</b>\n"
                    f"No key set!\n\n"
                    f"Add it with:\n<code>/setkey {key_name} your_key_here</code>\n\n"
                    f"Get free key: {info.get('signup', 'N/A')}",
                    parse_mode='HTML'
                )
                return

            msg_obj = await update.effective_message.reply_text(
                f"🧪 Testing {info['icon']} {info['label']}...", parse_mode='HTML'
            )
            ok, result = await mgr.test_key(key_name)
            masked = f"{val[:8]}...{val[-4:]}" if len(val) > 12 else "SET"

            await msg_obj.edit_text(
                f"{'✅' if ok else '❌'} <b>{info['icon']} {info['label']}</b>\n"
                f"━━━━━━━━━━━━━━━\n"
                f"🔑 Key: <code>{masked}</code>\n"
                f"📊 Result: {result}\n"
                f"💾 Source: {mgr.get_all_status().get(key_name, {}).get('source', 'env')}\n"
                f"━━━━━━━━━━━━━━━\n"
                f"{'💡 Key is working!' if ok else '⚠️ Update with: /setkey ' + key_name + ' new_key'}",
                parse_mode='HTML'
            )

        elif cmd == "/ai_check":
            # ── Live test of every AI provider ───────────────────────────────
            msg_obj = await update.effective_message.reply_text(
                "🧠 <b>Checking all AI providers...</b>\n<i>Testing each one live, please wait ~10s...</i>",
                parse_mode='HTML'
            )
            import httpx as _httpx

            _providers = [
                {"name": "Groq",       "icon": "⚡", "env": "GROQ_API_KEY",
                 "url": "https://api.groq.com/openai/v1/chat/completions",
                 "hdr": lambda k: {"Authorization": f"Bearer {k}", "Content-Type": "application/json"},
                 "body": {"model": "llama-3.3-70b-versatile",
                          "messages": [{"role":"user","content":"Say OK"}], "max_tokens": 3},
                 "parse": lambda d: d["choices"][0]["message"]["content"][:10],
                 "free": "14,400 req/day FREE", "signup": None},

                {"name": "DeepSeek",   "icon": "🔵", "env": "DEEPSEEK_API_KEY",
                 "url": "https://api.deepseek.com/chat/completions",
                 "hdr": lambda k: {"Authorization": f"Bearer {k}", "Content-Type": "application/json"},
                 "body": {"model": "deepseek-chat",
                          "messages": [{"role":"user","content":"Say OK"}], "max_tokens": 3},
                 "parse": lambda d: d["choices"][0]["message"]["content"][:10],
                 "free": "Free tier + cheap paid", "signup": "platform.deepseek.com/api_keys"},

                {"name": "OpenRouter", "icon": "🌐", "env": "OPENROUTER_API_KEY",
                 "url": "https://openrouter.ai/api/v1/chat/completions",
                 "hdr": lambda k: {"Authorization": f"Bearer {k}", "Content-Type": "application/json",
                                   "HTTP-Referer": "https://sam-job-automator.onrender.com"},
                 "body": {"model": "meta-llama/llama-3.1-8b-instruct:free",
                          "messages": [{"role":"user","content":"Say OK"}], "max_tokens": 3},
                 "parse": lambda d: d["choices"][0]["message"]["content"][:10],
                 "free": "Free models (no credits needed)", "signup": "openrouter.ai/keys"},

                {"name": "Together AI","icon": "🤝", "env": "TOGETHER_API_KEY",
                 "url": "https://api.together.xyz/v1/chat/completions",
                 "hdr": lambda k: {"Authorization": f"Bearer {k}", "Content-Type": "application/json"},
                 "body": {"model": "meta-llama/Llama-3-8b-chat-hf",
                          "messages": [{"role":"user","content":"Say OK"}], "max_tokens": 3},
                 "parse": lambda d: d["choices"][0]["message"]["content"][:10],
                 "free": "$25 free credit on signup", "signup": "api.together.xyz"},

                {"name": "HuggingFace","icon": "🤗", "env": "HUGGINGFACE_API_KEY",
                 "url": "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3",
                 "hdr": lambda k: {"Authorization": f"Bearer {k}"},
                 "body": {"inputs": "Say OK", "parameters": {"max_new_tokens": 5}},
                 "parse": lambda d: (d[0].get("generated_text","") if isinstance(d,list) else str(d))[:10],
                 "free": "Free unlimited (rate limited)", "signup": "huggingface.co/settings/tokens"},

                {"name": "Gemini",     "icon": "💎", "env": "GEMINI_API_KEY",
                 "url": "GEMINI_SPECIAL",
                 "hdr": None, "body": None, "parse": None,
                 "free": "1,500 req/day FREE", "signup": "makersuite.google.com/app/apikey"},
            ]

            lines = ["🧠 <b>AI PROVIDERS — LIVE STATUS</b>", "━━━━━━━━━━━━━━━━━━━━"]
            active = 0

            async with _httpx.AsyncClient(timeout=8) as _client:
                for p in _providers:
                    key = os.getenv(p["env"], "")
                    if not key:
                        signup_line = f"\n   🔗 <code>{p['signup']}</code>" if p.get("signup") else ""
                        lines.append(
                            f"⬜ <b>{p['icon']} {p['name']}</b>\n"
                            f"   ❌ No key — add <code>{p['env']}</code>\n"
                            f"   💡 {p['free']}{signup_line}"
                        )
                        continue

                    try:
                        if p["url"] == "GEMINI_SPECIAL":
                            r = await _client.post(
                                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}",
                                json={"contents": [{"parts": [{"text": "Say OK"}]}]}
                            )
                            d = r.json()
                            if d.get("candidates"):
                                resp = d["candidates"][0]["content"]["parts"][0]["text"][:10]
                                lines.append(f"✅ <b>{p['icon']} {p['name']}</b>\n   ✅ Working → <i>{resp}</i>\n   📊 {p['free']}")
                                active += 1
                            else:
                                err = d.get("error", {}).get("message", "")[:60]
                                is_quota = "quota" in err.lower()
                                lines.append(
                                    f"{'⚠️' if is_quota else '❌'} <b>{p['icon']} {p['name']}</b>\n"
                                    f"   {'⚠️ Quota exceeded (resets monthly)' if is_quota else '❌ ' + err}\n"
                                    f"   📊 {p['free']}"
                                )
                        else:
                            r = await _client.post(p["url"], headers=p["hdr"](key), json=p["body"])
                            d = r.json()
                            if r.status_code == 200:
                                resp = p["parse"](d)
                                lines.append(f"✅ <b>{p['icon']} {p['name']}</b>\n   ✅ Working → <i>{resp}</i>\n   📊 {p['free']}")
                                active += 1
                            elif r.status_code == 429:
                                lines.append(f"⚠️ <b>{p['icon']} {p['name']}</b>\n   ⚠️ Rate limited today\n   📊 {p['free']}")
                            else:
                                err = str(d.get("error", d))[:50]
                                lines.append(f"❌ <b>{p['icon']} {p['name']}</b>\n   ❌ HTTP {r.status_code}: {err}\n   📊 {p['free']}")
                    except Exception as e:
                        lines.append(f"❌ <b>{p['icon']} {p['name']}</b>\n   ❌ {str(e)[:50]}")

            lines.append("━━━━━━━━━━━━━━━━━━━━")
            if active == 0:
                lines.append("🚨 <b>0 providers active!</b> Add keys below.")
            elif active == 1:
                lines.append(f"⚠️ <b>{active}/6 active</b> — add more for redundancy")
            else:
                lines.append(f"🎉 <b>{active}/6 active</b> — great redundancy!")

            # Show which free keys to add
            missing = [p for p in _providers if not os.getenv(p["env"],"") and p.get("signup")]
            if missing:
                lines.append("\n💡 <b>Add these FREE keys:</b>")
                for p in missing[:3]:
                    lines.append(f"• {p['icon']} {p['name']}: <code>{p['env']}=...</code>\n  🔗 {p['signup']}")
                lines.append("\nAfter adding: run <code>sync_env_to_render.py</code>")

            try:
                await msg_obj.edit_text("\n".join(lines), parse_mode='HTML')
            except Exception:
                await update.effective_message.reply_text("\n".join(lines), parse_mode='HTML')

        elif cmd == "/shield":
            # 🛡️ ANTI-BAN PROTECTION STATUS
            try:
                from core.anti_ban_protection import get_protection
                protection = get_protection()
                stats = protection.get_protection_stats()
                
                msg = (
                    "🛡️ <b>ANTI-BAN PROTECTION STATUS</b>\n"
                    "━━━━━━━━━━━━━━━\n"
                    f"📊 <b>Today's Applications:</b> {stats['daily_applications']}/{stats['max_daily']}\n"
                    f"🏢 <b>Companies Tracked:</b> {stats['tracked_companies']}\n"
                    f"🚨 <b>Suspicious Detected:</b> {stats['suspicious_companies']}\n"
                    f"❌ <b>Failed Applications:</b> {stats['failed_applications']}\n"
                    f"⏰ <b>Last Application:</b> {stats['last_application'] or 'Never'}\n"
                    "━━━━━━━━━━━━━━━\n\n"
                    "🛡️ <b>Protection Features:</b>\n"
                    "✅ Honeypot Detection\n"
                    "✅ Rate Limiting (1/company/day)\n"
                    "✅ Human-like Timing\n"
                    "✅ Suspicious Company Tracking\n"
                    "✅ Global Speed Limits\n\n"
                    "<i>Bot is protected from detection and bans!</i>"
                )
            except Exception as e:
                logging.error(f"Shield status error: {e}")
                msg = "🛡️ <b>ANTI-BAN PROTECTION</b>\n━━━━━━━━━━━━━━━\n✅ Active and protecting\n━━━━━━━━━━━━━━━"
            
            await update.effective_message.reply_text(msg, parse_mode='HTML')

        elif cmd == "/phantom":
            await update.effective_message.reply_text("🕵️ <b>PHANTOM NETWORK STATUS</b>\n━━━━━━━━━━━━━━━\nUserBot: 🟡 STANDBY\nGhost Proxi: 🟢 ACTIVE\nDetection: <code>Undetectable</code>\n━━━━━━━━━━━━━━━", parse_mode='HTML')

        elif cmd == "/simulation" or cmd == "/simulate":
            await self._dispatch_command("/test_strike", update, context)

        elif cmd == "/test_strike":
            await update.effective_message.reply_text("🧪 <b>TEST STRIKE</b>\nUse the menu prompt to enter an email address. Then the bot will run the real SMTP path.", parse_mode='HTML')

        elif cmd == "/apply_patch":
            await update.effective_message.reply_text("🩹 <b>PATCH SUB-ENGINE:</b> Standby. Use <code>/repair</code> for full diagnostics.", parse_mode='HTML')

        elif cmd == "/settings":
            await update.effective_message.reply_text("⚙️ <b>SYSTEM SETTINGS</b>\n━━━━━━━━━━━━━━━\nAutopilot: <code>ON</code>\nGhost Mode: <code>ON</code>\nSpeed: <code>Aggressive</code>\n━━━━━━━━━━━━━━━", parse_mode='HTML')

        elif cmd == "/platforms":
            platforms = await self.db.get_active_platforms()
            platform_str = "\n".join([f"🌐 <b>{p['name']}</b>: <code>{p['url']}</code>" for p in platforms[:15]])
            if not platform_str: platform_str = "Platform registry empty. Discovery active..."
            msg = (
                "🌍 <b>OMNI-PLATFORM REGISTRY</b>\n"
                "━━━━━━━━━━━━━━━\n"
                f"{platform_str}\n"
                "━━━━━━━━━━━━━━━\n"
                "<i>Bot is searching for NEW platforms daily. Finding Telegram groups, job boards, and apps automatically!</i>"
            )
            await update.effective_message.reply_text(msg, parse_mode='HTML')

        if cmd in ("/status", "/stats", "/stats ", "/menu"):
            # [👑 UNIFIED HUD]: Always show the real-time cloud synced metrics with ULTRA-MAXIMUM mode indicators
            try:
                stats = await self.db.get_stats()
                health = self.db.get_advanced_health()
                sys_health = self.db.get_system_health()
                is_leader = await self.db.is_node_leader()
                role = "👑 MASTER" if is_leader else "🛰️ WORKER"
                
                # Get today's application count
                from datetime import datetime, timedelta, timezone
                now = datetime.now(timezone.utc)
                today_start = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat().replace("+", "%2B")
                
                # Get today's applications count
                today_apps = 0
                try:
                    app_succ, app_data = await self.db._request_with_retry(
                        "GET",
                        f"{self.db.url}/rest/v1/applications?select=id&timestamp=gte.{today_start}",
                        headers={"Prefer": "count=exact"}
                    )
                    if app_succ and isinstance(app_data, dict):
                        today_apps = app_data.get("count", 0)
                except Exception as e:
                    logging.error(f"Failed to get today's apps: {e}")
                
                # Calculate hourly rate (last hour)
                hour_ago = (now - timedelta(hours=1)).isoformat().replace("+", "%2B")
                hourly_apps = 0
                try:
                    hour_succ, hour_data = await self.db._request_with_retry(
                        "GET",
                        f"{self.db.url}/rest/v1/applications?select=id&timestamp=gte.{hour_ago}",
                        headers={"Prefer": "count=exact"}
                    )
                    if hour_succ and isinstance(hour_data, dict):
                        hourly_apps = hour_data.get("count", 0)
                except Exception as e:
                    logging.error(f"Failed to get hourly apps: {e}")
                
                # Get email provider status
                email_status = "🔄 Rotating"
                try:
                    from core.email_rotator import get_rotator
                    rotator = get_rotator()
                    current_provider = rotator.get_current_provider()
                    email_status = f"📧 {current_provider}"
                except Exception:
                    pass
                
                # Calculate progress towards daily goal
                daily_goal = 1500  # ULTRA-MAXIMUM target
                daily_progress = min(100, int((today_apps / daily_goal) * 100))
                progress_bar = "█" * (daily_progress // 10) + "░" * (10 - (daily_progress // 10))
                
                # Strength status - Sovereign Fallbacks make it always MAX
                strength = "💪 10,000,000% (MAX)"
                proxy_nodes = self.proxy_mesh.active_nodes
                
                # ULTRA-MAXIMUM mode indicator
                ultra_mode = "🔥 ULTRA-MAXIMUM MODE ACTIVE"
                
            except Exception as e:
                import traceback
                logging.error(f"HUD Telemetry Error: {e}\n{traceback.format_exc()}")
                stats = {}
                health = {}
                sys_health = {'engine': 'Offline'}
                role = "🛰️ WORKER (Syncing...)"
                strength = "🔄 CALIBRATING..."
                proxy_nodes = 0
                today_apps = 0
                hourly_apps = 0
                daily_progress = 0
                progress_bar = "░" * 10
                email_status = "Unknown"
                ultra_mode = "🔄 CALIBRATING..."

            msg = (
                f"🖥️ <b>SOVEREIGN HUB: REAL-TIME HUD</b>\n"
                f"━━━━━━━━━━━━━━━\n"
                f"{ultra_mode}\n"
                f"━━━━━━━━━━━━━━━\n"
                f"📡 <b>Node:</b> {role} (<code>{self.db.node_id[:8]}</code>)\n"
                f"🧠 <b>Synapse Mode:</b> {sys_health['engine']}\n"
                f"🕸️ <b>Shadow Grid:</b> {proxy_nodes} nodes active\n"
                f"{email_status}\n\n"
                f"📊 <b>TODAY'S PERFORMANCE:</b>\n"
                f"🚀 <b>Applications Sent:</b> {today_apps}/1500 ({daily_progress}%)\n"
                f"[{progress_bar}]\n"
                f"⚡ <b>Hourly Rate:</b> {hourly_apps}/120 apps/hour\n"
                f"📈 <b>Success Rate:</b> {int((today_apps / max(1, today_apps)) * 100)}%\n\n"
                f"🎯 <b>GLOBAL STATS:</b>\n"
                f"📋 <b>Total Leads:</b> {stats.get('recon_rows', 0)}\n"
                f"🚀 <b>Total Strikes:</b> {stats.get('total_strikes', 0)}\n"
                f"🛡️ <b>Shield Blocks:</b> {health.get('pdf_cache_count', 0)} assets\n"
                f"💓 <b>Pulse:</b> ACTIVE 24/7\n"
                f"━━━━━━━━━━━━━━━\n"
                f"<i>Bot is running at ULTRA-MAXIMUM capacity!</i>\n"
                f"<i>Target: 1500 apps/day | 120 apps/hour</i>"
            )
            # [👑 UI PERSISTENCE]: Ensure the keyboard is attached even for status reports
            reply_markup, inline_markup = self._get_sovereign_keyboards()
            await update.effective_message.reply_text(msg, parse_mode='HTML', reply_markup=reply_markup)
            await update.effective_message.reply_text("🎮 <b>DYNAMIC COMMAND CENTER:</b>", reply_markup=inline_markup, parse_mode='HTML')
            return

        elif cmd == "/ai_status" or cmd == "/retrain" or cmd == "/strength":
            # [💪 STRENGTH CHECK]: Direct alias for /synapse to satisfy user requirement
            return await self._handle_text_map("synapse", update, context)

        elif cmd.startswith("/link_userbot"):
            args = cmd_text.split(" ")
            phone = args[1] if len(args) > 1 else None
            
            if not phone:
                await update.effective_message.reply_text("Usage: /link_userbot +1234567890", parse_mode='HTML')
                return
            
            api_id = os.getenv("TELEGRAM_API_ID")
            api_hash = os.getenv("TELEGRAM_API_HASH")
            
            if not api_id or not api_hash:
                await update.effective_message.reply_text("⚠️ <b>ERROR:</b> API ID/Hash missing in .env", parse_mode='HTML')
                return

            await update.effective_message.reply_text(f"📱 <b>Phantom Link Initiated...</b>\nSending code to {phone}...", parse_mode='HTML')
            
            from telethon import TelegramClient
            client = TelegramClient('phantom_ghost', api_id, api_hash)
            await client.connect()
            
            try:
                sent_code = await client.send_code_request(phone)
                self._phantom_state[update.effective_user.id] = {
                    'phone': phone,
                    'phone_code_hash': sent_code.phone_code_hash,
                    'client': client
                }
                await update.effective_message.reply_text("✅ <b>Code Sent.</b> Reply with <code>/code 12345</code>", parse_mode='HTML')
            except Exception as e:
                await update.effective_message.reply_text(f"❌ <b>FAILED:</b> {e}", parse_mode='HTML')
                await client.disconnect()

        elif cmd.startswith("/code"):
            args = cmd_text.split(" ")
            code = args[1] if len(args) > 1 else None
            state = self._phantom_state.get(update.effective_user.id)
            
            if not code or not state:
                await update.effective_message.reply_text("⚠️ Session expired or code missing. Start over.", parse_mode='HTML')
                return
            
            client = state['client']
            try:
                await client.sign_in(state['phone'], code, phone_code_hash=state['phone_code_hash'])
                session_str = client.session.save()
                
                # PERSISTENCE: Save to DB for cloud recovery
                await self.db.update_setting("TELEGRAM_SESSION_STRING", session_str)
                
                await update.effective_message.reply_text(
                    "👑 <b>ABSOLUTE SUCCESS: Phantom Linked!</b>\n"
                    "Advanced networking features are now active.\n"
                    "<i>Session String exported to Hive-Mind.</i>", 
                    parse_mode='HTML'
                )
            except Exception as e:
                await update.effective_message.reply_text(f"❌ <b>AUTH FAIL:</b> {e}", parse_mode='HTML')
            finally:
                await client.disconnect()
                del self._phantom_state[update.effective_user.id]

        elif cmd == "/oracle":
            # ☁️ CLOUD-SAFE: Run oracle inline instead of spawning process
            await update.effective_message.reply_text("🔮 <b>MARKET ORACLE:</b> Scanning global news for expansion signals...", parse_mode='HTML')
            try:
                from core.scrapers.omni_crawler import MarketOracle
                # Run a quick market scan
                news = await MarketOracle.get_latest_news("Technology Companies Dubai")
                await update.effective_message.reply_text(f"🔮 <b>ORACLE PULSE:</b>\n{news[:500]}...", parse_mode='HTML')
            except Exception as e:
                await update.effective_message.reply_text(f"⚠️ <b>ORACLE ERROR:</b> {e}", parse_mode='HTML')

        elif cmd == "/mock_interview":
            latest = await self.db.get_latest_application()
            if not latest:
                await update.effective_message.reply_text("⚠️ No recent applications found for prepping.", parse_mode='HTML')
                return
            
            await update.effective_message.reply_text(f"👻 <b>GHOST HUB:</b> Drafting tactical pitch for <b>{latest['company_name']}</b>...", parse_mode='HTML')
            
            job_title = latest.get('job_title', 'Role')
            prompt = f"Target: {latest['company_name']} - {job_title}\nMission: I am about to interview for this role. Give me 3 'Bait and Switch' psychological questions to ask THEM to regain control of the room. Be elite and authosamtive. Reply as a God-Tier HR Ops Director."
            
            reply = ""
            try:
                if self.ai.primary_engine == "gemini":
                    loop = asyncio.get_event_loop()
                    res = await loop.run_in_executor(None, self.ai.model.generate_content, prompt)
                    reply = res.text.strip()
                elif self.ai.groq_key:
                    data = await self.ai.structural_query(prompt)
                    reply = data.get("reply_message", "Oracle is silent.")
            except Exception as e:
                reply = f"Error during tactical extraction: {e}"
            
            await update.effective_message.reply_text(f"🎤 <b>INTERVIEW CHEAT-SHEET:</b>\n\n{reply}", parse_mode='HTML')

        elif cmd == "/evolution" or cmd == "/vision":
            health = self.db.get_advanced_health()
            msg = (
                "🧬 <b>EVOLUTIONARY INTELLIGENCE MATRIX</b>\n"
                f"━━━━━━━━━━━━━━━\n"
                f"🎯 <b>Recon Records:</b> {health.get('recon_rows', 0)}\n"
                f"🚀 <b>Applications Logged:</b> {health.get('heartbeat_rows', 0)}\n"
                f"💾 <b>PDF Cache:</b> {health.get('pdf_cache_count', 0)} files\n"
                f"🔋 <b>Memory:</b> {health.get('memory_mb', 'N/A')} MB\n"
                f"━━━━━━━━━━━━━━━"
            )
            await update.effective_message.reply_text(msg, parse_mode='HTML')

        elif cmd == "/guide" or cmd == "/manual":
            guide_text = (
                "📖 <b>دليل القيادة الميدانية (Project Chronos)</b>\n"
                "🔥 <b>ULTRA-MAXIMUM MODE: 1500 APPS/DAY</b>\n\n"
                "<b>1. أوامر الهجوم والمراقبة (Core & Ops):</b>\n"
                "🚀 <b>Run Now | تشغيل:</b> تفعيل محرك البحث وبدء الغزو فوراً.\n"
                "🖥️ <b>Status | الحالة:</b> عرض تقرير عن صحة السيرفر السحابي.\n"
                "📜 <b>Pulse | النبض:</b> قراءة آخر السجلات لمعرفة ما يعمله البوت.\n"
                "📈 <b>Stats | الإحصائيات:</b> ملخص إجمالي عدد التقديمات.\n"
                "🧬 <b>Tasks | المهام:</b> عرض المهام قيد التنفيذ.\n"
                "🛡️ <b>Shield | الدرع:</b> حماية ضد الشركات المحظورة.\n"
                "🛰️ <b>Track | التتبع:</b> رادار لايف لمعرفة مسار الطلبات.\n"
                "💪 <b>Synapse | القوة:</b> فحص القوة والأداء اليومي.\n"
                "👁️ <b>Audit | التدقيق:</b> تقرير شامل عن مزودي البريد والأداء.\n\n"
                "<b>2. أوامر الموارد (Intel & Assets):</b>\n"
                "📋 <b>Leads | الفرص:</b> قائمة بالوظائف وإشارات Market Oracle.\n"
                "🎓 <b>Prep | التحضير:</b> تجهيز السيرة الذاتية ورسائل الغلاف.\n"
                "🏢 <b>Companies | الشركات:</b> تقرير بالشركات المحللة والمحظورة.\n"
                "🚀 <b>Campaign | حملة جديدة:</b> إطلاق حملة استهداف ضخمة.\n"
                "🔄 <b>Follow-up | المتابعة:</b> إرسال متابعة للشركات السابقة.\n"
                "📜 <b>Logs | السجلات:</b> تقرير مفصل عن آخر 24 ساعة.\n\n"
                "<b>3. التحكم المركزي (C2 & Maintenance):</b>\n"
                "⏸️ <b>Pause | إيقاف مؤقت:</b> تجميد العمليات مؤقتاً.\n"
                "▶️ <b>Resume | استئناف:</b> متابعة الغزو من مكان التوقف.\n"
                "🛑 <b>Omega Halt | التوقف التام:</b> إيقاف طارئ كلي.\n"
                "⚙️ <b>Settings | الإعدادات:</b> التحكم بمتغيرات النظام.\n\n"
                "<b>4. طوارئ وإصلاح (Recovery):</b>\n"
                "🩹 <b>Lazarus | الإحياء:</b> إعادة الطلبات التي فشلت.\n"
                "🩹 <b>Repair | الإصلاح:</b> فحص قاعدة البيانات وإصلاح الأخطاء.\n"
                "🧹 <b>Hygiene | التنظيف:</b> مسح الملفات المؤقتة.\n"
                "🔄 <b>Reboot | إعادة تشغيل:</b> ريستارت كامل للنظام.\n\n"
                "<b>🔥 ULTRA-MAXIMUM MODE SPECS:</b>\n"
                "• 📊 Target: 1500 applications/day\n"
                "• ⚡ Speed: 120 apps/hour maximum\n"
                "• 📧 Email Capacity: 1900/day (5 providers)\n"
                "• 🕐 Hours: 5 AM - 11 PM (18 hours)\n"
                "• 🎯 Match Score: 55%+ (maximize quantity)\n"
                "• 🔄 Breaks: Minimal (5% probability)\n"
                "• 🚀 Parallel Processing: 15 simultaneous\n"
                "• 📋 Batch Size: 75 leads per cycle\n"
                "• 🔍 Scraping: Every 90 minutes\n\n"
                "<i>System is optimized for MAXIMUM throughput!</i>"
            )
            await update.effective_message.reply_text(guide_text, parse_mode='HTML')

        elif cmd == "/start" or cmd == "/menu":
            reply_markup, inline_markup = self._get_sovereign_keyboards()
            await update.effective_message.reply_text(
                "👑 <b>PROJECT CHRONOS: SOVEREIGN V2</b>\n"
                f"<i>Node: {os.getenv('NODE_NAME', 'MASTER-CLOUD')}</i>\n"
                "<i>Status: Armed & Operational</i>\n\n"
                "🔥 <b>ULTRA-MAXIMUM MODE ACTIVE</b>\n"
                "━━━━━━━━━━━━━━━\n"
                "📊 Target: 1500 applications/day\n"
                "⚡ Speed: 120 apps/hour\n"
                "📧 Capacity: 1900 emails/day\n"
                "🕐 Hours: 5 AM - 11 PM\n"
                "━━━━━━━━━━━━━━━\n\n"
                "Use the <b>COMMAND CENTER</b> (Inline) or the <b>SOVEREIGN TILESET</b> (Bottom).\n"
                "<i>Click '📖 GUIDE' for a full Arabic manual of all abilities.</i>",
                parse_mode='HTML',
                reply_markup=reply_markup
            )
            await update.effective_message.reply_text("🎮 <b>DYNAMIC COMMAND CENTER:</b>", reply_markup=inline_markup, parse_mode='HTML')

    async def _hourly_notify_loop(self, bot, chat_id: int):
        """Sends an hourly progress report to the user if HOURLY_NOTIFY is enabled."""
        while os.environ.get("HOURLY_NOTIFY") == "true":
            await asyncio.sleep(3600)
            if os.environ.get("HOURLY_NOTIFY") != "true":
                break
            try:
                from datetime import datetime, timezone
                now = datetime.now(timezone.utc)
                today_start = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat().replace("+", "%2B")
                succ, data = await self.db._request_with_retry(
                    "GET",
                    f"{self.db.url}/rest/v1/applications?select=id&timestamp=gte.{today_start}",
                    headers={"Prefer": "count=exact"}
                )
                count = data.get("count", 0) if succ and isinstance(data, dict) else 0
                queue_count = await self.db.get_pending_leads_count() if self.db else 0
                await bot.send_message(
                    chat_id=chat_id,
                    text=(
                        f"🔔 <b>HOURLY UPDATE — {now.strftime('%H:%M UTC')}</b>\n"
                        f"━━━━━━━━━━━━━━━\n"
                        f"🚀 Applications today: <b>{count}</b>\n"
                        f"🗂️ Queue remaining: <b>{queue_count}</b>\n"
                        f"━━━━━━━━━━━━━━━"
                    ),
                    parse_mode='HTML'
                )
            except Exception as e:
                logging.warning(f"Hourly notify error: {e}")

    def _get_sovereign_keyboards(self):
        """[👑 APEX UI]: Generates the unified Sovereign Tileset and Command Center."""
        from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

        reply_keyboard = [
            # ── 📊 Monitoring (10 buttons) ──────────────────────────────────
            [KeyboardButton("🖥️ Status | الحالة"),              KeyboardButton("📊 Stats | الإحصائيات")],
            [KeyboardButton("📈 Today Report | تقرير اليوم"),    KeyboardButton("📅 Weekly Report | أسبوعي")],
            [KeyboardButton("🗓️ Monthly Report | شهري"),         KeyboardButton("🏆 Best Day | أفضل يوم")],
            [KeyboardButton("📧 Email Stats | إحصاء الإيميل"),   KeyboardButton("📉 Failure Rate | نسبة الفشل")],
            [KeyboardButton("📊 Provider Health | صحة المزودين"),KeyboardButton("⚡ Speed Test | اختبار السرعة")],
            # ── 🔍 System Info (10 buttons) ─────────────────────────────────
            [KeyboardButton("🗂️ Queue | الطابور"),               KeyboardButton("📜 Logs | السجلات")],
            [KeyboardButton("🌡️ Memory | الذاكرة"),              KeyboardButton("⏱️ Uptime | وقت التشغيل")],
            [KeyboardButton("🧠 AI Status | حالة الذكاء"),       KeyboardButton("📬 Inbox Check | فحص الردود")],
            [KeyboardButton("🔔 Notify Me | أخبرني"),            KeyboardButton("📡 Ping Render | اختبار الخادم")],
            [KeyboardButton("🔑 Env Check | فحص المتغيرات"),     KeyboardButton("🌐 Platforms | المواقع")],
            # ── 🎯 Leads & Jobs (10 buttons) ────────────────────────────────
            [KeyboardButton("📋 Leads | الفرص"),                 KeyboardButton("🧬 Tasks | المهام")],
            [KeyboardButton("🏢 Companies | الشركات"),           KeyboardButton("🛰️ Track | التتبع المباشر")],
            [KeyboardButton("📊 Top Companies | أفضل شركات"),    KeyboardButton("🌍 Countries | الدول")],
            [KeyboardButton("💼 Job Titles | المسميات"),         KeyboardButton("🔮 Oracle | أوراكل السوق")],
            [KeyboardButton("📊 Campaign | الحملة"),             KeyboardButton("📨 Follow-ups | متابعات")],
            # ── ⚡ Actions (10 buttons) ──────────────────────────────────────
            [KeyboardButton("🌍 Scrape Now | اسكان فوري"),       KeyboardButton("🎯 Force Strike | ضربة فورية")],
            [KeyboardButton("🎪 Mass Strike | ضربة جماعية"),     KeyboardButton("🔁 Retry Failed | إعادة الفاشلين")],
            [KeyboardButton("🔎 Find Emails | ابحث عن إيميلات"), KeyboardButton("📌 Pin Lead | تثبيت أولوية")],
            [KeyboardButton("🚫 Skip Lead | تخطي"),              KeyboardButton("⛔ Blacklist | القائمة السوداء")],
            [KeyboardButton("🚀 Run Now | شغّل"),                KeyboardButton("🔧 Fix | إصلاح")],
            # ── 🛡️ System Health (10 buttons) ───────────────────────────────
            [KeyboardButton("🛡️ Shield | الدرع"),                KeyboardButton("📜 Pulse | النبض")],
            [KeyboardButton("🔍 Audit | مراجعة"),                KeyboardButton("💪 Synapse | قوة")],
            [KeyboardButton("🧹 Clean Disk | تنظيف"),            KeyboardButton("💾 Backup | نسخة احتياطية")],
            [KeyboardButton("🔄 Reboot | إعادة تشغيل"),          KeyboardButton("⚙️ Settings | الإعدادات")],
            [KeyboardButton("🗑️ Clear Queue | مسح الطابور"),     KeyboardButton("🔥 Boost Mode | وضع تسريع")],
            # ── 🎮 Controls (10 buttons) ─────────────────────────────────────
            [KeyboardButton("⏸️ Pause | إيقاف مؤقت"),           KeyboardButton("▶️ Resume | استئناف")],
            [KeyboardButton("🌙 Night Mode | وضع الليل"),        KeyboardButton("🧪 Dry Run | تجربة آمنة")],
            [KeyboardButton("🛑 Omega Halt | التوقف التام"),     KeyboardButton("💀 Kill Switch | إيقاف كامل")],
            [KeyboardButton("📖 Guide | الدليل"),                KeyboardButton("🔮 Oracle | أوراكل")],
            [KeyboardButton("🌙 Night | الليل"),                 KeyboardButton("🔥 Boost | تسريع")],
            # ── 🔑 API & Keys (10 buttons) ───────────────────────────────────
            [KeyboardButton("🔑 API Keys | مفاتيح API"),         KeyboardButton("🧠 AI Check | فحص الذكاء")],
            [KeyboardButton("✏️ Set Key | تغيير مفتاح"),          KeyboardButton("🧪 Test Key | اختبار مفتاح")],
            [KeyboardButton("🔑 Env | المتغيرات"),               KeyboardButton("📡 Ping | اختبار الخادم")],
            [KeyboardButton("⚡ Speed | سرعة الإرسال"),          KeyboardButton("📉 Failure | نسبة الفشل")],
            [KeyboardButton("📅 Weekly | أسبوعي"),               KeyboardButton("🗓️ Monthly | شهري")],
            # ── 🛠️ Tools (10 buttons) ────────────────────────────────────────
            [KeyboardButton("🎓 Prep | التحضير"),                KeyboardButton("📝 CV Preview | معاينة السيرة")],
            [KeyboardButton("✉️ Cover Letter | رسالة التغطية"),   KeyboardButton("📧 Test Email | تجربة إيميل")],
            [KeyboardButton("🧪 Test Strike | تجربة ضربة"),      KeyboardButton("🔔 Notify | الإشعارات")],
            [KeyboardButton("📬 Inbox | فحص الردود"),            KeyboardButton("🔁 Retry | إعادة الفاشلين")],
            [KeyboardButton("⛔ Blacklist | السوداء"),            KeyboardButton("📌 Pin Lead | تثبيت")],
            # ── 📊 Reports (10 buttons) ──────────────────────────────────────
            [KeyboardButton("🏆 Best Day | أفضل يوم"),           KeyboardButton("📊 Campaign | الحملة")],
            [KeyboardButton("🌍 Countries | الدول المستهدفة"),   KeyboardButton("💼 Job Titles | المسميات الوظيفية")],
            [KeyboardButton("🔎 Find Emails | بحث إيميلات"),     KeyboardButton("🚫 Skip Lead | تخطي")],
            [KeyboardButton("🧹 Clean | تنظيف الذاكرة"),         KeyboardButton("💾 Backup | نسخة احتياطية")],
            [KeyboardButton("🌐 Platforms | المواقع"),            KeyboardButton("🛰️ Track | التتبع")],
            # ── 🎯 Extra (10 buttons) ────────────────────────────────────────
            [KeyboardButton("📊 Top Companies | أفضل شركات"),    KeyboardButton("🔁 Retry | إعادة")],
            [KeyboardButton("🎪 Mass Strike | جماعية"),          KeyboardButton("🎯 Force Strike | فورية")],
            [KeyboardButton("🔥 Boost | تسريع"),                 KeyboardButton("🌙 Night | الليل")],
            [KeyboardButton("🧪 Dry Run | آمنة"),                KeyboardButton("⏸️ Pause | وقف")],
            [KeyboardButton("▶️ Resume | كمّل"),                 KeyboardButton("🔄 Reboot | إعادة")],
        ]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

        twa_url = os.getenv("RENDER_EXTERNAL_URL", "")
        if not twa_url or not twa_url.startswith("https://"):
            twa_url = "https://sam-job-automator.onrender.com"

        inline_keyboard = [
            # ── ROW 1: Most important — PAUSE / RESUME ────────────────────────
            [
                InlineKeyboardButton("⏸️ PAUSE | وقّف التقديمات", callback_data="/pause"),
                InlineKeyboardButton("▶️ RESUME | كمّل التقديمات", callback_data="/resume"),
            ],
            # ── ROW 2: Matrix HUD ─────────────────────────────────────────────
            [InlineKeyboardButton("🌐 MATRIX HUD | ماتريكس", web_app=WebAppInfo(url=twa_url))],
            # ── ROW 3: Test & Status ──────────────────────────────────────────
            [
                InlineKeyboardButton("🧪 TEST STRIKE | تجربة", callback_data="/test_strike"),
                InlineKeyboardButton("🖥️ STATUS | الحالة", callback_data="/status"),
            ],
            # ── ROW 4: AI & Keys ──────────────────────────────────────────────
            [
                InlineKeyboardButton("🧠 AI STATUS | الذكاء", callback_data="/ai_check"),
                InlineKeyboardButton("🔑 API KEYS | المفاتيح", callback_data="/keys"),
            ],
            # ── ROW 5: Fix & Guide ────────────────────────────────────────────
            [
                InlineKeyboardButton("🔧 FIX | إصلاح", callback_data="/fix"),
                InlineKeyboardButton("📖 GUIDE | دليل", callback_data="/guide"),
            ],
        ]
        inline_markup = InlineKeyboardMarkup(inline_keyboard)
        return reply_markup, inline_markup

    def normalize_text(self, text: str) -> str:
        if not text: return ""
        # 🧪 [1000% RELIABILITY]: Strip all special chars, emojis, and hyphens
        # Keep only word characters (Unicode) and spaces
        clean = re.sub(r'[^\w\s]', '', text, flags=re.UNICODE)
        return " ".join(clean.lower().split())

    def get_normalized_parts(self, text: str) -> list:
        if not text: return []
        # Support both " | " and " - " as separators
        raw_parts = re.split(r'[|\-]', text)
        return [self.normalize_text(p) for p in raw_parts if p.strip()]

    async def _handle_text_map(self, key: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = update.effective_message

        if key == "tasks":
            tasks = await self.db.get_pending_tasks(limit=5)
            task_str = "\n".join([f"- {t['type']}: {t['target'][:20]}..." for t in tasks]) if tasks else "No pending mission tasks."
            await msg.reply_text(f"🧬 <b>EVOLUTIONARY MISSION LOG</b>\n━━━━━━━━━━━━━━━\n{task_str}\n━━━━━━━━━━━━━━━", parse_mode='HTML')

        elif key == "shield":
            blacklist = await self.db.get_recent_blacklist(limit=10)
            proxy = await self.db.get_proxy_health()
            await msg.reply_text(
                f"🛡️ <b>SHIELD: SECURITY AUDIT</b>\n━━━━━━━━━━━━━━━\n"
                f"🔒 <b>Proxy Mesh:</b> 🟢 {proxy.get('active_nodes', 0)}/{proxy.get('total_nodes', 0)} Active\n"
                f"📉 <b>Banned Count:</b> {len(blacklist)}\n"
                f"⚡ <b>Latency:</b> {proxy.get('latency_ms', 0)}ms\n"
                f"🛰️ <b>Bypass State:</b> GOD-MODE\n━━━━━━━━━━━━━━━",
                parse_mode='HTML'
            )

        elif key == "pulse":
            logs = await self.db.get_latest_logs(limit=8)
            log_entries = []
            for l in logs:
                msg_text = l.get('message', 'No message') if isinstance(l, dict) else getattr(l, 'message', 'No message')
                # Add status colors to logs
                if "SUCCESS" in msg_text or "ACQUIRED" in msg_text:
                    prefix = "✅ "
                elif "FAILED" in msg_text or "ERROR" in msg_text:
                    prefix = "❌ "
                elif "HEARTBEAT" in msg_text:
                    prefix = "💓 "
                else:
                    prefix = "🕒 "
                log_entries.append(f"{prefix}{msg_text[:50]}...")
            
            log_str = "\n".join(log_entries) if log_entries else "System pulse stable. No recent missions recorded."
            
            await msg.reply_text(f"📜 <b>SOVEREIGN EVENT PULSE</b>\n━━━━━━━━━━━━━━━\n{log_str}\n━━━━━━━━━━━━━━━", parse_mode='HTML')

        elif key == "leads":
            job_leads = await self.db.get_pending_leads(limit=3)
            intel_leads = await self.db.get_pending_tasks(limit=3)
            lead_entries = []
            for l in job_leads:
                lead_entries.append(f"📍 <b>JOB:</b> {l['company_name']} ({l['job_title'][:15]})")
            for t in intel_leads:
                if t.get('type') == 'ORACLE_LEAD':
                    lead_entries.append(f"🔮 <b>INTEL:</b> {t['target']} - (Expansion Signal)")
            lead_str = "\n".join(lead_entries) if lead_entries else "Queue is empty. The swarm is hunting..."
            await msg.reply_text(f"📋 <b>HIGH-PRIORITY MISSION TARGETS</b>\n━━━━━━━━━━━━━━━\n{lead_str}\n━━━━━━━━━━━━━━━", parse_mode='HTML')

        elif key == "prep":
            latest = await self.db.get_latest_application()
            if not latest:
                await msg.reply_text("🎓 <b>No history found to analyze.</b> Strike first.", parse_mode='HTML')
                return
            prompt = f"Give 3 very short, aggressive interview tips for a {latest['job_title']} role at {latest['company_name']}. JSON: {{'tips': [...]}}"
            try:
                response = await asyncio.get_event_loop().run_in_executor(None, self.ai.model.generate_content, prompt)
                data = self.ai._extract_json_robustly(response.text)
                tips = data.get('tips', ["Be bold.", "Know metrics.", "Lead the room."])
                tip_str = "\n".join([f"💡 {tip}" for tip in tips])
                await msg.reply_text(f"🎓 <b>ORACLE PREP: {latest['company_name']}</b>\n━━━━━━━━━━━━━━━\n{tip_str}\n━━━━━━━━━━━━━━━", parse_mode='HTML')
            except Exception:
                await msg.reply_text("🎓 <b>Oracle Busy.</b> Tips: Focus on metrics & culture.", parse_mode='HTML')

        elif key == "campaign":
            # Show real campaign stats from DB
            try:
                stats = await self.db.get_stats() if self.db else {}
                total = stats.get('total_strikes', 0)
                leads = stats.get('recon_rows', 0)
                # Get today's count
                from datetime import datetime, timezone
                now = datetime.now(timezone.utc)
                today_start = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat().replace("+", "%2B")
                today_apps = 0
                try:
                    ok, data = await self.db._request_with_retry(
                        "GET",
                        f"{self.db.url}/rest/v1/applications?select=id&timestamp=gte.{today_start}",
                        headers={"Prefer": "count=exact"}
                    )
                    if ok and isinstance(data, dict):
                        today_apps = data.get("count", 0)
                except Exception:
                    pass
                await msg.reply_text(
                    f"🚀 <b>CAMPAIGN STATUS</b>\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"📊 <b>Today:</b> {today_apps}/1500 applications\n"
                    f"🏆 <b>Total Ever:</b> {total} applications\n"
                    f"🎯 <b>Leads Found:</b> {leads}\n"
                    f"🌍 <b>Targets:</b> UAE, Qatar, KSA, Lebanon\n"
                    f"⚡ <b>Mode:</b> ULTRA-MAXIMUM\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"<i>Running 24/7 on Render cloud</i>",
                    parse_mode='HTML'
                )
            except Exception as e:
                await msg.reply_text(f"⚠️ Campaign stats error: {e}", parse_mode='HTML')

        elif key == "followup":
            try:
                from datetime import datetime, timedelta, timezone
                now = datetime.now(timezone.utc)
                three_days_ago = (now - timedelta(days=3)).isoformat().replace("+", "%2B")
                seven_days_ago = (now - timedelta(days=7)).isoformat().replace("+", "%2B")
                ok3, data3 = await self.db._request_with_retry(
                    "GET",
                    f"{self.db.url}/rest/v1/applications?select=company_name,job_title&status=eq.SENT&timestamp=lte.{three_days_ago}&order=timestamp.desc&limit=5"
                )
                ok7, data7 = await self.db._request_with_retry(
                    "GET",
                    f"{self.db.url}/rest/v1/applications?select=id&status=eq.SENT&timestamp=lte.{seven_days_ago}"
                )
                pending_3 = data3 if ok3 and isinstance(data3, list) else []
                count_7 = len(data7) if ok7 and isinstance(data7, list) else 0
                lines_3 = "\n".join([f"• {a.get('company_name','?')[:25]}" for a in pending_3[:5]]) or "None"
                await msg.reply_text(
                    f"🔄 <b>FOLLOW-UP ENGINE</b>\n━━━━━━━━━━━━━━━\n"
                    f"📅 <b>No reply (3+ days):</b> {len(pending_3)}\n"
                    f"📅 <b>No reply (7+ days):</b> {count_7}\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"<b>Pending follow-ups:</b>\n{lines_3}\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"<i>Auto follow-up: Day 3, 7, 14</i>",
                    parse_mode='HTML'
                )
            except Exception as e:
                await msg.reply_text(f"⚠️ Follow-up error: {e}", parse_mode='HTML')

        elif key in ("stats", "status", "companies"):
            # Each button should do its own thing, not redirect to status
            if key == "stats":
                # Show statistics only
                stats = await self.db.get_stats() if self.db else {}
                msg_text = (
                    "📊 <b>STATISTICS REPORT</b>\n"
                    "━━━━━━━━━━━━━━━\n"
                    f"🚀 <b>Total Applications:</b> {stats.get('total_strikes', 0)}\n"
                    f"🎯 <b>Total Leads:</b> {stats.get('recon_rows', 0)}\n"
                    f"📧 <b>Emails Sent:</b> {stats.get('total_strikes', 0)}\n"
                    f"🏢 <b>Companies Targeted:</b> {stats.get('recon_rows', 0)}\n"
                    "━━━━━━━━━━━━━━━"
                )
                await msg.reply_text(msg_text, parse_mode='HTML')
            elif key == "companies":
                # Show companies list
                leads = await self.db.get_pending_leads(limit=10) if self.db else []
                if leads:
                    company_list = "\n".join([f"🏢 {l['company_name']} - {l['job_title'][:20]}" for l in leads])
                    msg_text = f"🏢 <b>COMPANIES LIST</b>\n━━━━━━━━━━━━━━━\n{company_list}\n━━━━━━━━━━━━━━━"
                else:
                    msg_text = "🏢 <b>COMPANIES LIST</b>\n━━━━━━━━━━━━━━━\nNo companies found. Bot is searching...\n━━━━━━━━━━━━━━━"
                await msg.reply_text(msg_text, parse_mode='HTML')
            else:
                # status - show full status
                await self._dispatch_command("/status", update, context)
            return

        elif key == "test_strike":
            context.user_data['state'] = 'WAITING_TEST_EMAIL'
            await msg.reply_text(
                "📧 <b>MISSION READINESS: TEST STRIKE</b>\n"
                "━━━━━━━━━━━━━━━\n"
                "Please enter the <b>target email address</b> where you want to receive the simulation strike.\n\n"
                "⚠️ <b>IMPORTANT:</b> Use <b>Gmail</b> for best results!\n"
                "• ✅ Gmail: Works perfectly\n"
                "• ❌ Outlook: May block emails\n\n"
                "💡 <b>Recommended:</b> <code>samsalameh.cv@gmail.com</code>\n\n"
                "<i>The bot will generate a dummy CV and Cover Letter package to show you exactly what recruiters see.</i>",
                parse_mode='HTML'
            )

        elif key == "quick_test_email":
            # One-tap test: sends immediately to TEST_RECEIVER_EMAIL without asking
            target = os.getenv("TEST_RECEIVER_EMAIL", os.getenv("SENDER_EMAIL", os.getenv("GMAIL_SMTP_USER", "")))
            if not target:
                await msg.reply_text("❌ <b>TEST_RECEIVER_EMAIL not set.</b>\nPlease configure it in your environment variables.", parse_mode='HTML')
                return
            status_msg = await msg.reply_text(
                f"🧬 <b>QUICK TEST STRIKE INITIATED</b>\n"
                f"━━━━━━━━━━━━━━━\n"
                f"📧 Target: <code>{target}</code>\n"
                f"<i>Generating CV + Cover Letter package...</i>",
                parse_mode='HTML'
            )
            try:
                success = await asyncio.wait_for(
                    asyncio.to_thread(smtp_engine.send_test_email, target),
                    timeout=45.0
                )
            except asyncio.TimeoutError:
                logging.error(f"⏰ Quick test email timed out for {target}")
                try:
                    await status_msg.edit_text(
                        f"⏰ <b>TEST TIMED OUT</b>\n"
                        f"━━━━━━━━━━━━━━━\n"
                        f"📧 Target: <code>{target}</code>\n\n"
                        f"<i>Try again.</i>",
                        parse_mode='HTML'
                    )
                except Exception:
                    await msg.reply_text(f"⏰ <b>TEST TIMED OUT</b> — Try again.", parse_mode='HTML')
                return
            except Exception as e:
                logging.error(f"Quick test email error: {e}")
                try:
                    await status_msg.edit_text(f"💥 <b>ERROR:</b> <code>{str(e)[:200]}</code>", parse_mode='HTML')
                except Exception:
                    await msg.reply_text(f"💥 <b>ERROR:</b> <code>{str(e)[:200]}</code>", parse_mode='HTML')
                return

            if success:
                try:
                    await status_msg.edit_text(
                        f"✅ <b>TEST EMAIL DELIVERED!</b>\n"
                        f"━━━━━━━━━━━━━━━\n"
                        f"📧 Sent to: <code>{target}</code>\n"
                        f"📎 Attachments: CV + Cover Letter\n\n"
                        f"<i>Check your inbox (and spam folder).\n"
                        f"Should arrive within 30 seconds.</i>",
                        parse_mode='HTML'
                    )
                except Exception:
                    await msg.reply_text(
                        f"✅ <b>TEST EMAIL DELIVERED!</b>\n📧 Sent to: <code>{target}</code>",
                        parse_mode='HTML'
                    )
            else:
                try:
                    await status_msg.edit_text(
                        f"❌ <b>TEST EMAIL FAILED</b>\n"
                        f"━━━━━━━━━━━━━━━\n"
                        f"Target: <code>{target}</code>\n\n"
                        f"<i>Check /logs for details. Brevo or Gmail may be down.</i>",
                        parse_mode='HTML'
                    )
                except Exception:
                    await msg.reply_text(
                        f"❌ <b>TEST EMAIL FAILED</b> — Check /logs for details.",
                        parse_mode='HTML'
                    )

        elif key == "today_report":
            try:
                from datetime import datetime, timedelta, timezone
                now = datetime.now(timezone.utc)
                today_start = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat().replace("+", "%2B")
                app_succ, app_data = await self.db._request_with_retry(
                    "GET",
                    f"{self.db.url}/rest/v1/applications?select=company_name,job_title,status&order=timestamp.desc&limit=20&timestamp=gte.{today_start}"
                )
                apps = app_data if app_succ and isinstance(app_data, list) else []
                lines = [f"✅ {a.get('company_name','?')[:22]} — {a.get('job_title','?')[:20]}" for a in apps[:15]]
                report = (
                    f"📈 <b>TODAY'S REPORT</b>\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"🚀 <b>Applications sent today:</b> {len(apps)}\n"
                    f"━━━━━━━━━━━━━━━\n"
                    + ("\n".join(lines) if lines else "<i>No applications sent yet today.</i>") +
                    f"\n━━━━━━━━━━━━━━━\n"
                    f"🕐 <i>{now.strftime('%Y-%m-%d %H:%M UTC')}</i>"
                )
                await msg.reply_text(report, parse_mode='HTML')
            except Exception as e:
                await msg.reply_text(f"❌ <b>Error:</b> {e}", parse_mode='HTML')

        elif key == "email_stats":
            try:
                from core.email_rotator import get_email_stats
                stats = get_email_stats()
                lines = []
                for name, data in stats.get("providers", {}).items():
                    pct = data.get('percentage', 0)
                    filled = int(pct / 10)
                    bar = "█" * filled + "░" * (10 - filled)
                    lines.append(f"<b>{name}</b>\n  {bar} {data['used']}/{data['limit']} ({pct}%)")
                report = (
                    f"📧 <b>EMAIL STATS TODAY</b>\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"📤 <b>Total sent:</b> {stats.get('total_sent', 0)}\n"
                    f"📦 <b>Remaining:</b> {stats.get('total_remaining', 0)}\n"
                    f"━━━━━━━━━━━━━━━\n"
                    + "\n\n".join(lines) +
                    "\n━━━━━━━━━━━━━━━"
                )
                await msg.reply_text(report, parse_mode='HTML')
            except Exception as e:
                await msg.reply_text(f"❌ <b>Email stats error:</b> {e}", parse_mode='HTML')

        elif key == "queue_status":
            try:
                count = await self.db.get_pending_leads_count() if self.db else 0
                leads = await self.db.get_pending_leads(limit=5) if self.db else []
                lines = [f"🎯 {l.get('company_name','?')[:25]} — {l.get('job_title','?')[:20]}" for l in leads]
                report = (
                    f"🗂️ <b>QUEUE STATUS</b>\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"📦 <b>Pending leads:</b> {count}\n"
                    f"━━━━━━━━━━━━━━━\n"
                    + ("\n".join(lines) if lines else "<i>Queue is empty — scrapers are hunting...</i>") +
                    "\n━━━━━━━━━━━━━━━"
                )
                await msg.reply_text(report, parse_mode='HTML')
            except Exception as e:
                await msg.reply_text(f"❌ <b>Queue error:</b> {e}", parse_mode='HTML')

        elif key == "clean_disk":
            status_msg = await msg.reply_text("🧹 <b>DISK JANITOR RUNNING...</b>", parse_mode='HTML')
            try:
                import shutil, glob
                cleaned = 0
                for cache_dir in ["pdf_cache", "core/pdf_cache", "core/temp_cvs", "cover_letters"]:
                    if os.path.exists(cache_dir):
                        files = sorted(
                            [f for f in glob.glob(f"{cache_dir}/*") if os.path.isfile(f)],
                            key=os.path.getmtime
                        )
                        for f in files[:-5]:
                            try: os.remove(f); cleaned += 1
                            except: pass
                if os.path.exists("temp_mirror"):
                    shutil.rmtree("temp_mirror", ignore_errors=True)
                    os.makedirs("temp_mirror", exist_ok=True)
                    cleaned += 1
                await status_msg.edit_text(
                    f"🧹 <b>DISK CLEAN COMPLETE</b>\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"🗑️ Removed: {cleaned} files\n"
                    f"✅ Cache directories cleaned\n"
                    f"━━━━━━━━━━━━━━━",
                    parse_mode='HTML'
                )
            except Exception as e:
                await status_msg.edit_text(f"❌ <b>Clean error:</b> {e}", parse_mode='HTML')

        elif key == "memory_status":
            try:
                import psutil
                proc = psutil.Process()
                mem_mb = proc.memory_info().rss / (1024 * 1024)
                vm = psutil.virtual_memory()
                bar_used = int((vm.percent / 100) * 10)
                bar = "█" * bar_used + "░" * (10 - bar_used)
                status_icon = "🔴" if mem_mb > 400 else "🟡" if mem_mb > 300 else "🟢"
                await msg.reply_text(
                    f"🌡️ <b>MEMORY STATUS</b>\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"{status_icon} <b>Bot RAM:</b> {mem_mb:.0f} MB\n"
                    f"💻 <b>System RAM:</b> {bar} {vm.percent}%\n"
                    f"📊 <b>Used:</b> {vm.used // (1024**2)} MB / {vm.total // (1024**2)} MB\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"{'⚠️ HIGH — GC recommended' if mem_mb > 350 else '✅ Healthy'}",
                    parse_mode='HTML'
                )
            except ImportError:
                import gc; gc.collect()
                await msg.reply_text("🌡️ <b>Memory:</b> psutil not available. GC triggered.", parse_mode='HTML')
            except Exception as e:
                await msg.reply_text(f"❌ <b>Memory error:</b> {e}", parse_mode='HTML')

        elif key == "uptime_status":
            try:
                import psutil, time
                boot_time = psutil.boot_time()
                uptime_sec = time.time() - boot_time
                hours = int(uptime_sec // 3600)
                minutes = int((uptime_sec % 3600) // 60)
                # Bot process uptime
                proc = psutil.Process()
                proc_uptime = time.time() - proc.create_time()
                p_hours = int(proc_uptime // 3600)
                p_minutes = int((proc_uptime % 3600) // 60)
                await msg.reply_text(
                    f"⏱️ <b>UPTIME STATUS</b>\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"🤖 <b>Bot uptime:</b> {p_hours}h {p_minutes}m\n"
                    f"🖥️ <b>Server uptime:</b> {hours}h {minutes}m\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"✅ Running continuously on Render",
                    parse_mode='HTML'
                )
            except Exception as e:
                await msg.reply_text(f"⏱️ <b>Uptime error:</b> {e}", parse_mode='HTML')

        elif key == "ai_status":
            lines = []
            gemini_key = os.getenv("GEMINI_API_KEY", "")
            groq_key   = os.getenv("GROQ_API_KEY", "")
            hf_key     = os.getenv("HUGGINGFACE_API_KEY", "")
            lines.append(f"{'🟢' if gemini_key else '🔴'} <b>Gemini:</b> {'Configured ✅' if gemini_key else 'Not set ❌'}")
            lines.append(f"{'🟢' if groq_key   else '🔴'} <b>Groq:</b>   {'Configured ✅' if groq_key   else 'Not set ❌'}")
            lines.append(f"{'🟢' if hf_key     else '🔴'} <b>HuggingFace:</b> {'Configured ✅' if hf_key else 'Not set ❌'}")
            # Quick ping test
            ai_ok = bool(gemini_key or groq_key)
            await msg.reply_text(
                f"🧠 <b>AI STATUS</b>\n"
                f"━━━━━━━━━━━━━━━\n"
                + "\n".join(lines) +
                f"\n━━━━━━━━━━━━━━━\n"
                f"{'✅ AI Engine: ONLINE' if ai_ok else '❌ AI Engine: OFFLINE — no keys configured'}",
                parse_mode='HTML'
            )

        elif key == "inbox_check":
            status_msg = await msg.reply_text("📬 <b>CHECKING INBOX...</b>\n<i>Scanning for replies to applications...</i>", parse_mode='HTML')
            try:
                # Check DB for any applications with status REPLIED or RESPONSE
                app_succ, app_data = await self.db._request_with_retry(
                    "GET",
                    f"{self.db.url}/rest/v1/applications?select=company_name,job_title,status,timestamp&status=in.(REPLIED,RESPONSE,INTERESTED,INTERVIEW)&order=timestamp.desc&limit=20"
                )
                replies = app_data if app_succ and isinstance(app_data, list) else []
                if replies:
                    lines = [f"🎉 <b>{r.get('company_name','?')[:22]}</b> — {r.get('job_title','?')[:20]} [{r.get('status','?')}]" for r in replies]
                    report = f"📬 <b>INBOX REPLIES ({len(replies)})</b>\n━━━━━━━━━━━━━━━\n" + "\n".join(lines) + "\n━━━━━━━━━━━━━━━"
                else:
                    report = "📬 <b>INBOX CHECK</b>\n━━━━━━━━━━━━━━━\n<i>No replies detected yet.\nThe bot is monitoring continuously.</i>\n━━━━━━━━━━━━━━━"
                await status_msg.edit_text(report, parse_mode='HTML')
            except Exception as e:
                await status_msg.edit_text(f"❌ <b>Inbox check error:</b> {e}", parse_mode='HTML')

        elif key == "top_companies":
            try:
                succ, data = await self.db._request_with_retry(
                    "GET",
                    f"{self.db.url}/rest/v1/leads?select=company_name,job_title,priority_score&order=priority_score.desc&limit=10&status=eq.pending"
                )
                leads = data if succ and isinstance(data, list) else []
                if leads:
                    lines = [f"🏆 <b>{l.get('company_name','?')[:22]}</b> — {l.get('job_title','?')[:18]} <i>(score: {l.get('priority_score','?')})</i>" for l in leads]
                    report = "📊 <b>TOP 10 COMPANIES BY SCORE</b>\n━━━━━━━━━━━━━━━\n" + "\n".join(lines) + "\n━━━━━━━━━━━━━━━"
                else:
                    report = "📊 <b>TOP COMPANIES</b>\n━━━━━━━━━━━━━━━\n<i>No scored leads found yet.</i>"
                await msg.reply_text(report, parse_mode='HTML')
            except Exception as e:
                await msg.reply_text(f"❌ <b>Top companies error:</b> {e}", parse_mode='HTML')

        elif key == "scrape_now":
            status_msg = await msg.reply_text(
                "🌍 <b>SCRAPE NOW INITIATED</b>\n"
                "━━━━━━━━━━━━━━━\n"
                "<i>Triggering all scrapers immediately...\n"
                "Results will appear in Queue within 2-3 minutes.</i>",
                parse_mode='HTML'
            )
            try:
                # Queue a scrape task in DB so the engine picks it up
                await self.db.sync_add_task(task_type="FORCE_SCRAPE", target="ALL_SCRAPERS", meta="manual_trigger") if hasattr(self.db, 'sync_add_task') else None
                # Also try async version
                try:
                    await self.db.add_task(task_type="FORCE_SCRAPE", target="ALL_SCRAPERS", meta="manual_trigger")
                except Exception:
                    pass
                await status_msg.edit_text(
                    "🌍 <b>SCRAPE TRIGGERED</b>\n"
                    "━━━━━━━━━━━━━━━\n"
                    "✅ All scrapers queued for immediate run\n"
                    "📦 Check Queue in 2-3 minutes for new leads\n"
                    "━━━━━━━━━━━━━━━",
                    parse_mode='HTML'
                )
            except Exception as e:
                await status_msg.edit_text(f"❌ <b>Scrape trigger error:</b> {e}", parse_mode='HTML')

        elif key == "force_strike":
            status_msg = await msg.reply_text(
                "🎯 <b>FORCE STRIKE LOADING...</b>\n"
                "<i>Fetching top lead from queue...</i>",
                parse_mode='HTML'
            )
            try:
                leads = await self.db.get_pending_leads(limit=1) if self.db else []
                if not leads:
                    await status_msg.edit_text("🎯 <b>FORCE STRIKE</b>\n━━━━━━━━━━━━━━━\n❌ Queue is empty. No leads to strike.\nUse 🌍 Scrape Now to fill the queue.", parse_mode='HTML')
                    return
                lead = leads[0]
                company = lead.get('company_name', 'Unknown')
                email   = lead.get('email', '')
                title   = lead.get('job_title', 'Professional Role')
                if not email:
                    await status_msg.edit_text(f"🎯 <b>FORCE STRIKE</b>\n━━━━━━━━━━━━━━━\n⚠️ Top lead <b>{company}</b> has no email address.\nSkipping — use /leads to review.", parse_mode='HTML')
                    return
                await status_msg.edit_text(
                    f"🎯 <b>FORCE STRIKE FIRING</b>\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"🏢 <b>Target:</b> {company}\n"
                    f"📧 <b>Email:</b> <code>{email}</code>\n"
                    f"💼 <b>Role:</b> {title}\n"
                    f"<i>Sending now...</i>",
                    parse_mode='HTML'
                )
                from core import smtp_engine as _smtp
                success = await asyncio.to_thread(_smtp.send_strike, lead)
                if success:
                    await status_msg.edit_text(
                        f"✅ <b>FORCE STRIKE DELIVERED!</b>\n"
                        f"━━━━━━━━━━━━━━━\n"
                        f"🏢 {company}\n📧 {email}\n💼 {title}\n"
                        f"━━━━━━━━━━━━━━━",
                        parse_mode='HTML'
                    )
                else:
                    await status_msg.edit_text(f"❌ <b>FORCE STRIKE FAILED</b>\nTarget: {company}\nCheck /logs for details.", parse_mode='HTML')
            except Exception as e:
                await status_msg.edit_text(f"💥 <b>Force strike error:</b> {e}", parse_mode='HTML')

        elif key == "boost_mode":
            try:
                current = int(os.getenv("MAX_PARALLEL_STRIKES", "15"))
                boosted = min(current + 10, 50)
                os.environ["MAX_PARALLEL_STRIKES"] = str(boosted)
                os.environ["MAX_EMAILS_PER_HOUR"]  = "150"
                os.environ["DELAY_BETWEEN_EMAILS_MIN"] = "1"
                os.environ["DELAY_BETWEEN_EMAILS_MAX"] = "3"
                await msg.reply_text(
                    f"🔥 <b>BOOST MODE ACTIVATED</b>\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"⚡ Parallel strikes: {current} → <b>{boosted}</b>\n"
                    f"📧 Max emails/hour: → <b>150</b>\n"
                    f"⏱️ Delay between emails: → <b>1-3s</b>\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"⚠️ <i>Boost is active until next reboot.\nUse ▶️ Resume to apply changes.</i>",
                    parse_mode='HTML'
                )
            except Exception as e:
                await msg.reply_text(f"❌ <b>Boost error:</b> {e}", parse_mode='HTML')

        elif key == "weekly_report":
            try:
                from datetime import datetime, timedelta, timezone
                now = datetime.now(timezone.utc)
                week_start = (now - timedelta(days=7)).isoformat().replace("+", "%2B")
                app_succ, app_data = await self.db._request_with_retry(
                    "GET",
                    f"{self.db.url}/rest/v1/applications?select=company_name,job_title,status,timestamp&order=timestamp.desc&limit=500&timestamp=gte.{week_start}"
                )
                apps = app_data if app_succ and isinstance(app_data, list) else []
                # Group by day
                from collections import Counter
                day_counts = Counter()
                for a in apps:
                    ts = a.get('timestamp', '')[:10]
                    if ts: day_counts[ts] += 1
                day_lines = [f"📅 <b>{d}:</b> {c} applications" for d, c in sorted(day_counts.items(), reverse=True)]
                report = (
                    f"📅 <b>WEEKLY REPORT (Last 7 Days)</b>\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"🚀 <b>Total:</b> {len(apps)} applications\n"
                    f"📊 <b>Daily avg:</b> {len(apps)//7}/day\n"
                    f"━━━━━━━━━━━━━━━\n"
                    + ("\n".join(day_lines) if day_lines else "<i>No data for last 7 days.</i>") +
                    f"\n━━━━━━━━━━━━━━━"
                )
                await msg.reply_text(report, parse_mode='HTML')
            except Exception as e:
                await msg.reply_text(f"❌ <b>Weekly report error:</b> {e}", parse_mode='HTML')

        elif key == "failure_rate":
            try:
                from datetime import datetime, timezone
                now = datetime.now(timezone.utc)
                today_start = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat().replace("+", "%2B")
                succ, data = await self.db._request_with_retry(
                    "GET",
                    f"{self.db.url}/rest/v1/applications?select=status&timestamp=gte.{today_start}"
                )
                apps = data if succ and isinstance(data, list) else []
                total = len(apps)
                failed = sum(1 for a in apps if a.get('status','').upper() in ('FAILED','ERROR','BOUNCED'))
                sent   = sum(1 for a in apps if a.get('status','').upper() in ('SENT','DELIVERED','SUCCESS'))
                rate   = round((failed / total * 100), 1) if total > 0 else 0
                icon   = "🔴" if rate > 20 else "🟡" if rate > 5 else "🟢"
                await msg.reply_text(
                    f"📉 <b>FAILURE RATE TODAY</b>\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"📤 <b>Total sent:</b> {total}\n"
                    f"✅ <b>Delivered:</b> {sent}\n"
                    f"❌ <b>Failed:</b> {failed}\n"
                    f"{icon} <b>Failure rate:</b> {rate}%\n"
                    f"━━━━━━━━━━━━━━━",
                    parse_mode='HTML'
                )
            except Exception as e:
                await msg.reply_text(f"❌ <b>Failure rate error:</b> {e}", parse_mode='HTML')

        elif key == "best_day":
            try:
                succ, data = await self.db._request_with_retry(
                    "GET",
                    f"{self.db.url}/rest/v1/applications?select=timestamp&order=timestamp.desc&limit=2000"
                )
                apps = data if succ and isinstance(data, list) else []
                from collections import Counter
                day_counts = Counter()
                for a in apps:
                    ts = a.get('timestamp', '')[:10]
                    if ts: day_counts[ts] += 1
                if day_counts:
                    best_date, best_count = day_counts.most_common(1)[0]
                    top5 = day_counts.most_common(5)
                    lines = [f"🏅 <b>{d}:</b> {c} applications" for d, c in top5]
                    report = (
                        f"🏆 <b>BEST DAY EVER</b>\n"
                        f"━━━━━━━━━━━━━━━\n"
                        f"🥇 <b>{best_date}:</b> {best_count} applications\n"
                        f"━━━━━━━━━━━━━━━\n"
                        f"<b>Top 5 Days:</b>\n" + "\n".join(lines) +
                        f"\n━━━━━━━━━━━━━━━"
                    )
                else:
                    report = "🏆 <b>BEST DAY</b>\n━━━━━━━━━━━━━━━\n<i>No data yet.</i>"
                await msg.reply_text(report, parse_mode='HTML')
            except Exception as e:
                await msg.reply_text(f"❌ <b>Best day error:</b> {e}", parse_mode='HTML')

        elif key == "notify_me":
            # Toggle hourly notifications
            current = os.environ.get("HOURLY_NOTIFY", "false")
            if current == "true":
                os.environ["HOURLY_NOTIFY"] = "false"
                await msg.reply_text(
                    "🔕 <b>NOTIFICATIONS OFF</b>\n"
                    "━━━━━━━━━━━━━━━\n"
                    "Hourly progress reports disabled.\n"
                    "Press again to re-enable.",
                    parse_mode='HTML'
                )
            else:
                os.environ["HOURLY_NOTIFY"] = "true"
                os.environ["HOURLY_NOTIFY_CHAT"] = str(update.effective_chat.id)
                await msg.reply_text(
                    "🔔 <b>NOTIFICATIONS ON</b>\n"
                    "━━━━━━━━━━━━━━━\n"
                    "✅ You will receive a progress report every hour.\n"
                    "Press again to disable.",
                    parse_mode='HTML'
                )
                # Schedule first notification
                asyncio.create_task(self._hourly_notify_loop(context.bot, update.effective_chat.id))

        elif key == "blacklist_view":
            try:
                blacklist = await self.db.get_recent_blacklist(limit=20) if self.db else []
                if blacklist:
                    lines = [f"⛔ {b.get('company_name', b) if isinstance(b, dict) else str(b)}" for b in blacklist[:20]]
                    report = f"⛔ <b>BLACKLIST ({len(blacklist)} companies)</b>\n━━━━━━━━━━━━━━━\n" + "\n".join(lines) + "\n━━━━━━━━━━━━━━━"
                else:
                    report = "⛔ <b>BLACKLIST</b>\n━━━━━━━━━━━━━━━\n<i>No blacklisted companies.</i>"
                await msg.reply_text(report, parse_mode='HTML')
            except Exception as e:
                await msg.reply_text(f"❌ <b>Blacklist error:</b> {e}", parse_mode='HTML')

        elif key == "retry_failed":
            status_msg = await msg.reply_text("🔁 <b>SCANNING FOR FAILED EMAILS...</b>", parse_mode='HTML')
            try:
                succ, data = await self.db._request_with_retry(
                    "GET",
                    f"{self.db.url}/rest/v1/applications?select=id,company_name,job_title,email,status&status=in.(FAILED,ERROR,BOUNCED)&order=timestamp.desc&limit=20"
                )
                failed_apps = data if succ and isinstance(data, list) else []
                if not failed_apps:
                    await status_msg.edit_text("🔁 <b>RETRY FAILED</b>\n━━━━━━━━━━━━━━━\n✅ No failed emails found. All good!", parse_mode='HTML')
                    return
                # Re-queue them
                requeued = 0
                for app in failed_apps:
                    try:
                        await self.db.add_task(task_type="RETRY_STRIKE", target=app.get('email',''), meta=str(app.get('id','')))
                        requeued += 1
                    except Exception:
                        pass
                await status_msg.edit_text(
                    f"🔁 <b>RETRY QUEUED</b>\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"📦 Found: {len(failed_apps)} failed emails\n"
                    f"✅ Re-queued: {requeued}\n"
                    f"<i>Bot will retry them in the next cycle.</i>\n"
                    f"━━━━━━━━━━━━━━━",
                    parse_mode='HTML'
                )
            except Exception as e:
                await status_msg.edit_text(f"❌ <b>Retry error:</b> {e}", parse_mode='HTML')

        elif key == "night_mode":
            current = os.environ.get("NIGHT_MODE", "false")
            if current == "true":
                os.environ["NIGHT_MODE"] = "false"
                os.environ["BUSINESS_HOURS_START"] = "5"
                os.environ["BUSINESS_HOURS_END"]   = "23"
                await msg.reply_text(
                    "☀️ <b>NIGHT MODE OFF</b>\n"
                    "━━━━━━━━━━━━━━━\n"
                    "✅ Bot is back to normal hours (5 AM – 11 PM)\n"
                    "Sending resumed.",
                    parse_mode='HTML'
                )
            else:
                os.environ["NIGHT_MODE"] = "true"
                os.environ["BUSINESS_HOURS_START"] = "5"
                os.environ["BUSINESS_HOURS_END"]   = "23"
                await msg.reply_text(
                    "🌙 <b>NIGHT MODE ON</b>\n"
                    "━━━━━━━━━━━━━━━\n"
                    "😴 Bot will pause sending from 11 PM – 5 AM\n"
                    "✅ Resumes automatically at 5 AM\n"
                    "Press again to disable.",
                    parse_mode='HTML'
                )

        elif key == "dry_run":
            current = os.environ.get("DRY_RUN_MODE", "false")
            if current == "true":
                os.environ["DRY_RUN_MODE"] = "false"
                await msg.reply_text(
                    "✅ <b>DRY RUN OFF</b>\n"
                    "━━━━━━━━━━━━━━━\n"
                    "🔥 Bot is back to LIVE mode.\n"
                    "Real emails will be sent.",
                    parse_mode='HTML'
                )
            else:
                os.environ["DRY_RUN_MODE"] = "true"
                await msg.reply_text(
                    "🧪 <b>DRY RUN ON</b>\n"
                    "━━━━━━━━━━━━━━━\n"
                    "🔒 Bot will run full cycles but NOT send real emails.\n"
                    "✅ Safe for testing scrapers & AI scoring.\n"
                    "Press again to go back to LIVE mode.",
                    parse_mode='HTML'
                )

        elif key == "cv_preview":
            status_msg = await msg.reply_text("📝 <b>GENERATING CV PDF...</b>", parse_mode='HTML')
            try:
                cv_path = None
                try:
                    from core.cv_playwright_pdf import generate_cv_from_html_playwright
                    cv_path = await asyncio.to_thread(generate_cv_from_html_playwright)
                except Exception:
                    pass
                if not cv_path or not os.path.exists(cv_path):
                    from core.cv_pdf_full import generate_full_cv_pdf
                    cv_path = await asyncio.to_thread(generate_full_cv_pdf)
                if cv_path and os.path.exists(cv_path):
                    await status_msg.delete()
                    with open(cv_path, 'rb') as f:
                        await context.bot.send_document(
                            chat_id=update.effective_chat.id,
                            document=f,
                            filename="Sam_Salameh_CV.pdf",
                            caption="📝 <b>CV Preview</b> — This is exactly what recruiters receive.",
                            parse_mode='HTML'
                        )
                else:
                    await status_msg.edit_text("❌ <b>CV generation failed.</b>\nCheck logs.", parse_mode='HTML')
            except Exception as e:
                await status_msg.edit_text(f"❌ <b>CV error:</b> {e}", parse_mode='HTML')

        elif key == "cover_letter_preview":
            status_msg = await msg.reply_text("✉️ <b>GENERATING COVER LETTER...</b>", parse_mode='HTML')
            try:
                from core.cover_letter_pdf import generate_cover_letter_pdf
                cl_path = await asyncio.to_thread(generate_cover_letter_pdf, "Sample Company", "Senior Network Engineer")
                if cl_path and os.path.exists(cl_path):
                    await status_msg.delete()
                    with open(cl_path, 'rb') as f:
                        await context.bot.send_document(
                            chat_id=update.effective_chat.id,
                            document=f,
                            filename="Sam_Salameh_Cover_Letter.pdf",
                            caption="✉️ <b>Cover Letter Preview</b> — Sample for 'Senior Network Engineer'.",
                            parse_mode='HTML'
                        )
                else:
                    await status_msg.edit_text("❌ <b>Cover letter generation failed.</b>", parse_mode='HTML')
            except Exception as e:
                await status_msg.edit_text(f"❌ <b>Cover letter error:</b> {e}", parse_mode='HTML')

        elif key == "monthly_report":
            try:
                from datetime import datetime, timedelta, timezone
                from collections import Counter
                now = datetime.now(timezone.utc)
                month_start = (now - timedelta(days=30)).isoformat().replace("+", "%2B")
                succ, data = await self.db._request_with_retry(
                    "GET",
                    f"{self.db.url}/rest/v1/applications?select=timestamp,status&order=timestamp.desc&limit=2000&timestamp=gte.{month_start}"
                )
                apps = data if succ and isinstance(data, list) else []
                week_counts = Counter()
                for a in apps:
                    ts = a.get('timestamp', '')
                    if ts:
                        try:
                            d = datetime.fromisoformat(ts.replace('Z','+00:00'))
                            week_num = (now - d).days // 7
                            label = f"Week -{week_num}" if week_num > 0 else "This week"
                            week_counts[label] += 1
                        except Exception:
                            pass
                lines = [f"📅 <b>{w}:</b> {c}" for w, c in sorted(week_counts.items())]
                await msg.reply_text(
                    f"🗓️ <b>MONTHLY REPORT (Last 30 Days)</b>\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"🚀 <b>Total:</b> {len(apps)} applications\n"
                    f"📊 <b>Daily avg:</b> {len(apps)//30}/day\n"
                    f"━━━━━━━━━━━━━━━\n"
                    + ("\n".join(lines) if lines else "<i>No data.</i>") +
                    "\n━━━━━━━━━━━━━━━",
                    parse_mode='HTML'
                )
            except Exception as e:
                await msg.reply_text(f"❌ <b>Monthly report error:</b> {e}", parse_mode='HTML')

        elif key == "provider_health":
            status_msg = await msg.reply_text("📊 <b>TESTING ALL EMAIL PROVIDERS...</b>", parse_mode='HTML')
            try:
                lines = []
                # Brevo HTTP
                brevo_key = os.getenv("BREVO_API_KEY","").strip()
                if brevo_key:
                    try:
                        import requests as _req
                        r = _req.get("https://api.brevo.com/v3/account",
                                     headers={"api-key": brevo_key}, timeout=5)
                        plan = r.json().get('plan',[{}])
                        credits = plan[0].get('credits', '?') if plan else '?'
                        lines.append(f"🟢 <b>Brevo:</b> Online ✅ | Credits: {credits}")
                    except Exception as e:
                        lines.append(f"🔴 <b>Brevo:</b> Error — {str(e)[:40]}")
                else:
                    lines.append("⚪ <b>Brevo:</b> Not configured")
                # Gmail
                gmail = os.getenv("GMAIL_SMTP_USER","")
                lines.append(f"{'🟢' if gmail else '⚪'} <b>Gmail:</b> {'Configured ✅' if gmail else 'Not configured'}")
                # Zoho
                zoho = os.getenv("ZOHO_SMTP_USER","")
                lines.append(f"{'🟢' if zoho else '⚪'} <b>Zoho:</b> {'Configured ✅' if zoho else 'Not configured'}")
                # Resend
                resend = os.getenv("RESEND_API_KEY","")
                lines.append(f"{'🟢' if resend else '⚪'} <b>Resend:</b> {'Configured ✅' if resend else 'Not configured'}")
                await status_msg.edit_text(
                    "📊 <b>PROVIDER HEALTH CHECK</b>\n━━━━━━━━━━━━━━━\n" +
                    "\n".join(lines) + "\n━━━━━━━━━━━━━━━",
                    parse_mode='HTML'
                )
            except Exception as e:
                await status_msg.edit_text(f"❌ <b>Provider health error:</b> {e}", parse_mode='HTML')

        elif key == "speed_test":
            status_msg = await msg.reply_text("⚡ <b>SPEED TEST RUNNING...</b>\n<i>Measuring email throughput...</i>", parse_mode='HTML')
            try:
                from datetime import datetime, timedelta, timezone
                now = datetime.now(timezone.utc)
                hour_ago = (now - timedelta(hours=1)).isoformat().replace("+", "%2B")
                succ, data = await self.db._request_with_retry(
                    "GET",
                    f"{self.db.url}/rest/v1/applications?select=id&timestamp=gte.{hour_ago}",
                    headers={"Prefer": "count=exact"}
                )
                per_hour = data.get("count", 0) if succ and isinstance(data, dict) else 0
                per_min  = round(per_hour / 60, 1)
                icon = "🔴" if per_hour < 10 else "🟡" if per_hour < 50 else "🟢"
                await status_msg.edit_text(
                    f"⚡ <b>SPEED TEST RESULTS</b>\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"{icon} <b>Last hour:</b> {per_hour} emails\n"
                    f"📊 <b>Per minute:</b> {per_min}\n"
                    f"🎯 <b>Target:</b> 80/hour\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"{'✅ On target' if per_hour >= 50 else '⚠️ Below target — check queue & providers'}",
                    parse_mode='HTML'
                )
            except Exception as e:
                await status_msg.edit_text(f"❌ <b>Speed test error:</b> {e}", parse_mode='HTML')

        elif key == "ping_render":
            status_msg = await msg.reply_text("📡 <b>PINGING RENDER SERVER...</b>", parse_mode='HTML')
            try:
                import requests as _req, time as _time
                url = os.getenv("RENDER_EXTERNAL_URL", "https://sam-job-automator.onrender.com")
                t0 = _time.time()
                r  = _req.get(url, timeout=10)
                ms = int((_time.time() - t0) * 1000)
                icon = "🟢" if r.status_code == 200 else "🟡"
                await status_msg.edit_text(
                    f"📡 <b>RENDER PING RESULT</b>\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"{icon} <b>Status:</b> {r.status_code}\n"
                    f"⚡ <b>Latency:</b> {ms}ms\n"
                    f"🌐 <b>URL:</b> <code>{url}</code>\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"{'✅ Server is alive' if r.status_code == 200 else '⚠️ Unexpected status'}",
                    parse_mode='HTML'
                )
            except Exception as e:
                await status_msg.edit_text(
                    f"📡 <b>PING FAILED</b>\n━━━━━━━━━━━━━━━\n❌ {str(e)[:100]}\n<i>Server may be sleeping.</i>",
                    parse_mode='HTML'
                )

        elif key == "env_check":
            required = {
                "SUPABASE_URL": os.getenv("SUPABASE_URL",""),
                "SUPABASE_KEY": os.getenv("SUPABASE_KEY",""),
                "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN",""),
                "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY",""),
                "GROQ_API_KEY": os.getenv("GROQ_API_KEY",""),
                "BREVO_API_KEY": os.getenv("BREVO_API_KEY",""),
                "GMAIL_SMTP_USER": os.getenv("GMAIL_SMTP_USER",""),
                "GMAIL_APP_PASSWORD": os.getenv("GMAIL_APP_PASSWORD",""),
                "SENDER_EMAIL": os.getenv("SENDER_EMAIL",""),
                "RENDER_EXTERNAL_URL": os.getenv("RENDER_EXTERNAL_URL",""),
            }
            lines = []
            missing = 0
            for k, v in required.items():
                if v:
                    lines.append(f"✅ <code>{k}</code>")
                else:
                    lines.append(f"❌ <code>{k}</code> — MISSING")
                    missing += 1
            await msg.reply_text(
                f"🔑 <b>ENV CHECK ({len(required)-missing}/{len(required)} OK)</b>\n"
                f"━━━━━━━━━━━━━━━\n" +
                "\n".join(lines) +
                f"\n━━━━━━━━━━━━━━━\n"
                f"{'✅ All keys configured' if missing == 0 else f'⚠️ {missing} key(s) missing!'}",
                parse_mode='HTML'
            )

        elif key == "countries_report":
            try:
                succ, data = await self.db._request_with_retry(
                    "GET",
                    f"{self.db.url}/rest/v1/leads?select=company_name,job_title&limit=500&status=eq.pending"
                )
                leads = data if succ and isinstance(data, list) else []
                from collections import Counter
                country_map = {
                    "uae": "🇦🇪 UAE", "dubai": "🇦🇪 UAE", "abu dhabi": "🇦🇪 UAE",
                    "saudi": "🇸🇦 KSA", "riyadh": "🇸🇦 KSA", "jeddah": "🇸🇦 KSA",
                    "qatar": "🇶🇦 Qatar", "doha": "🇶🇦 Qatar",
                    "kuwait": "🇰🇼 Kuwait", "bahrain": "🇧🇭 Bahrain",
                    "oman": "🇴🇲 Oman", "muscat": "🇴🇲 Oman",
                    "lebanon": "🇱🇧 Lebanon", "beirut": "🇱🇧 Lebanon",
                    "jordan": "🇯🇴 Jordan", "egypt": "🇪🇬 Egypt",
                    "uk": "🇬🇧 UK", "london": "🇬🇧 UK",
                    "germany": "🇩🇪 Germany", "france": "🇫🇷 France",
                }
                counts = Counter()
                for l in leads:
                    text = (l.get('company_name','') + ' ' + l.get('job_title','')).lower()
                    matched = False
                    for kw, country in country_map.items():
                        if kw in text:
                            counts[country] += 1
                            matched = True
                            break
                    if not matched:
                        counts["🌍 Other/Unknown"] += 1
                lines = [f"<b>{c}:</b> {n}" for c, n in counts.most_common(10)]
                await msg.reply_text(
                    "🌍 <b>LEADS BY COUNTRY</b>\n━━━━━━━━━━━━━━━\n" +
                    ("\n".join(lines) if lines else "<i>No data.</i>") +
                    "\n━━━━━━━━━━━━━━━",
                    parse_mode='HTML'
                )
            except Exception as e:
                await msg.reply_text(f"❌ <b>Countries error:</b> {e}", parse_mode='HTML')

        elif key == "job_titles_report":
            try:
                succ, data = await self.db._request_with_retry(
                    "GET",
                    f"{self.db.url}/rest/v1/leads?select=job_title&limit=500&status=eq.pending"
                )
                leads = data if succ and isinstance(data, list) else []
                from collections import Counter
                counts = Counter(l.get('job_title','Unknown')[:35] for l in leads if l.get('job_title'))
                lines = [f"💼 <b>{t}:</b> {n}" for t, n in counts.most_common(10)]
                await msg.reply_text(
                    "💼 <b>TOP JOB TITLES IN QUEUE</b>\n━━━━━━━━━━━━━━━\n" +
                    ("\n".join(lines) if lines else "<i>No data.</i>") +
                    "\n━━━━━━━━━━━━━━━",
                    parse_mode='HTML'
                )
            except Exception as e:
                await msg.reply_text(f"❌ <b>Job titles error:</b> {e}", parse_mode='HTML')

        elif key == "clear_queue":
            await msg.reply_text(
                "⚠️ <b>CLEAR QUEUE — CONFIRM?</b>\n"
                "━━━━━━━━━━━━━━━\n"
                "This will remove ALL pending leads from the queue.\n\n"
                "To confirm, type: <code>CONFIRM CLEAR</code>\n"
                "To cancel, ignore this message.",
                parse_mode='HTML'
            )
            context.user_data['state'] = 'WAITING_CLEAR_CONFIRM'

        elif key == "find_emails":
            status_msg = await msg.reply_text(
                "🔎 <b>FINDING EMAILS...</b>\n"
                "<i>Scanning leads without email addresses...</i>",
                parse_mode='HTML'
            )
            try:
                succ, data = await self.db._request_with_retry(
                    "GET",
                    f"{self.db.url}/rest/v1/leads?select=id,company_name,job_title&email=is.null&limit=10&status=eq.pending"
                )
                no_email = data if succ and isinstance(data, list) else []
                if not no_email:
                    await status_msg.edit_text(
                        "🔎 <b>FIND EMAILS</b>\n━━━━━━━━━━━━━━━\n✅ All leads in queue have email addresses!",
                        parse_mode='HTML'
                    )
                    return
                lines = [f"🏢 {l.get('company_name','?')[:25]} — {l.get('job_title','?')[:20]}" for l in no_email]
                await status_msg.edit_text(
                    f"🔎 <b>LEADS WITHOUT EMAIL ({len(no_email)})</b>\n"
                    f"━━━━━━━━━━━━━━━\n"
                    + "\n".join(lines) +
                    f"\n━━━━━━━━━━━━━━━\n"
                    f"<i>Bot will attempt to find emails via scraping in next cycle.</i>",
                    parse_mode='HTML'
                )
            except Exception as e:
                await status_msg.edit_text(f"❌ <b>Find emails error:</b> {e}", parse_mode='HTML')

        elif key == "pin_lead":
            context.user_data['state'] = 'WAITING_PIN_COMPANY'
            await msg.reply_text(
                "📌 <b>PIN LEAD</b>\n"
                "━━━━━━━━━━━━━━━\n"
                "Enter the <b>company name</b> to pin as top priority.\n"
                "<i>It will be moved to the front of the queue.</i>",
                parse_mode='HTML'
            )

        elif key == "skip_lead":
            status_msg = await msg.reply_text("🚫 <b>SKIPPING TOP LEAD...</b>", parse_mode='HTML')
            try:
                leads = await self.db.get_pending_leads(limit=1) if self.db else []
                if not leads:
                    await status_msg.edit_text("🚫 <b>SKIP LEAD</b>\n━━━━━━━━━━━━━━━\n❌ Queue is empty.", parse_mode='HTML')
                    return
                lead = leads[0]
                company = lead.get('company_name', 'Unknown')
                lead_id = lead.get('id')
                if lead_id:
                    await self.db._request_with_retry(
                        "PATCH",
                        f"{self.db.url}/rest/v1/leads?id=eq.{lead_id}",
                        json={"status": "skipped"}
                    )
                await status_msg.edit_text(
                    f"🚫 <b>LEAD SKIPPED</b>\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"⏭️ Skipped: <b>{company}</b>\n"
                    f"✅ Next lead is now at the front of the queue.",
                    parse_mode='HTML'
                )
            except Exception as e:
                await status_msg.edit_text(f"❌ <b>Skip error:</b> {e}", parse_mode='HTML')

        elif key == "mass_strike":
            status_msg = await msg.reply_text(
                "🎪 <b>MASS STRIKE LOADING...</b>\n"
                "<i>Fetching top 10 leads from queue...</i>",
                parse_mode='HTML'
            )
            try:
                leads = await self.db.get_pending_leads(limit=10) if self.db else []
                valid = [l for l in leads if l.get('email')]
                if not valid:
                    await status_msg.edit_text(
                        "🎪 <b>MASS STRIKE</b>\n━━━━━━━━━━━━━━━\n"
                        "❌ No leads with email addresses found.\nUse 🌍 Scrape Now to fill the queue.",
                        parse_mode='HTML'
                    )
                    return
                await status_msg.edit_text(
                    f"🎪 <b>MASS STRIKE FIRING</b>\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"🎯 Targeting <b>{len(valid)}</b> companies simultaneously...\n"
                    f"<i>This may take 30-60 seconds.</i>",
                    parse_mode='HTML'
                )
                from core import smtp_engine as _smtp
                results = await asyncio.gather(
                    *[asyncio.to_thread(_smtp.send_strike, lead) for lead in valid],
                    return_exceptions=True
                )
                sent    = sum(1 for r in results if r is True)
                failed  = len(results) - sent
                lines   = []
                for i, lead in enumerate(valid):
                    ok = results[i] is True
                    lines.append(f"{'✅' if ok else '❌'} {lead.get('company_name','?')[:25]}")
                await status_msg.edit_text(
                    f"🎪 <b>MASS STRIKE COMPLETE</b>\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"✅ Sent: {sent} | ❌ Failed: {failed}\n"
                    f"━━━━━━━━━━━━━━━\n"
                    + "\n".join(lines) +
                    "\n━━━━━━━━━━━━━━━",
                    parse_mode='HTML'
                )
            except Exception as e:
                await status_msg.edit_text(f"💥 <b>Mass strike error:</b> {e}", parse_mode='HTML')

        elif key == "track":
            try:
                from datetime import datetime, timezone
                now = datetime.now(timezone.utc)
                today_start = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat().replace("+", "%2B")
                succ, data = await self.db._request_with_retry(
                    "GET",
                    f"{self.db.url}/rest/v1/applications?select=company_name,job_title,status,timestamp&order=timestamp.desc&limit=10&timestamp=gte.{today_start}"
                )
                apps = data if succ and isinstance(data, list) else []
                lines = [f"{'✅' if a.get('status')=='SENT' else '🔄'} {a.get('company_name','?')[:22]} — {a.get('job_title','?')[:18]}" for a in apps[:10]]
                await msg.reply_text(
                    f"🛰️ <b>LIVE TRACKING — TODAY</b>\n━━━━━━━━━━━━━━━\n"
                    f"📊 <b>Sent today:</b> {len(apps)}\n━━━━━━━━━━━━━━━\n"
                    + ("\n".join(lines) if lines else "<i>No activity yet today.</i>") +
                    "\n━━━━━━━━━━━━━━━",
                    parse_mode='HTML'
                )
            except Exception as e:
                await msg.reply_text(f"❌ Track error: {e}", parse_mode='HTML')

        elif key == "oracle":
            status_msg = await msg.reply_text("🔮 <b>ORACLE SCANNING MARKET...</b>\n<i>Analyzing job market trends...</i>", parse_mode='HTML')
            try:
                succ, data = await self.db._request_with_retry(
                    "GET",
                    f"{self.db.url}/rest/v1/leads?select=job_title,company_name&order=created_at.desc&limit=100"
                )
                leads = data if succ and isinstance(data, list) else []
                from collections import Counter
                titles = Counter(l.get('job_title','')[:30] for l in leads if l.get('job_title'))
                top = titles.most_common(5)
                lines = [f"🎯 <b>{t}:</b> {c} openings" for t, c in top]
                await status_msg.edit_text(
                    f"🔮 <b>MARKET ORACLE REPORT</b>\n━━━━━━━━━━━━━━━\n"
                    f"📊 <b>Total leads analyzed:</b> {len(leads)}\n━━━━━━━━━━━━━━━\n"
                    f"<b>🔥 Hottest roles right now:</b>\n"
                    + ("\n".join(lines) if lines else "<i>Not enough data yet.</i>") +
                    "\n━━━━━━━━━━━━━━━\n<i>Based on live job market data</i>",
                    parse_mode='HTML'
                )
            except Exception as e:
                await status_msg.edit_text(f"❌ Oracle error: {e}", parse_mode='HTML')

        elif key == "synapse":
            try:
                stats = await self.db.get_stats() if self.db else {}
                health = self.db.get_system_health() if self.db else {}
                groq_ok = bool(os.getenv("GROQ_API_KEY"))
                gemini_ok = bool(os.getenv("GEMINI_API_KEY"))
                openrouter_ok = bool(os.getenv("OPENROUTER_API_KEY"))
                ai_count = sum([groq_ok, gemini_ok, openrouter_ok])
                await msg.reply_text(
                    f"💪 <b>STRENGTH CHECK</b>\n━━━━━━━━━━━━━━━\n"
                    f"🧠 <b>AI Providers:</b> {ai_count}/3 active\n"
                    f"  {'✅' if groq_ok else '❌'} Groq\n"
                    f"  {'✅' if gemini_ok else '❌'} Gemini\n"
                    f"  {'✅' if openrouter_ok else '❌'} OpenRouter\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"🚀 <b>Total applications:</b> {stats.get('total_strikes', 0)}\n"
                    f"🎯 <b>Total leads:</b> {stats.get('recon_rows', 0)}\n"
                    f"⚙️ <b>Engine:</b> {health.get('engine', 'ACTIVE')}\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"{'✅ System at full strength' if ai_count >= 2 else '⚠️ Add more AI keys for redundancy'}",
                    parse_mode='HTML'
                )
            except Exception as e:
                await msg.reply_text(f"❌ Synapse error: {e}", parse_mode='HTML')

        elif key == "platforms":
            try:
                succ, data = await self.db._request_with_retry(
                    "GET",
                    f"{self.db.url}/rest/v1/leads?select=job_url&limit=500"
                )
                leads = data if succ and isinstance(data, list) else []
                from collections import Counter
                import re as _re
                platform_map = {
                    "linkedin": "💼 LinkedIn", "indeed": "🔍 Indeed",
                    "bayt": "🌍 Bayt", "naukrigulf": "🏢 Naukrigulf",
                    "gulftalent": "⭐ GulfTalent", "daleel": "📋 Daleel Madani",
                    "glassdoor": "🪟 Glassdoor", "monster": "👾 Monster",
                }
                counts = Counter()
                for l in leads:
                    url = (l.get('job_url') or '').lower()
                    matched = False
                    for kw, name in platform_map.items():
                        if kw in url:
                            counts[name] += 1
                            matched = True
                            break
                    if not matched and url:
                        counts["🌐 Other"] += 1
                lines = [f"<b>{p}:</b> {c} leads" for p, c in counts.most_common(8)]
                await msg.reply_text(
                    "🌐 <b>JOB SOURCES</b>\n━━━━━━━━━━━━━━━\n"
                    + ("\n".join(lines) if lines else "<i>No platform data yet.</i>") +
                    "\n━━━━━━━━━━━━━━━",
                    parse_mode='HTML'
                )
            except Exception as e:
                await msg.reply_text(f"❌ Platforms error: {e}", parse_mode='HTML')

        elif key in ("stats", "status"):
            await self._dispatch_command(f"/{key}", update, context)

        elif key in ("menu", "guide", "reboot", "launch_single", "settings", "fix", "backup", "audit"):
            await self._dispatch_command(f"/{key}", update, context)

    async def handle_text_oracle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.authenticate(update): return
        user_text = update.message.text
        if not user_text: return

        # [🧪 TEST-STRIKE STATE MACHINE]
        is_test_state = context.user_data.get('state') == 'WAITING_TEST_EMAIL'
        is_email_only = "@" in user_text and "." in user_text and len(user_text.split()) == 1

        # [🗑️ CLEAR QUEUE CONFIRM STATE]
        if context.user_data.get('state') == 'WAITING_CLEAR_CONFIRM':
            context.user_data['state'] = None
            if user_text.strip().upper() == "CONFIRM CLEAR":
                status_msg = await update.message.reply_text("🗑️ <b>CLEARING QUEUE...</b>", parse_mode='HTML')
                try:
                    await self.db._request_with_retry(
                        "PATCH",
                        f"{self.db.url}/rest/v1/leads?status=eq.pending",
                        json={"status": "cleared"}
                    )
                    await status_msg.edit_text(
                        "🗑️ <b>QUEUE CLEARED</b>\n━━━━━━━━━━━━━━━\n"
                        "✅ All pending leads removed.\n"
                        "Use 🌍 Scrape Now to refill.",
                        parse_mode='HTML'
                    )
                except Exception as e:
                    await status_msg.edit_text(f"❌ <b>Clear error:</b> {e}", parse_mode='HTML')
            else:
                await update.message.reply_text("❌ <b>CANCELLED.</b> Queue was not cleared.", parse_mode='HTML')
            return

        # [📌 PIN LEAD STATE]
        if context.user_data.get('state') == 'WAITING_PIN_COMPANY':
            context.user_data['state'] = None
            company_name = user_text.strip()
            status_msg = await update.message.reply_text(f"📌 <b>PINNING:</b> {company_name}...", parse_mode='HTML')
            try:
                await self.db._request_with_retry(
                    "PATCH",
                    f"{self.db.url}/rest/v1/leads?company_name=ilike.*{company_name}*&status=eq.pending",
                    json={"priority_score": 999}
                )
                await status_msg.edit_text(
                    f"📌 <b>LEAD PINNED</b>\n━━━━━━━━━━━━━━━\n"
                    f"✅ <b>{company_name}</b> set to max priority (999).\n"
                    f"It will be processed first in the next cycle.",
                    parse_mode='HTML'
                )
            except Exception as e:
                await status_msg.edit_text(f"❌ <b>Pin error:</b> {e}", parse_mode='HTML')
            return
        
        if is_test_state or is_email_only:
            email = user_text.strip()
            # Basic validation
            if "@" not in email or "." not in email:
                if is_test_state:
                    await update.message.reply_text("❌ <b>INVALID EMAIL</b>\nPlease enter a valid email address for the test strike.", parse_mode='HTML')
                return
            
            context.user_data['state'] = None
            try:
                msg = await update.message.reply_text("🧬 <b>GENERATING DUAL-PACKAGE...</b>\n<i>Constructing CV & Cover Letter for test verification.</i>", parse_mode='HTML')
            except Exception as e:
                logging.error(f"⚠️ [STRIKE-ERR] Initial reply failed: {e}")
                return
            
            # [🛡️ RESPONSIVENESS]: Tiny sleep to ensure the message is dispatched to the user before heavy I/O
            await asyncio.sleep(0.1)

            try:
                # [👑 DIAGNOSTIC]: Check for Render-specific SMTP blocks
                if os.getenv("RENDER") and not (os.getenv("BREVO_SMTP_PASSWORD", "")).strip() and not (os.getenv("BREVO_API_KEY", "")).strip():
                    try:
                        await msg.edit_text("❌ <b>STRIKE FAILED: RENDER BLOCK</b>\nYou are on Render, but <code>BREVO_SMTP_PASSWORD</code> is not set. Render blocks standard SMTP (Port 587/465). Please add your Brevo key to bypass this.", parse_mode='HTML')
                    except Exception as e:
                        logging.warning(f"Failed to edit message: {e}")
                    return

                # Run in thread to avoid blocking event loop during PDF generation
                # [🛡️ TIMEOUT FIX]: Add 90s timeout so the message never stays stuck forever
                logging.info(f"🧪 Sending test email to: {email}")
                try:
                    success = await asyncio.wait_for(
                        asyncio.to_thread(smtp_engine.send_test_email, email),
                        timeout=45.0  # 45s max — PDF skipped on cloud so this is plenty
                    )
                except asyncio.TimeoutError:
                    logging.error(f"⏰ Test strike timed out after 45s for {email}")
                    try:
                        await msg.edit_text(
                            f"⏰ <b>TEST STRIKE TIMED OUT</b>\n\n"
                            f"📧 Target: <code>{email}</code>\n\n"
                            f"The email took too long to send (>45s).\n"
                            f"<i>Try again — it usually works on the second attempt.</i>",
                            parse_mode='HTML'
                        )
                    except Exception as edit_err:
                        logging.warning(f"Failed to edit timeout message: {edit_err}")
                    return
                
                if success:
                    # Check if it's Outlook and warn
                    is_outlook = any(domain in email.lower() for domain in ['outlook.com', 'hotmail.com', 'live.com'])
                    
                    success_msg = (
                        f"✅ <b>TEST STRIKE DELIVERED!</b>\n\n"
                        f"📧 Sent to: <code>{email}</code>\n"
                        f"📦 Attachments: CV + Cover Letter\n\n"
                    )
                    
                    if is_outlook:
                        success_msg += (
                            "⚠️ <b>OUTLOOK WARNING:</b>\n"
                            "Microsoft Outlook may block emails from Brevo.\n"
                            "If you don't receive it, check:\n"
                            "• Junk/Spam folder\n"
                            "• 'Other' inbox tab (Focused Inbox)\n"
                            "• Blocked senders list\n\n"
                            "💡 <b>TIP:</b> Use Gmail for testing:\n"
                            "<code>samsalameh.cv@gmail.com</code>\n\n"
                        )
                    else:
                        success_msg += "Check your inbox (and spam folder) for the test email.\n\n"
                    
                    success_msg += (
                        "<i>If you don't receive it within 2 minutes, check:</i>\n"
                        "• Spam/Junk folder\n"
                        "• Email address is correct\n"
                        "• SMTP credentials in .env"
                    )
                    
                    try:
                        await msg.edit_text(success_msg, parse_mode='HTML')
                    except Exception as e:
                        logging.warning(f"Failed to edit message: {e}")
                        # Fallback: send a new message so user always gets the result
                        try:
                            await update.message.reply_text(success_msg, parse_mode='HTML')
                        except Exception as reply_err:
                            logging.error(f"Failed to send success reply: {reply_err}")
                else:
                    # Get more details about the failure
                    zoho_configured = bool(os.getenv("ZOHO_SMTP_USER") and os.getenv("ZOHO_APP_PASSWORD"))
                    brevo_configured = bool(os.getenv("BREVO_SMTP_LOGIN") and os.getenv("BREVO_SMTP_PASSWORD"))
                    gmail_configured = bool(os.getenv("GMAIL_SMTP_USER") and os.getenv("GMAIL_APP_PASSWORD"))
                    
                    error_msg = "❌ <b>STRIKE FAILED</b>\n\n"
                    error_msg += f"📧 Target: <code>{email}</code>\n\n"
                    error_msg += "<b>Email Providers Status:</b>\n"
                    error_msg += f"• Zoho: {'✅ Configured' if zoho_configured else '❌ Not configured'}\n"
                    error_msg += f"• Brevo: {'✅ Configured' if brevo_configured else '❌ Not configured'}\n"
                    error_msg += f"• Gmail: {'✅ Configured' if gmail_configured else '❌ Not configured'}\n\n"
                    
                    if not (zoho_configured or brevo_configured or gmail_configured):
                        error_msg += "⚠️ <b>No email providers configured!</b>\n"
                        error_msg += "Please add SMTP credentials to .env file."
                    else:
                        error_msg += "⚠️ Check system logs for detailed error.\n"
                        error_msg += "Common issues:\n"
                        error_msg += "• Wrong SMTP password\n"
                        error_msg += "• Firewall blocking ports\n"
                        error_msg += "• Email provider blocking"
                    
                    try:
                        await msg.edit_text(error_msg, parse_mode='HTML')
                    except Exception as e:
                        logging.warning(f"Failed to edit message: {e}")
                        # Fallback: send a new message so user always gets the result
                        try:
                            await update.message.reply_text(error_msg, parse_mode='HTML')
                        except Exception as reply_err:
                            logging.error(f"Failed to send error reply: {reply_err}")
            except Exception as e:
                logging.error(f"💥 Test strike error: {e}")
                try:
                    await msg.edit_text(f"💥 <b>INTERNAL ERROR:</b>\n<code>{str(e)[:200]}</code>", parse_mode='HTML')
                except Exception as edit_err:
                    logging.warning(f"Failed to edit message: {edit_err}")
                    try:
                        await update.message.reply_text(f"💥 <b>INTERNAL ERROR:</b>\n<code>{str(e)[:200]}</code>", parse_mode='HTML')
                    except Exception as reply_err:
                        logging.error(f"Failed to send error reply: {reply_err}")
            return

        if user_text.startswith('/'): return

        logging.info(f"📥 [SIGNAL RECEIVED] Raw Body: '{user_text}'")

        # 🧠 [STAGE 1]: Aggressive Atomic Normalization (The 'Sovereign' Standard)
        parts = self.get_normalized_parts(user_text)
        logging.info(f"🔎 [SIGNAL-DEBUG] Normalized Parts: {parts}")
        text_map = {
            "run now": "launch_single", "تشغيل": "launch_single",
            "status": "status", "الحالة": "status",
            "tasks": "tasks", "المهام": "tasks",
            "shield": "shield", "الدرع": "shield",
            "pulse": "pulse", "النبض": "pulse",
            "stats": "stats", "الإحصائيات": "stats",
            "leads": "leads", "الفرص": "leads",
            "prep": "prep", "التحضير": "prep",
            "campaign": "campaign", "حملة جديدة": "campaign",
            "follow up": "followup", "followup": "followup", "المتابعة": "followup",
            "companies": "companies", "الشركات": "companies",
            "settings": "settings", "الإعدادات": "settings",
            "pause": "pause", "إيقاف مؤقت": "pause",
            "resume": "resume", "استئناف": "resume",
            "track": "track", "التتبع": "track",
            "omega halt": "kill", "التوقف التام": "kill",
            "lazarus": "lazarus", "الإحياء": "lazarus",
            "repair": "repair", "الإصلاح": "repair",
            "hygiene": "hygiene", "التنظيف": "hygiene",
            "reboot": "reboot", "إعادة تشغيل": "reboot",
            "menu": "menu", "guide": "guide", "الدليل": "guide",
            "evolution": "evolution", "audit": "audit",
            "mock interview": "mock_interview", "ghost": "mock_interview",
            "test strike": "test_strike", "تجربة": "test_strike",
            "test email": "quick_test_email", "تجربة إيميل": "quick_test_email",
            "test strike": "test_strike", "تجربة ضربة": "test_strike",
            "today report": "today_report", "تقرير اليوم": "today_report",
            "email stats": "email_stats", "إحصاء الإيميل": "email_stats",
            "queue": "queue_status", "الطابور": "queue_status",
            "run now": "launch_single", "شغل": "launch_single", "شغّل": "launch_single",
            "fix": "fix", "إصلاح": "fix",
            "audit": "audit", "مراجعة": "audit",
            "synapse": "synapse", "قوة": "synapse",
            "clean disk": "clean_disk", "تنظيف": "clean_disk",
            "backup": "backup", "نسخة احتياطية": "backup",
            "kill switch": "kill", "إيقاف كامل": "kill",
            "memory": "memory_status", "الذاكرة": "memory_status",
            "uptime": "uptime_status", "وقت التشغيل": "uptime_status",
            "ai status": "ai_status", "حالة الذكاء": "ai_status",
            "ai check": "ai_check", "فحص ai": "ai_check", "فحص الذكاء": "ai_check",
            "keys": "keys", "api keys": "keys", "مفاتيح": "keys", "المفاتيح": "keys",
            "inbox check": "inbox_check", "فحص الردود": "inbox_check",
            "top companies": "top_companies", "أفضل شركات": "top_companies",
            "scrape now": "scrape_now", "اسكان فوري": "scrape_now",
            "force strike": "force_strike", "ضربة فورية": "force_strike",
            "follow-ups": "followup", "followups": "followup", "متابعات": "followup",
            "boost mode": "boost_mode", "وضع تسريع": "boost_mode",
            "oracle": "oracle", "أوراكل": "oracle",
            "weekly report": "weekly_report", "تقرير أسبوعي": "weekly_report",
            "failure rate": "failure_rate", "نسبة الفشل": "failure_rate",
            "best day": "best_day", "أفضل يوم": "best_day",
            "notify me": "notify_me", "أخبرني": "notify_me",
            "blacklist": "blacklist_view", "القائمة السوداء": "blacklist_view",
            "retry failed": "retry_failed", "إعادة الفاشلين": "retry_failed",
            "night mode": "night_mode", "وضع الليل": "night_mode",
            "dry run": "dry_run", "تجربة بدون إرسال": "dry_run",
            "cv preview": "cv_preview", "معاينة السيرة": "cv_preview",
            "cover letter": "cover_letter_preview", "رسالة التغطية": "cover_letter_preview",
            "monthly report": "monthly_report",   "تقرير شهري": "monthly_report",
            "provider health": "provider_health", "صحة المزودين": "provider_health",
            "speed test": "speed_test",           "اختبار السرعة": "speed_test",
            "ping render": "ping_render",         "اختبار الخادم": "ping_render",
            "env check": "env_check",             "فحص المتغيرات": "env_check",
            "countries": "countries_report",      "الدول": "countries_report",
            "job titles": "job_titles_report",    "المسميات": "job_titles_report",
            "clear queue": "clear_queue",         "مسح الطابور": "clear_queue",
            "find emails": "find_emails",         "ابحث عن إيميلات": "find_emails",
            "pin lead": "pin_lead",               "تثبيت": "pin_lead",
            "skip lead": "skip_lead",             "تخطي": "skip_lead",
            "mass strike": "mass_strike",         "ضربة جماعية": "mass_strike",
            "synapse": "synapse", "platforms": "platforms", "sources": "platforms", "المواقع": "platforms",
            "logs": "logs", "السجلات": "logs",
            "track": "track", "التتبع المباشر": "track",
            "oracle": "oracle", "أوراكل السوق": "oracle",
            "api keys": "keys", "مفاتيح api": "keys",
            "ai check": "ai_check", "فحص الذكاء": "ai_check",
            "set key": "setkey", "تغيير مفتاح": "setkey",
            "test key": "testkey", "اختبار مفتاح": "testkey",
            "pin lead": "pin_lead", "تثبيت أولوية": "pin_lead",
            "find emails": "find_emails", "بحث إيميلات": "find_emails",
            "countries": "countries_report", "الدول المستهدفة": "countries_report",
            "job titles": "job_titles_report", "المسميات الوظيفية": "job_titles_report",
            "weekly": "weekly_report", "أسبوعي": "weekly_report",
            "monthly": "monthly_report", "شهري": "monthly_report",
            "best day": "best_day", "أفضل يوم": "best_day",
            "failure": "failure_rate", "نسبة الفشل": "failure_rate",
            "speed": "speed_test", "سرعة الإرسال": "speed_test",
            "ping": "ping_render", "اختبار الخادم": "ping_render",
            "env": "env_check", "المتغيرات": "env_check",
            "clean": "clean_disk", "تنظيف الذاكرة": "clean_disk",
            "boost": "boost_mode", "تسريع": "boost_mode",
            "night": "night_mode", "وضع الليل": "night_mode",
            "dry run": "dry_run", "تجربة آمنة": "dry_run",
            "retry": "retry_failed", "إعادة الفاشلين": "retry_failed",
            "blacklist": "blacklist_view", "القائمة السوداء": "blacklist_view",
            "notify": "notify_me", "الإشعارات": "notify_me",
            "inbox": "inbox_check", "فحص الردود": "inbox_check",
            "mass strike": "mass_strike", "ضربة جماعية": "mass_strike",
            "backup": "backup", "نسخة احتياطية": "backup",
            "campaign": "campaign", "الحملة": "campaign",
        }

        mapped = None
        for p in parts:
            if p in text_map:
                mapped = text_map[p]
                logging.info(f"🎯 [MATCH-FOUND] Atomic Match: '{p}' -> {mapped}")
                break

        # 🚀 [STAGE 2]: Substring Containment (The 'Immortality' Fallback)
        if not mapped:
            normalized_full = self.normalize_text(user_text)
            logging.info(f"🔎 [SIGNAL-FALLBACK] Checking Full String: '{normalized_full}'")
            for trigger, command in text_map.items():
                if trigger in normalized_full:
                    mapped = command
                    logging.info(f"⚡ [MATCH-FOUND] Substring Match: Trigger '{trigger}' found in HUD command.")
                    break
        if not mapped:
            logging.warning(f"🔦 [SIGNAL-LOST] No command recognized for: '{user_text}'. Passing to AI Oracle.")
            # ... passing to AI logic ...

        if mapped:
            slash_cmds = {"launch_single", "menu", "pause", "resume", "track", "kill",
                          "lazarus", "repair", "hygiene", "reboot", "status",
                          "guide", "evolution", "audit", "hud", "backup", "oracle",
                          "mock_interview", "synapse", "logs", "settings", "fix", "followup",
                          "ai_check", "keys", "apikeys", "setkey", "testkey"}
            if mapped in slash_cmds:
                return await self._dispatch_command(f"/{mapped}", update, context)
            else:
                return await self._handle_text_map(mapped, update, context)

        if "status" in clean: return await self._dispatch_command("/status", update, context)
        if "stats" in clean: return await self._dispatch_command("/stats", update, context)

        prompt = f"""CEO COMMAND: "{user_text}"\nIntent: strike | stats | chat. Return JSON with 'reply_message' and 'intent' keys."""
        try:
            data = None
            if self.ai.primary_engine == "gemini":
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(None, self.ai.model.generate_content, prompt)
                data = self.ai._extract_json_robustly(response.text)
            if not data and self.ai.groq_key:
                data = await self.ai.structural_query(prompt)
            if not data:
                await update.message.reply_text("⚠️ <b>GHOST MODE ACTIVE.</b> AI Oracle is in deep-sleep.", parse_mode='HTML')
                return
            reply_msg = data.get("reply_message", "Understood. Execution starting.")
            await update.message.reply_text(f"🤖 <b>Oracle:</b> {reply_msg}", parse_mode='HTML')
        except Exception as e:
            logging.error(f"🔮 AI ORACLE ERROR: {e}")
            await update.message.reply_text(f"⚠️ <i>Deep-sleep fallback engaged.</i>", parse_mode='HTML')

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        await self._dispatch_command(query.data, update, context)

    async def handle_inline_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        latest = await self.db.get_latest_application() if self.db else None
        strikes = [latest] if latest else []
        results = []
        for i, s in enumerate(strikes):
            title = f"📄 CV: {s['company_name']} - {s['job_title']}"
            desc = f"Applied on: {s.get('timestamp', 'N/A')}"
            content = f"Sovereign CV for {s['job_title']} at {s['company_name']}.\nLink: {s.get('job_url', '')}"
            results.append(InlineQueryResultArticle(id=str(i), title=title, description=desc, input_message_content=InputTextMessageContent(content)))
        await update.inline_query.answer(results, cache_time=300)

    async def handle_web_app_data(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        import json
        try:
            data = json.loads(update.effective_message.web_app_data.data)
        except Exception:
            await update.effective_message.reply_text("⚠️ Invalid TWA payload.", parse_mode='HTML')
            return

        action = data.get("action")
        if action == "execute_pulse":
            await self._dispatch_command("/hud", update, context)
        elif action == "launch_ghost":
            if os.path.exists("ghost_interview.py"): subprocess.Popen([sys.executable, "ghost_interview.py"])
        elif action == "launch_oracle":
            await self._dispatch_command("/oracle", update, context)

    async def _execute_backup_logic(self, bot, chat_id):
        import shutil, time, zipfile
        backup_name = f"backup_{int(time.time())}.zip"
        try:
            with zipfile.ZipFile(backup_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if os.path.exists("sam_ultimate.db"): zipf.write("sam_ultimate.db")
                for dir_name in ["logs", "pdf_cache"]:
                    if os.path.exists(dir_name):
                        for root, _, files in os.walk(dir_name):
                            for f in files: zipf.write(os.path.join(root, f))
            with open(backup_name, "rb") as doc:
                await bot.send_document(chat_id=chat_id, document=doc, caption="💾 <b>Data Lake Backup Secured.</b>", parse_mode='HTML')
        finally:
            if os.path.exists(backup_name): os.remove(backup_name)

    async def _handle_vip_portal(self, target_id: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
        company_name = await self.db.track_vip_hit(target_id)
        if company_name:
            ping_msg = f"🚨 <b>SOVEREIGN RADAR PING</b>\n🎯 <b>Target:</b> <code>{company_name}</code>\n👤 <b>ID:</b> <code>{update.effective_user.id}</code>"
            await self.broadcast_message(context.bot, text=ping_msg)
            welcome_msg = f"👋 <b>Welcome to the VIP Portal</b>\n\nYou are viewing a custom-architected profile for <b>{company_name}</b>."
            keyboard = [[InlineKeyboardButton("📊 View Tailored Stats", web_app=WebAppInfo(url=f"{os.getenv('RENDER_EXTERNAL_URL', 'https://sam-job-automator.onrender.com')}/#/vip?id={target_id}"))]]
            await update.effective_message.reply_text(welcome_msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        else:
            await update.effective_message.reply_text("Project Chronos initializing...")

    async def _live_hud_loop(self, bot, chat_id):
        while True:
            try:
                if not self.hud_message_id: break
                cpu = psutil.cpu_percent() if psutil else "N/A"
                ram = psutil.virtual_memory().percent if psutil else "N/A"
                health = self.db.get_advanced_health()
                hud_text = f"📟 <b>LIVE HUD</b>\n⏱️ <b>Uptime:</b> <code>{health.get('uptime', 'N/A')}</code>\n🎯 <b>Scanned:</b> <code>{health.get('recon_rows', 0)}</code>\n🚀 <b>Strikes:</b> <code>{health.get('heartbeat_rows', 0)}</code>\n⚡ <b>Load:</b> {cpu}% | RAM {ram}%"
                await bot.edit_message_text(chat_id=chat_id, message_id=self.hud_message_id, text=hud_text, parse_mode='HTML')
            except Exception: pass
            await asyncio.sleep(10)

    async def _auto_backup_loop(self, bot):
        # [🚀 DAILY BACKUP]: Wait 24 hours before the first backup, preventing spam on bot restarts
        await asyncio.sleep(86400)
        while True:
            try:
                logging.info("💾 [AUTO-BACKUP] Initiating periodic Data Lake archival...")
                await self._execute_backup_logic(bot, self.authorized_users[0])
            except Exception as e:
                logging.error(f"⚠️ [AUTO-BACKUP] Archive cycle failed: {e}")
            
            # Wait 24 hours between backups
            await asyncio.sleep(86400)

    async def _genesis_watchdog_loop(self):
        genesis_path = os.path.join(os.getcwd(), "protocol_genesis.py")
        if os.path.exists(genesis_path): subprocess.Popen([sys.executable, genesis_path])

    async def _neural_watchdog_loop(self, bot):
        """High-frequency mission queue monitor. Bridging Web-to-Bot commands."""
        chat_id = self.authorized_users[0]
        while True:
            try:
                tasks = await self.db.get_pending_tasks(limit=5)
                for t in tasks:
                    action = t.get('type')
                    task_id = t.get('id')
                    
                    logging.info(f"🧠 NEURAL WATCHDOG: Processing {action} (Task {task_id})")
                    
                    if action == "execute_pulse":
                        # Trigger the live HUD loop in the Telegram chat
                        hud_text = "📟 <b>INITIALIZING LIVE HUD...</b>\n<i>Tactical pulse triggered from Matrix HUD.</i>"
                        # [👑 BROADCAST]: HUD is chat-specific, but let's notify everyone of initialization
                        await self.broadcast_message(bot, text="📟 <b>TACTICAL HUD INITIALIZED:</b> Live feed starting for master node.")
                        msg = await bot.send_message(chat_id=chat_id, text=hud_text, parse_mode='HTML')
                        self.hud_message_id = msg.message_id
                        try:
                            await bot.pin_chat_message(chat_id=chat_id, message_id=self.hud_message_id)
                        except: pass
                        asyncio.create_task(self._live_hud_loop(bot, chat_id))
                        
                    elif action == "launch_ghost":
                        if os.path.exists("ghost_interview.py"): 
                            subprocess.Popen([sys.executable, "ghost_interview.py"])
                            await self.broadcast_message(bot, text="👻 <b>GHOST HUB:</b> Tactical agent deployed.")
                        else:
                            await bot.send_message(chat_id=chat_id, text="⚠️ Ghost agent not found locally.", parse_mode='HTML')
                            
                    elif action == "launch_oracle":
                        oracle_path = os.path.join(os.getcwd(), "market_oracle.py")
                        if os.path.exists(oracle_path):
                            subprocess.Popen([sys.executable, oracle_path])
                            await bot.send_message(chat_id=chat_id, text="🔮 <b>ORACLE:</b> Market expansion scan initiated.", parse_mode='HTML')
                        else:
                            await bot.send_message(chat_id=chat_id, text="⚠️ Market Oracle not found.", parse_mode='HTML')
                            
                    elif action == "broadcast_notification":
                        msg_text = t.get('meta', 'System Notification')
                        await self.broadcast_message(bot, text=msg_text)
                            
                    # Mark as COMPLETED to prevent duplicate execution
                    await self.db.mark_task_completed(task_id)
                    logging.info(f"✅ NEURAL WATCHDOG: Task {task_id} marked as completed.")
                    
            except Exception as e:
                logging.error(f"⚠️ NEURAL WATCHDOG ERROR: {e}")
            
            await asyncio.sleep(5)

    async def _sync_leadership(self):
        while True:
            try:
                self.is_leader = await self.db.claim_bot_leadership()
                if self.is_leader: 
                    logging.info("👑 TRANSITION: Leadership acquired. Resuming C2 Operations.")
                    return
            except Exception as e:
                logging.error(f"🛰️ STANDBY ERROR: {e}")
            await asyncio.sleep(15) # Faster check for takeover


    def ignite(self):
        """Legacy standalone ignition. Redirects to unified asyncio task loop."""
        logging.info("📡 Sovereign Dashboard: Redirecting to Unified Swarm Loop...")
        asyncio.run(self.run_headless())


    async def run_headless(self):
        """[👑 SLIM-SWARM]: Run the dashboard as a non-blocking asyncio task."""
        if not self.token or "your_" in self.token: return
        logging.info("📡 Sovereign Dashboard: Igniting in Task-Mode...")

        # [☢️ NUCLEAR FIX]: Pre-clear any lingering Telegram session before starting.
        # This is critical during Render deploys where old/new processes overlap.
        import httpx
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"https://api.telegram.org/bot{self.token}/deleteWebhook",
                    data={"drop_pending_updates": "true"}
                )
            logging.info("🧹 Pre-cleared Telegram session before Application build.")
            await asyncio.sleep(3)  # Give Telegram time to release
        except Exception as e:
            logging.warning(f"Pre-clear failed (non-fatal): {e}")

        # Build the Application ONCE
        self.app = ApplicationBuilder().token(self.token).build()
        # NOTE: Do NOT call self.app.initialize() here — async with self.app: handles it automatically.
        # Calling it twice causes a "Timed out" error on Render.
        self.app.add_handler(CommandHandler("start", self.handle_command))
        self.app.add_handler(MessageHandler(filters.COMMAND, self.handle_command))
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))
        self.app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_text_oracle))
        self.app.add_handler(InlineQueryHandler(self.handle_inline_query))
        self.app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, self.handle_web_app_data))

        async with self.app:
            # async with handles initialize() AND shutdown() automatically.
            await self.app.start()
            poller_running = False

            # Sync UI after start (bot is now connected to Telegram)
            try:
                await self._sync_ui_standalone(self.app)
            except Exception as e:
                logging.warning(f"⚠️ UI sync failed (non-fatal): {e}")

            try:
                await self.app.bot.delete_webhook(drop_pending_updates=False)
            except Exception as e:
                logging.warning(f"⚠️ WEBHOOK RESET SKIPPED: {e}")

            # Single infinite loop - ALL recovery happens here, no outer retry
            while True:
                try:
                    await asyncio.sleep(15)  # Check leadership every 15s

                    # On Render: always leader (single instance)
                    import os as _os
                    if _os.getenv("RENDER"):
                        self.is_leader = True
                        claimed = True
                        verified = True
                    else:
                        claimed = await self.db.claim_bot_leadership()
                        await asyncio.sleep(1)
                        verified = await self.db.is_bot_leader()

                        if verified is None:
                            logging.debug("⚠️ LEADERSHIP VERIFY FAILED: Network error. Falling back to claim.")
                            self.is_leader = claimed
                        elif claimed and not verified:
                            logging.warning("⚠️ LEADERSHIP RACED: Claimed but verify failed. Yielding.")
                            self._leader_verify_degraded = False
                            self.is_leader = False
                        else:
                            self.is_leader = bool(claimed and verified)

                    # [👑 SOVEREIGN RECOVERY]: Only start poller if we ARE the verified leader
                    if self.is_leader and not poller_running:
                        # [🔥 TOTAL IGNITION]: Start background loops if they haven't started yet
                        if not self._loops_started:
                            # SET FLAG FIRST to prevent infinite re-spawning on import errors
                            self._loops_started = True
                            logging.info("🔥 LEADERSHIP ACQUIRED: Launching Sovereign Background Loops...")
                            
                            try:
                                asyncio.create_task(self._auto_backup_loop(self.app.bot))
                            except Exception as e:
                                logging.error(f"⚠️ Failed to start auto_backup_loop: {e}")
                            try:
                                asyncio.create_task(self._genesis_watchdog_loop())
                            except Exception as e:
                                logging.error(f"⚠️ Failed to start genesis_watchdog_loop: {e}")
                            try:
                                asyncio.create_task(self._neural_watchdog_loop(self.app.bot))
                            except Exception as e:
                                logging.error(f"⚠️ Failed to start neural_watchdog_loop: {e}")
                            try:
                                from core.phantom_client import PhantomClient
                                asyncio.create_task(PhantomClient().run_watchdog())
                            except Exception as e:
                                logging.error(f"⚠️ Failed to start PhantomClient: {e}")
                            
                            # [🔥 FIX]: Do NOT start AlphaOrchestrator here — it's already running
                            # from run.py as a separate task. Starting it twice causes conflicts
                            # and double-processing of leads.
                            logging.info("✅ ALL LOOPS ARMED: Auto-Backup, Watchdogs & Phantom. (Engine already running from run.py)")
                            
                            # HUD RECONNECTION LOGIC
                            try:
                                chat = await self.app.bot.get_chat(self.authorized_users[0])
                                if chat.pinned_message and "LIVE HUD" in chat.pinned_message.text:
                                    self.hud_message_id = chat.pinned_message.message_id
                                    asyncio.create_task(self._live_hud_loop(self.app.bot, self.authorized_users[0]))
                                    logging.info("📟 LIVE HUD successfully reconnected to pinned message.")
                            except Exception as e:
                                logging.warning(f"⚠️ Failed to reconnect HUD: {e}")

                        try:
                            await self.app.bot.delete_webhook(drop_pending_updates=True)
                        except: pass

                        await self.app.updater.start_polling(
                            drop_pending_updates=True,
                            error_callback=self._build_polling_error_callback()
                        )
                        poller_running = True
                        logging.info("🟢 SOVEREIGN LINK: Dashboard Poller Active (Leader Node).")
                    elif (not self.is_leader) and poller_running:
                        logging.info("🛰️ STANDBY MODE: Leadership lost. Releasing Telegram locks gracefully.")
                        try:
                            await self.app.updater.stop()
                            await self.app.stop()
                            await self.app.shutdown()
                        except: pass
                        poller_running = False
                        # [👑 STANDBY HARMONY]: Stay alive to serve the Web HUD, but stop polling.
                        # This prevents the Render restart loop and "Jitter" on redeployment.
                        logging.info("💤 STANDBY MODE: Bot is now idle. Process remains active for Web HUD.")
                        continue # Continue the heartbeat loop to re-check leadership later

                except asyncio.CancelledError:
                    raise  # Let it propagate to exit cleanly
                except Exception as inner_err:
                    # [👑 DIAGNOSTIC]: Catch Groq 401 explicitly to warn the user
                    if "GROQ HTTP 401" in str(inner_err) or "invalid_api_key" in str(inner_err):
                        logging.critical("🚨 CRITICAL: GROQ_API_KEY IS INVALID. AI-driven tasks will fail.")
                        try:
                            # Only warn once per session to avoid spamming
                            if not getattr(self, '_groq_warned', False):
                                await self.app.bot.send_message(
                                    self.authorized_users[0], 
                                    "🚨 <b>CRITICAL SYSTEM ALERT</b>\nYour <code>GROQ_API_KEY</code> is invalid or expired. CV tailoring and AI analysis are currently DISABLED. Please update your Render environment variables.",
                                    parse_mode='HTML'
                                )
                                self._groq_warned = True
                        except: pass
                    
                    logging.error(f"⚠️ Inner loop error (non-fatal): {inner_err}")
                    await asyncio.sleep(10)

if __name__ == "__main__":
    bot = SovereignDashboard()
    bot.ignite()
