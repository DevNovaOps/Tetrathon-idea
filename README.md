<div align="center">
  <img src="backend/static/img/finora-banner.png" alt="Finora Banner" width="100%" />
</div>

<br>

<p align="center">
  <code>Transparent AI Credit Intelligence</code> &nbsp;•&nbsp;
  <code>Explainable Wealth Generation</code> &nbsp;•&nbsp;
  <code>Alternative Digital Signals</code>
</p>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/💻_UI_PREVIEW-FINORA.VERCEL.APP-6366F1?style=for-the-badge" alt="Preview" /></a>
  <a href="#"><img src="https://img.shields.io/badge/✏️_MOCKUP-FIGMA-00C4CC?style=for-the-badge" alt="Figma" /></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FinTech_Hackathon-24_Hours-F97316?style=for-the-badge" alt="Hackathon" />
  <img src="https://img.shields.io/badge/Status-Live_Preview_on_Vercel-10B981?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/RBAC-3_Roles-8B5CF6?style=for-the-badge" alt="Roles" />
  <img src="https://img.shields.io/badge/DB-Local_MySQL_Only-475569?style=for-the-badge" alt="DB" />
  <img src="https://img.shields.io/badge/Frontend-Vanilla_JS_+_CSS-3B82F6?style=for-the-badge" alt="Frontend" />
  <br>
  <img src="https://img.shields.io/badge/API-Django_REST-092E20?style=for-the-badge" alt="API" />
  <img src="https://img.shields.io/badge/AI-Groq_LLaMA_3-FF9900?style=for-the-badge" alt="AI" />
  <img src="https://img.shields.io/badge/UI_Hosted-Vercel-000000?style=for-the-badge" alt="Hosting" />
</p>

---

## 🛠️ Technology Stack

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=py,django,mysql,js,html,css,github,figma" alt="Skill Icons" />
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/PYTHON-3.11-09090B?style=for-the-badge&logo=python&logoColor=3776AB&labelColor=27272A" alt="Python" />
  <img src="https://img.shields.io/badge/DJANGO-5.0-09090B?style=for-the-badge&logo=django&logoColor=092E20&labelColor=27272A" alt="Django" />
  <img src="https://img.shields.io/badge/MYSQL-8.0-09090B?style=for-the-badge&logo=mysql&logoColor=4479A1&labelColor=27272A" alt="MySQL" />
  <img src="https://img.shields.io/badge/GROQ-LLaMA_3-09090B?style=for-the-badge&logo=openai&logoColor=FF9900&labelColor=27272A" alt="Groq" />
  <img src="https://img.shields.io/badge/JAVASCRIPT-ES6-09090B?style=for-the-badge&logo=javascript&logoColor=F7DF1E&labelColor=27272A" alt="JS" />
</p>

---

## 🚀 Problem Statement Mapping

**The Challenge:** Traditional credit scoring relies heavily on historical repayment data, excluding millions of "thin-file" or "new-to-credit" users. Furthermore, financial planning tools are often static, offering generic advice rather than personalized, dynamic insights.

**The Finora Solution:**
1. **Alternative Credit Engine:** Ingests non-traditional digital signals (utility bills, OTT subscriptions, UPI transaction behaviors, e-commerce velocity) to generate a holistic, alternative Credit Score.
2. **Explainable AI (XAI):** Moves beyond the "black box" by generating human-readable AI memories that transparently explain *why* a score changed and exactly *what* to do next.
3. **Hyper-Personalized Wealth Management:** Dynamically allocates investment portfolios (Aggressive, Moderate, Conservative) based on continuous behavioral analysis and dynamic risk profiling.

---

## 💎 Key Features

