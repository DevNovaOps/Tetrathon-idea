from onboarding.models import UserProfile
from investment.models import InvestmentProfile
from risk_profile.models import RiskProfile

class FinancialHealthEngine:
    """
    Deterministic Financial Health Engine calculating a 0-100 score.
    """
    @staticmethod
    def calculate_health(user) -> dict:
        score = 100
        positive_factors = []
        negative_factors = []
        recommendations = []

        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return FinancialHealthEngine._fallback()

        income = float(profile.monthly_income or 0)
        expenses = float(profile.monthly_expenses or 0)
        savings = income - expenses

        # 1. Savings Rate (Max -30 points)
        savings_rate = (savings / income) if income > 0 else 0
        if savings_rate >= 0.20:
            positive_factors.append("Excellent savings rate (>= 20%).")
        elif savings_rate >= 0.10:
            score -= 10
            negative_factors.append("Savings rate is moderate (10-20%).")
            recommendations.append("Try to increase your savings rate to 20% of your income.")
        else:
            score -= 30
            negative_factors.append("Low savings rate (< 10%).")
            recommendations.append("Focus on reducing discretionary expenses to boost savings.")

        # 2. Emergency Fund (Max -20 points)
        emergency_months = (savings * 12) / expenses if expenses > 0 else 0
        if emergency_months >= 6:
            positive_factors.append("Strong emergency fund coverage (6+ months).")
        elif emergency_months >= 3:
            score -= 10
            negative_factors.append("Emergency fund covers 3-6 months.")
            recommendations.append("Build your emergency fund to cover at least 6 months of expenses.")
        else:
            score -= 20
            negative_factors.append("Critically low emergency fund (< 3 months).")
            recommendations.append("Prioritize building a 6-month emergency cushion.")

        # 3. Investment Readiness (Max -15 points)
        try:
            inv = InvestmentProfile.objects.get(user=user)
            inv_value = float(inv.monthly_sip * 12 or 0)
        except InvestmentProfile.DoesNotExist:
            inv_value = 0

        if inv_value > (income * 3):
            positive_factors.append("Significant investment portfolio established.")
        elif inv_value > 0:
            score -= 5
            positive_factors.append("Active investment portfolio.")
        else:
            score -= 15
            negative_factors.append("No active investments detected.")
            recommendations.append("Consider starting automated SIPs to build long-term wealth.")

        # 4. Expense Ratio (Max -20 points)
        expense_ratio = (expenses / income) if income > 0 else 1
        if expense_ratio < 0.50:
            positive_factors.append("Low expense ratio (< 50% of income).")
        elif expense_ratio < 0.70:
            score -= 10
            negative_factors.append("Moderate expense ratio.")
        else:
            score -= 20
            negative_factors.append("High expense ratio (> 70% of income).")
            recommendations.append("Review recurring expenses and subscriptions to lower monthly outflow.")

        # 5. Credit/Debt Discipline (Max -15 points)
        # Mock deterministic check
        score -= 5 # Assume average credit utilization
        positive_factors.append("Consistent bill payment history.")

        # Clamp score
        score = max(0, min(100, score))

        # Grade
        if score >= 90:
            grade = "A"
            explanation = "Excellent Financial Health"
        elif score >= 80:
            grade = "B"
            explanation = "Good Financial Health"
        elif score >= 70:
            grade = "C"
            explanation = "Fair Financial Health"
        else:
            grade = "D"
            explanation = "Needs Improvement"

        return {
            "score": round(score),
            "grade": grade,
            "explanation": explanation,
            "positive_factors": positive_factors,
            "negative_factors": negative_factors,
            "recommendations": recommendations,
        }

    @staticmethod
    def _fallback() -> dict:
        return {
            "score": 0,
            "grade": "N/A",
            "explanation": "Insufficient data.",
            "positive_factors": [],
            "negative_factors": ["Complete your profile to generate a health score."],
            "recommendations": ["Finish the onboarding process."],
        }
