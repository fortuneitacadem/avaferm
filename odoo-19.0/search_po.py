import os

po_path = os.path.join('addons', 'website_slides', 'i18n', 'uz.po')

with open(po_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'Comments' in line or 'Izohlar' in line or 'eLearning' in line:
        print(f"Line {i+1}: {line.strip()}")
        # Print surrounding lines
        start = max(0, i - 2)
        end = min(len(lines), i + 3)
        for j in range(start, end):
            print(f"  [{j+1}] {lines[j].strip()}")
        print("-" * 40)