| Feature | Description |
| :--- | :--- |
| **🤖 AI Financial Assistant** | An interactive, conversational LLaMA-3 powered advisor that dynamically assesses risk tolerance and gathers financial goals. |
| **📊 Intelligent Credit Engine** | Processes alternative digital signals alongside traditional inputs to create an inclusive credit score with dynamic modifiers. |
| **🧠 Explainable AI Memory** | An event-driven architecture that tracks financial milestones (e.g., "Paid 3 utility bills on time") and translates them into transparent insights. |
| **📈 Dynamic Wealth Simulator** | Projects portfolio growth using CAGR calculations across different risk scenarios to optimize asset allocation. |
| **🎮 Gamified Learning** | A financial literacy module featuring interactive quizzes, progressive learning tracks, and XP-based achievements. |
| **🔐 Enterprise-Grade Security** | Built on Django 5 with session-based authentication, Google OAuth integration, and secure RESTful endpoints. |

---

## 🏗️ Architecture & Workflows

### 1. Overall System Architecture
*(Save your Eraser Enterprise Cloud Architecture export as `backend/static/img/architecture.png` to display it here)*
![Overall System Architecture](backend/static/img/architecture.png)

### 2. AI Decision Pipeline
```mermaid
graph TD
    A[User Input / Transactions] --> B{AI Data Aggregator}
    B --> C[Risk Profile Engine]
    B --> D[Credit Score Engine]
    C --> E[Groq LLaMA-3 Inference]
    D --> E
    E --> F[Explainable AI Insights]
    E --> G[Investment Allocation Engine]
    F --> H((Frontend Dashboard))
    G --> H
```

### 3. Credit Score Engine Architecture
```mermaid
flowchart LR
    subgraph Data Sources
        T[UPI Transactions]
        O[OTT / Utility Bills]
        E[E-commerce Velocity]
    end
    
    subgraph Credit Engine
        FE[Feature Extraction]
        WT[Weighting Matrix]
        BM[Baseline Calculation]
    end
    
    T --> FE
    O --> FE
    E --> FE
    FE --> WT
    WT --> BM
    BM --> CS((Final Credit Score))
```

### 4. Risk Assessment Workflow
```mermaid
sequenceDiagram
    participant User
    participant AIAssistant
    participant RiskEngine
    participant Database

    User->>AIAssistant: Provides financial goals & demographics
    AIAssistant->>RiskEngine: Submits structured JSON profile
    RiskEngine->>RiskEngine: Calculates Risk Score (0-100)
    RiskEngine->>RiskEngine: Categorizes (Conservative, Moderate, Aggressive)
    RiskEngine->>Database: Persists Risk Profile
    RiskEngine-->>AIAssistant: Triggers Portfolio Allocation
    AIAssistant-->>User: Presents customized investment strategy
```

### 5. Event-Driven Architecture (AI Memory)
```mermaid
graph TD
    E1[Bill Payment] -->|Signal| EB(Event Bus / Signals)
    E2[Quiz Completed] -->|Signal| EB
    E3[Profile Update] -->|Signal| EB
    
    EB -->|Dispatch| M[Memory Service]
    M -->|Create| DB[(AI Memory DB)]
    
    DB -->|Fetch| XAI[Explainability Engine]
    XAI -->|Generate Insights| UI[User Interface]
```

### 6. Database ER Architecture (Core)
```mermaid
erDiagram
    USER ||--o{ CREDIT_SCORE : has
    USER ||--o{ RISK_PROFILE : has
    USER ||--o{ TRANSACTIONS : executes
    USER ||--o{ AI_MEMORY : triggers
    
    CREDIT_SCORE {
        int base_score
        int digital_signal_modifier
        datetime last_updated
    }
    RISK_PROFILE {
        int score
        string risk_bucket
    }
    TRANSACTIONS {
        decimal amount
        string category
        string type
    }
    AI_MEMORY {
        string memory_type
        text summary
    }
```

