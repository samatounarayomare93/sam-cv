from datetime import datetime, timezone
now = datetime.now(timezone.utc)
month = now.month + 1 if now.month < 12 else 1
year = now.year if now.month < 12 else now.year + 1
next_month = datetime(year, month, 1, tzinfo=timezone.utc)
days_left = (next_month - now).days
print(f"Today: {now.strftime('%Y-%m-%d')}")
print(f"Render quota resets: {next_month.strftime('%Y-%m-%d')}")
print(f"Days until reset: {days_left} days")
