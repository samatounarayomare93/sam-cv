def is_fake_domain(email_addr):
    if not email_addr or '@' not in email_addr:
        return True
    domain = email_addr.split('@')[-1].lower()
    if len(domain) > 40:
        return True
    domain_words = domain.replace('.com','').replace('.org','').replace('.net','').replace('-',' ').split()
    if len(domain_words) > 4:
        return True
    fake_patterns = ['hr@new.com','hr@my.com','hr@it.com','hr@top.com',
                     'hr@word.com','hr@list.com','hr@well.com','hr@future.com',
                     'hr@common.com','hr@venture.com','hr@best.com']
    if email_addr.lower() in fake_patterns:
        return True
    return False

tests = [
    ('SABIS', 'careers@sabis.com', True),
    ('Strategic Growth', 'hr@strategicgrowthdrivesnewofficeopeningintunbridgewells.com', False),
    ('New Company', 'hr@new.com', False),
    ('Emirates', 'careers@emirates.com', True),
    ('NFI', 'careers@nfi.com', True),
    ('Word Inc', 'hr@word.com', False),
    ('Juno Search', 'careers@junosearchpartners.com', True),
    ('Milton Hershey', 'careers@miltonhersheyschool.com', True),
]

print('=== FAKE DOMAIN FILTER TEST ===')
for company, email, should_pass in tests:
    is_fake = is_fake_domain(email)
    actual_pass = not is_fake
    ok = actual_pass == should_pass
    print(f"  {'OK' if ok else 'FAIL'} | {company}: {email} | fake={is_fake} | expected_pass={should_pass}")
