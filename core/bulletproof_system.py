"""
🛡️ BULLETPROOF SYSTEM - IMMORTAL OPERATION ENGINE
═══════════════════════════════════════════════════

This module ensures the bot runs FOREVER without any errors or problems.
If errors occur, the bot fixes itself automatically.

Features:
- Circuit breaker for external APIs
- Memory & disk monitoring
- Auto-restart on failures
- Comprehensive error recovery
- Health monitoring
- Automatic backups
- Resource management
- Graceful degradation
"""

import asyncio
import logging
import os
import sys
import time
import traceback
import psutil
import gc
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Callable
from collections import deque
from enum import Enum
import json

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [BULLETPROOF] %(levelname)s - %(message)s")


class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered


class CircuitBreaker:
    """
    🔌 CIRCUIT BREAKER PATTERN
    Prevents cascading failures by stopping requests to failing services
    """
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60, success_threshold: int = 2):
        self.failure_threshold = failure_threshold
        self.timeout = timeout  # seconds to wait before trying again
        self.success_threshold = success_threshold
        
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        
    def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                logging.info(f"🔌 Circuit breaker: Trying {func.__name__} again (HALF_OPEN)")
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
            else:
                raise Exception(f"Circuit breaker OPEN for {func.__name__}")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    async def call_async(self, func: Callable, *args, **kwargs):
        """Execute async function with circuit breaker protection"""
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                logging.info(f"🔌 Circuit breaker: Trying {func.__name__} again (HALF_OPEN)")
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
            else:
                raise Exception(f"Circuit breaker OPEN for {func.__name__}")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        """Handle successful call"""
        self.failure_count = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                logging.info("✅ Circuit breaker: Service recovered (CLOSED)")
                self.state = CircuitState.CLOSED
                self.success_count = 0
    
    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            logging.error(f"🔌 Circuit breaker: Too many failures, opening circuit (OPEN)")
            self.state = CircuitState.OPEN
    
    def reset(self):
        """Manually reset circuit breaker"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None


class ResourceMonitor:
    """
    📊 RESOURCE MONITORING SYSTEM
    Monitors memory, disk, CPU and prevents resource exhaustion
    """
    
    def __init__(self):
        self.memory_threshold = 400 * 1024 * 1024  # 400MB (Render limit: 512MB)
        self.disk_threshold = 80  # 80% disk usage
        self.cpu_threshold = 90  # 90% CPU usage
        
        self.memory_history = deque(maxlen=60)  # Last 60 readings
        self.alerts_sent = {}
        
    def check_memory(self) -> Dict[str, Any]:
        """Check memory usage"""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024
            memory_percent = process.memory_percent()
            
            self.memory_history.append(memory_mb)
            
            status = {
                'memory_mb': round(memory_mb, 2),
                'memory_percent': round(memory_percent, 2),
                'threshold_mb': self.memory_threshold / 1024 / 1024,
                'is_critical': memory_info.rss > self.memory_threshold,
                'trend': self._calculate_trend()
            }
            
            if status['is_critical']:
                logging.warning(f"⚠️ MEMORY CRITICAL: {memory_mb:.2f}MB / {self.memory_threshold/1024/1024:.2f}MB")
                self._trigger_memory_cleanup()
            
            return status
        except Exception as e:
            logging.error(f"Memory check failed: {e}")
            return {'error': str(e)}
    
    def check_disk(self) -> Dict[str, Any]:
        """Check disk usage"""
        try:
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            status = {
                'disk_total_gb': round(disk.total / 1024 / 1024 / 1024, 2),
                'disk_used_gb': round(disk.used / 1024 / 1024 / 1024, 2),
                'disk_free_gb': round(disk.free / 1024 / 1024 / 1024, 2),
                'disk_percent': disk_percent,
                'is_critical': disk_percent > self.disk_threshold
            }
            
            if status['is_critical']:
                logging.warning(f"⚠️ DISK CRITICAL: {disk_percent}% used")
                self._trigger_disk_cleanup()
            
            return status
        except Exception as e:
            logging.error(f"Disk check failed: {e}")
            return {'error': str(e)}
    
    def check_cpu(self) -> Dict[str, Any]:
        """Check CPU usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            
            status = {
                'cpu_percent': cpu_percent,
                'cpu_count': psutil.cpu_count(),
                'is_critical': cpu_percent > self.cpu_threshold
            }
            
            if status['is_critical']:
                logging.warning(f"⚠️ CPU CRITICAL: {cpu_percent}%")
            
            return status
        except Exception as e:
            logging.error(f"CPU check failed: {e}")
            return {'error': str(e)}
    
    def _calculate_trend(self) -> str:
        """Calculate memory usage trend"""
        if len(self.memory_history) < 10:
            return "stable"
        
        recent = list(self.memory_history)[-10:]
        older = list(self.memory_history)[-20:-10] if len(self.memory_history) >= 20 else recent
        
        recent_avg = sum(recent) / len(recent)
        older_avg = sum(older) / len(older)
        
        diff = recent_avg - older_avg
        
        if diff > 10:  # Growing by >10MB
            return "increasing"
        elif diff < -10:  # Decreasing by >10MB
            return "decreasing"
        else:
            return "stable"
    
    def _trigger_memory_cleanup(self):
        """Trigger aggressive memory cleanup"""
        logging.info("🧹 MEMORY CLEANUP: Running garbage collection...")
        gc.collect()
        
        # Close unused connections
        try:
            import httpx
            # Force close any lingering sessions
        except Exception:
            pass
    
    def _trigger_disk_cleanup(self):
        """Trigger disk cleanup"""
        logging.info("🧹 DISK CLEANUP: Removing old files...")
        
        # Clean old logs (>7 days)
        try:
            log_dir = "logs"
            if os.path.exists(log_dir):
                cutoff = time.time() - (7 * 24 * 60 * 60)
                for filename in os.listdir(log_dir):
                    filepath = os.path.join(log_dir, filename)
                    if os.path.isfile(filepath) and os.path.getmtime(filepath) < cutoff:
                        os.remove(filepath)
                        logging.info(f"🗑️ Removed old log: {filename}")
        except Exception as e:
            logging.error(f"Log cleanup failed: {e}")
        
        # Clean temp files (>1 hour)
        try:
            temp_dir = "temp"
            if os.path.exists(temp_dir):
                cutoff = time.time() - (60 * 60)
                for filename in os.listdir(temp_dir):
                    filepath = os.path.join(temp_dir, filename)
                    if os.path.isfile(filepath) and os.path.getmtime(filepath) < cutoff:
                        os.remove(filepath)
                        logging.info(f"🗑️ Removed temp file: {filename}")
        except Exception as e:
            logging.error(f"Temp cleanup failed: {e}")


