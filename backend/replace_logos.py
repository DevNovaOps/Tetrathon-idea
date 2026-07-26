import os
import re

ROOT = r"d:\Tetrathon\Tetrathon-idea\backend\templates"
files = [
    os.path.join(ROOT, "base.html"),
    os.path.join(ROOT, "landing", "index.html"),
    os.path.join(ROOT, "auth", "login.html"),
    os.path.join(ROOT, "auth", "signup.html"),
    os.path.join(ROOT, "auth", "forgot-password.html"),
    os.path.join(ROOT, "onboarding", "index.html"),
]

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    original = content
    # Replace <svg> inside <div class="brand-icon">
    content = re.sub(r'(<div class="brand-icon">)\s*<svg.*?</svg>\s*(</div>)', r'\1\n            <img src="{% static \'img/logo-icon.png\' %}" alt="Finora Logo" style="width: 100%; height: 100%; object-fit: contain;">\n          \2', content, flags=re.DOTALL)
    
    # Replace <svg> inside <div class="logo-icon-box">
    content = re.sub(r'(<div class="logo-icon-box">)\s*<svg.*?</svg>\s*(</div>)', r'\1\n              <img src="{% static \'img/logo-icon.png\' %}" alt="Finora Logo" style="width: 100%; height: 100%; object-fit: contain;">\n            \2', content, flags=re.DOTALL)

    # Replace <svg> inside <div class="nav-logo-icon">
    content = re.sub(r'(<div class="nav-logo-icon">)\s*<svg.*?</svg>\s*(</div>)', r'\1\n          <img src="{% static \'img/logo-icon.png\' %}" alt="Finora Logo" style="width: 100%; height: 100%; object-fit: contain;">\n        \2', content, flags=re.DOTALL)
    
    if content != original:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Updated logos in {f}")
