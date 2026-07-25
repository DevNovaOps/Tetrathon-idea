import os
import re
import shutil

ROOT_DIR = r"D:\Tetrathon\Tetrathon-idea"
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
TEMPLATES_DIR = os.path.join(BACKEND_DIR, "templates")
STATIC_DIR = os.path.join(BACKEND_DIR, "static")

# Create dirs if not exist
os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

# Generate base.html
BASE_HTML = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{% block title %}Finora{% endblock %}</title>
  <meta name="description" content="AI-powered financial wellness platform." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet" />
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  {% load static %}
  {% block extra_css %}{% endblock %}
</head>
<body>
  <div class="bg-glow bg-glow--1" aria-hidden="true"></div>
  <div class="bg-glow bg-glow--2" aria-hidden="true"></div>
  <div class="bg-glow bg-glow--3" aria-hidden="true"></div>
  <div class="bg-grid-overlay" aria-hidden="true"></div>
  {% block background_extras %}{% endblock %}

  <div class="dashboard-container">
    <!-- LEFT SIDEBAR -->
    <aside class="sidebar" id="sidebar">
      <div class="sidebar-header">
        <a href="{% url 'landing' %}" class="brand-logo" aria-label="Finora Home">
          <div class="brand-icon">
            <svg width="26" height="26" viewBox="0 0 28 28" fill="none">
              <rect width="28" height="28" rx="8" fill="url(#brandGrad)"/>
              <path d="M9 19V9h8v2.5H12v2h4v2.5h-4V19H9z" fill="#fff"/>
              <defs>
                <linearGradient id="brandGrad" x1="0" y1="0" x2="28" y2="28">
                  <stop stop-color="#6366F1"/>
                  <stop offset="1" stop-color="#8B5CF6"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <span class="brand-name">Finora</span>
        </a>
      </div>

      <nav class="sidebar-nav">
        <ul class="nav-list">
          <li>
            <a href="{% url 'dashboard' %}" class="nav-link {% if request.resolver_match.url_name == 'dashboard' %}active{% endif %}">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>
              </svg>
              <span>Dashboard</span>
            </a>
          </li>
          <li>
            <a href="{% url 'credit-score' %}" class="nav-link {% if request.resolver_match.url_name == 'credit-score' %}active{% endif %}">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
              <span>Credit Score</span>
            </a>
          </li>
          <li>
            <a href="{% url 'improve-score' %}" class="nav-link {% if request.resolver_match.url_name == 'improve-score' %}active{% endif %}">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M23 6l-9.5 9.5-5-5L1 18"/><path d="M17 6h6v6"/>
              </svg>
              <span>Improve Score</span>
            </a>
          </li>
          <li>
            <a href="{% url 'ai-assistant' %}" class="nav-link {% if request.resolver_match.url_name == 'ai-assistant' %}active{% endif %}">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 2a10 10 0 1 0 10 10H12V2z"/><path d="M12 12L2.5 7.5"/><path d="M12 12v10"/>
              </svg>
              <span>AI Assistant</span>
            </a>
          </li>
          <li>
            <a href="{% url 'risk-profile' %}" class="nav-link {% if request.resolver_match.url_name == 'risk-profile' %}active{% endif %}">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/>
              </svg>
              <span>Risk Profile</span>
            </a>
          </li>
          <li>
            <a href="{% url 'investment' %}" class="nav-link {% if request.resolver_match.url_name == 'investment' %}active{% endif %}">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
              </svg>
              <span>Investments</span>
            </a>
          </li>
          <li>
            <a href="{% url 'simulator' %}" class="nav-link {% if request.resolver_match.url_name == 'simulator' %}active{% endif %}">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/>
              </svg>
              <span>Simulator</span>
            </a>
          </li>
          <li>
            <a href="{% url 'reports' %}" class="nav-link {% if request.resolver_match.url_name == 'reports' %}active{% endif %}">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>
              </svg>
              <span>Reports</span>
            </a>
          </li>
          <li>
            <a href="#" class="nav-link">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
              </svg>
              <span>Learn</span>
            </a>
          </li>
          <li>
            <a href="#" class="nav-link">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/>
              </svg>
              <span>Achievements</span>
            </a>
          </li>
          <li>
            <a href="#" class="nav-link">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/>
              </svg>
              <span>Notifications</span>
            </a>
          </li>
          <li>
            <a href="#" class="nav-link">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
              </svg>
              <span>Profile</span>
            </a>
          </li>
          <li>
            <a href="#" class="nav-link">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.6a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
              </svg>
              <span>Settings</span>
            </a>
          </li>
        </ul>
      </nav>

      <div class="sidebar-user">
        <div class="user-avatar-small">
          <span>{{ request.user.first_name|default:"D"|make_list|first|upper }}</span>
        </div>
        <div class="user-info-small">
          <span class="user-name-small">{{ request.user.first_name|default:"Dev" }}</span>
          <span class="user-tier-small">Pro AI Plan</span>
        </div>
      </div>
    </aside>

    <!-- MAIN CONTENT -->
    <main class="main-content">
      <header class="top-nav">
        <div class="greeting-area">
          <button class="mobile-toggle" id="mobileToggle" aria-label="Toggle menu">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/>
            </svg>
          </button>
          <div>
            <h1 class="welcome-title">{% block page_title %}{% endblock %}</h1>
            <p class="welcome-subtitle">{% block page_subtitle %}{% endblock %}</p>
          </div>
        </div>

        <div class="nav-actions-right">
          {% block top_nav_extras %}{% endblock %}
          
          <button class="icon-btn" id="themeToggle" aria-label="Toggle Theme">
            <svg class="ti ti--sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
            </svg>
            <svg class="ti ti--moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
            </svg>
          </button>

          <button class="icon-btn" aria-label="Notifications">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/>
            </svg>
            <span class="bell-badge"></span>
          </button>

          <div class="user-profile-btn">
            <div class="profile-avatar-circle">
              <span>{{ request.user.first_name|default:"D"|make_list|first|upper }}</span>
            </div>
            <span class="profile-username">{{ request.user.first_name|default:"Dev" }}</span>
          </div>
        </div>
      </header>

      {% block content %}{% endblock %}

    </main>
  </div>
  
  {% block extra_js %}{% endblock %}
