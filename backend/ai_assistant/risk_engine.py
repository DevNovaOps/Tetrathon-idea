"""
Deterministic Risk Scoring Engine.
The LLM NEVER decides risk. This engine uses weighted factors only.
"""
import re


def _parse_currency(value: str) -> int:
    """Extract a numeric value from a currency string like '₹25,000' or '50000'."""
    cleaned = re.sub(r'[^\d]', '', str(value))
    return int(cleaned) if cleaned else 0


class RiskEngine:
    """Calculates a deterministic risk score (0-100) from assessment answers."""

    @staticmethod
    def calculate(answers: dict) -> dict:
        """
        Takes a dict of {question_key: answer_string} and returns
        {"score": int, "level": str}.
        """
        score = 0

        # 1. Income level (0-15 points) — higher income = more capacity for risk
        income = _parse_currency(answers.get('monthly_income', '0'))
        if income >= 100000:
            score += 15
        elif income >= 50000:
            score += 12
        elif income >= 25000:
            score += 8
        else:
            score += 4

        # 2. Expense ratio (0-20 points) — lower ratio = more room for risk
        expenses = _parse_currency(answers.get('monthly_expenses', '0'))
        if income > 0:
            ratio = expenses / income
            if ratio <= 0.3:
                score += 20
            elif ratio <= 0.5:
                score += 15
            elif ratio <= 0.7:
                score += 8
            else:
                score += 3

        # 3. Savings rate (0-15 points)
        savings = _parse_currency(answers.get('current_savings', '0'))
        if income > 0:
            savings_rate = savings / income
            if savings_rate >= 0.30:
                score += 15
            elif savings_rate >= 0.20:
                score += 12
            elif savings_rate >= 0.10:
                score += 8
            else:
                score += 3

        # 4. Emergency fund (0-15 points)
        ef = answers.get('emergency_fund', '').lower()
        if ef == 'yes':
            score += 15
        elif ef == 'building one':
            score += 8
        else:
            score += 2

        # 5. Investment experience (0-15 points)
        exp = answers.get('investment_experience', '').lower()
        if exp == 'advanced':
            score += 15
        elif exp == 'intermediate':
            score += 12
        elif exp == 'beginner':
            score += 7
        else:
            score += 2

        # 6. Self-declared risk tolerance (0-20 points)
        tolerance = answers.get('risk_tolerance', '').lower()
        if tolerance == 'high':
            score += 20
        elif tolerance == 'moderate':
            score += 12
        else:
            score += 5

        # Clamp 0-100
        score = max(0, min(100, score))

        # Map to level
        if score <= 30:
            level = 'Low'
        elif score <= 70:
            level = 'Moderate'
        else:
            level = 'High'

        return {"score": score, "level": level}