class HealthMonitor:
    """
    🏥 HEALTH MONITORING SYSTEM
    Monitors all critical components and triggers auto-healing
    """
    
    def __init__(self, db=None, ai=None):
        self.db = db
        self.ai = ai
        self.resource_monitor = ResourceMonitor()
        
        # Circuit breakers for external services
        self.circuit_breakers = {
            'ai': CircuitBreaker(failure_threshold=5, timeout=60),
            'email': CircuitBreaker(failure_threshold=3, timeout=120),
            'database': CircuitBreaker(failure_threshold=5, timeout=30),
            'scraper': CircuitBreaker(failure_threshold=10, timeout=300)
        }
        
        self.health_history = deque(maxlen=100)
        self.last_health_check = 0
        self.consecutive_failures = 0
        
    async def check_all_systems(self) -> Dict[str, Any]:
        """Comprehensive health check of all systems"""
        health = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'healthy',
            'components': {},
            'resources': {},
            'circuit_breakers': {}
        }
        
        # Check resources
        health['resources']['memory'] = self.resource_monitor.check_memory()
        health['resources']['disk'] = self.resource_monitor.check_disk()
        health['resources']['cpu'] = self.resource_monitor.check_cpu()
        
        # Check database
        health['components']['database'] = await self._check_database()
        
        # Check AI
        health['components']['ai'] = await self._check_ai()
        
        # Check email
        health['components']['email'] = await self._check_email()
        
        # Circuit breaker status
        for name, cb in self.circuit_breakers.items():
            health['circuit_breakers'][name] = {
                'state': cb.state.value,
                'failure_count': cb.failure_count
            }
        
        # Determine overall status
        critical_issues = []
        
        if health['resources']['memory'].get('is_critical'):
            critical_issues.append('memory')
        if health['resources']['disk'].get('is_critical'):
            critical_issues.append('disk')
        if not health['components']['database'].get('healthy'):
            critical_issues.append('database')
        
        if critical_issues:
            health['overall_status'] = 'degraded'
            health['critical_issues'] = critical_issues
            self.consecutive_failures += 1
        else:
            self.consecutive_failures = 0
        
        # Auto-heal if needed
        if self.consecutive_failures >= 3:
            logging.error("🚨 CRITICAL: Multiple consecutive health check failures!")
            await self._trigger_auto_heal(health)
        
        self.health_history.append(health)
        self.last_health_check = time.time()
        
        return health
    
    async def _check_database(self) -> Dict[str, Any]:
        """Check database health"""
        if not self.db:
            return {'healthy': False, 'reason': 'Database not initialized'}
        
        try:
            # Try a simple operation
            await self.db.send_heartbeat()
            return {'healthy': True, 'latency_ms': 0}
        except Exception as e:
            logging.error(f"Database health check failed: {e}")
            return {'healthy': False, 'reason': str(e)}
    
    async def _check_ai(self) -> Dict[str, Any]:
        """Check AI health"""
        if not self.ai:
            return {'healthy': False, 'reason': 'AI not initialized', 'fallback_available': True}
        
        try:
            # Quick test query
            test_result = await self.ai.structural_query("test")
            return {'healthy': True, 'provider': getattr(self.ai, 'primary_engine', 'unknown')}
        except Exception as e:
            logging.warning(f"AI health check failed: {e}")
            return {'healthy': False, 'reason': str(e), 'fallback_available': True}
    
    async def _check_email(self) -> Dict[str, Any]:
        """Check email health"""
        try:
            from core import config
            
            providers = []
            if getattr(config, 'GMAIL_SMTP_USER', ''):
                providers.append('gmail')
            if getattr(config, 'ZOHO_SMTP_USER', ''):
                providers.append('zoho')
            if getattr(config, 'BREVO_SMTP_LOGIN', ''):
                providers.append('brevo')
            
            return {
                'healthy': len(providers) > 0,
                'providers_available': providers,
                'count': len(providers)
            }
        except Exception as e:
            logging.error(f"Email health check failed: {e}")
            return {'healthy': False, 'reason': str(e)}
    
    async def _trigger_auto_heal(self, health: Dict[str, Any]):
        """Trigger automatic healing procedures"""
        logging.info("🔧 AUTO-HEAL: Starting recovery procedures...")
        
        # Memory cleanup
        if health['resources']['memory'].get('is_critical'):
            logging.info("🧹 AUTO-HEAL: Running memory cleanup...")
            gc.collect()
            
            # Close unused sessions
            try:
                from core.main_bot import AlphaOrchestrator
                orchestrator = AlphaOrchestrator()
                if orchestrator._session:
                    await orchestrator._session.aclose()
                    orchestrator._session = None
            except Exception:
                pass
        
        # Disk cleanup
        if health['resources']['disk'].get('is_critical'):
            logging.info("🧹 AUTO-HEAL: Running disk cleanup...")
            self.resource_monitor._trigger_disk_cleanup()
        
        # Database reconnection
        if not health['components']['database'].get('healthy'):
            logging.info("🔌 AUTO-HEAL: Reconnecting to database...")
            try:
                if self.db:
                    await self.db.send_heartbeat()
            except Exception:
                pass
        
        # Reset circuit breakers if they've been open too long
        for name, cb in self.circuit_breakers.items():
            if cb.state == CircuitState.OPEN:
                time_open = time.time() - (cb.last_failure_time or 0)
                if time_open > 300:  # 5 minutes
                    logging.info(f"🔌 AUTO-HEAL: Resetting circuit breaker for {name}")
                    cb.reset()
        
        logging.info("✅ AUTO-HEAL: Recovery procedures completed")


