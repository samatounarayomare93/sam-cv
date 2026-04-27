"""
MAXIMUM POWER Uplink Module - Telegram Communication Bridge
Provides a high-performance, feature-rich interface for sending messages to Telegram.
"""

import logging
import config
import asyncio
import time
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

# Global bot instance (set by main_bot.py)
_bot_instance = None

# Message priority levels
class Priority(Enum):
    CRITICAL = 0  # Immediate delivery, max retries
    HIGH = 1      # Fast delivery
    NORMAL = 2    # Standard delivery
    LOW = 3       # Best effort

# Message types for categorization
class MessageType(Enum):
    STATUS = "📊"
    HEALTH = "🏥"
    ERROR = "🚨"
    SUCCESS = "✅"
    INFO = "ℹ️"
    WARNING = "⚠️"
    MISSION = "🎯"
    STRIKE = "⚔️"

@dataclass
class UplinkMessage:
    """MAXIMUM POWER: Rich message object with metadata"""
    content: str
    priority: Priority = Priority.NORMAL
    msg_type: MessageType = MessageType.INFO
    retry_count: int = 3
    timestamp: float = field(default_factory=time.time)
    parse_mode: str = 'HTML'
    
    def format_with_type(self) -> str:
        """Add type emoji prefix if not present"""
        content = self.content.strip()
        if not content.startswith(self.msg_type.value):
            return f"{self.msg_type.value} {content}"
        return content


