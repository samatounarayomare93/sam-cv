"""
MAXIMUM POWER DATA VALIDATION LAYER
=====================================
Adds comprehensive validation to prevent bad data from entering the system.
"""

import re
from typing import Optional, Tuple

class ValidationError(Exception):
    """Raised when data validation fails"""
    pass

def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """Validate email format with comprehensive checks"""
    if not email or not isinstance(email, str):
        return False, "Email is empty or not a string"

    email = email.strip().lower()

    # Basic regex
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return False, "Invalid email format"

    # Check for disposable/temporary emails
    disposable_domains = [
        '10minutemail.com', 'tempmail.com', 'guerrillamail.com',
        'mailinator.com', 'trashmail.com', 'temp-mail.org'
    ]
    domain = email.split('@')[1]
    if any(d in domain for d in disposable_domains):
        return False, "Disposable email domain"

    # Check for test/no-reply mailboxes using local-part only.
    # This avoids false positives like person@example.com.
    local_part = email.split('@', 1)[0]
    if any(keyword in local_part for keyword in ['test', 'noreply', 'no-reply', 'donotreply']):
        return False, "Test/no-reply email address"

    # Check minimum length
    if len(email) < 6:
        return False, "Email too short"

    # Check for role-based emails (may indicate generic inbox)
    role_based = ['admin@', 'support@', 'info@', 'contact@', 'sales@']
    if any(email.startswith(role) for role in role_based):
        # These are acceptable but flag them
        return True, "role_based"

    return True, None

def validate_salary(salary_str: str) -> Tuple[bool, int]:
    """Validate and parse salary string"""
    if not salary_str:
        return True, 0

    # Remove currency symbols and commas
    cleaned = str(salary_str).replace('$', '').replace(',', '').replace('€', '').strip()

    try:
        salary = int(float(cleaned))
        if salary < 0:
            return False, 0
        if salary > 1000000:  # Sanity check - too high
            return False, 0
        return True, salary
    except (ValueError, TypeError):
        return False, 0

def validate_job_title(title: str) -> Tuple[bool, Optional[str]]:
    """Validate job title"""
    if not title or len(title.strip()) < 3:
        return False, "Title too short"

    title = title.strip()

    # Check for suspicious patterns
    if len(title) > 200:
        return False, "Title too long"

    # Check for test/invalid titles
    test_patterns = ['test', 'xxx', 'placeholder', 'to be filled']
    if any(p in title.lower() for p in test_patterns):
        return False, "Test/placeholder title"

    return True, None

def validate_location(location: str) -> Tuple[bool, Optional[str]]:
    """Validate location string"""
    if not location:
        return True, None  # Empty location is acceptable

    location = location.strip()
    if len(location) < 2:
        return False, "Location too short"

    if len(location) > 200:
        return False, "Location too long"

    return True, None

def validate_company_name(name: str) -> Tuple[bool, Optional[str]]:
    """Validate company name"""
    if not name:
        return False, "Company name is required"

    name = name.strip()
    if len(name) < 2:
        return False, "Company name too short"

    if len(name) > 200:
        return False, "Company name too long"

    # Check for test/placeholder
    if name.lower() in ['unknown', 'test company', 'test', 'example']:
        return False, "Invalid company name"

    return True, None

def validate_url(url: str) -> Tuple[bool, Optional[str]]:
    """Validate URL format"""
    if not url:
        return True, None  # URL optional

    url = url.strip()
    if not (url.startswith('http://') or url.startswith('https://')):
        return False, "URL must start with http:// or https://"

    if len(url) > 500:
        return False, "URL too long"

    return True, None

def sanitize_string(value: str, max_length: int = 500) -> str:
    """Sanitize string input"""
    if not value:
        return ""

    # Strip whitespace
    value = str(value).strip()

    # Remove null bytes
    value = value.replace('\x00', '')

    # Limit length
    if len(value) > max_length:
        value = value[:max_length]

    return value

class DataValidator:
    """Centralized data validation for all system inputs"""

    @staticmethod
    def validate_lead(lead: dict) -> Tuple[bool, list]:
        """Validate a lead/job dictionary"""
        errors = []

        # Required fields validation
        required_fields = {
            'company_name': validate_company_name,
            'job_title': validate_job_title,
            'email': validate_email,
        }

        for field, validator in required_fields.items():
            value = lead.get(field, '')
            if field == 'email' and not value:
                errors.append(f"Missing required field: {field}")
                continue

            is_valid, error_msg = validator(value)
            if not is_valid:
                errors.append(f"Invalid {field}: {error_msg}")

        # Optional fields validation
        optional_validators = {
            'location': validate_location,
            'salary': validate_salary,
            'url': validate_url,
            'link': validate_url,
        }

        for field, validator in optional_validators.items():
            value = lead.get(field, '')
            if value:  # Only validate if present
                is_valid, error_msg = validator(value)
                if not is_valid:
                    errors.append(f"Invalid {field}: {error_msg}")

        return len(errors) == 0, errors

    @staticmethod
    def clean_lead(lead: dict) -> dict:
        """Clean and sanitize lead data"""
        cleaned = {}

        text_fields = ['company_name', 'job_title', 'location', 'description']
        for field in text_fields:
            if field in lead:
                cleaned[field] = sanitize_string(lead[field], 1000 if field == 'description' else 200)

        # Email
        if 'email' in lead:
            email = lead['email'].strip().lower()
            cleaned['email'] = email

        # URL fields
        for url_field in ['url', 'link']:
            if url_field in lead:
                cleaned[url_field] = lead[url_field].strip()

        # Preserve other fields
        for key, value in lead.items():
            if key not in cleaned:
                cleaned[key] = value

        return cleaned

