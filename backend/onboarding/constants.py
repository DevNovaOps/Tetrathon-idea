"""Constants for the onboarding app — choice tuples matching frontend selects."""

# ── Step 1: Personal Information ──────────────────────────────────────────

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Non-Binary', 'Non-Binary'),
    ('Prefer not to say', 'Prefer not to say'),
]

LANGUAGE_CHOICES = [
    ('English', 'English'),
    ('Hindi', 'Hindi'),
    ('Spanish', 'Spanish'),
    ('German', 'German'),
]

# ── Step 2: Financial Profile ─────────────────────────────────────────────

EXISTING_LOAN_CHOICES = [
    ('None', 'None'),
    ('Personal Loan', 'Personal Loan'),
    ('Education Loan', 'Education Loan'),
    ('Home Loan', 'Home Loan'),
]

UPI_USAGE_CHOICES = [
    ('Daily (15+ txns/wk)', 'Daily (15+ txns/wk)'),
    ('Moderate (5-15 txns/wk)', 'Moderate (5-15 txns/wk)'),
    ('Rare (1-5 txns/wk)', 'Rare (1-5 txns/wk)'),
]

BILL_PAYMENT_CHOICES = [
    ('Always On-Time', 'Always On-Time'),
    ('Occasionally Delayed', 'Occasionally Delayed'),
    ('Auto-Debit Enabled', 'Auto-Debit Enabled'),
]

# ── Step 3: Investment Profile ────────────────────────────────────────────

INVESTMENT_EXPERIENCE_CHOICES = [
    ('Beginner (< 1 yr)', 'Beginner (< 1 yr)'),
    ('Intermediate (1-3 yrs)', 'Intermediate (1-3 yrs)'),
    ('Advanced (3+ yrs)', 'Advanced (3+ yrs)'),
]

EMERGENCY_FUND_CHOICES = [
    ('Yes (6 Months Saved)', 'Yes (6 Months Saved)'),
    ('Yes (3 Months Saved)', 'Yes (3 Months Saved)'),
    ('Building Currently', 'Building Currently'),
    ('Not Yet', 'Not Yet'),
]

FINANCIAL_GOAL_CHOICES = [
    ('Wealth Accumulation', 'Wealth Accumulation & Growth'),
    ('Buying a House', 'Buying a House'),
    ('Retirement Fund', 'Early Retirement Fund'),
    ('Child Education', 'Education Fund'),
]

RISK_PREFERENCE_CHOICES = [
    ('Conservative (Low Risk)', 'Conservative (Low Risk)'),
    ('Moderate (Balanced)', 'Moderate (Balanced Portfolio)'),
    ('Aggressive (High Growth)', 'Aggressive (High Growth)'),
]

INVESTMENT_DURATION_CHOICES = [
    ('Short-Term (1-3 yrs)', 'Short-Term (1-3 yrs)'),
    ('Medium-Term (3-5 yrs)', 'Medium-Term (3-5 yrs)'),
    ('Long-Term (5+ Years)', 'Long-Term (5+ Years)'),
]

# ── Helpers ───────────────────────────────────────────────────────────────

def valid_values(choices: list) -> set:
    """Extract valid choice values from a choices list."""
    return {value for value, _ in choices}
