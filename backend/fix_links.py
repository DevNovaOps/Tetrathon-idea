import os
import re

ROOT = r"d:\Tetrathon\Tetrathon-idea\backend\templates"

replacements = [
    (r"href=[\'\"]\.\./02-auth/login\.html[\'\"]", 'href="{% url \'login\' %}"'),
    (r"href=[\'\"]\.\./01-landing-page/index\.html[\'\"]", 'href="{% url \'landing\' %}"'),
    (r"href=[\'\"]login\.html[\'\"]", 'href="{% url \'login\' %}"'),
    (r"href=[\'\"]forgot-password\.html[\'\"]", 'href="{% url \'forgot-password\' %}"'),
    (r"href=[\'\"]signup\.html[\'\"]", 'href="{% url \'signup\' %}"'),
    (r"href=[\'\"]\.\./04-dashboard/dashboard\.html[\'\"]", 'href="{% url \'dashboard\' %}"'),
    (r"href=[\'\"]\.\./03-onboarding/index\.html[\'\"]", 'href="{% url \'onboarding\' %}"'),
]

files = [
    os.path.join(ROOT, "landing", "index.html"),
    os.path.join(ROOT, "auth", "forgot-password.html"),
    os.path.join(ROOT, "auth", "login.html"),
    os.path.join(ROOT, "auth", "signup.html"),
]

for f in files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        original_content = content
        for pattern, repl in replacements:
            content = re.sub(pattern, repl, content)
            
        if content != original_content:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Fixed links in {f}")
