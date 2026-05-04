"""
Additional Job Platforms - Extended Coverage
Adds more job sites for better coverage
"""

ADDITIONAL_PLATFORMS = [
    # Remote Work Platforms
    {"name": "Remote.co", "url": "remote.co", "auto_apply": True, "remote": True},
    {"name": "We Work Remotely", "url": "weworkremotely.com", "auto_apply": True, "remote": True},
    {"name": "RemoteOK", "url": "remoteok.com", "auto_apply": True, "remote": True},
    {"name": "FlexJobs", "url": "flexjobs.com", "auto_apply": True, "remote": True},
    {"name": "Working Nomads", "url": "workingnomads.com", "auto_apply": True, "remote": True},
    
    # Tech-Focused
    {"name": "AngelList", "url": "angel.co", "auto_apply": True, "tech": True},
    {"name": "Stack Overflow Jobs", "url": "stackoverflow.com/jobs", "auto_apply": True, "tech": True},
    {"name": "GitHub Jobs", "url": "jobs.github.com", "auto_apply": True, "tech": True},
    {"name": "Dice", "url": "dice.com", "auto_apply": True, "tech": True},
    {"name": "CyberCoders", "url": "cybercoders.com", "auto_apply": True, "tech": True},
    
    # Middle East Specific
    {"name": "Akhtaboot", "url": "akhtaboot.com", "auto_apply": True, "countries": "JO,LB,AE"},
    {"name": "Tanqeeb", "url": "tanqeeb.com", "auto_apply": True, "countries": "AE,SA,KW"},
    {"name": "Mihnati", "url": "mihnati.com", "auto_apply": True, "countries": "AE,SA"},
    {"name": "Laimoon", "url": "laimoon.com", "auto_apply": True, "countries": "AE,SA"},
    {"name": "Naukri Middle East", "url": "naukri.com", "auto_apply": True, "countries": "AE,SA,QA"},
    
    # Lebanon Specific
    {"name": "Jobs in Lebanon", "url": "jobsinlebanon.com", "auto_apply": True, "countries": "LB"},
    {"name": "Lebanon Opportunities", "url": "lebanon-opportunities.com", "auto_apply": True, "countries": "LB"},
    {"name": "Beirut.com Jobs", "url": "beirut.com/jobs", "auto_apply": True, "countries": "LB"},
    
    # International
    {"name": "Jooble", "url": "jooble.org", "auto_apply": True, "global": True},
    {"name": "Adzuna", "url": "adzuna.com", "auto_apply": True, "global": True},
    {"name": "Neuvoo", "url": "neuvoo.com", "auto_apply": True, "global": True},
    {"name": "Jobrapido", "url": "jobrapido.com", "auto_apply": True, "global": True},
    {"name": "Trovit", "url": "trovit.com", "auto_apply": True, "global": True},
    
    # Specialized
    {"name": "Idealist", "url": "idealist.org", "auto_apply": True, "nonprofit": True},
    {"name": "ReliefWeb", "url": "reliefweb.int", "auto_apply": True, "humanitarian": True},
    {"name": "Devex", "url": "devex.com", "auto_apply": True, "development": True},
    {"name": "UN Jobs", "url": "unjobs.org", "auto_apply": True, "international": True},
    
    # Freelance/Contract
    {"name": "Upwork", "url": "upwork.com", "auto_apply": False, "freelance": True},
    {"name": "Freelancer", "url": "freelancer.com", "auto_apply": False, "freelance": True},
    {"name": "Toptal", "url": "toptal.com", "auto_apply": False, "freelance": True},
    {"name": "Guru", "url": "guru.com", "auto_apply": False, "freelance": True},
]

# Search Queries for Discovery
DISCOVERY_QUERIES = [
    # Lebanon
    'site:*.lb "jobs" OR "careers" OR "vacancies"',
    '"jobs in lebanon" OR "careers lebanon" OR "hiring lebanon"',
    '"beirut jobs" OR "tripoli jobs" OR "sidon jobs"',
    
    # Dubai/UAE
    '"jobs in dubai" OR "careers dubai" OR "hiring dubai"',
    '"abu dhabi jobs" OR "sharjah jobs"',
    'site:*.ae "careers" OR "jobs" OR "vacancies"',
    
    # Saudi Arabia
    '"jobs in riyadh" OR "careers riyadh" OR "hiring riyadh"',
    '"jeddah jobs" OR "dammam jobs"',
    'site:*.sa "careers" OR "jobs" OR "vacancies"',
    
    # Remote
    '"remote jobs" OR "work from home" OR "remote positions"',
    '"remote network engineer" OR "remote IT jobs"',
    
    # General
    '"network engineer jobs" OR "IT jobs" OR "system administrator"',
    '"senior network engineer" OR "network architect"',
]

# Email Discovery Patterns (Extended)
EXTENDED_EMAIL_PATTERNS = [
    # English
    "talent@{domain}", "people@{domain}", "recruiting@{domain}",
    "jobs-apply@{domain}", "career@{domain}", "work@{domain}",
    "join-us@{domain}", "opportunities@{domain}", "positions@{domain}",
    
    # Arabic transliterations
    "wazaef@{domain}", "tawzif@{domain}", "amal@{domain}",
    
    # Department specific
    "it-jobs@{domain}", "tech-jobs@{domain}", "engineering@{domain}",
    "network-team@{domain}", "infrastructure@{domain}",
    
    # Regional
    "mena-jobs@{domain}", "gcc-jobs@{domain}", "levant-jobs@{domain}",
]

def get_all_platforms():
    """Returns combined list of all platforms"""
    return ADDITIONAL_PLATFORMS

def get_discovery_queries():
    """Returns search queries for platform discovery"""
    return DISCOVERY_QUERIES

def get_email_patterns():
    """Returns extended email patterns"""
    return EXTENDED_EMAIL_PATTERNS
