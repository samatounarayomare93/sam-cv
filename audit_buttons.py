"""
Audit all keyboard buttons vs their handlers in text_map
"""
import re

with open("core/telegram_dashboard.py", "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

# Extract all KeyboardButton labels
kb_buttons = re.findall(r'KeyboardButton\("([^"]+)"', content)

# Extract all text_map keys
text_map_match = re.search(r'text_map\s*=\s*\{(.+?)\}\s*\n\s*mapped', content, re.DOTALL)
text_map_keys = set()
if text_map_match:
    text_map_content = text_map_match.group(1)
    keys = re.findall(r'"([^"]+)"\s*:', text_map_content)
    text_map_keys = {k.lower() for k in keys}

# Extract all elif key == handlers
handled_keys = set(re.findall(r'elif key == "([^"]+)"', content))

print(f"Total keyboard buttons: {len(kb_buttons)}")
print(f"Total text_map entries: {len(text_map_keys)}")
print(f"Total elif key handlers: {len(handled_keys)}")

print("\n" + "="*60)
print("BUTTON AUDIT:")
print("="*60)

working = []
broken = []

for btn in kb_buttons:
    # Extract the command part (before |)
    label = btn.split("|")[0].strip()
    # Remove emoji
    clean = re.sub(r'[^\w\s]', '', label).strip().lower()
    # Try to find in text_map
    found_in_map = any(clean in k or k in clean for k in text_map_keys)
    found_in_handler = any(clean in k or k in clean for k in handled_keys)
    
    if found_in_map or found_in_handler:
        working.append(btn)
    else:
        broken.append((btn, clean))

print(f"\n✅ Working buttons: {len(working)}")
print(f"❌ Possibly broken: {len(broken)}")

if broken:
    print("\nPossibly broken buttons:")
    for btn, clean in broken:
        print(f"  - '{btn}' (normalized: '{clean}')")
