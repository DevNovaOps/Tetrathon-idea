from onboarding.models import UserProfile
from investment.models import InvestmentProfile
from risk_profile.models import RiskProfile
import datetime
import random

class AnalyticsService:
    @staticmethod
    def get_summary(user, month_str=None, year_str=None):
        try:
            profile = UserProfile.objects.get(user=user) if user else None
            base_income = float(profile.monthly_income) if (profile and profile.monthly_income) else 51000.0
            base_expenses = float(profile.monthly_expenses) if (profile and profile.monthly_expenses) else 9000.0
        except Exception:
            base_income = 51000.0
            base_expenses = 9000.0

        try:
            inv_profile = InvestmentProfile.objects.get(user=user)
            base_inv = float(inv_profile.monthly_sip * 12 or 30000)
        except InvestmentProfile.DoesNotExist:
            base_inv = 30000.0

        try:
            risk_profile = RiskProfile.objects.get(user=user)
            risk_level = risk_profile.risk_bucket
        except RiskProfile.DoesNotExist:
            risk_level = "Moderate"

        # Calculate target date for deterministic monthly variance
        try:
            target_year = int(year_str) if year_str else datetime.date.today().year
            target_month = int(month_str) if month_str else datetime.date.today().month
        except (ValueError, TypeError):
            target_year, target_month = datetime.date.today().year, datetime.date.today().month

        # Use deterministic random seed matching ChartService so summary numbers match chart bars exactly
        seed_str = f"{user.email if user else 'demo'}-{target_year}-{target_month}"
        random.seed(seed_str)

        inc_var = random.uniform(0.92, 1.08)
        exp_var = random.uniform(0.90, 1.15)

        income = round(base_income * inc_var)
        expenses = round(base_expenses * exp_var)
        savings = income - expenses

        # Let investment value vary and grow deterministically with month/year
        inv_seed = f"inv-{user.email if user else 'demo'}-{target_year}-{target_month}"
        random.seed(inv_seed)
        inv_var = random.uniform(0.96, 1.05)
        month_offset = (target_year - 2026) * 12 + (target_month - 6)
        investment_value = round(base_inv * (1 + month_offset * 0.015) * inv_var)
        if investment_value < 0:
            investment_value = round(base_inv)

        # Derived metrics for this specific month
        net_worth = round((savings * 12) + investment_value)
        savings_rate = (savings / income * 100) if income > 0 else 0
        expense_ratio = (expenses / income * 100) if income > 0 else 0
        emergency_fund_coverage = round((savings * 12) / expenses, 1) if expenses > 0 else 0

        # Deterministic monthly credit score and investment growth changes
        random.seed(f"perf-diff-{user.email if user else 'demo'}-{target_year}-{target_month}")
        inv_growth_val = round(random.uniform(8.5, 16.0), 1)
        credit_change_val = random.randint(10, 32)

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
            "investment_growth": f"+{inv_growth_val}%",
            "credit_score_change": f"+{credit_change_val} pts",
            "risk_level": risk_level,
            
            # Raw values for other services
            "_raw": {
                "income": income,
                "expenses": expenses,
                "savings": savings,
                "investment_value": investment_value,
                "base_expenses": base_expenses
            }
        }

    @staticmethod
    def get_performance(user, month_str=None, year_str=None):
        summary = AnalyticsService.get_summary(user, month_str, year_str)
        raw = summary["_raw"]

        try:
            target_year = int(year_str) if year_str else datetime.date.today().year
            target_month = int(month_str) if month_str else datetime.date.today().month
        except (ValueError, TypeError):
            target_year, target_month = datetime.date.today().year, datetime.date.today().month

        # Calculate dynamic expense reduction compared to base expenses
        base_exp = raw.get("base_expenses", 9000)
        exp_diff_pct = round(((raw["expenses"] - base_exp) / base_exp) * 100, 1) if base_exp > 0 else -6.0
        exp_red_str = f"{'+' if exp_diff_pct > 0 else ''}{exp_diff_pct}%" if exp_diff_pct != 0 else "-5.4%"

        return {
            "savings_rate": summary["savings_rate"],
            "investment_growth": summary["investment_growth"],
            "credit_score_change": summary["credit_score_change"],
            "expense_reduction": exp_red_str,
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
            "_raw": {"income": 0, "expenses": 0, "savings": 0, "investment_value": 0, "base_expenses": 0}
        }
