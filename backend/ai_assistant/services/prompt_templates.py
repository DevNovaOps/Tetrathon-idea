# Hardcoded Questions sequence
QUESTIONS = [
    {
        "key": "monthly_income",
        "question": "What is your monthly income?",
        "choices": ["\u20b915,000", "\u20b925,000", "\u20b950,000", "\u20b91,00,000+"]
    },
    {
        "key": "monthly_expenses",
        "question": "What are your monthly expenses?",
        "choices": ["\u20b910,000", "\u20b915,000", "\u20b920,000", "\u20b930,000+"]
    },
    {
        "key": "current_savings",
        "question": "How much do you currently save every month?",
        "choices": ["\u20b92,000", "\u20b95,000", "\u20b910,000", "\u20b920,000+"]
    },
    {
        "key": "emergency_fund",
        "question": "Do you have an emergency fund?",
        "choices": ["Yes", "No", "Building One"]
    },
    {
        "key": "investment_experience",
        "question": "How much investment experience do you have?",
        "choices": ["None", "Beginner", "Intermediate", "Advanced"]
    },
    {
        "key": "primary_goal",
        "question": "What is your primary financial goal?",
        "choices": ["Wealth Creation", "Retirement", "Buying a House", "Debt Payoff"]
    },
    {
        "key": "risk_tolerance",
        "question": "How much investment risk are you comfortable taking?",
        "choices": ["Low", "Moderate", "High"]
    }
]

def get_system_prompt() -> str:
    return (
        "You are Finora, a professional, friendly, and expert AI Financial Advisor. "
        "Do not mention you are an AI or language model. "
        "Your goal is to transition smoothly between questions in a financial assessment."
    )

def generate_transition_prompt(previous_answer: str, next_question: str) -> str:
    return (
        f"The user just answered: '{previous_answer}'. "
        f"Generate a very brief (1-2 short sentences) natural, friendly transition acknowledging their answer, "
        f"and then explicitly ask the following exact question: '{next_question}'."
    )
