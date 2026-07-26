from onboarding.models import UserProfile
from investment.models import InvestmentProfile
from risk_profile.models import RiskProfile
import datetime
import random

class FinancialHealthEngine:
    """
    Deterministic Financial Health Engine calculating a 0-100 score.
    """
    @staticmethod
    def calculate_health(user, month_str=None, year_str=None) -> dict:
        score = 100
        positive_factors = []
        negative_factors = []
        recommendations = []

        from .analytics_service import AnalyticsService
        summary = AnalyticsService.get_summary(user, month_str, year_str)
        raw = summary.get("_raw", {})

        income = float(raw.get("income", 0))
        expenses = float(raw.get("expenses", 0))
        savings = float(raw.get("savings", 0))
        base_expenses = float(raw.get("base_expenses", expenses or 9000))

        # 1. Savings Rate (Max -30 points)
        savings_rate = (savings / income) if income > 0 else 0
        if savings_rate >= 0.50:
            positive_factors.append(f"Exceptional savings rate ({round(savings_rate*100, 1)}%).")
        elif savings_rate >= 0.20:
            positive_factors.append(f"Strong savings rate ({round(savings_rate*100, 1)}%).")
        elif savings_rate >= 0.10:
            score -= 10
            negative_factors.append(f"Savings rate is moderate ({round(savings_rate*100, 1)}%).")
            recommendations.append("Try to increase your savings rate to 20% of your income.")
        else:
            score -= 30
            negative_factors.append(f"Low savings rate ({round(savings_rate*100, 1)}%).")
            recommendations.append("Focus on reducing discretionary expenses to boost savings.")

        # 2. Emergency Fund (Max -20 points)
        emergency_months = (savings * 12) / expenses if expenses > 0 else 0
        if emergency_months >= 6:
            positive_factors.append(f"Strong emergency fund coverage ({round(emergency_months, 1)} months).")
        elif emergency_months >= 3:
            score -= 10
            negative_factors.append(f"Emergency fund covers {round(emergency_months, 1)} months.")
            recommendations.append("Build your emergency fund to cover at least 6 months of expenses.")
        else:
            score -= 20
            negative_factors.append(f"Critically low emergency fund ({round(emergency_months, 1)} months).")
            recommendations.append("Prioritize building a 6-month emergency cushion.")

        # 3. Investment Readiness (Max -15 points)
        inv_value = float(raw.get("investment_value", 0))
        if inv_value > (income * 3):
            positive_factors.append("Significant investment portfolio established.")
        elif inv_value > 0:
            score -= 5
            positive_factors.append("Active investment portfolio.")
        else:
            score -= 15
            negative_factors.append("No active investments detected.")
            recommendations.append("Consider starting automated SIPs to build long-term wealth.")

        # 4. Expense Ratio & Monthly Control (Max -20 points)
        expense_ratio = (expenses / income) if income > 0 else 1
        if expense_ratio < 0.50:
            positive_factors.append(f"Low expense ratio ({round(expense_ratio*100, 1)}% of income).")
        elif expense_ratio < 0.70:
            score -= 10
            negative_factors.append(f"Moderate expense ratio ({round(expense_ratio*100, 1)}% of income).")
        else:
            score -= 20
            negative_factors.append(f"High expense ratio ({round(expense_ratio*100, 1)}% of income).")
            recommendations.append("Review recurring expenses and subscriptions to lower monthly outflow.")

        # 5. Monthly Spending vs Baseline & Deterministic Monthly Variation
        if base_expenses > 0 and expenses > base_expenses:
            diff_pct = round(((expenses - base_expenses) / base_expenses) * 100, 1)
            penalty = min(12, int(diff_pct * 0.8))
            score -= penalty
            if diff_pct > 2.0:
                negative_factors.append(f"Monthly spending exceeded baseline by {diff_pct}%.")
                recommendations.append("Track daily expenses to stay within your baseline budget.")
        elif base_expenses > 0 and expenses < base_expenses:
            diff_pct = round(((base_expenses - expenses) / base_expenses) * 100, 1)
            bonus = min(6, int(diff_pct * 0.5))
            score += bonus
            if diff_pct > 2.0:
                positive_factors.append(f"Monthly spending optimized {diff_pct}% below baseline.")

        # Deterministic monthly adjustment so score varies naturally across months
        try:
            target_year = int(year_str) if year_str else datetime.date.today().year
            target_month = int(month_str) if month_str else datetime.date.today().month
        except (ValueError, TypeError):
            target_year, target_month = datetime.date.today().year, datetime.date.today().month

        random.seed(f"health-var-{user.email if user else 'demo'}-{target_year}-{target_month}")
        month_adj = random.randint(-5, 4)
        score += month_adj

        # Clamp score
        score = max(0, min(100, round(score)))

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
            "score": score,
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
