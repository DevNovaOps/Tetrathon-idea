"""
Financial Metrics Calculator.
Responsible strictly for calculating financial ratios and base metrics from UserProfile.
"""
from decimal import Decimal
from onboarding.models import UserProfile

class FinancialMetricsCalculator:
    """Calculates granular financial ratios and metrics for downstream use."""

    def __init__(self, profile: UserProfile):
        self.profile = profile
        self.income = profile.monthly_income or Decimal('0.00')
        self.expenses = profile.monthly_expenses or Decimal('0.00')
        self.savings = profile.savings or Decimal('0.00')
        self.investment = profile.monthly_investment_budget or Decimal('0.00')
        
        # Calculate derived raw numbers
        self.cash_flow = max(Decimal('0.00'), self.income - self.expenses)
        self.monthly_surplus = max(Decimal('0.00'), self.cash_flow - self.savings - self.investment)

    def calculate(self) -> dict:
        """Returns all calculated financial metrics."""
        
        income_float = float(self.income)
        expenses_float = float(self.expenses)
        
        # 1. Ratios (Clamped between 0.0 and 1.0 for percentages)
        if income_float > 0:
            raw_expense_ratio = expenses_float / income_float
            raw_savings_ratio = float(self.savings) / income_float
            raw_investment_ratio = float(self.investment) / income_float
            raw_cash_flow_ratio = float(self.cash_flow) / income_float
            
            expense_ratio = min(1.0, max(0.0, raw_expense_ratio))
            # Savings can exceed 100% of monthly income technically (cumulative), but for ratio we clamp
            # wait, 'savings' field in profile represents TOTAL savings, not monthly. 
            # So savings ratio shouldn't be clamped to 1.0, it represents "months of income saved".
            savings_ratio = max(0.0, raw_savings_ratio) 
            
            investment_ratio = min(1.0, max(0.0, raw_investment_ratio))
            cash_flow_ratio = min(1.0, max(0.0, raw_cash_flow_ratio))
            
            debt_ratio = self._estimate_debt_ratio(income_float)
        else:
            expense_ratio = 0.0
            savings_ratio = 0.0
            investment_ratio = 0.0
            cash_flow_ratio = 0.0
            debt_ratio = 0.0

        # 2. Coverage
        ef_coverage = self._estimate_emergency_fund_coverage()

        # 3. Base Score Mappings (0-100) for the Scoring Engine & Breakdowns
        scores = {
            "payment_behaviour": self._score_payment_behaviour(),
            "savings_habit": self._score_savings_habit(savings_ratio),
            "financial_stability": self._score_financial_stability(expense_ratio, ef_coverage),
            "investment_behaviour": self._score_investment_behaviour(investment_ratio),
            "upi_activity": self._score_upi_activity(),
            "utility_bills": self._score_utility_bills()
        }

        return {
            "raw": {
                "income": income_float,
                "expenses": expenses_float,
                "savings": float(self.savings),
                "investment": float(self.investment),
                "cash_flow": float(self.cash_flow),
                "monthly_surplus": float(self.monthly_surplus),
                "expense_ratio": expense_ratio,
                "savings_ratio": savings_ratio,
                "investment_ratio": investment_ratio,
                "debt_ratio": debt_ratio,
                "cash_flow_ratio": cash_flow_ratio,
                "emergency_fund_coverage": ef_coverage,
            },
            "scores": scores
        }

    # --- Internal Estimators ---
    def _estimate_debt_ratio(self, income: float) -> float:
        loans = self.profile.existing_loans
        if loans == 'None': return 0.0
        if loans == 'Personal Loan': return 0.20
        if loans in ['Home Loan', 'Car Loan']: return 0.40
        if loans == 'Multiple Loans': return 0.60
        return 0.0

    def _estimate_emergency_fund_coverage(self) -> int:
        fund = self.profile.emergency_fund
        if fund == 'More than 6 months of expenses': return 7
        if fund == '3-6 months of expenses': return 4
        if fund == 'Less than 3 months of expenses': return 2
        return 0

    # --- Sub-Scores (0-100) ---
    def _score_payment_behaviour(self) -> int:
        score = 50
        loans = self.profile.existing_loans
        if loans == 'None': score = 100
        elif loans == 'Personal Loan': score = 60
        elif loans in ['Home Loan', 'Car Loan']: score = 80
        elif loans == 'Multiple Loans': score = 30
        
        bills = self.profile.bill_payment_habit
        if bills == 'Always on time': score = min(100, score + 20)
        elif bills == 'Occasionally late': score = max(0, score - 20)
        elif bills == 'Frequently late': score = max(0, score - 40)
        return score

    def _score_savings_habit(self, savings_ratio: float) -> int:
        # If total savings is at least 3 months of income, score is 100.
        ideal = 3.0
        if savings_ratio <= 0: return 0
        return min(100, int((savings_ratio / ideal) * 100))

    def _score_financial_stability(self, expense_ratio: float, ef_coverage: int) -> int:
        score = 50
        if ef_coverage >= 6: score = 100
        elif ef_coverage >= 3: score = 80
        elif ef_coverage > 0: score = 40
        else: score = 10
        
        if expense_ratio > 0:
            if expense_ratio < 0.3: score = min(100, score + 10)
            elif expense_ratio > 0.8: score = max(0, score - 30)
        return score

    def _score_investment_behaviour(self, investment_ratio: float) -> int:
        score = 30
        exp = self.profile.investment_experience
        if exp == 'Advanced (Stocks, Crypto, etc.)': score = 100
        elif exp == 'Intermediate (Mutual Funds, FDs)': score = 80
        elif exp == 'Beginner (Just starting)': score = 50
        
        if investment_ratio > 0:
            score = min(100, score + 20)
        return score

    def _score_upi_activity(self) -> int:
        usage = self.profile.upi_usage
        if usage == 'Multiple times a day': return 95
        elif usage == 'Daily': return 85
        elif usage == 'Few times a week': return 60
        elif usage == 'Rarely': return 30
        return 0

    def _score_utility_bills(self) -> int:
        bills = self.profile.bill_payment_habit
        if bills == 'Always on time': return 95
        elif bills == 'Occasionally late': return 50
        elif bills == 'Frequently late': return 20
        return 0
