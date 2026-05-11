"""
Check each handler - is it real or just a placeholder?
"""
import re

with open("core/telegram_dashboard.py", "r", encoding="utf-8", errors="replace") as f:
    lines = f.readlines()

# Find all elif key == blocks and check if they have real content
handlers = {}
i = 0
while i < len(lines):
    m = re.match(r'\s*elif key == "(\w+)":', lines[i])
    if m:
        key = m.group(1)
        # Collect next lines until next elif/def
        body = []
        j = i + 1
        while j < len(lines):
            next_line = lines[j]
            if re.match(r'\s*(elif key ==|elif cmd ==|def |async def )', next_line):
                break
            body.append(next_line.strip())
            j += 1
        
        body_text = " ".join(body)
        
        # Classify
        is_placeholder = (
            "Coming soon" in body_text or
            "Not implemented" in body_text or
            "TODO" in body_text or
            len([b for b in body if b and not b.startswith('#')]) < 3
        )
        
        has_db = "self.db" in body_text or "db._request" in body_text
        has_real_data = "reply_text" in body_text and (has_db or "os.getenv" in body_text or "import" in body_text)
        
        handlers[key] = {
            "lines": j - i,
            "has_db": has_db,
            "has_real_data": has_real_data,
            "is_placeholder": is_placeholder,
            "preview": body_text[:100]
        }
    i += 1

print(f"Total handlers: {len(handlers)}")
print("\n" + "="*60)

real = []
placeholder = []
for key, info in handlers.items():
    if info["is_placeholder"] or info["lines"] < 4:
        placeholder.append(key)
    else:
        real.append(key)

print(f"✅ Real handlers ({len(real)}):")
for k in sorted(real):
    db = " [DB]" if handlers[k]["has_db"] else ""
    print(f"  ✅ {k}{db}")

print(f"\n⚠️ Short/placeholder handlers ({len(placeholder)}):")
for k in sorted(placeholder):
    print(f"  ⚠️ {k} ({handlers[k]['lines']} lines)")
