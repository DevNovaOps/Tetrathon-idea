"""
Financial Metrics Calculator.
Maps UserProfile fields to normalized 0-100 scores.
"""
from decimal import Decimal
from onboarding.models import UserProfile
from .constants import IDEAL_SAVINGS_RATIO

class FinancialMetricsCalculator:
    """Calculates normalized 0-100 sub-scores for credit evaluation."""

    def __init__(self, profile: UserProfile):
        self.profile = profile
        self.income = profile.monthly_income or Decimal('0.00')
        self.expenses = profile.monthly_expenses or Decimal('0.00')
        self.savings = profile.savings or Decimal('0.00')
        
    def calculate_all(self) -> dict:
        """Returns a dictionary of all sub-metrics mapped 0-100."""
        return {
            "payment_behaviour": self._calc_payment_behaviour(),
            "savings_habit": self._calc_savings_habit(),
            "financial_stability": self._calc_financial_stability(),
            "investment_behaviour": self._calc_investment_behaviour(),
            "upi_activity": self._calc_upi_activity(),
            "utility_bills": self._calc_utility_bills()
        }
        
    def _calc_payment_behaviour(self) -> int:
        score = 50
        loans = self.profile.existing_loans
        if loans == 'None':
            score = 100
        elif loans == 'Personal Loan':
            score = 60
        elif loans in ['Home Loan', 'Car Loan']:
            score = 80 # Secured loans are better
        elif loans == 'Multiple Loans':
            score = 30
        
        # Factor in bill payments
        bills = self.profile.bill_payment_habit
        if bills == 'Always on time':
            score = min(100, score + 20)
        elif bills == 'Occasionally late':
            score = max(0, score - 20)
        elif bills == 'Frequently late':
            score = max(0, score - 40)
            
        return score

    def _calc_savings_habit(self) -> int:
        if self.income == 0:
            return 0
        ratio = float(self.savings / self.income)
        # 20% savings = 100 score
        score = min(100, int((ratio / IDEAL_SAVINGS_RATIO) * 100))
        return score

    def _calc_financial_stability(self) -> int:
        score = 50
        fund = self.profile.emergency_fund
        if fund == 'More than 6 months of expenses':
            score = 100
        elif fund == '3-6 months of expenses':
            score = 80
        elif fund == 'Less than 3 months of expenses':
            score = 40
        elif fund == 'None':
            score = 10
            
        # Modulate by expense ratio
        if self.income > 0:
            expense_ratio = float(self.expenses / self.income)
            if expense_ratio < 0.3:
                score = min(100, score + 10)
            elif expense_ratio > 0.8:
                score = max(0, score - 20)
                
        return score

    def _calc_investment_behaviour(self) -> int:
        score = 30
        exp = self.profile.investment_experience
        if exp == 'Advanced (Stocks, Crypto, etc.)':
            score = 100
        elif exp == 'Intermediate (Mutual Funds, FDs)':
            score = 80
        elif exp == 'Beginner (Just starting)':
            score = 50
            
        budget = self.profile.monthly_investment_budget or Decimal('0')
        if budget > 0:
            score = min(100, score + 20)
            
        return score

    def _calc_upi_activity(self) -> int:
        usage = self.profile.upi_usage
        if usage == 'Multiple times a day':
            return 95
        elif usage == 'Daily':
            return 85
        elif usage == 'Few times a week':
            return 60
        elif usage == 'Rarely':
            return 30
        return 0

    def _calc_utility_bills(self) -> int:
        bills = self.profile.bill_payment_habit
        if bills == 'Always on time':
            return 95
        elif bills == 'Occasionally late':
            return 50
        elif bills == 'Frequently late':
            return 20
        return 0
