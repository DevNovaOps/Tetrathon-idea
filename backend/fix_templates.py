import os
import glob
import re

files = glob.glob('d:/Tetrathon/Tetrathon-idea/backend/templates/**/*.html', recursive=True)
modified = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    if r"\'" in content:
        content = content.replace(r"\'", "'")
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        modified += 1
        print(f"Fixed {f}")

print(f"Total fixed: {modified}")
