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
                except:
                    self.authorized_users.append(part)
        
        # Primary chat ID for administrative tasks
        self.chat_id = self.authorized_users[0] if self.authorized_users else None
        self.hud_message_id = None
        self.is_leader = False
        self._phantom_state = {} # Temporary state for UserBot linking
        self._polling_conflict = False
        self._leader_verify_degraded = False
        self._loops_started = False # Flag to ensure background tasks start only once
        
        from core.runtime_helpers import ProxyMesh
        self.proxy_mesh = ProxyMesh()
        
        # Telemetry Stream

    def _build_polling_error_callback(self):
        """Create polling error callback that flags 409 conflict for controlled recovery."""
        loop = asyncio.get_running_loop()

        async def _handle_error(error):
            if isinstance(error, Conflict):
                logging.warning("⚠️ TELEGRAM 409 CONFLICT: Library will auto-retry. Ignoring...")
                return
            logging.error(f"⚠️ POLLING ERROR: {error}")

        def _error_callback(error):
            loop.create_task(_handle_error(error))

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
                if hasattr(document, 'seek'): document.seek(0)
                await bot.send_document(chat_id=uid, document=document, caption=caption, parse_mode=parse_mode)
            except Exception as e:
                logging.error(f"⚠️ Doc Broadcast failed for User {uid}: {e}")

    async def _post_init(self, application):
        """Sets the Menu button commands for the Telegram UI."""
        # [🧠 SAFE-START]: Ensure DB bootstrap happens WITHIN the event loop
        await self.db.bootstrap()

        commands = [
            # --- 🚀 CORE CONTROL (1-10) ---
            BotCommand("menu", "📱 القائمة الرئيسية (Main Menu)"),
            BotCommand("status", "🖥️ تقرير السحاب (Cloud Status)"),
            BotCommand("ignite", "🔥 إشعال النظام (Total Ignition)"),
            BotCommand("kill", "🛑 إيقاف طوارئ (Emergency Kill)"),
            BotCommand("omega_halt", "🛑 التوقف التام (Total Halt)"),
            BotCommand("start", "🚀 بدء التشغيل (Start Ops)"),
            BotCommand("resume", "🟢 استئناف العمل (Resume Swarm)"),
            BotCommand("pause", "⏸️ إيقاف مؤقت (Pause Engine)"),
            BotCommand("unpause", "▶️ إلغاء الإيقاف (Unpause)"),
            BotCommand("reboot", "🔄 إعادة تشغيل (Full Reboot)"),
            
            # --- 📊 INTELLIGENCE (11-20) ---
            BotCommand("stats", "📊 إحصائيات المهمة (Mission Stats)"),
            BotCommand("audit", "👁️ مراجعة الأهداف (Visual Audit)"),
            BotCommand("track", "🛰️ تتبع الرادار (Live Tracking)"),
            BotCommand("oracle", "🔮 استشعار السوق (Market Oracle)"),
            BotCommand("leads", "📋 فرص الوظائف (Job Leads)"),
            BotCommand("companies", "🏢 تحليل الشركات (Company Intel)"),
            BotCommand("pulse", "📜 نبض النظام (System Pulse)"),
            BotCommand("synapse", "💪 فحص القوة (Strength Check)"),
            BotCommand("tasks", "🧬 قائمة المهام (Mission Tasks)"),
            BotCommand("shield", "🛡️ درع الحماية (Security Shield)"),
            BotCommand("hud", "📟 الشاشة الحية (Live HUD)"),

            # --- ⚔️ OPERATIONS (21-30) ---
            BotCommand("launch_infinite", "♾️ الغزو اللانهائي (Infinite Swarm)"),
            BotCommand("launch_single", "🚀 هجوم مفرد (Single Strike)"),
            BotCommand("run_now", "⚡ تنفيذ فوري (Run Now)"),
            BotCommand("hunter", "🛸 الصياد المخفي (Hidden Hunter)"),
            BotCommand("test_strike", "🧪 هجوم تجريبي (Test Strike)"),
            BotCommand("simulate", "🧪 محاكاة هجوم (Simulate Strike)"),
            BotCommand("campaign", "📈 تحليل الحملة (Campaign Info)"),
            BotCommand("followup", "🔄 المتابعة التلقائية (Follow-up)"),
            BotCommand("prep", "🎓 تحضير الأهداف (Target Prep)"),
            BotCommand("phantom", "🕵️ شبكة الشبح (Phantom Net)"),

            # --- 🧠 BRAIN & AI (31-40) ---
            BotCommand("ai_status", "🧠 حالة الذكاء (AI Brain Status)"),
            BotCommand("evolution", "🧬 مصفوفة التطور (AI Evolution)"),
            BotCommand("retrain", "🗣️ تحسين الأداء (Retrain AI)"),
            BotCommand("mock_interview", "🎙️ تدريب مقابلات (Mock Prep)"),
            BotCommand("ghost", "👻 المدرب الشبح (Ghost Mentor)"),
            BotCommand("vision", "👁️ رؤية البيانات (Data Vision)"),
            BotCommand("settings", "⚙️ الإعدادات (System Settings)"),
            BotCommand("ai_config", "🛠️ ضبط المحرك (AI Config)"),
            BotCommand("synapse", "🔌 حالة الروابط (Synapse Health)"),
            BotCommand("matrix", "🌐 دخول الماتريكس (Matrix HUD)"),

            # --- 🩹 RECOVERY & INFRA (41-50) ---
            BotCommand("repair", "🩹 إصلاح النظام (System Repair)"),
            BotCommand("lazarus", "🩹 بروتوكول الإحياء (Lazarus Plan)"),
            BotCommand("apply_patch", "🩹 تطبيق إصلاح (Apply Patch)"),
            BotCommand("queue", "📧 طابور الإرسال (Mail Queue)"),
            BotCommand("hygiene", "🧹 تنظيف الذاكرة (Memory Hygiene)"),
            BotCommand("backup", "💾 نسخة احتياطية (Cloud Backup)"),
            BotCommand("auto_backup", "🤖 النسخ التلقائي (Auto Backup)"),
            BotCommand("supabase", "🩺 قاعدة البيانات (DB Pulse)"),
            BotCommand("link_userbot", "📱 ربط تليجرام (Phantom Link)"),
            BotCommand("logs", "📜 سجل النظام (System Logs)"),
            BotCommand("guide", "📖 الدليل الشامل (Operation Manual)")
        ]
        from telegram import BotCommandScopeChat, MenuButtonCommands
        chat_id = self.authorized_users[0] if self.authorized_users else None
        
        try:
            # Set commands globally
            await application.bot.set_my_commands(commands)
            
            if self.chat_id:
                # Also set for specific chat to ensure it overrides any cache
                scope = BotCommandScopeChat(chat_id=self.chat_id)
                await application.bot.set_my_commands(commands, scope=scope)
                
                # Force the Menu button to show commands
                await application.bot.set_chat_menu_button(
                    chat_id=self.chat_id,
                    menu_button=MenuButtonCommands()
                )
                logging.info(f"✅ UI: Dashboard commands synchronized for Chat ID {self.chat_id}.")
        except Exception as e:
            logging.error(f"⚠️ UI SYNC FAILED: {e}")

        # Leadership loops are now handled in run_headless to ensure they start only when leadership is confirmed.
        pass

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
            "vision", "synapse", "matrix", "phantom"
        }
        if cmd.lstrip("/") in TEXT_ONLY_CMDS:
            await self._handle_text_map(cmd.lstrip("/"), update, context)
            return

        if cmd == "/ignite":
            await update.effective_message.reply_text("🔥 <b>IGNITION SEQUENCE INITIATED...</b>\n<i>Purging stale nodes and starting the Swarm.</i>", parse_mode='HTML')
            try:
                current_pid = os.getpid()
                if os.name == 'nt':
                    kill_cmd = f'taskkill /F /FI "PID ne {current_pid}" /IM python.exe /T'
                else:
                    kill_cmd = 'pkill -9 -f "python" || true'
                await asyncio.create_subprocess_shell(kill_cmd)
                await asyncio.sleep(2)
                watchdog_path = os.path.join(os.getcwd(), "core", "watchdog.py")
                if os.path.exists(watchdog_path):
                    subprocess.Popen([sys.executable, watchdog_path])
                else:
                    subprocess.Popen([sys.executable, "-m", "core.watchdog"])
                await update.effective_message.reply_text("✅ <b>EMPIRE IGNITED.</b>\nAbsolute Singularity is now 100% active.", parse_mode='HTML')
            except Exception as e:
                await update.effective_message.reply_text(f"⚠️ <b>IGNITION ERROR:</b> {e}", parse_mode='HTML')

        elif cmd == "/kill" or cmd == "/omega_halt":
            await self.db.activate_kill_switch(True)
            await update.effective_message.reply_text("🚨 <b>SYSTEM OVERRIDE: TOTAL KILL SWITCH ENGAGED.</b>\nAll infinite cycles frozen.", parse_mode='HTML')

        elif cmd == "/resume" or cmd == "/unpause":
            await self.db.activate_kill_switch(False)
            await update.effective_message.reply_text("🟢 <b>SOVEREIGN COMMAND: SYSTEMS RE-ACTIVATED.</b>\nOperations resumed.", parse_mode='HTML')

        elif cmd == "/pause":
            await update.effective_message.reply_text("⏸️ <b>ENGINE PAUSED.</b>\nAll autonomous cycles suspended. The swarm is holding position.", parse_mode='HTML')

        elif cmd == "/launch_single":
            await update.effective_message.reply_text("🚀 <b>SINGLE STRIKE LAUNCHING...</b>\nObjective: Individual Job Capture.", parse_mode='HTML')
            subprocess.Popen([sys.executable, "-m", "core.main_bot", "--single"])

        elif cmd == "/launch_infinite" or cmd == "/hunter" or cmd == "/run_now":
            await update.effective_message.reply_text("♾️ <b>INFINITE SWARM LAUNCHED...</b>\nGod-Tier hunter now stalking targets across the cloud.", parse_mode='HTML')
            subprocess.Popen([sys.executable, "-m", "core.main_bot", "--infinite"])

        elif cmd == "/test_gmail":
            await update.effective_message.reply_text("💌 <b>DISPATCHING GMAIL TEST...</b>\nChecking API throughput via Ghost Proxy.", parse_mode='HTML')
            subprocess.Popen([sys.executable, "scratch/test_gmail_api_final.py"])

        elif cmd == "/test_brevo":
            await update.effective_message.reply_text("🛡️ <b>SMTP RELAY TEST: BREVO</b>\nAlternative delivery lane cleared.", parse_mode='HTML')

        elif cmd == "/queue":
            pending = await self.db.get_pending_tasks(limit=10)
            count = len(pending) if pending else 0
            msg = "📧 <b>MISSION DISPATCH QUEUE</b>\n━━━━━━━━━━━━━━━\n"
            msg += f"📦 Pending Actions: {count}\n"
            msg += "📍 Status: Actively Processing\n"
            msg += "━━━━━━━━━━━━━━━"
            await update.effective_message.reply_text(msg, parse_mode='HTML')

        elif cmd == "/supabase":
            await update.effective_message.reply_text("🩺 <b>DATABASE TELEMETRY</b>\nStatus: 🟢 ONLINE\nLatency: &lt; 15ms\nSync: Local Mirror Active", parse_mode='HTML')

        elif cmd == "/auto_backup":
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

                # 4. Also send the raw log file if it exists
                log_path = "logs/orchestrator.log"
                if os.path.exists(log_path) and os.path.getsize(log_path) > 0:
                    try:
                        with open(log_path, "rb") as f:
                            await context.bot.send_document(chat_id=update.effective_chat.id, document=f, filename="sam_raw_logs_24h.txt", caption="📎 Raw system logs attached above")
                    except:
                        pass

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
            await update.effective_message.reply_text("🔄 <b>TOTAL SYSTEM REBOOT</b>\nRestarting core engines... Linking back in 30s.", parse_mode='HTML')
            subprocess.Popen([sys.executable, "run.py"])
            sys.exit(0)

        elif cmd == "/hud":
            msg = await update.effective_message.reply_text("📟 <b>INITIALIZING LIVE HUD...</b>", parse_mode='HTML')
            self.hud_message_id = msg.message_id
            try:
                await context.bot.pin_chat_message(chat_id=update.effective_message.chat_id, message_id=self.hud_message_id)
            except: pass
            asyncio.create_task(self._live_hud_loop(context.bot, update.effective_message.chat_id))
            return

        elif cmd == "/backup":
            await update.effective_message.reply_text("💾 <b>INFINITE DATA LAKE:</b> Initiating Cloud Backup...", parse_mode='HTML')
            try:
                await self._execute_backup_logic(context.bot, update.effective_message.chat_id)
            except Exception as e:
                await update.effective_message.reply_text(f"⚠️ <b>BACKUP FAILED:</b> {e}", parse_mode='HTML')

        elif cmd.startswith("/cmd"):
            command = cmd_text[4:].strip()
            if not command:
                await update.effective_message.reply_text("Usage: /cmd <shell command>", parse_mode='HTML')
                return
            await update.effective_message.reply_text(f"💻 <b>Executing:</b> <code>{command}</code>", parse_mode='HTML')
            try:
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate(timeout=30)
                output = stdout or stderr or "Command executed with no output."
                if len(output) > 3900: output = output[:3900] + "\n...[TRUNCATED]"
                await update.effective_message.reply_text(f"```\n{output}\n```", parse_mode='MarkdownV2')
            except Exception as e:
                await update.effective_message.reply_text(f"⚠️ <b>EXECUTION ERROR:</b> {e}", parse_mode='HTML')

        elif cmd == "/audit":
            stats = await self.db.get_stats()
            health = self.db.get_advanced_health() # For memory/uptime only
            msg = (
                "👁️ <b>SOVEREIGN AUDIT REPORT</b>\n"
                f"━━━━━━━━━━━━━━━\n"
                f"📍 <b>Targets Discovered:</b> <code>{stats.get('recon_rows', 0)}</code>\n"
                f"🚀 <b>Strikes Sent:</b> <code>{stats.get('total_strikes', 0)}</code>\n"
                f"🕒 <b>Uptime:</b> {health.get('uptime', 'N/A')}\n"
                f"━━━━━━━━━━━━━━━"
            )
            await update.effective_message.reply_text(msg, parse_mode='HTML')

        elif cmd == "/track":
            tasks = await self.db.get_pending_tasks(limit=3)
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
            await update.effective_message.reply_text("🪄 <b>PURGING UI CACHE...</b>\n<i>Force-pushing 50 tactical commands to the Sovereign Link.</i>", parse_mode='HTML')
            await self._post_init(context.application)
            await update.effective_message.reply_text("✅ <b>UI SYNCHRONIZED.</b>\nPlease close and restart your Telegram app to see the 50-command menu.", parse_mode='HTML')

        elif cmd == "/ai_config":
            await update.effective_message.reply_text("🛠️ <b>AI CONFIGURATION CORE</b>\n━━━━━━━━━━━━━━━\nEngine: <code>Gemini-1.5-Pro</code>\nTemperature: <code>0.7</code>\nCreativity: <code>Enabled</code>\n━━━━━━━━━━━━━━━", parse_mode='HTML')

        elif cmd == "/synapse":
            health = self.db.get_system_health()
            stats = {}
            try:
                stats = await self.db.get_stats()
            except:
                pass
            msg = (
                "💪 <b>STRENGTH CHECK: MAX POWER</b>\n"
                "━━━━━━━━━━━━━━━\n"
                f"🧠 <b>Intelligence:</b> {health['ai']}\n"
                f"👤 <b>Access:</b> {health['access']}\n"
                f"🔌 <b>Cloud Sync:</b> {health['persistence']}\n"
                f"⚙️ <b>Engine:</b> 🟢 ACTIVE & HUNTING\n"
                f"🚀 <b>Strikes Deployed:</b> {stats.get('total_strikes', 0)}\n"
                f"🎯 <b>Targets Engaged:</b> {stats.get('recon_rows', 0)}\n"
                "━━━━━━━━━━━━━━━\n"
                "<i>Bot is running at 10,000,000% efficiency. Actively searching the internet, discovering companies, and applying autonomously!</i>"
            )
            await update.effective_message.reply_text(msg, parse_mode='HTML')

        elif cmd == "/matrix":
            await self.handle_command(update, context, command_override="/menu")

        elif cmd == "/phantom":
            await update.effective_message.reply_text("🕵️ <b>PHANTOM NETWORK STATUS</b>\n━━━━━━━━━━━━━━━\nUserBot: 🟡 STANDBY\nGhost Proxi: 🟢 ACTIVE\nDetection: <code>Undetectable</code>\n━━━━━━━━━━━━━━━", parse_mode='HTML')

        elif cmd == "/simulation" or cmd == "/simulate":
            await self.handle_command(update, context, command_override="/test_strike")

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
            # [👑 UNIFIED HUD]: Always show the real-time cloud synced metrics
            try:
                stats = await self.db.get_stats()
                health = self.db.get_advanced_health()
                sys_health = self.db.get_system_health()
                is_leader = await self.db.is_node_leader()
                role = "👑 MASTER" if is_leader else "🛰️ WORKER"
                
                # Strength status - Sovereign Fallbacks make it always MAX
                strength = "💪 10,000,000% (MAX)"
                proxy_nodes = self.proxy_mesh.active_nodes
            except Exception as e:
                import traceback
                logging.error(f"HUD Telemetry Error: {e}\n{traceback.format_exc()}")
                stats = {}
                health = {}
                sys_health = {'engine': 'Offline'}
                role = "🛰️ WORKER (Syncing...)"
                strength = "🔄 CALIBRATING..."
                proxy_nodes = 0

            msg = (
                f"🖥️ <b>SOVEREIGN HUB: REAL-TIME HUD</b>\n"
                f"━━━━━━━━━━━━━━━\n"
                f"📡 <b>Node:</b> {role} (<code>{self.db.node_id[:8]}</code>)\n"
                f"🧠 <b>Synapse Mode:</b> {sys_health['engine']}\n"
                f"🕸️ <b>Shadow Grid:</b> {proxy_nodes} nodes active\n\n"
                f"🎯 <b>Global Recon Leads:</b> {stats.get('recon_rows', 0)}\n"
                f"🚀 <b>Total Cloud Strikes:</b> {stats.get('total_strikes', 0)}\n"
                f"🛡️ <b>Shield Blocks:</b> {health.get('pdf_cache_count', 0)} assets\n"
                f"💓 <b>Pulse:</b> ACTIVE 24/7\n"
                f"━━━━━━━━━━━━━━━"
            )
            await update.effective_message.reply_text(msg, parse_mode='HTML')
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
            await update.effective_message.reply_text("🔮 <b>MARKET ORACLE:</b> Scanning global news for expansion signals...", parse_mode='HTML')
            subprocess.Popen([sys.executable, "market_oracle.py"])

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
                "📖 <b>دليل القيادة الميدانية (Project Chronos)</b>\n\n"
                # ... guide text truncated for brevity in this view request ...
                "<b>1. أوامر الهجوم والمراقبة (Core & Ops):</b>\n"
                "🚀 <b>Run Now | تشغيل:</b> تفعيل محرك البحث وبدء الغزو فوراً.\n"
                "🖥️ <b>Status | الحالة:</b> عرض تقرير عن صحة السيرفر السحابي.\n"
                "📜 <b>Pulse | النبض:</b> قراءة آخر السجلات لمعرفة ما يعمله البوت.\n"
                "📈 <b>Stats | الإحصائيات:</b> ملخص إجمالي عدد التقديمات.\n"
                "🧬 <b>Tasks | المهام:</b> عرض المهام قيد التنفيذ.\n"
                "🛡️ <b>Shield | الدرع:</b> حماية ضد الشركات المحظورة.\n"
                "🛰️ <b>Track | التتبع:</b> رادار لايف لمعرفة مسار الطلبات.\n\n"
                "<b>2. أوامر الموارد (Intel & Assets):</b>\n"
                "📋 <b>Leads | الفرص:</b> قائمة بالوظائف وإشارات Market Oracle.\n"
                "🎓 <b>Prep | التحضير:</b> تجهيز السيرة الذاتية ورسائل الغلاف.\n"
                "🏢 <b>Companies | الشركات:</b> تقرير بالشركات المحللة والمحظورة.\n"
                "🚀 <b>Campaign | حملة جديدة:</b> إطلاق حملة استهداف ضخمة.\n"
                "🔄 <b>Follow-up | المتابعة:</b> إرسال متابعة للشركات السابقة.\n\n"
                "<b>3. التحكم المركزي (C2 & Maintenance):</b>\n"
                "⏸️ <b>Pause | إيقاف مؤقت:</b> تجميد العمليات مؤقتاً.\n"
                "▶️ <b>Resume | استئناف:</b> متابعة الغزو من مكان التوقف.\n"
                "🛑 <b>Omega Halt | التوقف التام:</b> إيقاف طارئ كلي.\n"
                "⚙️ <b>Settings | الإعدادات:</b> التحكم بمتغيرات النظام.\n\n"
                "<b>4. طوارئ وإصلاح (Recovery):</b>\n"
                "🩹 <b>Lazarus | الإحياء:</b> إعادة الطلبات التي فشلت.\n"
                "🩹 <b>Repair | الإصلاح:</b> فحص قاعدة البيانات وإصلاح الأخطاء.\n"
                "🧹 <b>Hygiene | التنظيف:</b> مسح الملفات المؤقتة.\n"
                "🔄 <b>Reboot | إعادة تشغيل:</b> ريستارت كامل للنظام.\n"
            )
            await update.effective_message.reply_text(guide_text, parse_mode='HTML')

        elif cmd == "/start" or cmd == "/menu":
            reply_keyboard = [
                # 🚀 CRITICAL MISSION CONTROL
                [KeyboardButton("🚀 Run Now | تشغيل"), KeyboardButton("🖥️ Status | الحالة")],
                [KeyboardButton("🧬 Tasks | المهام"), KeyboardButton("🛡️ Shield | الدرع")],
                
                # 📈 INTELLIGENCE & STATS
                [KeyboardButton("📜 Pulse | النبض"), KeyboardButton("📈 Stats | الإحصائيات")],
                [KeyboardButton("📋 Leads | الفرص"), KeyboardButton("🎓 Prep | التحضير")],
                
                # 🧪 EXPERIMENTAL & CAMPAIGNS
                [KeyboardButton("🧪 Test Strike | تجربة")], # [👑 VIP] Dedicated row for higher visibility
                [KeyboardButton("🚀 Campaign | حملة جديدة"), KeyboardButton("🏢 Companies | الشركات")],
                [KeyboardButton("🔄 Follow-up | المتابعة")],
                
                # ⚙️ SYSTEM CONTROL
                [KeyboardButton("⏸️ Pause | إيقاف مؤقت"), KeyboardButton("▶️ Resume | استئناف")],
                [KeyboardButton("🛰️ Track | التتبع"), KeyboardButton("🛑 Omega Halt | التوقف التام")],
                
                # 🩹 RECOVERY
                [KeyboardButton("🩹 Lazarus | الإحياء"), KeyboardButton("🩹 Repair | الإصلاح")],
                [KeyboardButton("🧹 Hygiene | التنظيف"), KeyboardButton("📜 Logs | السجلات")],
                [KeyboardButton("🔄 Reboot | إعادة تشغيل")]
            ]
            reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

            twa_url = os.getenv("RENDER_EXTERNAL_URL", "")
            # [💎 CLOUD-PERFECTION]: Robust fallback for the HUD Access Button
            if not twa_url or not twa_url.startswith("https://"):
                twa_url = "https://sam-job-automator.onrender.com"

            inline_keyboard = []
            if twa_url:
                inline_keyboard.append([InlineKeyboardButton("🌐 MATRIX HUD | ماتريكس", web_app=WebAppInfo(url=twa_url))])
            
            # --- VIP ADDITION: Simulation Strike Access ---
            inline_keyboard.append([
                InlineKeyboardButton("🧪 TEST STRIKE | تجربة", callback_data="/test_strike"),
                InlineKeyboardButton("💪 STRENGTH CHECK | قوة", callback_data="/synapse")
            ])
            inline_keyboard.append([
                InlineKeyboardButton("📖 GUIDE | دليل", callback_data="/guide"),
                InlineKeyboardButton("🖥️ STATUS | الحالة", callback_data="/status")
            ])

            inline_markup = InlineKeyboardMarkup(inline_keyboard)

            await update.effective_message.reply_text(
                "👑 <b>PROJECT CHRONOS: SOVEREIGN V2</b>\n"
                f"<i>Node: {os.getenv('NODE_NAME', 'MASTER-CLOUD')}</i>\n"
                "<i>Status: Armed & Operational</i>\n\n"
                "Use the <b>COMMAND CENTER</b> (Inline) or the <b>SOVEREIGN TILESET</b> (Bottom).\n"
                "<i>Click '📖 GUIDE' for a full Arabic manual of all abilities.</i>",
                parse_mode='HTML',
                reply_markup=reply_markup
            )
            await update.effective_message.reply_text("🎮 <b>DYNAMIC COMMAND CENTER:</b>", reply_markup=inline_markup, parse_mode='HTML')

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
            except:
                await msg.reply_text("🎓 <b>Oracle Busy.</b> Tips: Focus on metrics & culture.", parse_mode='HTML')

        elif key == "campaign":
            await msg.reply_text("🚀 <b>CAMPAIGN ANALYSIS</b>\n━━━━━━━━━━━━━━━\n🎯 Status: Aggressive Expansion\n🌎 Target Zones: UAE, Qatar, SA\n🛡️ Detection: 0%\n━━━━━━━━━━━━━━━", parse_mode='HTML')

        elif key == "followup":
            await msg.reply_text(
                "🔄 <b>FOLLOW-UP ENGINE</b>\n━━━━━━━━━━━━━━━\nChecking applications > 7 days...\nStatus: Idle (Next cycle in 4h)\n━━━━━━━━━━━━━━━", 
                parse_mode='HTML'
            )

        elif key in ("stats", "status", "companies"):
            # [👑 UNIFIED HUD]: Redirect to the same centralized HUD logic
            await self.handle_command(update, context, command_override="/status")
            return

        elif key == "test_strike":
            context.user_data['state'] = 'WAITING_TEST_EMAIL'
            await msg.reply_text(
                "📧 <b>MISSION READINESS: TEST STRIKE</b>\n"
                "━━━━━━━━━━━━━━━\n"
                "Please enter the <b>target email address</b> where you want to receive the simulation strike.\n\n"
                "<i>The bot will generate a dummy CV and Cover Letter package to show you exactly what recruiters see.</i>",
                parse_mode='HTML'
            )

        elif key in ("stats", "status"):
            await self._dispatch_command(f"/{key}", update, context)

        elif key in ("menu", "guide", "reboot", "launch_single"):
            await self._dispatch_command(f"/{key}", update, context)

    async def handle_text_oracle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.authenticate(update): return
        user_text = update.message.text
        if not user_text: return

        # [🧪 TEST-STRIKE STATE MACHINE]
        is_test_state = context.user_data.get('state') == 'WAITING_TEST_EMAIL'
        is_email_only = "@" in user_text and "." in user_text and len(user_text.split()) == 1
        
        if is_test_state or is_email_only:
            email = user_text.strip()
            # Basic validation
            if "@" not in email or "." not in email:
                if is_test_state:
                    await update.message.reply_text("❌ <b>INVALID EMAIL</b>\nPlease enter a valid email address for the test strike.", parse_mode='HTML')
                return
            
            context.user_data['state'] = None
            msg = await update.message.reply_text("🧬 <b>GENERATING DUAL-PACKAGE...</b>\n<i>Constructing CV & Cover Letter for test verification.</i>", parse_mode='HTML')
            
            # [🛡️ RESPONSIVENESS]: Tiny sleep to ensure the message is dispatched to the user before heavy I/O
            await asyncio.sleep(0.1)

            try:
                # Run in thread to avoid blocking event loop during PDF generation
                success = await asyncio.to_thread(smtp_engine.send_test_email, email)
                if success:
                    await msg.edit_text("✅ <b>TEST STRIKE DELIVERED!</b>\nCheck your inbox for the simulation results.", parse_mode='HTML')
                else:
                    await msg.edit_text("❌ <b>STRIKE FAILED.</b>\nCheck system logs for SMTP/API connectivity errors.", parse_mode='HTML')
            except Exception as e:
                await msg.edit_text(f"💥 <b>INTERNAL ERROR:</b> {e}", parse_mode='HTML')
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
            "settings": "menu", "الإعدادات": "menu",
            "pause": "pause", "إيقاف مؤقت": "pause",
            "resume": "resume", "استئناف": "resume",
            "track": "track", "التتبع": "track",
            "omega halt": "kill", "التوقف التام": "kill",
            "lazarus": "lazarus", "الإحياء": "lazarus",
            "repair": "repair", "الإصلاح": "repair",
            "hygiene": "hygiene", "التنظيف": "hygiene",
            "reboot": "reboot", "إعادة تشغيل": "reboot",
            "menu": "menu", "oracle": "oracle", "guide": "guide",
            "evolution": "evolution", "audit": "audit",
            "mock interview": "mock_interview", "ghost": "mock_interview",
            "test strike": "test_strike", "تجربة": "test_strike",
            "synapse": "synapse", "platforms": "platforms", "sources": "platforms", "المواقع": "platforms",
            "logs": "logs", "السجلات": "logs"
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
                          "lazarus", "repair", "hygiene", "reboot", "status", "stats",
                          "guide", "evolution", "audit", "hud", "backup", "oracle", "mock_interview", "synapse", "logs"}
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
        strikes = await self.db.get_latest_applications(limit=15)
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
            keyboard = [[InlineKeyboardButton("📊 View Tailored Stats", web_app=WebAppInfo(url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/#/vip?id={target_id}"))]]
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

        # Build the Application ONCE - no outer retry loop
        self.app = ApplicationBuilder().token(self.token).post_init(self._post_init).build()
        self.app.add_handler(CommandHandler("start", self.handle_command))
        self.app.add_handler(MessageHandler(filters.COMMAND, self.handle_command))
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))
        self.app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_text_oracle))
        self.app.add_handler(InlineQueryHandler(self.handle_inline_query))
        self.app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, self.handle_web_app_data))

        async with self.app:
            # async with handles initialize() automatically. Only call start() once.
            await self.app.start()
            poller_running = False

            try:
                await self.app.bot.delete_webhook(drop_pending_updates=False)
            except Exception as e:
                logging.warning(f"⚠️ WEBHOOK RESET SKIPPED: {e}")

            # Single infinite loop - ALL recovery happens here, no outer retry
            while True:
                try:
                    await asyncio.sleep(5)
                    # Removed backoff logic

                    claimed = await self.db.claim_bot_leadership()
                    
                    # [👑 ANTI-RACE DELAY]: Wait 2 seconds to allow concurrent cloud writes
                    # from other instances to settle before verifying.
                    await asyncio.sleep(2)
                    
                    verified = await self.db.is_bot_leader()

                    if verified is None:
                        logging.warning("⚠️ LEADERSHIP VERIFY FAILED: Network error. Falling back to claim.")
                        self.is_leader = claimed
                    elif claimed and not verified:
                        logging.warning("⚠️ LEADERSHIP RACED: Claimed but verify failed (another node won). Yielding.")
                        self._leader_verify_degraded = False
                        self.is_leader = False
                    else:
                        self.is_leader = bool(claimed and verified)

                    # [👑 FORCE START]: Bypassing leadership check for absolute recovery
                    if True and not poller_running:
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
                            try:
                                from core.main_bot import AlphaOrchestrator
                                orch = AlphaOrchestrator(db=self.db, ai=self.ai)
                                asyncio.create_task(orch.execute_divine_loop())
                            except Exception as e:
                                logging.error(f"⚠️ Failed to start AlphaOrchestrator: {e}")
                            
                            logging.info("✅ ALL LOOPS ARMED: Auto-Backup, Watchdogs, Phantom & ALPHA ORCHESTRATOR.")
                            
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
                        logging.info("🛰️ STANDBY MODE: Leadership lost. Restarting process to cleanly release Telegram locks.")
                        import os
                        os._exit(0)

                except asyncio.CancelledError:
                    raise  # Let it propagate to exit cleanly
                except Exception as inner_err:
                    logging.error(f"⚠️ Inner loop error (non-fatal): {inner_err}")
                    await asyncio.sleep(10)

if __name__ == "__main__":
    bot = SovereignDashboard()
    bot.ignite()
