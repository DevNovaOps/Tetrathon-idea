# Finora Backend

Django 5 + DRF backend for the Finora FinTech platform.
Implements **Module 2 (Authentication)** and **Module 3 (Multi-Step Onboarding)**.

---

## Quick Start

### Prerequisites

- Python 3.11+
- MySQL 8+
- Google OAuth 2.0 credentials (from Google Cloud Console)

### 1. Create MySQL Database

```sql
CREATE DATABASE finora_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
SECRET_KEY=your-random-secret-key
DEBUG=True
DB_NAME=finora_db
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_HOST=127.0.0.1
DB_PORT=3306
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py makemigrations accounts onboarding
python manage.py migrate
```

### 5. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 6. Setup Google OAuth (django-allauth)

After the first migration, add a Site and SocialApp via Django Admin:

```bash
python manage.py runserver
```

1. Go to `http://localhost:8000/admin/`
2. Under **Sites**, change `example.com` to `localhost:8000`
3. Under **Social applications**, add:
   - Provider: **Google**
   - Client ID: *(from Google Cloud Console)*
   - Secret Key: *(from Google Cloud Console)*
   - Sites: move `localhost:8000` to **Chosen sites**

Or use the settings-based configuration (already set in `settings.py` via `SOCIALACCOUNT_PROVIDERS`).

### 7. Start the Server

```bash
python manage.py runserver
```

Visit: `http://localhost:8000/`

---

## API Endpoints

### Authentication

| Method | Endpoint                              | Description                  |
|--------|---------------------------------------|------------------------------|
| POST   | `/api/auth/register/`                 | Create account & auto-login  |
| POST   | `/api/auth/login/`                    | Authenticate & create session|
| POST   | `/api/auth/logout/`                   | Destroy session              |
| GET    | `/api/auth/user/`                     | Get authenticated user data  |
| GET    | `/accounts/google/login/`             | Initiate Google OAuth flow   |
| GET    | `/accounts/google/login/callback/`    | Google OAuth callback        |

### Onboarding

| Method | Endpoint                    | Description                    |
|--------|-----------------------------|--------------------------------|
| POST   | `/api/onboarding/step1/`    | Save personal information      |
| POST   | `/api/onboarding/step2/`    | Save financial profile         |
| POST   | `/api/onboarding/step3/`    | Save investment profile        |
| GET    | `/api/onboarding/review/`   | Get all onboarding data        |
| POST   | `/api/onboarding/finish/`   | Complete onboarding            |

---

## Project Structure

```
backend/
├── config/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/            # Module 2: Authentication
│   ├── models.py        # Custom User model
│   ├── managers.py      # UserManager
│   ├── serializers.py   # Register/Login validation
│   ├── services.py      # Business logic
│   ├── views.py         # API views
│   ├── adapters.py      # Google OAuth adapters
│   ├── signals.py       # Auto-create UserProfile
│   ├── urls.py
│   └── admin.py
├── onboarding/          # Module 3: Multi-step Onboarding
│   ├── models.py        # UserProfile model
│   ├── serializers.py   # Step validation
│   ├── services.py      # Business logic
│   ├── views.py         # API views
│   ├── urls.py
│   └── admin.py
├── manage.py
├── requirements.txt
└── .env.example
```

---

## API Response Format

All APIs return consistent JSON:

```json
// Success
{
    "success": true,
    "message": "Step completed successfully.",
    "data": { ... }
}

// Validation Error
{
    "success": false,
    "errors": {
        "field_name": ["Error message."]
    }
}

// Server Error
{
    "success": false,
    "message": "Something went wrong."
}
```
