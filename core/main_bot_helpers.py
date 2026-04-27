"""
Main Bot Helpers - Deterministic filtering and scoring logic.
Restored from legacy archive for test compatibility and swarm optimization.
"""

from typing import Any, Dict, Tuple
from core import config

TARGET_KEYWORDS = [
    "hr", "operations", "admin", "assistant", "manager", "people", "coordinator", "officer", "recruitment", "talent"
]

BAD_TITLE_KEYWORDS = ["intern", "junior", "scholarship", "volunteer", "apprentice", "trainee"]


def is_valid_target(company_name: str, location: str, salary: Any, phase: str, description: str = "") -> Tuple[bool, str, float, int]:
    """Validate company/location/salary against configured mission rules."""
    loc_lower = str(location or "").lower().strip()
    desc_lower = str(description or "").lower()
    company_lower = str(company_name or "").lower()

    for exc in getattr(config, "EXCLUDED_COMPANIES", []):
        if exc in company_lower:
            return False, f"Banned company: {exc}", 0, 0

    try:
        salary_val = float(str(salary).replace("$", "").replace(",", "") or 0)
    except ValueError:
        salary_val = 0.0

    is_prime = any(city in loc_lower for city in getattr(config, "PRIME_LEBANON_CITIES", []))
    is_lebanon = is_prime or "lebanon" in loc_lower or "lb" in loc_lower or "remote" in loc_lower or loc_lower == ""
    perk_count = sum(1 for kw in getattr(config, "GLOBAL_SPONSOR_KEYWORDS", ["visa", "relocation", "sponsorship"]) if kw in desc_lower)

    phase = phase if phase in ("lebanon", "global") else "global"

    if phase == "lebanon":
        if is_lebanon:
            min_allowed = getattr(config, "MIN_SALARY_LEBANON_PRIME", 1500) if is_prime else getattr(config, "MIN_SALARY_LEBANON_OTHER", 1000)
            if salary_val == 0 or salary_val >= min_allowed:
                return True, "Valid Lebanon target.", salary_val, perk_count
            return False, "Lebanon salary too low.", 0, 0
        if (salary_val >= 6000 or salary_val == 0) and perk_count > 0:
            return True, "Valid global override target.", salary_val, perk_count
        return False, "Not Lebanon and no override.", 0, 0

    if is_lebanon:
        return False, "Global phase skipping Lebanon.", 0, 0

    loc_match = any(target.lower() in loc_lower for target in getattr(config, "GOD_MODE_LOCATIONS", []))
    if (salary_val >= getattr(config, "MIN_SALARY_GLOBAL", 6000) or salary_val == 0) and (perk_count > 0 or loc_match):
        return True, "Valid premium global target.", salary_val, perk_count
    return False, "Global target skipped criteria.", 0, 0


def is_relevant_to_cv(job_title: str, description: str = ""):
    """Keyword-based relevance check with legacy return shape."""
    title_lower = str(job_title or "").lower().strip()
    if not title_lower:
        return True, "No title", "", "0"

    if any(b.lower() in title_lower for b in getattr(config, "BANNED_TITLES", [])):
        return False, "Banned title", "", "0"

    if any(k in title_lower for k in TARGET_KEYWORDS):
        return True, "Matched keywords", "", "0"

    return False, "No relevant keywords.", "", "0"


def fast_filter(lead: Dict[str, Any], current_phase: str = None) -> bool:
    """Quick pass/fail filter for obvious mismatches."""
    phase = (current_phase or "global").lower()
    location = str(lead.get("location", "")).lower()

    if phase == "lebanon":
        allowed = ["lebanon", "lb", "beirut", "keserwan", "kesrouane", "jbeil", "byblos", "metn", "matn", "maten", "jabal lebanon", "mount lebanon", "remote"]
    else:
        allowed = ["remote", "worldwide", "global", "uae", "dubai", "qa", "sa", "gcc", "gulf", "middle east", "lebanon", "beirut", "lb"]

    if location and not any(x in location for x in allowed):
        return False

    title = str(lead.get("job_title", "")).lower()
    if any(k in title for k in BAD_TITLE_KEYWORDS):
        return False

    return True


def lead_priority_score(lead: Dict[str, Any]) -> int:
    """Compute a simple lead priority score."""
    score = 0
    title = str(lead.get("job_title", "")).lower()
    description = str(lead.get("description", "")).lower()
    location = str(lead.get("location", "")).lower()

    if any(k in title for k in ["manager", "lead", "director", "head"]):
        score += 20
    if any(k in title for k in ["hr", "operations", "admin", "talent", "recruit"]):
        score += 15
    if any(k in location for k in ["remote", "worldwide", "global"]):
        score += 10
    if any(k in description for k in ["visa", "relocation", "sponsorship"]):
        score += 12

    salary_val = 0.0
    for key in ["salary_min", "salary", "estimated_salary"]:
        raw = lead.get(key, 0)
        try:
            salary_val = max(salary_val, float(str(raw).replace("$", "").replace(",", "") or 0))
        except Exception:
            continue

    score += min(int(salary_val // 500), 20)
    return score


def render_application_body(template_body: str, lead: Dict[str, Any]) -> str:
    """Render known placeholders safely."""
    body = template_body or ""
    company = str(lead.get("company_name", "Hiring Team")).strip() or "Hiring Team"
    title = str(lead.get("job_title", "Professional Role")).strip() or "Professional Role"
    try:
        return body.format(company_name=company, job_title=title)
    except Exception:
        return body.replace("{company_name}", company).replace("{job_title}", title)
