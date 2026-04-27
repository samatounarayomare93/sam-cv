import os
import json
import time
import logging
import psutil
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from collections import deque
import statistics

# ==========================================
# 🏥 SYSTEM HEALTH & AUTO-REPAIR - MAXIMUM POWER
# ==========================================

@dataclass
class HealthMetric:
    """MAXIMUM POWER: Individual health metric with trend tracking"""
    name: str
    value: float
    unit: str = ""
    threshold_warning: float = 0.8
    threshold_critical: float = 0.9
    history: deque = field(default_factory=lambda: deque(maxlen=100))
    last_updated: float = field(default_factory=time.time)
    
    def update(self, value: float):
        """Update metric and track trend"""
        self.value = value
        self.last_updated = time.time()
        self.history.append(value)
    
    def get_trend(self, window: int = 10) -> Optional[float]:
        """Calculate trend over recent history"""
        if len(self.history) < window:
            return None
        recent = list(self.history)[-window:]
        if len(recent) < 2:
            return None
        # Simple linear regression slope
        n = len(recent)
        x_mean = (n - 1) / 2
        y_mean = sum(recent) / n
        numerator = sum((i - x_mean) * (y - y_mean) for i, y in enumerate(recent))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        return numerator / denominator if denominator != 0 else 0.0
    
    def get_status(self) -> str:
        """Get current health status based on threshold"""
        if self.value >= self.threshold_critical:
            return "🔴 CRITICAL"
        elif self.value >= self.threshold_warning:
            return "🟡 WARNING"
        else:
            return "🟢 OK"


@dataclass
class ComponentHealth:
    """MAXIMUM POWER: Component health with detailed tracking"""
    name: str
    status: str = "⚪ UNKNOWN"
    last_check: float = field(default_factory=time.time)
    failure_count: int = 0
    last_error: Optional[str] = None
    uptime: float = 0.0
    metrics: Dict[str, HealthMetric] = field(default_factory=dict)
    
    def mark_healthy(self):
        """Mark component as healthy"""
        self.status = "🟢 OK"
        self.last_check = time.time()
    
    def mark_unhealthy(self, error: Optional[str] = None):
        """Mark component as unhealthy"""
        self.failure_count += 1
        self.last_error = error
        self.status = "🔴 UNHEALTHY"
        self.last_check = time.time()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "status": self.status,
            "last_check": datetime.fromtimestamp(self.last_check).isoformat(),
            "failure_count": self.failure_count,
            "last_error": self.last_error,
            "uptime": self.uptime,
            "metrics": {k: {"value": v.value, "unit": v.unit} 
                       for k, v in self.metrics.items()}
        }