### 7. REST API Request Flow
```mermaid
graph LR
    Client([Frontend App]) -->|HTTPS Request| N[Nginx / Web Server]
    N -->|WSGI| D[Django Router]
    D -->|Auth Check| M[Middleware]
    M -->|Valid Session| V[API View]
    V --> S[Service Layer]
    S --> DB[(MySQL)]
    DB --> S
    S --> V
    V -->|JSON Response| Client
```

### 8. Project Service Architecture
```text
finora/
├── backend/
│   ├── accounts/           # User models, OAuth, Authentication API
│   ├── ai_assistant/       # Groq integration, conversational logic
│   ├── ai_memory/          # Event tracking, Explainable AI insights
│   ├── credit_score/       # Scoring engine, signal modifiers
│   ├── digital_signals/    # Alternative data ingestion (UPI, OTT)
│   ├── growth_simulator/   # CAGR projections, wealth algorithms
│   ├── investment/         # Asset allocation, portfolio generation
│   ├── learning/           # Quizzes, educational content
│   ├── risk_profile/       # Risk assessment scoring
│   ├── transactions/       # Spending categorization, history
│   ├── web/                # Frontend template rendering (Monolithic views)
│   └── config/             # Core Django settings & routing
└── (Add your frontend/mobile folders here for full-stack expansion)
```

---

## 📸 Screenshots

*(Replace the paths below with your actual screenshot images once added to the repository)*

1. **Landing Page:** `![Landing Page](backend/static/img/screenshots/landing.png)`
2. **Dashboard & AI Insights:** `![Dashboard](backend/static/img/screenshots/dashboard.png)`
3. **Credit Score Engine:** `![Credit Score](backend/static/img/screenshots/credit_score.png)`
4. **AI Risk Assessment Chat:** `![AI Chat](backend/static/img/screenshots/ai_chat.png)`
5. **Growth Simulator:** `![Simulator](backend/static/img/screenshots/simulator.png)`

---

## ⚙️ Installation & Usage

### Prerequisites
- Python 3.11+
- MySQL 8.0+
- Groq API Key

### Setup Instructions

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

4. **Environment Variables:**
   Create a `.env` file in the `backend/` directory:
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
   python manage.py seed_demo_users  # Seeds database with rich presentation data
   ```

6. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```
   *Navigate to `http://127.0.0.1:8000` in your browser.*

---

## 📖 API Documentation

Finora follows a strictly separated Service Layer Architecture. Key API endpoints:

- **Authentication:** 
  - `POST /api/auth/login/`
  - `POST /api/auth/register/`
- **Dashboard & Core:**
  - `GET /api/dashboard/summary/`
  - `GET /api/credit-score/`
- **AI & Analytics:**
  - `POST /api/assistant/chat/`
  - `GET /api/reports/insights/`
- **Alternative Signals:**
  - `POST /api/signals/ingest/`

*(A fully interactive Swagger/OpenAPI documentation is available at `/api/docs/` when running locally)*

---

## 🛣️ Roadmap

- [x] **Phase 1:** Core Authentication, Dashboard, and Traditional Financial Tracking.
- [x] **Phase 2:** Integration of Groq LLaMA-3 for Conversational Risk Assessment.
- [x] **Phase 3:** Alternative Credit Engine (Digital Signals) and Explainable AI (XAI) Memory.
- [ ] **Phase 4:** Plaid / Account Aggregator Integration for live bank transaction syncing.
- [ ] **Phase 5:** Mobile Application rollout using React Native.
- [ ] **Phase 6:** Predictive Default Modeling using XGBoost on historical transaction data.

---

## 🔮 Future Scope
As Finora scales, the vision expands into a comprehensive **B2B2C ecosystem**. By white-labeling our Alternative Credit Engine APIs, traditional banks and NBFCs can leverage Finora's AI to underwrite previously "unscorable" individuals. Furthermore, integration with decentralized finance (DeFi) protocols could allow users to seamlessly stake savings directly from the growth simulator.

---
<div align="center">
  <i>Built with ❤️ for the Hackathon</i>
</div>
