import os
import re

TEMPLATES_DIR = r"D:\Tetrathon\Tetrathon-idea\backend\templates"

# Map the old HTML paths to the new URL names we defined in web/urls.py
link_mapping = {
    r"../01-landing-page/index.html": "landing",
    r"../02-auth/login.html": "login",
    r"../02-auth/signup.html": "signup",
    r"../02-auth/forgot-password.html": "forgot-password",
    r"../03-onboarding/index.html": "onboarding",
    r"../04-dashboard/dashboard.html": "dashboard",
    r"../05-credit-score/credit-score.html": "credit-score",
    r"../06-improve-score/improve-score.html": "improve-score",
    r"../07-ai-assistant/ai-assistant.html": "ai-assistant",
    r"../08-risk-profile/risk-profile.html": "risk-profile",
    r"../09-investment/investment.html": "investment",
    r"../10-growth-simulator/growth-simulator.html": "simulator",
    r"../11-reports/reports.html": "reports",
    
    # Also handle links without the leading ../ for same-folder or absolute matches
    r"01-landing-page/index.html": "landing",
    r"02-auth/login.html": "login",
    r"02-auth/signup.html": "signup",
    r"02-auth/forgot-password.html": "forgot-password",
    r"03-onboarding/index.html": "onboarding",
    r"04-dashboard/dashboard.html": "dashboard",
    r"05-credit-score/credit-score.html": "credit-score",
    r"06-improve-score/improve-score.html": "improve-score",
    r"07-ai-assistant/ai-assistant.html": "ai-assistant",
    r"08-risk-profile/risk-profile.html": "risk-profile",
    r"09-investment/investment.html": "investment",
    r"10-growth-simulator/growth-simulator.html": "simulator",
    r"11-reports/reports.html": "reports",
    
    # And handle specific file basenames if they navigate laterally
    r"login.html": "login",
    r"signup.html": "signup",
    r"forgot-password.html": "forgot-password",
}

for root, _, files in os.walk(TEMPLATES_DIR):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                
            modified = False
            # Find and replace all hrefs matching our mapping
            for old_link, route_name in link_mapping.items():
                # Regex to match href="old_link" exactly, ignoring quotes
                pattern = rf'href=([\'"]){re.escape(old_link)}([\'"])'
                new_href = rf'href=\1{{% url \'{route_name}\' %}}\2'
                
                if re.search(pattern, content):
                    content = re.sub(pattern, new_href, content)
                    modified = True
                    
            if modified:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Updated links in {os.path.relpath(path, TEMPLATES_DIR)}")
print("Done fixing links!")
