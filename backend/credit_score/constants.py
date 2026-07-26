"""
Constants for the Credit Score Module.
Contains all configurable weights, risk tiers, and baseline metrics to keep the business logic clean.
"""

# Score Bounds
MIN_SCORE = 300
MAX_SCORE = 900

# Risk Levels & Grades
RISK_LEVELS = [
    {"min": 300, "max": 549, "level": "High Risk", "grade": "Poor", "category": "Poor"},
    {"min": 550, "max": 649, "level": "Medium Risk", "grade": "Fair", "category": "Fair"},
    {"min": 650, "max": 749, "level": "Low Risk", "grade": "Good", "category": "Good"},
    {"min": 750, "max": 849, "level": "Very Low Risk", "grade": "Very Good", "category": "Very Good"},
    {"min": 850, "max": 900, "level": "Excellent Risk", "grade": "Excellent", "category": "Excellent"},
]

# Weights for Sub-metrics
# These MUST add up to 1.0 (100%)
METRIC_WEIGHTS = {
    "payment_behaviour": 0.22,
    "savings_habit": 0.18,
    "financial_stability": 0.18,
    "investment_behaviour": 0.13,
    "upi_activity": 0.08,
    "utility_bills": 0.09,
    "digital_signals": 0.12,
}

# Feature Importance Display Order
FEATURE_LABELS = {
    "payment_behaviour": "Debt Management",
    "savings_habit": "Savings",
    "financial_stability": "Income Stability",
    "investment_behaviour": "Investment Behaviour",
    "upi_activity": "UPI Usage",
    "utility_bills": "Electricity Bills",
    "digital_signals": "Digital Footprint"
}

# Ideal Thresholds for Explanations
IDEAL_SAVINGS_RATIO = 0.20
IDEAL_EXPENSE_RATIO_MAX = 0.50
