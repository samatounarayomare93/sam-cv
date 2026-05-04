"""
Enhanced Telegram Notifications
Real-time updates and rich notifications
"""

import os
import asyncio
from datetime import datetime
from typing import Dict, List, Any

class EnhancedNotifications:
    """Enhanced notification system with rich formatting"""
    
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
    
    async def send_message(self, text: str, parse_mode: str = "HTML"):
        """Send formatted message"""
        import httpx
        async with httpx.AsyncClient() as client:
            try:
                await client.post(
                    f"{self.base_url}/sendMessage",
                    json={
                        "chat_id": self.chat_id,
                        "text": text,
                        "parse_mode": parse_mode,
                        "disable_web_page_preview": True
                    }
                )
            except Exception as e:
                print(f"Notification error: {e}")
    
    async def notify_new_job(self, job: Dict[str, Any]):
        """Notify about new job discovered"""
        text = f"""
🎯 <b>New Job Discovered!</b>

<b>Title:</b> {job.get('title', 'N/A')}
<b>Company:</b> {job.get('company', 'N/A')}
<b>Location:</b> {job.get('location', 'N/A')}
<b>Platform:</b> {job.get('platform', 'N/A')}

<b>Match Score:</b> {job.get('match_score', 0)}% 🎯

<b>URL:</b> {job.get('url', 'N/A')}

⏰ <i>Discovered at {datetime.now().strftime('%H:%M:%S')}</i>
"""
        await self.send_message(text)
    
    async def notify_email_sent(self, job: Dict[str, Any], email: str):
        """Notify about email sent"""
        text = f"""
✉️ <b>Email Sent!</b>

<b>To:</b> {email}
<b>Company:</b> {job.get('company', 'N/A')}
<b>Position:</b> {job.get('title', 'N/A')}

✅ <i>CV and Cover Letter attached</i>

⏰ <i>Sent at {datetime.now().strftime('%H:%M:%S')}</i>
"""
        await self.send_message(text)
    
    async def notify_daily_summary(self, stats: Dict[str, Any]):
        """Send daily summary"""
        text = f"""
📊 <b>Daily Summary Report</b>

<b>Jobs Discovered:</b> {stats.get('jobs_found', 0)} 🔍
<b>Emails Sent:</b> {stats.get('emails_sent', 0)} ✉️
<b>Success Rate:</b> {stats.get('success_rate', 0)}% 📈

<b>Top Platforms:</b>
{self._format_platforms(stats.get('platforms', {}))}

<b>Top Locations:</b>
{self._format_locations(stats.get('locations', {}))}

<b>AI Analysis:</b>
• High Match: {stats.get('high_match', 0)} jobs
• Medium Match: {stats.get('medium_match', 0)} jobs
• Low Match: {stats.get('low_match', 0)} jobs

🎯 <i>Keep going! Your dream job is coming!</i>

⏰ <i>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>
"""
        await self.send_message(text)
    
    async def notify_error(self, error: str, context: str = ""):
        """Notify about errors"""
        text = f"""
⚠️ <b>Error Alert</b>

<b>Context:</b> {context}
<b>Error:</b> {error}

<i>Bot is still running, will retry automatically</i>

⏰ <i>{datetime.now().strftime('%H:%M:%S')}</i>
"""
        await self.send_message(text)
    
    async def notify_milestone(self, milestone: str, count: int):
        """Notify about milestones"""
        emojis = {
            "10": "🎉",
            "50": "🎊",
            "100": "🏆",
            "500": "🌟",
            "1000": "💎"
        }
        emoji = emojis.get(str(count), "🎯")
        
        text = f"""
{emoji} <b>Milestone Reached!</b>

<b>{milestone}:</b> {count}

<i>Great progress! Keep it up!</i>

⏰ <i>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>
"""
        await self.send_message(text)
    
    async def notify_response_received(self, company: str, subject: str):
        """Notify about email response"""
        text = f"""
🎉 <b>EMAIL RESPONSE RECEIVED!</b>

<b>From:</b> {company}
<b>Subject:</b> {subject}

📧 <i>Check your email inbox!</i>

⏰ <i>{datetime.now().strftime('%H:%M:%S')}</i>
"""
        await self.send_message(text)
    
    def _format_platforms(self, platforms: Dict[str, int]) -> str:
        """Format platform statistics"""
        if not platforms:
            return "• No data yet"
        
        sorted_platforms = sorted(platforms.items(), key=lambda x: x[1], reverse=True)[:5]
        return "\n".join([f"• {name}: {count}" for name, count in sorted_platforms])
    
    def _format_locations(self, locations: Dict[str, int]) -> str:
        """Format location statistics"""
        if not locations:
            return "• No data yet"
        
        sorted_locations = sorted(locations.items(), key=lambda x: x[1], reverse=True)[:5]
        return "\n".join([f"• {name}: {count}" for name, count in sorted_locations])


# Global instance
_notifier = None

def get_notifier():
    """Get or create notifier instance"""
    global _notifier
    if _notifier is None:
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if bot_token and chat_id:
            _notifier = EnhancedNotifications(bot_token, chat_id)
    return _notifier


async def notify_new_job(job: Dict[str, Any]):
    """Quick notification helper"""
    notifier = get_notifier()
    if notifier:
        await notifier.notify_new_job(job)


async def notify_email_sent(job: Dict[str, Any], email: str):
    """Quick notification helper"""
    notifier = get_notifier()
    if notifier:
        await notifier.notify_email_sent(job, email)


async def notify_daily_summary(stats: Dict[str, Any]):
    """Quick notification helper"""
    notifier = get_notifier()
    if notifier:
        await notifier.notify_daily_summary(stats)
