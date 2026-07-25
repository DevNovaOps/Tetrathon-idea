import os

d = r'D:\Tetrathon\Tetrathon-idea\backend\templates'
for r, dirs, fs in os.walk(d):
    for f in fs:
        if f.endswith('.html'):
            p = os.path.join(r, f)
            with open(p, 'r', encoding='utf-8') as file:
                content = file.read()
            # Replace escaped quotes
            content = content.replace("\\'", "'")
            with open(p, 'w', encoding='utf-8') as file:
                file.write(content)
print("Done")
