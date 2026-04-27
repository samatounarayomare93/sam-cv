"""Root compatibility shim for SMTP engine after core migration."""

import logging
from typing import Any, Dict, Iterable, Optional

from core import smtp_engine as _core


def _get_available_providers():
    """Expose provider discovery for compatibility and tests."""
    return _core._get_available_providers()


def send_email(
    to_email: str,
    company_name: str,
    job_title: str,
    custom_body: str,
    platform: str,
    mission_type: str,
    attachment_paths: Optional[Iterable[str]] = None,
    pdf_path=None,
    retry_count: int = 0,
    sender_name: str = "Sam Salameh",
    highlights: Optional[Iterable[Dict[str, Any]]] = None,
    **_kwargs,
):
    """Compatibility wrapper that keeps provider checks testable."""
    providers = _get_available_providers()
    if not providers:
        logging.warning("No SMTP providers configured")
        return False
    resolved_attachments = list(attachment_paths or [])
    if pdf_path:
        if isinstance(pdf_path, (list, tuple, set)):
            resolved_attachments.extend(list(pdf_path))
        else:
            resolved_attachments.append(pdf_path)

    return _core.send_email(
        to_email=to_email,
        company_name=company_name,
        job_title=job_title,
        custom_body=custom_body,
        platform=platform,
        mission_type=mission_type,
        attachment_paths=resolved_attachments,
        retry_count=retry_count,
        sender_name=sender_name,
        highlights=list(highlights or []),
    )


def send_strike(lead: Dict[str, Any], attachment_paths=None, sender_name: str = "Sam Salameh"):
    """Compatibility wrapper expected by legacy modules and tests."""
    return send_email(
        to_email=lead.get("email", ""),
        company_name=lead.get("company_name", "Unknown Company"),
        job_title=lead.get("job_title", "Professional Role"),
        custom_body=lead.get("custom_body", ""),
        platform=lead.get("platform", "omni"),
        mission_type=lead.get("mission_type", "global"),
        attachment_paths=attachment_paths,
        sender_name=sender_name,
        highlights=lead.get("highlights", []),
    )


def send_test_email(recipient_email=None, attachment_paths=None, highlights=None):
    """Pass-through test email helper."""
    return _core.send_test_email(recipient_email, attachment_paths, highlights)
