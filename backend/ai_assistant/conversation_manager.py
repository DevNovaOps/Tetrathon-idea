"""
Conversation Manager — defines the assessment questions, chips, and progression logic.
"""

ASSESSMENT_QUESTIONS = [
    {
        "key": "monthly_income",
        "question": "What is your approximate monthly income?",
        "topic": "monthly income",
        "chips": ["₹15,000", "₹25,000", "₹50,000", "₹1,00,000+"],
        "weight": 1.0,
    },
    {
        "key": "monthly_expenses",
        "question": "What are your average monthly expenses?",
        "topic": "monthly expenses",
        "chips": ["₹10,000", "₹15,000", "₹20,000", "₹30,000+"],
        "weight": 1.0,
    },
    {
        "key": "current_savings",
        "question": "How much do you currently save every month?",
        "topic": "current savings",
        "chips": ["₹2,000", "₹5,000", "₹10,000", "₹20,000+"],
        "weight": 1.0,
    },
    {
        "key": "emergency_fund",
        "question": "Do you have an emergency fund?",
        "topic": "emergency fund status",
        "chips": ["Yes", "No", "Building One"],
        "weight": 1.5,
    },
    {
        "key": "investment_experience",
        "question": "How would you describe your investment experience?",
        "topic": "investment experience",
        "chips": ["None", "Beginner", "Intermediate", "Advanced"],
        "weight": 1.2,
    },
    {
        "key": "risk_tolerance",
        "question": "How much investment risk are you comfortable with?",
        "topic": "risk tolerance",
        "chips": ["Low", "Moderate", "High"],
        "weight": 2.0,
    },
]

TOTAL_QUESTIONS = len(ASSESSMENT_QUESTIONS)


def get_question(step: int) -> dict | None:
    """Returns the question dict for the given step (0-indexed), or None if done."""
    if 0 <= step < TOTAL_QUESTIONS:
        return ASSESSMENT_QUESTIONS[step]
    return None


def get_progress(step: int) -> int:
    """Returns progress percentage (0-100)."""
    if TOTAL_QUESTIONS == 0:
        return 0
    return min(100, int((step / TOTAL_QUESTIONS) * 100))