</body>
</html>
"""

with open(os.path.join(TEMPLATES_DIR, "base.html"), "w") as f:
    f.write(BASE_HTML)

mapping = {
    "01-landing-page": "landing",
    "02-auth": "auth",
    "03-onboarding": "onboarding",
    "04-dashboard": "dashboard",
    "05-credit-score": "credit_score",
    "06-improve-score": "improve_score",
    "07-ai-assistant": "ai_assistant",
    "08-risk-profile": "risk_profile",
    "09-investment": "investment",
    "10-growth-simulator": "growth_simulator",
    "11-reports": "reports",
    "12-notifications": "notifications",
    "13-education": "education",
    "14-achievements": "achievements",
    "15-profile": "profile",
    "16-settings": "settings"
}

for folder in os.listdir(ROOT_DIR):
    if folder in mapping:
        app_name = mapping[folder]
        src_dir = os.path.join(ROOT_DIR, folder)
        dest_template_dir = os.path.join(TEMPLATES_DIR, app_name)
        dest_static_dir = os.path.join(STATIC_DIR, app_name)
        
        os.makedirs(dest_template_dir, exist_ok=True)
        os.makedirs(dest_static_dir, exist_ok=True)
        
        for file in os.listdir(src_dir):
            src_file = os.path.join(src_dir, file)
            if os.path.isfile(src_file):
                if file.endswith(".html"):
                    with open(src_file, "r", encoding="utf-8") as f:
                        html = f.read()
                    
                    # Extract everything after </header> and before </main>
                    body_match = re.search(r'</header>(.*?)</main>', html, re.DOTALL | re.IGNORECASE)
                    if not body_match:
                        # Fallback for pages without <header> (like login/landing)
                        body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)
                        if not body_match:
                            print(f"Could not parse body for {file}")
                            continue
                        # If it's a fallback, we probably don't want the base.html layout, but we'll try
                        page_body = body_match.group(1)
                    else:
                        page_body = body_match.group(1)
                    
                    # Extract title and subtitle
                    title_match = re.search(r'<h1 class="welcome-title">(.*?)</h1>', html)
                    subtitle_match = re.search(r'<p class="welcome-subtitle">(.*?)</p>', html)
                    
                    title = title_match.group(1) if title_match else ""
                    subtitle = subtitle_match.group(1) if subtitle_match else ""
                    
                    # Also grab any extra nav buttons like month-selector in reports
                    # We look between greeting-area end and themeToggle
                    # This is tricky, let's just grab the whole nav-actions-right minus themeToggle/Notifs/Profile
                    nav_actions = ""
                    nav_right_match = re.search(r'<div class="nav-actions-right">(.*?)<button class="icon-btn" id="themeToggle"', html, re.DOTALL)
                    if nav_right_match:
                        nav_actions = nav_right_match.group(1).strip()
                    
                    # CSS/JS files
                    css_files = re.findall(r'<link rel="stylesheet" href="(.*?)"\s*/>', html)
                    js_files = re.findall(r'<script src="(.*?)"></script>', html)
                    
                    css_blocks = []
                    for css in css_files:
                        if not css.startswith("http"):
                            css_blocks.append(f'<link rel="stylesheet" href="{{% static \'{app_name}/{css}\' %}}" />')
                    
                    js_blocks = []
                    for js in js_files:
                        if not js.startswith("http"):
                            js_blocks.append(f'<script src="{{% static \'{app_name}/{js}\' %}}"></script>')
                    
                    # Replace internal HTML images/links to static if needed
                    # (Skipping for now as most SVGs are inline)

                    new_html = f"{{% extends 'base.html' %}}\n{{% load static %}}\n\n"
                    new_html += f"{{% block title %}}{title}{{% endblock %}}\n"
                    new_html += f"{{% block page_title %}}{title}{{% endblock %}}\n"
                    new_html += f"{{% block page_subtitle %}}{subtitle}{{% endblock %}}\n"
                    
                    if css_blocks:
                        new_html += f"{{% block extra_css %}}\n" + "\n".join(css_blocks) + f"\n{{% endblock %}}\n"
                        
                    if js_blocks:
                        new_html += f"{{% block extra_js %}}\n" + "\n".join(js_blocks) + f"\n{{% endblock %}}\n"
                        
                    if nav_actions:
                        new_html += f"{{% block top_nav_extras %}}\n{nav_actions}\n{{% endblock %}}\n"
                        
                    new_html += f"\n{{% block content %}}\n{page_body}\n{{% endblock %}}\n"
                    
                    with open(os.path.join(dest_template_dir, file), "w", encoding="utf-8") as out:
                        out.write(new_html)
                        
                else:
                    # Move css, js, png, etc. to static
                    shutil.copy2(src_file, os.path.join(dest_static_dir, file))

print("Migration completed!")