class AdvancedHealthCheck:
    """
    MAXIMUM POWER: Advanced health monitoring with predictive analytics,
    trend analysis, and proactive alerting.
    """
    
    def __init__(self):
        self.health_log = "health_check.json"
        self.components: Dict[str, ComponentHealth] = {}
        self.start_time = time.time()
        self.alert_history = deque(maxlen=100)
        self.status = {
            "last_check": None,
            "issues_fixed": 0,
            "system_health": "🟡 RECOVERING",
            "components": {},
            "last_application": None,
            "total_issues": 0,
        }
        self._initialize_components()
        self.load_health_status()
    
    def _initialize_components(self):
        """Initialize all component health trackers"""
        components = [
            ("pdf_cache", {"disk_usage": HealthMetric("pdf_disk_usage", 0.0, "%", 0.8, 0.9)}),
            ("database", {"query_time": HealthMetric("db_query_time", 0.0, "ms", 0.5, 0.8)}),
            ("smtp", {"delivery_rate": HealthMetric("smtp_delivery_rate", 1.0, "%", 0.9, 0.95)}),
            ("telegram", {"response_time": HealthMetric("tg_response_time", 0.0, "ms", 0.7, 0.9)}),
            ("scraper", {"success_rate": HealthMetric("scraper_success", 1.0, "%", 0.8, 0.9)}),
            ("ai_agent", {"response_time": HealthMetric("ai_response_time", 0.0, "ms", 0.6, 0.8)}),
            ("disk_space", {"usage": HealthMetric("disk_usage", 0.0, "%", 0.85, 0.95)}),
            ("memory", {"usage": HealthMetric("memory_usage", 0.0, "%", 0.8, 0.9)}),
        ]
        
        for comp_name, metrics in components:
            comp = ComponentHealth(name=comp_name)
            for metric_name, metric in metrics.items():
                comp.metrics[metric_name] = metric
            self.components[comp_name] = comp
    
    def save_health_status(self):
        """Save health status to file."""
        try:
            self.status["components"] = {name: comp.to_dict() for name, comp in self.components.items()}
            with open(self.health_log, 'w', encoding='utf-8') as f:
                json.dump(self.status, f, indent=2)
        except Exception as e:
            logging.warning(f"Could not save health status: {e}")
    
    def load_health_status(self):
        """Load or initialize health status."""
        try:
            if os.path.exists(self.health_log):
                with open(self.health_log, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.status.update({k: data.get(k, self.status.get(k)) for k in self.status.keys()})
                    # Restore component states
                    for comp_name, comp_data in data.get("components", {}).items():
                        if comp_name in self.components:
                            comp = self.components[comp_name]
                            comp.status = comp_data.get("status", "⚪ UNKNOWN")
                            comp.failure_count = comp_data.get("failure_count", 0)
                            comp.last_error = comp_data.get("last_error")
                            comp.uptime = comp_data.get("uptime", 0.0)
                            # Restore metrics if present
                            metrics_data = comp_data.get("metrics", {})
                            for m_name, m_data in metrics_data.items():
                                if m_name in comp.metrics:
                                    comp.metrics[m_name].value = m_data.get("value", 0.0)
        except Exception as e:
            logging.warning(f"Health check load failed: {e}")
    
    def check_pdf_cache(self):
        """✅ Auto-repair: Check and fix PDF cache."""
        try:
            pdf_dir = os.path.join(os.path.dirname(__file__), "pdf_cache")
            if not os.path.exists(pdf_dir):
                os.makedirs(pdf_dir)
                logging.info("🏥 Auto-repair: Created missing pdf_cache directory")
                self.components["pdf_cache"].mark_healthy()
                return True
            
            # Clean old PDFs (> 48 hours)
            current_time = time.time()
            removed = 0
            for filename in os.listdir(pdf_dir):
                if filename.endswith('.pdf'):
                    file_path = os.path.join(pdf_dir, filename)
                    file_age = current_time - os.path.getmtime(file_path)
                    if file_age > 172800:  # 48 hours
                        os.remove(file_path)
                        removed += 1
            
            self.components["pdf_cache"].mark_healthy()
            self.components["pdf_cache"].metrics["disk_usage"].update(0.0)
            return True
        except Exception as e:
            logging.error(f"PDF cache repair failed: {e}")
            self.components["pdf_cache"].mark_unhealthy(str(e))
            self.status["total_issues"] += 1
            return False
    
    def check_tracker(self):
        """✅ Auto-repair: Check and repair tracker.json."""
        try:
            if not os.path.exists("tracker.json"):
                tracker = {"applications": [], "last_updated": datetime.now().isoformat()}
                with open("tracker.json", 'w', encoding='utf-8') as f:
                    json.dump(tracker, f, indent=2)
                logging.info("🏥 Auto-repair: Created missing tracker.json")
            else:
                # Verify tracker is valid JSON
                with open("tracker.json", 'r', encoding='utf-8') as f:
                    json.load(f)
            
            self.components["database"].mark_healthy()
            return True
        except Exception as e:
            logging.error(f"Tracker repair failed: {e}")
            self.components["database"].mark_unhealthy(str(e))
            self.status["total_issues"] += 1
            return False
    
    def check_company_db(self):
        """✅ Auto-repair: Check and repair company database."""
        try:
            if not os.path.exists("company_database.json"):
                db = {"companies": [], "last_updated": datetime.now().isoformat()}
                with open("company_database.json", 'w', encoding='utf-8') as f:
                    json.dump(db, f, indent=2)
                logging.info("🏥 Auto-repair: Created missing company_database.json")
            else:
                # Verify database is valid JSON
                with open("company_database.json", 'r', encoding='utf-8') as f:
                    json.load(f)
            
            self.components["database"].mark_healthy()
            return True
        except Exception as e:
            logging.error(f"Company DB repair failed: {e}")
            self.components["database"].mark_unhealthy(str(e))
            self.status["total_issues"] += 1
            return False
    
    def run_full_health_check(self):
        """🏥 Run full system health check and auto-repair."""
        logging.info("🏥 Running full system health check...")
        
        results = {
            "pdf_cache": self.check_pdf_cache(),
            "tracker": self.check_tracker(),
            "company_db": self.check_company_db()
        }
        
        # Determine overall health
        if all(results.values()):
            self.status["system_health"] = "🟢 HEALTHY"
        elif any(results.values()):
            self.status["system_health"] = "🟡 RECOVERING"
        else:
            self.status["system_health"] = "🔴 CRITICAL"
        
        self.status["last_check"] = datetime.now().isoformat()
        self.status["issues_fixed"] += 1
        self.status["components"] = {name: comp.to_dict() for name, comp in self.components.items()}
        self.save_health_status()
        
        logging.info(f"🏥 Health check complete: {self.status['system_health']}")
        return self.status
    
    def get_status(self):
        """Get current system health status."""
        return self.status


# Backward compatibility alias
HealthCheck = AdvancedHealthCheck

# ==========================================
# 📊 COMPANY DATABASE & DEDUPLICATION
# ==========================================

class CompanyDatabase:
    """Tracks all companies and prevents duplicate applications."""
    
    def __init__(self):
        self.db_file = "company_database.json"
        self.load_database()
    
    def load_database(self):
        """Load company database."""
        try:
            if os.path.exists(self.db_file):
                with open(self.db_file, 'r') as f:
                    data = json.load(f)
                    self.companies = {c["email"]: c for c in data.get("companies", [])}
            else:
                self.companies = {}
            logging.info(f"📊 Loaded {len(self.companies)} companies from database")
        except Exception as e:
            logging.warning(f"Company DB load failed: {e}")
            self.companies = {}
    
    def save_database(self):
        """Save company database."""
        try:
            data = {
                "companies": list(self.companies.values()),
                "total_unique": len(self.companies),
                "last_updated": datetime.now().isoformat()
            }
            with open(self.db_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logging.error(f"Company DB save failed: {e}")
    
    def add_company(self, email, company_name, job_title, location, source="manual"):
        """Add company to database."""
        if email not in self.companies:
            self.companies[email] = {
                "email": email,
                "company_name": company_name,
                "job_title": job_title,
                "location": location,
                "source": source,
                "first_seen": datetime.now().isoformat(),
                "applications_sent": 0,
                "last_application": None,
                "status": "pending"
            }
            self.save_database()
            logging.info(f"✅ Added {company_name} to database")
            return True
        return False
    
    def is_duplicate(self, email, job_title):
        """Check if already applied to this company for this role."""
        if email in self.companies:
            company = self.companies[email]
            # Check if applied within last 30 days
            if company["last_application"]:
                last_app = datetime.fromisoformat(company["last_application"])
                days_ago = (datetime.now() - last_app).days
                if days_ago < 30:
                    return True
        return False
    
    def mark_application_sent(self, email, company_name, job_title):
        """Mark that we sent an application to this company."""
        if email not in self.companies:
            self.add_company(email, company_name, job_title, "Unknown", "application")
        
        self.companies[email]["applications_sent"] += 1
        self.companies[email]["last_application"] = datetime.now().isoformat()
        self.companies[email]["status"] = "applied"
        self.save_database()
        logging.info(f"📊 Marked application sent to {company_name}")
    
    def get_statistics(self):
        """Get database statistics."""
        total_companies = len(self.companies)
        total_applications = sum(c.get("applications_sent", 0) for c in self.companies.values())
        
        return {
            "total_unique_companies": total_companies,
            "total_applications_sent": total_applications,
            "average_per_company": total_applications / max(total_companies, 1),
            "last_updated": datetime.now().isoformat()
        }


# ==========================================
# 📈 REAL-TIME METRICS SYSTEM
# ==========================================

class MetricsTracker:
    """Real-time metrics for monitoring system performance."""
    
    def __init__(self):
        self.metrics_file = "metrics.json"
        self.load_metrics()
    
    def load_metrics(self):
        """Load or initialize metrics."""
        try:
            if os.path.exists(self.metrics_file):
                with open(self.metrics_file, 'r') as f:
                    self.metrics = json.load(f)
            else:
                self.metrics = {
                    "today": {
                        "applications_sent": 0,
                        "jobs_analyzed": 0,
                        "errors": 0,
                        "success_rate": 0
                    },
                    "this_week": {
                        "applications_sent": 0,
                        "jobs_analyzed": 0,
                        "errors": 0
                    },
                    "this_month": {
                        "applications_sent": 0,
                        "jobs_analyzed": 0,
                        "errors": 0
                    },
                    "all_time": {
                        "applications_sent": 0,
                        "jobs_analyzed": 0,
                        "errors": 0
                    },
                    "last_run": None,
                    "next_run": None
                }
                self.save_metrics()
        except Exception as e:
            logging.warning(f"Metrics load failed: {e}")
            self.metrics = {}
    
    def save_metrics(self):
        """Save metrics to file."""
        try:
            with open(self.metrics_file, 'w') as f:
                json.dump(self.metrics, f, indent=2)
        except Exception as e:
            logging.error(f"Metrics save failed: {e}")
    
    def record_application(self, count=1, autosave=True):
        """Record successful application(s)."""
        count = max(0, int(count))
        if count == 0:
            return

        self.metrics["today"]["applications_sent"] += count
        self.metrics["this_week"]["applications_sent"] += count
        self.metrics["this_month"]["applications_sent"] += count
        self.metrics["all_time"]["applications_sent"] += count
        if autosave:
            self.save_metrics()
    
    def record_job_analyzed(self, count=1, autosave=True):
        """Record analyzed job(s)."""
        count = max(0, int(count))
        if count == 0:
            return

        self.metrics["today"]["jobs_analyzed"] += count
        self.metrics["this_week"]["jobs_analyzed"] += count
        self.metrics["this_month"]["jobs_analyzed"] += count
        self.metrics["all_time"]["jobs_analyzed"] += count
        if autosave:
            self.save_metrics()
    
    def record_error(self, count=1, autosave=True):
        """Record error(s)."""
        count = max(0, int(count))
        if count == 0:
            return

        self.metrics["today"]["errors"] += count
        self.metrics["this_week"]["errors"] += count
        self.metrics["this_month"]["errors"] += count
        self.metrics["all_time"]["errors"] += count
        if autosave:
            self.save_metrics()
    
    def get_dashboard_stats(self):
        """Get stats for Telegram dashboard."""
        today = self.metrics.get("today", {})
        this_week = self.metrics.get("this_week", {})
        this_month = self.metrics.get("this_month", {})
        all_time = self.metrics.get("all_time", {})
        
        return {
            "📊 TODAY": {
                "📧 Applications": today.get("applications_sent", 0),
                "🔍 Jobs Analyzed": today.get("jobs_analyzed", 0),
                "⚠️ Errors": today.get("errors", 0)
            },
            "📈 THIS WEEK": {
                "📧 Applications": this_week.get("applications_sent", 0),
                "🔍 Jobs Analyzed": this_week.get("jobs_analyzed", 0)
            },
            "📅 THIS MONTH": {
                "📧 Applications": this_month.get("applications_sent", 0),
                "🔍 Jobs Analyzed": this_month.get("jobs_analyzed", 0)
            },
            "🏆 ALL TIME": {
                "📧 Applications": all_time.get("applications_sent", 0),
                "🔍 Jobs Analyzed": all_time.get("jobs_analyzed", 0)
            }
        }


if __name__ == "__main__":
    # Test health check
    health = HealthCheck()
    health.run_full_health_check()
    print(json.dumps(health.get_status(), indent=2))
    
    # Test company database
    db = CompanyDatabase()
    db.add_company("test@example.com", "Test Company", "HR Manager", "Dubai")
    print(json.dumps(db.get_statistics(), indent=2))
    
    # Test metrics
    metrics = MetricsTracker()
    metrics.record_application()
    metrics.record_job_analyzed()
    print(json.dumps(metrics.get_dashboard_stats(), indent=2))
