<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0D1526,50:6366F1,100:8B5CF6&height=210&section=header&text=Finora&fontSize=80&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Transparent%20AI%20Credit%20Intelligence&descAlignY=56&descSize=18" width="100%" alt="Finora banner" />

<br/>

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&duration=3200&pause=900&color=6366F1&center=true&vCenter=true&multiline=true&repeat=true&width=760&height=75&lines=Alternative+Digital+Signals+%C2%B7+Explainable+Wealth+Generation;AI+Financial+Assistant+%C2%B7+Risk+Assessment+%C2%B7+Credit+Scoring;FinTech+Hackathon+%C2%B7+24+Hours)](https://finora.vercel.app/)

<br/>

<a href="https://finora.vercel.app/">
  <img src="https://img.shields.io/badge/%F0%9F%96%A5%EF%B8%8F_UI_Preview-finora.vercel.app-6366F1?style=for-the-badge&labelColor=0f172a" alt="UI Preview"/>
</a>
&nbsp;
<a href="https://figma.com/">
  <img src="https://img.shields.io/badge/%F0%9F%96%8A%EF%B8%8F_Mockup-Figma-06B6D4?style=for-the-badge&labelColor=0f172a" alt="Mockup"/>
</a>

<br/><br/>

<img src="https://img.shields.io/badge/FinTech_Hackathon-24_Hours-FF6B35?style=flat-square" alt="Hackathon"/>
<img src="https://img.shields.io/badge/Status-Live_Preview_on_Vercel-22C55E?style=flat-square" alt="Status"/>
<img src="https://img.shields.io/badge/AI-Groq_LLaMA_3-7C3AED?style=flat-square" alt="AI"/>
<img src="https://img.shields.io/badge/DB-Local_MySQL_Only-336791?style=flat-square&logo=mysql&logoColor=white" alt="DB"/>
<img src="https://img.shields.io/badge/Frontend-Vanilla_JS_+_CSS-61DAFB?style=flat-square&logo=javascript&logoColor=black" alt="Frontend"/>
<img src="https://img.shields.io/badge/API-Django_5-092E20?style=flat-square&logo=django&logoColor=white" alt="API"/>
<img src="https://img.shields.io/badge/UI_Hosted-Vercel-black?style=flat-square&logo=vercel&logoColor=white" alt="Vercel"/>

<br/><br/>

```text
🤖 AI ASSISTANT  →  📊 CREDIT SCORE  →  🧠 EXPLAINABLE AI  →  📈 WEALTH GROWTH
```

</div>

---

> **FinTech Hackathon** · Next-Gen Financial Operations Platform  
> **UI Preview (Vercel):** [https://finora.vercel.app/](https://finora.vercel.app/) — frontend only  
> **Full stack (API + MySQL):** **local only** — database is not connected on Vercel

Finora democratizes credit access and optimizes wealth accumulation by ingesting non-traditional digital signals and delivering Explainable AI insights — built as a central intelligence platform for users' financial health.

<div align="center">

| 🤖 AI Assistant | 📊 Credit Engine | 🧠 XAI Memory | 📈 Wealth |
|:---:|:---:|:---:|:---:|
| Conversational LLaMA-3 | Alternative signals | Transparent insights | Dynamic CAGR projection |
| Dynamic risk profiling | UPI / OTT ingestion | Event-driven tracking | Asset allocation |
| Natural language goals | Baseline modifiers | Milestone highlights | Actionable roadmaps |

</div>

---

## Table of Contents

<details open>
<summary><b>Navigate</b></summary>

| # | Section | # | Section |
|---:|---|---:|---|
| 1 | [Overview](#1-overview) | 6 | [Architecture](#6-architecture) |
| 2 | [Problem & Goal](#2-problem--goal) | 7 | [Repository Structure](#7-repository-structure) |
| 3 | [Links & Credentials](#3-links--credentials) | 8 | [Authentication](#8-authentication) |
| 4 | [Features & Deliverables](#4-features--deliverables) | 9 | [Setup (Local)](#9-setup-local) |
| 5 | [Technology Stack](#5-technology-stack) | 10 | [Screenshots](#10-screenshots) |

</details>

---

## 1. Overview

**Finora** is a full-stack web app for the FinTech Hackathon. It covers the user's financial lifecycle end-to-end:

| Capability | What it does |
|---|---|
| AI Financial Assistant | Conversational interface powered by Groq LLaMA-3 to assess risk tolerance and goals. |
| Alternative Credit Score | Ingests non-traditional digital signals (UPI, OTT, utilities) to generate dynamic scores. |
| Explainable AI (XAI) | Translates credit and risk changes into transparent, human-readable insights. |
| Dynamic Wealth Simulator | Projects portfolio growth using real-time CAGR across different risk buckets. |
| Financial Reports | Dashboards displaying categorized expenses, savings, and performance metrics. |

Stack shape: **Vanilla JS + CSS** frontend · **Django 5** REST API · **MySQL** (local) · Groq LLM · Session Authentication · dark mode.

> End-to-end data workflows need local MySQL + API. The Vercel URL is a **UI preview** only.

---

## 2. Problem & Goal

| Pain (traditional finance) | Finora fix |
|---|---|
| Invisible "thin-file" users | Alternative digital signals integrated directly into scoring |
| "Black Box" credit scores | Explainable AI (XAI) provides transparent reasoning |
| Static financial advice | Dynamic, conversational AI Assistant |
| Disconnected wealth planning | Interactive Growth Simulator tied to real-time risk profiles |

**Hackathon objective:** Build a scalable, AI-driven personal finance platform that democratizes access to credit and intelligently guides wealth generation.

---

## 3. Links & Credentials

| Resource | Link / note |
|---|---|
| UI Preview (Vercel) | [https://finora.vercel.app/](https://finora.vercel.app/) — **no live MySQL** |
| Full stack + database | Local — Django `:8000` + MySQL |
| Local API | `http://127.0.0.1:8000` |

### Demo Users (Local)
Run `python manage.py seed_demo_users` to generate:

| Persona | Email | Password | Landing |
|---|---|---|---|
| Conservative | `demo_conservative@finora.com` | `Finora@123` | `/dashboard` |
| Moderate | `demo_moderate@finora.com` | `Finora@123` | `/dashboard` |
| Aggressive | `kabir_growth@finora.com` | `Finora@123` | `/dashboard` |

---

## 4. Features & Deliverables

### Mandatory

| # | Feature | Status |
|---:|---|:---:|
| 01 | Email/password login & Google OAuth | ✅ |
| 02 | Financial Dashboard with live charts & KPI | ✅ |
| 03 | AI Assistant (Conversational Risk Profiling) | ✅ |
| 04 | Alternative Credit Engine (Digital Signals) | ✅ |
| 05 | Explainable AI Insights (XAI) | ✅ |
| 06 | Dynamic Wealth Simulator & CAGR charts | ✅ |
| 07 | Spending categorization & history | ✅ |

### Bonus

| # | Feature | Status |
|---:|---|:---:|
| B1 | Dark mode / Light mode toggle | ✅ |
| B2 | Gamified Financial Learning Module | ✅ |
| B3 | Automated Database Seeder for hackathon | ✅ |
| B4 | Interactive API Documentation (Swagger) | ✅ |

---

## 5. Technology Stack

<div align="center">
<img src="https://skillicons.dev/icons?i=py,django,mysql,js,html,css,github,figma&theme=dark" alt="Stack icons"/>
</div>

<br/>

<div align="center">

<img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django"/>
<img src="https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL"/>
<img src="https://img.shields.io/badge/Groq-LLaMA_3-FF9900?style=for-the-badge&logo=openai&logoColor=white" alt="Groq"/>
<img src="https://img.shields.io/badge/JavaScript-ES6-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JS"/>

</div>

---

## 6. Architecture

![Enterprise Cloud Architecture](backend/static/diagram-export-7-27-2026-12_18_14-AM.png)

---

## 7. Repository Structure

```text
backend/
├── accounts/           # User models, OAuth, Authentication API
├── ai_assistant/       # Groq integration, conversational logic
├── ai_memory/          # Event tracking, Explainable AI insights
├── config/             # Core Django settings & routing
├── core/               # Shared utilities, base models
├── credit_score/       # Scoring engine, signal modifiers
├── investment/         # Asset allocation, portfolio generation
├── learning/           # Quizzes, educational content
├── notifications/      # Real-time alerts, event subscriptions
├── onboarding/         # Initial user setup flows
├── reports/            # Financial reporting, AI Insights generator
├── risk_profile/       # Risk assessment scoring
├── static/             # Static assets (CSS, JS, Images)
├── templates/          # Frontend HTML rendering (Monolithic views)
├── transactions/       # Spending categorization, history
├── user_profile/       # Profile management, connected services
├── user_settings/      # User preferences
└── web/                # Base views for web frontend
```

---

## 8. Authentication

Authentication is handled securely via Django's Session framework for traditional email/password logins, alongside a Google OAuth provider integration. User profiles are tracked securely ensuring the AI and financial logic scopes all data directly to the authenticated session context.

---

## 9. Setup (Local)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/finora.git
   cd finora/backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables (.env):**
   ```env
   SECRET_KEY=your_django_secret
   DEBUG=True
   GROQ_API_KEY=your_groq_api_key
   DB_NAME=finora
   DB_USER=root
   DB_PASSWORD=your_password
   ```

5. **Run Migrations & Seed Data:**
   ```bash
   python manage.py migrate
   python manage.py seed_demo_users
   ```

6. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```
   *Navigate to `http://127.0.0.1:8000` in your browser.*

---

## 10. Screenshots

*(Replace the paths below with your actual screenshot images once added to the repository)*

1. **Landing Page:** `![Landing Page](backend/static/img/screenshots/landing.png)`
2. **Dashboard & AI Insights:** `![Dashboard](backend/static/img/screenshots/dashboard.png)`
3. **Credit Score Engine:** `![Credit Score](backend/static/img/screenshots/credit_score.png)`
4. **AI Risk Assessment Chat:** `![AI Chat](backend/static/img/screenshots/ai_chat.png)`
5. **Growth Simulator:** `![Simulator](backend/static/img/screenshots/simulator.png)`

---
<div align="center">
  <i>Built with ❤️ for the Hackathon</i>
</div>
