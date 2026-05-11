import re

with open('core/telegram_dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the reply_keyboard section
start = content.find('reply_keyboard = [')
end = content.find('reply_markup = ReplyKeyboardMarkup', start)
keyboard_section = content[start:end]

# Extract all button labels
buttons = re.findall(r'KeyboardButton\("([^"]+)"\)', keyboard_section)

print(f"Total buttons in keyboard: {len(buttons)}")
print()
for i, b in enumerate(buttons, 1):
    # Show just the English part (before |)
    label = b.split('|')[0].strip()
    print(f"{i:3}. {label}")