class UplinkQueue:
    """MAXIMUM POWER: Async message queue for high-throughput Telegram messaging"""
    
    def __init__(self, max_workers=3):
        self._queue = asyncio.Queue()
        self._workers = []
        self._max_workers = max_workers
        self._running = False
        self._stats = {
            'sent': 0,
            'failed': 0,
            'retried': 0,
            'queued': 0,
        }
    
    async def start(self):
        """Start the message queue workers"""
        if self._running:
            return
        
        self._running = True
        for i in range(self._max_workers):
            worker = asyncio.create_task(self._worker(i))
            self._workers.append(worker)
        logger.info(f"Uplink queue started with {self._max_workers} workers")
    
    async def stop(self):
        """Stop all workers gracefully"""
        self._running = False
        for worker in self._workers:
            worker.cancel()
        logger.info("Uplink queue stopped")
    
    async def _worker(self, worker_id: int):
        """Worker that processes messages from queue"""
        while self._running:
            try:
                message = await asyncio.wait_for(self._queue.get(), timeout=1.0)
                success = await self._send_with_retry(message)
                
                if success:
                    self._stats['sent'] += 1
                else:
                    self._stats['failed'] += 1
                
                self._queue.task_done()
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Uplink worker {worker_id} error: {e}")
    
    async def _send_with_retry(self, message: UplinkMessage) -> bool:
        """Send message with retry logic based on priority"""
        formatted = message.format_with_type()
        
        for attempt in range(message.retry_count):
            try:
                if not _bot_instance:
                    logger.debug("Uplink: No bot instance available")
                    return False
                
                chat_id = getattr(config, 'TELEGRAM_CHAT_ID', None)
                if not chat_id:
                    logger.debug("Uplink: No chat ID configured")
                    return False
                
                # Use exponential backoff, shorter for high priority
                base_delay = 1 if message.priority == Priority.CRITICAL else 2
                
                await _bot_instance.send_message(
                    chat_id=chat_id,
                    text=formatted,
                    parse_mode=message.parse_mode
                )
                return True
                
            except Exception as e:
                logger.warning(f"Uplink send attempt {attempt+1}/{message.retry_count} failed: {e}")
                if attempt < message.retry_count - 1:
                    delay = base_delay * (2 ** attempt)
                    await asyncio.sleep(min(delay, 30))  # Cap at 30s
        
        return False
    
    def send(self, message: UplinkMessage):
        """Queue a message for async delivery"""
        self._stats['queued'] += 1
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self._queue.put(message))
        except RuntimeError:
            logger.debug("Uplink queue not running; message will use sync fallback")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get queue statistics"""
        return self._stats.copy()


# Global queue instance
_uplink_queue = UplinkQueue()


def set_bot(bot):
    """Set the global bot instance for uplink communication."""
    global _bot_instance
    _bot_instance = bot
    
    # Start the queue when bot is set
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.create_task(_uplink_queue.start())
        else:
            loop.run_until_complete(_uplink_queue.start())
    except Exception as e:
        logger.warning(f"Failed to start uplink queue: {e}")


def send_message(text: str, parse_mode: str = 'HTML', 
                 priority: Priority = Priority.NORMAL,
                 msg_type: MessageType = MessageType.INFO,
                 retry: int = None) -> bool:
    """
    MAXIMUM POWER: Send a message to Telegram via async queue.
    
    Args:
        text: Message content
        parse_mode: 'HTML' or 'Markdown'
        priority: Message priority (CRITICAL, HIGH, NORMAL, LOW)
        msg_type: Type of message for auto-emoji prefix
        retry: Override default retry count (default based on priority)
    
    Returns:
        True if queued successfully, False otherwise
    """
    if not _bot_instance:
        logger.debug("Uplink: No bot instance available")
        return False
    
    chat_id = getattr(config, 'TELEGRAM_CHAT_ID', None)
    if not chat_id:
        logger.debug("Uplink: No chat ID configured")
        return False
    
    # Determine retry count based on priority if not specified
    if retry is None:
        retry_map = {
            Priority.CRITICAL: 5,
            Priority.HIGH: 3,
            Priority.NORMAL: 2,
            Priority.LOW: 1,
        }
        retry = retry_map.get(priority, 2)
    
    message = UplinkMessage(
        content=text,
        priority=priority,
        msg_type=msg_type,
        retry_count=retry,
        parse_mode=parse_mode
    )
    
    # Try to use async queue, fallback to sync if needed
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            _uplink_queue.send(message)
            return True
        else:
            # Fallback to synchronous send for compatibility
            return _send_sync(message)
    except Exception as e:
        logger.error(f"Uplink queue error: {e}")
        return _send_sync(message)


def _send_sync(message: UplinkMessage) -> bool:
    """Synchronous fallback for sending messages"""
    formatted = message.format_with_type()
    
    for attempt in range(message.retry_count):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(
                    _bot_instance.send_message(
                        chat_id=config.TELEGRAM_CHAT_ID,
                        text=formatted,
                        parse_mode=message.parse_mode
                    )
                )
                return True
            finally:
                loop.close()
        except Exception as e:
            logger.warning(f"Uplink sync send attempt {attempt+1} failed: {e}")
            if attempt < message.retry_count - 1:
                time.sleep(2 ** attempt)
    
    return False


# Backward compatibility functions
def send_health_alert(message: str) -> bool:
    """Send a health alert message."""
    return send_message(message, priority=Priority.HIGH, msg_type=MessageType.HEALTH)


def send_error_alert(message: str) -> bool:
    """Send an error alert message."""
    return send_message(message, priority=Priority.CRITICAL, msg_type=MessageType.ERROR)


def send_success_notification(message: str) -> bool:
    """Send a success notification."""
    return send_message(message, priority=Priority.NORMAL, msg_type=MessageType.SUCCESS)


def send_system_status(message: str) -> bool:
    """Send a system status update."""
    return send_message(message, priority=Priority.NORMAL, msg_type=MessageType.STATUS)


def send_mission_update(message: str) -> bool:
    """Send a mission progress update."""
    return send_message(message, priority=Priority.NORMAL, msg_type=MessageType.MISSION)


def send_strike_notification(company: str, job_title: str, phase: str = "GLOBAL") -> bool:
    """Send a successful strike notification."""
    text = (
        f"🎯 <b>STRIKE SUCCESS</b>\n\n"
        f"🏢 <b>Company:</b> {company}\n"
        f"💼 <b>Role:</b> {job_title}\n"
        f"🌍 <b>Phase:</b> {phase}\n"
        f"⏰ <b>Time:</b> {datetime.now().strftime('%H:%M:%S')}"
    )
    return send_message(text, priority=Priority.HIGH, msg_type=MessageType.STRIKE)


def get_queue_stats() -> Dict[str, Any]:
    """Get current queue statistics"""
    return _uplink_queue.get_stats()