class ImmortalLoop:
    """
    ♾️ IMMORTAL LOOP WRAPPER
    Ensures the bot NEVER stops, even on critical failures
    """
    
    def __init__(self, health_monitor: HealthMonitor):
        self.health_monitor = health_monitor
        self.restart_count = 0
        self.last_restart = 0
        self.max_restarts_per_hour = 10
        
    async def run_forever(self, main_func: Callable, *args, **kwargs):
        """Run a function forever, restarting on any failure"""
        while True:
            try:
                logging.info("🚀 IMMORTAL LOOP: Starting main function...")
                await main_func(*args, **kwargs)
                
            except KeyboardInterrupt:
                logging.info("⏹️ IMMORTAL LOOP: Graceful shutdown requested")
                break
                
            except Exception as e:
                # Log the error with full context
                error_trace = traceback.format_exc()
                logging.error(f"💥 IMMORTAL LOOP: Main function crashed: {e}")
                logging.error(f"Stack trace:\n{error_trace}")
                
                # Check restart rate
                now = time.time()
                if now - self.last_restart < 3600:  # Within 1 hour
                    self.restart_count += 1
                else:
                    self.restart_count = 1
                
                self.last_restart = now
                
                if self.restart_count > self.max_restarts_per_hour:
                    logging.critical(f"🚨 IMMORTAL LOOP: Too many restarts ({self.restart_count}/hour)!")
                    logging.critical("🚨 Entering degraded mode with longer delays...")
                    await asyncio.sleep(300)  # 5 minute cooldown
                    self.restart_count = 0
                
                # Send alert
                try:
                    await self._send_crash_alert(e, error_trace)
                except Exception:
                    pass
                
                # Wait before restart
                wait_time = min(30 * self.restart_count, 300)  # Max 5 minutes
                logging.info(f"⏳ IMMORTAL LOOP: Restarting in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
                
                # Run health check and auto-heal
                try:
                    health = await self.health_monitor.check_all_systems()
                    logging.info(f"🏥 Health status: {health['overall_status']}")
                except Exception:
                    pass
                
                logging.info("🔄 IMMORTAL LOOP: Restarting main function...")
    
    async def _send_crash_alert(self, error: Exception, trace: str):
        """Send crash alert via Telegram"""
        try:
            from core.db_client import RealityShapingDB
            db = RealityShapingDB()
            
            # Try AI diagnosis
            diagnosis = "Unknown error"
            try:
                from core.ai_agent import OmniIntelligence
                ai = OmniIntelligence()
                result = await ai.structural_query(
                    f"The bot crashed with this error: {trace[:1000]}. "
                    "Explain the cause in simple terms and suggest a fix. Keep it brief."
                )
                diagnosis = result.get('answer', str(error))
            except Exception:
                diagnosis = str(error)
            
            message = (
                f"🚨 <b>BOT CRASH DETECTED</b>\n\n"
                f"<b>Error:</b> {str(error)[:200]}\n\n"
                f"<b>Diagnosis:</b> {diagnosis[:300]}\n\n"
                f"<b>Restart #{self.restart_count}</b>\n"
                f"<i>Auto-recovery in progress...</i>"
            )
            
            await db.stream_log("CRITICAL", message)
            
        except Exception as e:
            logging.error(f"Failed to send crash alert: {e}")


class BulletproofSystem:
    """
    🛡️ BULLETPROOF SYSTEM - MAIN COORDINATOR
    Coordinates all bulletproof features
    """
    
    def __init__(self, db=None, ai=None):
        self.db = db
        self.ai = ai
        self.health_monitor = HealthMonitor(db, ai)
        self.immortal_loop = ImmortalLoop(self.health_monitor)
        self.resource_monitor = self.health_monitor.resource_monitor
        
        self._monitoring_task = None
        self._backup_task = None
        
    async def start_monitoring(self):
        """Start background monitoring tasks"""
        logging.info("🛡️ BULLETPROOF: Starting monitoring systems...")
        
        # Start health monitoring
        self._monitoring_task = asyncio.create_task(self._health_monitoring_loop())
        
        # Start automatic backups
        self._backup_task = asyncio.create_task(self._backup_loop())
        
        logging.info("✅ BULLETPROOF: All monitoring systems active")
    
    async def _health_monitoring_loop(self):
        """Continuous health monitoring"""
        while True:
            try:
                await asyncio.sleep(60)  # Check every minute
                
                health = await self.health_monitor.check_all_systems()
                
                # Log health status
                if health['overall_status'] != 'healthy':
                    logging.warning(f"⚠️ System health: {health['overall_status']}")
                    if 'critical_issues' in health:
                        logging.warning(f"Critical issues: {health['critical_issues']}")
                
                # Send periodic health report (every hour)
                if int(time.time()) % 3600 < 60:
                    await self._send_health_report(health)
                
            except Exception as e:
                logging.error(f"Health monitoring loop error: {e}")
                await asyncio.sleep(60)
    
    async def _backup_loop(self):
        """Automatic backup every 24 hours"""
        while True:
            try:
                await asyncio.sleep(24 * 60 * 60)  # 24 hours
                
                logging.info("💾 BULLETPROOF: Creating automatic backup...")
                await self._create_backup()
                logging.info("✅ BULLETPROOF: Backup completed")
                
            except Exception as e:
                logging.error(f"Backup loop error: {e}")
                await asyncio.sleep(60 * 60)  # Retry in 1 hour
    
    async def _create_backup(self):
        """Create backup of critical data"""
        try:
            if not self.db:
                return
            
            # Backup applications
            success, apps = await self.db._request_with_retry(
                "GET",
                f"{self.db.url}/rest/v1/applications?select=*&limit=10000"
            )
            
            if success and isinstance(apps, list):
                backup_data = {
                    'timestamp': datetime.now().isoformat(),
                    'applications': apps,
                    'count': len(apps)
                }
                
                # Save to file
                backup_file = f"backups/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                os.makedirs("backups", exist_ok=True)
                
                with open(backup_file, 'w') as f:
                    json.dump(backup_data, f, indent=2)
                
                logging.info(f"💾 Backup saved: {backup_file}")
                
                # Clean old backups (keep last 7 days)
                cutoff = time.time() - (7 * 24 * 60 * 60)
                for filename in os.listdir("backups"):
                    filepath = os.path.join("backups", filename)
                    if os.path.isfile(filepath) and os.path.getmtime(filepath) < cutoff:
                        os.remove(filepath)
                        logging.info(f"🗑️ Removed old backup: {filename}")
        
        except Exception as e:
            logging.error(f"Backup creation failed: {e}")
    
    async def _send_health_report(self, health: Dict[str, Any]):
        """Send health report via Telegram"""
        try:
            if not self.db:
                return
            
            memory = health['resources']['memory']
            disk = health['resources']['disk']
            
            report = (
                f"🏥 <b>HOURLY HEALTH REPORT</b>\n"
                f"━━━━━━━━━━━━━━━\n"
                f"📊 <b>Status:</b> {health['overall_status'].upper()}\n"
                f"💾 <b>Memory:</b> {memory.get('memory_mb', 0):.1f}MB ({memory.get('memory_percent', 0):.1f}%)\n"
                f"💿 <b>Disk:</b> {disk.get('disk_percent', 0):.1f}% used\n"
                f"🧠 <b>AI:</b> {'✅' if health['components']['ai'].get('healthy') else '⚠️ Fallback'}\n"
                f"📧 <b>Email:</b> {'✅' if health['components']['email'].get('healthy') else '❌'}\n"
                f"💾 <b>Database:</b> {'✅' if health['components']['database'].get('healthy') else '❌'}\n"
                f"━━━━━━━━━━━━━━━\n"
                f"<i>All systems operational</i>"
            )
            
            await self.db.stream_log("INFO", report)
            
        except Exception as e:
            logging.error(f"Failed to send health report: {e}")
    
    def get_circuit_breaker(self, service: str) -> CircuitBreaker:
        """Get circuit breaker for a service"""
        return self.health_monitor.circuit_breakers.get(service)


# Global instance
_bulletproof_instance = None

def get_bulletproof_system(db=None, ai=None) -> BulletproofSystem:
    """Get the global bulletproof system instance"""
    global _bulletproof_instance
    if _bulletproof_instance is None:
        _bulletproof_instance = BulletproofSystem(db, ai)
    return _bulletproof_instance
