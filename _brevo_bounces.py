"""Check Brevo bounce details to understand what's happening."""
import os, sys, requests
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()

key = os.getenv('BREVO_API_KEY', '')
headers = {'api-key': key, 'Accept': 'application/json'}

print("=== BREVO BOUNCE ANALYSIS ===\n")

# Get hard bounces
r = requests.get(
    'https://api.brevo.com/v3/contacts?limit=50&sort=desc&offset=0',
    headers=headers, timeout=10
)

# Get blocked/bounced contacts
for endpoint, label in [
    ('https://api.brevo.com/v3/contacts/blockedContacts?limit=20', 'BLOCKED'),
    ('https://api.brevo.com/v3/smtp/blockedContacts?limit=20', 'SMTP BLOCKED'),
]:
    r = requests.get(endpoint, headers=headers, timeout=10)
    if r.status_code == 200:
        data = r.json()
        contacts = data.get('contacts', data.get('blockedContacts', []))
        print(f"{label} ({len(contacts)} found):")
        for c in contacts[:15]:
            email = c.get('email', '?')
            reason = c.get('reason', {})
            rtype = reason.get('code', reason.get('message', '?')) if isinstance(reason, dict) else str(reason)
            print(f"  {email:40} Reason: {rtype}")
        print()
    else:
        print(f"{label}: {r.status_code} - {r.text[:80]}\n")

# Get email activity with events
print("=== RECENT EMAIL EVENTS ===\n")
r = requests.get(
    'https://api.brevo.com/v3/smtp/statistics/events?limit=30&sort=desc',
    headers=headers, timeout=10
)
if r.status_code == 200:
    events = r.json().get('events', [])
    bounce_count = 0
    delivered_count = 0
    for e in events:
        event = e.get('event', '?')
        email = e.get('email', '?')
        subject = e.get('subject', '?')[:40]
        date = e.get('date', '?')[:16]
        if event in ['hardBounce', 'softBounce', 'blocked', 'invalid']:
            bounce_count += 1
            reason = e.get('reason', '')
            print(f"  ❌ {event:12} | {email:35} | {reason[:40]}")
        elif event == 'delivered':
            delivered_count += 1
    print(f"\nSummary: {delivered_count} delivered, {bounce_count} bounced/blocked in last 30 events")
else:
    print(f"Events: {r.status_code} - {r.text[:100]}")

# Check sending stats
print("\n=== SENDING STATS (last 30 days) ===")
r = requests.get(
    'https://api.brevo.com/v3/smtp/statistics/aggregatedReport?startDate=2026-04-01&endDate=2026-05-06',
    headers=headers, timeout=10
)
if r.status_code == 200:
    s = r.json()
    total = s.get('requests', 0)
    delivered = s.get('delivered', 0)
    bounced = s.get('hardBounces', 0) + s.get('softBounces', 0)
    spam = s.get('spamReports', 0)
    opens = s.get('uniqueOpens', 0)
    rate = round(delivered/total*100, 1) if total else 0
    print(f"  Sent:      {total}")
    print(f"  Delivered: {delivered} ({rate}%)")
    print(f"  Bounced:   {bounced}")
    print(f"  Spam:      {spam}")
    print(f"  Opens:     {opens}")
    if bounced > delivered:
        print("\n  ⚠️  MORE BOUNCES THAN DELIVERIES!")
        print("  This means emails are going to fake/invalid addresses.")
        print("  Fix: Improve email validation before sending.")
