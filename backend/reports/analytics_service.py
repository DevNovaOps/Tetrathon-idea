from onboarding.models import UserProfile
from investment.models import InvestmentProfile
from risk_profile.models import RiskProfile

class AnalyticsService:
    @staticmethod
    def get_summary(user):
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return AnalyticsService._fallback_summary()

        income = float(profile.monthly_income or 0)
        expenses = float(profile.monthly_expenses or 0)
        savings = income - expenses

        try:
            inv_profile = InvestmentProfile.objects.get(user=user)
            investment_value = float(inv_profile.monthly_sip * 12 or 0)
        except InvestmentProfile.DoesNotExist:
            investment_value = 0.0

        try:
            risk_profile = RiskProfile.objects.get(user=user)
            risk_level = risk_profile.risk_bucket
        except RiskProfile.DoesNotExist:
            risk_level = "Unknown"

        # Mock derived standard metrics
        credit_score_change = "+18 pts"
        net_worth = (savings * 12) + investment_value
        savings_rate = (savings / income * 100) if income > 0 else 0
        expense_ratio = (expenses / income * 100) if income > 0 else 0
        emergency_fund_coverage = round((savings * 12) / expenses, 1) if expenses > 0 else 0

        return {
            "total_income": f"₹{income:,.0f}",
            "total_expenses": f"₹{expenses:,.0f}",
            "total_savings": f"₹{savings:,.0f}",
            "investment_value": f"₹{investment_value:,.0f}",
            "monthly_savings": f"₹{savings:,.0f}",
            "net_worth": f"₹{net_worth:,.0f}",
            "cash_flow": f"₹{savings:,.0f}",
            "savings_rate": f"{savings_rate:.1f}%",
            "expense_ratio": f"{expense_ratio:.1f}%",
            "emergency_fund_coverage": f"{emergency_fund_coverage} Months",
            "investment_growth": "+12%",
            "credit_score_change": credit_score_change,
            "risk_level": risk_level,
            
            # Raw values for other services
            "_raw": {
                "income": income,
                "expenses": expenses,
                "savings": savings,
                "investment_value": investment_value
            }
        }

    @staticmethod
    def get_performance(user):
        summary = AnalyticsService.get_summary(user)
        return {
            "savings_rate": summary["savings_rate"],
            "investment_growth": summary["investment_growth"],
            "credit_score_change": summary["credit_score_change"],
            "expense_reduction": "-6%",
            "emergency_fund_months": summary["emergency_fund_coverage"]
        }

    @staticmethod
    def _fallback_summary():
        return {
            "total_income": "₹0",
            "total_expenses": "₹0",
            "total_savings": "₹0",
            "investment_value": "₹0",
            "monthly_savings": "₹0",
            "net_worth": "₹0",
            "cash_flow": "₹0",
            "savings_rate": "0%",
            "expense_ratio": "0%",
            "emergency_fund_coverage": "0 Months",
            "investment_growth": "0%",
            "credit_score_change": "0 pts",
            "risk_level": "Unknown",
            "_raw": {"income": 0, "expenses": 0, "savings": 0, "investment_value": 0}
        }
