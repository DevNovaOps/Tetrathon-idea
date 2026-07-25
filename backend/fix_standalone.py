import os
import re

ROOT_DIR = r"D:\Tetrathon\Tetrathon-idea"
TEMPLATES_DIR = os.path.join(ROOT_DIR, "backend", "templates")
STATIC_DIR = os.path.join(ROOT_DIR, "backend", "static")

standalone_apps = {
    "01-landing-page": "landing",
    "02-auth": "auth",
    "03-onboarding": "onboarding"
}

for folder, app_name in standalone_apps.items():
    src_dir = os.path.join(ROOT_DIR, folder)
    dest_template_dir = os.path.join(TEMPLATES_DIR, app_name)
    
    for file in os.listdir(src_dir):
        if file.endswith(".html"):
            src_file = os.path.join(src_dir, file)
            with open(src_file, "r", encoding="utf-8") as f:
                html = f.read()
                
            # Replace basic css/js links with django static
            html = re.sub(r'<link rel="stylesheet" href="(.*?\.css)"\s*/>', rf'<link rel="stylesheet" href="{{% static \'{app_name}/\1\' %}}" />', html)
            html = re.sub(r'<script src="(.*?\.js)"></script>', rf'<script src="{{% static \'{app_name}/\1\' %}}"></script>', html)
            
            # Add {% load static %} at the top
            html = "{% load static %}\n" + html
            
            with open(os.path.join(dest_template_dir, file), "w", encoding="utf-8") as out:
                out.write(html)
            print(f"Fixed standalone template: {file}")
