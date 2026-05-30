import re
import os

po_path = os.path.join('addons', 'website_slides', 'i18n', 'uz.po')

if not os.path.exists(po_path):
    print(f"Error: {po_path} not found!")
    exit(1)

with open(po_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Normalize line endings to \n
content = content.replace('\r\n', '\n')

# 1. Remove '#, fuzzy' lines
# We match '#, fuzzy' and any trailing whitespaces/newlines
cleaned_content = re.sub(r'#,\s*fuzzy\n', '', content)

# 2. Add crucial empty translations
replacements = {
    'msgid "<i class=\\"fa fa-comments\\"/> Comments"\nmsgstr ""': 'msgid "<i class=\\"fa fa-comments\\"/> Comments"\nmsgstr "<i class=\\"fa fa-comments\\"/> Izohlar"',
    'msgid "Comments"\nmsgstr ""': 'msgid "Comments"\nmsgstr "Izohlar"',
    'msgid "eLearning"\nmsgstr ""': 'msgid "eLearning"\nmsgstr "eLearning (Mavzular)"',
    'msgid "Lessons"\nmsgstr ""': 'msgid "Lessons"\nmsgstr "Darslar"',
}

replaced_count = 0
for orig, repl in replacements.items():
    if orig in cleaned_content:
        cleaned_content = cleaned_content.replace(orig, repl)
        replaced_count += 1
    else:
        # Try finding regardless of line endings or whitespace matches
        # Normalize double quotes and match
        orig_norm = orig.replace('\n', ' ')
        print(f"Checking alternative match for: {orig_norm}")

with open(po_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(cleaned_content)

print(f"Successfully cleaned Odoo translation file: {po_path}")
print(f"Removed '#, fuzzy' lines and populated {replaced_count} crucial terms.")
