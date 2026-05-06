"""
🔧 ERROR RECOVERY SYSTEM
═══════════════════════════════════════════════════

Comprehensive error recovery and retry logic for all operations.
Ensures the bot never stops due to transient errors.
"""

import asyncio
import logging
import time
import random
from typing import Callable, Any, Optional, Dict
from functools import wraps
from enum import Enum

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [RECOVERY] %(levelname)s - %(message)s")


class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"  # Retry immediately
    MEDIUM = "medium"  # Retry with backoff
    HIGH = "high"  # Retry with long backoff
    CRITICAL = "critical"  # Alert and retry


class SmartRetry:
    """
    🔄 SMART RETRY SYSTEM
    Intelligent retry logic with exponential backoff and jitter
    """
    
    def __init__(
        self,
        max_retries: int = 5,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        
        self.retry_counts = {}
        self.last_errors = {}
    
    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay with exponential backoff and jitter"""
        delay = min(
            self.base_delay * (self.exponential_base ** attempt),
            self.max_delay
        )
        
        if self.jitter:
            # Add random jitter (±25%)
            jitter_amount = delay * 0.25
            delay += random.uniform(-jitter_amount, jitter_amount)
        
        return max(0, delay)
    
    async def retry_async(
        self,
        func: Callable,
        *args,
        error_handler: Optional[Callable] = None,
        **kwargs
    ) -> Any:
        """Retry an async function with smart backoff"""
        func_name = func.__name__
        
        for attempt in range(self.max_retries):
            try:
                result = await func(*args, **kwargs)
                
                # Reset retry count on success
                if func_name in self.retry_counts:
                    del self.retry_counts[func_name]
                
                return result
                
            except Exception as e:
                # Track retry count
                self.retry_counts[func_name] = attempt + 1
                self.last_errors[func_name] = str(e)
                
                # Check if we should retry
                if attempt >= self.max_retries - 1:
                    logging.error(
                        f"❌ {func_name} failed after {self.max_retries} attempts: {e}"
                    )
                    
                    # Call error handler if provided
                    if error_handler:
                        try:
                            return await error_handler(e, attempt)
                        except Exception:
                            pass
                    
                    raise e
                
                # Calculate delay
                delay = self.calculate_delay(attempt)
                
                # Classify error severity
                severity = self._classify_error(e)
                
                logging.warning(
                    f"⚠️ {func_name} failed (attempt {attempt + 1}/{self.max_retries}): {e}"
                )
                logging.info(
                    f"⏳ Retrying in {delay:.2f}s (severity: {severity.value})..."
                )
                
                await asyncio.sleep(delay)
    
    def retry_sync(
        self,
        func: Callable,
        *args,
        error_handler: Optional[Callable] = None,
        **kwargs
    ) -> Any:
        """Retry a sync function with smart backoff"""
        func_name = func.__name__
        
        for attempt in range(self.max_retries):
            try:
                result = func(*args, **kwargs)
                
                # Reset retry count on success
                if func_name in self.retry_counts:
                    del self.retry_counts[func_name]
                
                return result
                
            except Exception as e:
                # Track retry count
                self.retry_counts[func_name] = attempt + 1
                self.last_errors[func_name] = str(e)
                
                # Check if we should retry
                if attempt >= self.max_retries - 1:
                    logging.error(
                        f"❌ {func_name} failed after {self.max_retries} attempts: {e}"
                    )
                    
                    # Call error handler if provided
                    if error_handler:
                        try:
                            return error_handler(e, attempt)
                        except Exception:
                            pass
                    
                    raise e
                
                # Calculate delay
                delay = self.calculate_delay(attempt)
                
                # Classify error severity
                severity = self._classify_error(e)
                
                logging.warning(
                    f"⚠️ {func_name} failed (attempt {attempt + 1}/{self.max_retries}): {e}"
                )
                logging.info(
                    f"⏳ Retrying in {delay:.2f}s (severity: {severity.value})..."
                )
                
                time.sleep(delay)
    
    def _classify_error(self, error: Exception) -> ErrorSeverity:
        """Classify error severity"""
        error_str = str(error).lower()
        
        # Critical errors
        if any(word in error_str for word in ['auth', 'permission', 'forbidden', '403', '401']):
            return ErrorSeverity.CRITICAL
        
        # High severity
        if any(word in error_str for word in ['timeout', 'connection', 'network']):
            return ErrorSeverity.HIGH
        
        # Medium severity
        if any(word in error_str for word in ['rate limit', '429', 'too many']):
            return ErrorSeverity.MEDIUM
        
        # Low severity (default)
        return ErrorSeverity.LOW
    
    def get_stats(self) -> Dict[str, Any]:
        """Get retry statistics"""
        return {
            'active_retries': len(self.retry_counts),
            'retry_counts': dict(self.retry_counts),
            'last_errors': dict(self.last_errors)
        }


def with_retry(max_retries: int = 5, base_delay: float = 1.0):
    """
    Decorator for automatic retry with smart backoff
    
    Usage:
        @with_retry(max_retries=3, base_delay=2.0)
        async def my_function():
            # Your code here
            pass
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            retry = SmartRetry(max_retries=max_retries, base_delay=base_delay)
            return await retry.retry_async(func, *args, **kwargs)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            retry = SmartRetry(max_retries=max_retries, base_delay=base_delay)
            return retry.retry_sync(func, *args, **kwargs)
        
        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


class ErrorRecovery:
    """
    🔧 ERROR RECOVERY COORDINATOR
    Manages error recovery strategies for different components
    """
    
    def __init__(self):
        self.retry_system = SmartRetry()
        self.error_history = []
        self.recovery_strategies = {}
        
        # Register default recovery strategies
        self._register_default_strategies()
    
    def _register_default_strategies(self):
        """Register default recovery strategies"""
        
        # Database recovery
        self.recovery_strategies['database'] = {
            'retry_count': 5,
            'base_delay': 2.0,
            'fallback': 'use_local_sqlite'
        }
        
        # AI recovery
        self.recovery_strategies['ai'] = {
            'retry_count': 3,
            'base_delay': 1.0,
            'fallback': 'use_template'
        }
        
        # Email recovery
        self.recovery_strategies['email'] = {
            'retry_count': 3,
            'base_delay': 5.0,
            'fallback': 'try_next_provider'
        }
        
        # Scraper recovery
        self.recovery_strategies['scraper'] = {
            'retry_count': 3,
            'base_delay': 10.0,
            'fallback': 'use_cached_data'
        }
    
    async def recover_database(self, error: Exception, db) -> bool:
        """Recover from database errors"""
        logging.info("🔧 RECOVERY: Attempting database recovery...")
        
        try:
            # Try to reconnect
            await db.send_heartbeat()
            logging.info("✅ RECOVERY: Database connection restored")
            return True
        except Exception:
            logging.warning("⚠️ RECOVERY: Database still unavailable, using local SQLite")
            return False
    
    async def recover_ai(self, error: Exception, ai) -> Optional[Dict]:
        """Recover from AI errors"""
        logging.info("🔧 RECOVERY: Attempting AI recovery...")
        
        try:
            # Try alternative AI provider
            if hasattr(ai, 'switch_provider'):
                await ai.switch_provider()
                logging.info("✅ RECOVERY: Switched to alternative AI provider")
                return {'recovered': True, 'method': 'alternative_provider'}
        except Exception:
            pass
        
        # Fallback to templates
        logging.info("🔧 RECOVERY: Using fallback templates (no AI)")
        return {'recovered': True, 'method': 'fallback_template'}
    
    async def recover_email(self, error: Exception, provider: str) -> Optional[str]:
        """Recover from email errors"""
        logging.info(f"🔧 RECOVERY: Attempting email recovery (failed provider: {provider})...")
        
        # Try next provider
        providers = ['gmail', 'zoho', 'brevo', 'yahoo']
        
        try:
            current_index = providers.index(provider)
            next_provider = providers[(current_index + 1) % len(providers)]
            
            logging.info(f"✅ RECOVERY: Switching to {next_provider}")
            return next_provider
        except Exception:
            logging.warning("⚠️ RECOVERY: No alternative email provider available")
            return None
    
    async def recover_scraper(self, error: Exception, url: str) -> Optional[Dict]:
        """Recover from scraper errors"""
        logging.info(f"🔧 RECOVERY: Attempting scraper recovery for {url}...")
        
        # Try with different user agent
        try:
            from core.runtime_helpers import get_evasion
            evasion = get_evasion()
            evasion.rotate_identity()
            
            logging.info("✅ RECOVERY: Rotated scraper identity")
            return {'recovered': True, 'method': 'identity_rotation'}
        except Exception:
            logging.warning("⚠️ RECOVERY: Scraper recovery failed")
            return None
    
    def log_error(self, component: str, error: Exception, context: Dict = None):
        """Log error for analysis"""
        error_record = {
            'timestamp': time.time(),
            'component': component,
            'error': str(error),
            'error_type': type(error).__name__,
            'context': context or {}
        }
        
        self.error_history.append(error_record)
        
        # Keep only last 1000 errors
        if len(self.error_history) > 1000:
            self.error_history = self.error_history[-1000:]
    
    def get_error_stats(self) -> Dict[str, Any]:
        """Get error statistics"""
        if not self.error_history:
            return {'total_errors': 0}
        
        # Count errors by component
        component_counts = {}
        error_type_counts = {}
        
        for record in self.error_history:
            component = record['component']
            error_type = record['error_type']
            
            component_counts[component] = component_counts.get(component, 0) + 1
            error_type_counts[error_type] = error_type_counts.get(error_type, 0) + 1
        
        return {
            'total_errors': len(self.error_history),
            'by_component': component_counts,
            'by_type': error_type_counts,
            'recent_errors': self.error_history[-10:]
        }


# Global instance
_recovery_instance = None

def get_error_recovery() -> ErrorRecovery:
    """Get the global error recovery instance"""
    global _recovery_instance
    if _recovery_instance is None:
        _recovery_instance = ErrorRecovery()
    return _recovery_instance
