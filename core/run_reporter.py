from typing import Any, Dict


def build_cycle_report(stats: Dict[str, int]) -> str:
    """Build a concise cycle summary for logs or notifications."""
    return (
        "📊 Cycle summary\n"
        f"Raw leads: {stats.get('raw_leads', 0)}\n"
        f"Processed: {stats.get('processed_leads', 0)}\n"
        f"Duplicates: {stats.get('duplicates', 0)}\n"
        f"Rejected: {stats.get('rejected', 0)}\n"
        f"Sent: {stats.get('sent', 0)}\n"
        f"Failed: {stats.get('failed', 0)}"
    )


def build_preflight_report(status: Dict[str, Any]) -> str:
    """Build a small startup readiness report."""
    return (
        "🧪 Preflight\n"
        f"Mailers ready: {status.get('at_least_one_mailer', False)}\n"
        f"Scrapers ready: {status.get('scraper_available', False)}\n"
        f"Telegram ready: {status.get('telemetry_enabled', False)}\n"
        f"DB ready: {status.get('db_available', False)}\n"
        f"Ready: {status.get('ready', False)}"
    )
