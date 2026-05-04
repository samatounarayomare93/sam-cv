import requests, os
from dotenv import load_dotenv
from collections import Counter, defaultdict
load_dotenv()

api_key = os.getenv('BREVO_API_KEY')
headers = {'api-key': api_key}

r = requests.get('https://api.brevo.com/v3/smtp/statistics/events', 
    headers=headers, params={'limit': 100})
events = r.json().get('events', [])

print(f"Total events: {len(events)}")
print()

# Group by recipient + subject
sends = defaultdict(list)
for e in events:
    key = f"{e.get('email')} | {e.get('subject','')[:50]}"
    sends[key].append(e.get('event'))

print("=== DUPLICATE SENDS (same email + subject) ===")
duplicates = {k: v for k, v in sends.items() if len(v) > 1}
for key, events_list in list(duplicates.items())[:10]:
    print(f"  {len(events_list)}x | {key}")
    print(f"     Events: {events_list}")

print()
print("=== DELIVERY RATE ===")
all_events = [e.get('event') for e in events]
c = Counter(all_events)
for event, count in c.most_common():
    print(f"  {event}: {count}")

print()
print("=== DELIVERED TO REAL COMPANIES ===")
delivered = [e for e in events if e.get('event') == 'delivered']
for e in delivered:
    print(f"  ✅ {e.get('email')} | {e.get('subject','')[:60]}")
