"""Constants for the accounts app."""

# ── Auth provider choices ──────────────────────────────────────────────────
AUTH_PROVIDER_EMAIL = 'email'
AUTH_PROVIDER_GOOGLE = 'google'

AUTH_PROVIDER_CHOICES = [
    (AUTH_PROVIDER_EMAIL, 'Email'),
    (AUTH_PROVIDER_GOOGLE, 'Google'),
]

# ── Supported countries ───────────────────────────────────────────────────
COUNTRY_CHOICES = [
    ('IN', 'India'),
    ('US', 'United States'),
    ('UK', 'United Kingdom'),
    ('AE', 'United Arab Emirates'),
]

VALID_COUNTRY_CODES = {code for code, _ in COUNTRY_CHOICES}

# ── Password rules ────────────────────────────────────────────────────────
PASSWORD_MIN_LENGTH = 8
PASSWORD_RULES_MESSAGE = (
    'Password must be at least 8 characters and include an uppercase letter, '
    'a lowercase letter, a digit, and a special character.'
)
