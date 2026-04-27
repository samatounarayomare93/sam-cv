from typing import Any, Dict


def normalize_lead(lead: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize lead records into one shared schema."""
    return {
        'company_name': lead.get('company_name') or lead.get('company') or 'Unknown',
        'job_title': lead.get('job_title') or lead.get('title') or 'Role',
        'link': lead.get('link') or lead.get('url') or lead.get('job_url') or '',
        'email': lead.get('email') or '',
        'description': lead.get('description') or lead.get('summary') or '',
        'source': lead.get('source') or lead.get('platform') or 'unknown',
        'posted_at': lead.get('posted_at') or lead.get('date_posted') or '',
        'is_guessed': bool(lead.get('is_guessed', False)),
    }
