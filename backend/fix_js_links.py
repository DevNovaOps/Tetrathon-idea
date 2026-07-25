import os
import re

STATIC_DIR = r"D:\Tetrathon\Tetrathon-idea\backend\static"

link_mapping = {
    r"\.\./01-landing-page/index\.html": "/",
    r"/01-landing-page/index\.html": "/",
    r"\.\./02-auth/login\.html": "/login/",
    r"/02-auth/login\.html": "/login/",
    r"\.\./02-auth/signup\.html": "/signup/",
    r"/02-auth/signup\.html": "/signup/",
    r"\.\./03-onboarding/index\.html": "/onboarding/",
    r"/03-onboarding/index\.html": "/onboarding/",
    r"\.\./04-dashboard/dashboard\.html": "/dashboard/",
    r"/04-dashboard/dashboard\.html": "/dashboard/",
}

for root, _, files in os.walk(STATIC_DIR):
    for file in files:
        if file.endswith(".js"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                
            modified = False
            for old_link, new_link in link_mapping.items():
                if re.search(old_link, content):
                    content = re.sub(old_link, new_link, content)
                    modified = True
                    
            if modified:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Fixed JS redirects in {os.path.relpath(path, STATIC_DIR)}")
print("Done fixing JS redirects!")
