"""
Explanation Generator.
Generates dynamic positive factors, negative factors, and AI explanations
derived directly from the UserProfile metrics.
"""
from decimal import Decimal
from onboarding.models import UserProfile
from .constants import IDEAL_SAVINGS_RATIO, IDEAL_EXPENSE_RATIO_MAX

class ExplanationGenerator:
    """Generates text explanations based on raw profile data."""

    def __init__(self, profile: UserProfile, metrics: dict):
        self.profile = profile
        self.metrics = metrics
        self.income = profile.monthly_income or Decimal('0.00')
        self.expenses = profile.monthly_expenses or Decimal('0.00')
        self.savings = profile.savings or Decimal('0.00')
        
    def generate_all(self) -> dict:
        return {
            "positive_factors": self._get_positive_factors(),
            "negative_factors": self._get_negative_factors(),
            "ai_explanations": self._get_ai_explanations(),
            "recommendations": self._get_recommendations()
        }
        
    def _get_positive_factors(self) -> list:
        factors = []
        
        if self.profile.bill_payment_habit == 'Always on time':
            factors.append({
                "name": "On-time Utility Bill Payments",
                "impact_text": "High Impact",
                "badge_color": "green"
            })
            
        if self.profile.existing_loans == 'None':
            factors.append({
                "name": "Zero Active Debt",
                "impact_text": "High Impact",
                "badge_color": "green"
            })
            
        if self.profile.upi_usage in ['Daily', 'Multiple times a day']:
            factors.append({
                "name": "Active Digital Footprint",
                "impact_text": "Medium",
                "badge_color": "blue"
            })
            
        if self.income > 0 and (self.savings / self.income) >= Decimal(str(IDEAL_SAVINGS_RATIO)):
            factors.append({
                "name": "Consistent Savings Habit",
                "impact_text": "High Impact",
                "badge_color": "green"
            })
            
        return factors

    def _get_negative_factors(self) -> list:
        factors = []
        
        if self.profile.bill_payment_habit == 'Frequently late':
            factors.append({
                "name": "Late Bill Payments",
                "impact_text": "Reduce",
                "badge_color": "orange"
            })
            
        if self.profile.existing_loans == 'Multiple Loans':
            factors.append({
                "name": "High Debt Burden",
                "impact_text": "High Impact",
                "badge_color": "orange"
            })
            
        if self.profile.emergency_fund in ['None', 'Less than 3 months of expenses']:
            factors.append({
                "name": "Low Emergency Fund",
                "impact_text": "Build Up",
                "badge_color": "orange"
            })
            
        if self.income > 0 and (self.expenses / self.income) > Decimal(str(IDEAL_EXPENSE_RATIO_MAX)):
            factors.append({
                "name": "High Expense Ratio",
                "impact_text": "Reduce",
                "badge_color": "orange"
            })
            
        return factors

    def _get_ai_explanations(self) -> list:
        explanations = []
        
        # 1. Bill Payments
        if self.profile.bill_payment_habit == 'Always on time':
            explanations.append({
                "title": "Your score benefits from flawless utility payments.",
                "desc": "A 100% on-time payment record across bills signals strong reliability to the scoring engine.",
                "icon_color": "green",
                "icon_type": "check"
            })
        else:
            explanations.append({
                "title": "Late payments are impacting your score.",
                "desc": "Frequent late payments signal liquidity risk. Automating payments could prevent point deductions.",
                "icon_color": "orange",
                "icon_type": "alert"
            })
            
        # 2. Savings Ratio
        if self.income > 0:
            ratio = float(self.savings / self.income) * 100
            if ratio >= IDEAL_SAVINGS_RATIO * 100:
                explanations.append({
                    "title": "Strong savings behaviour detected.",
                    "desc": f"Your monthly savings rate is {ratio:.1f}%, which meets the optimal 20% benchmark recommended for financial health.",
                    "icon_color": "blue",
                    "icon_type": "sparkle"
                })
            else:
                explanations.append({
                    "title": "Increasing savings can boost your score.",
                    "desc": f"Your savings rate of {ratio:.1f}% is below the 20% target. Diverting more funds to savings adds up to 15 points.",
                    "icon_color": "orange",
                    "icon_type": "alert"
                })
                
        # 3. Emergency Fund
        if self.profile.emergency_fund in ['3-6 months of expenses', 'More than 6 months of expenses']:
            explanations.append({
                "title": "Your emergency fund provides solid financial stability.",
                "desc": "Having adequate runway prevents reliance on high-interest credit during unexpected events.",
                "icon_color": "purple",
                "icon_type": "shield"
            })
            
        # 4. Investment
        budget = self.profile.monthly_investment_budget or Decimal('0')
        if budget > 0:
            explanations.append({
                "title": "Maintaining investments improves long-term stability.",
                "desc": f"Consistent monthly investments of ₹{budget:,.0f} signals financial discipline to AI scoring models.",
                "icon_color": "cyan",
                "icon_type": "trend"
            })

        return explanations

    def _get_recommendations(self) -> list:
        # For the frontend quick insights mini cards
        # Return a dict containing: risk_level, score_category, top_strength, improvement_opportunity
        
        sorted_metrics = sorted(self.metrics.items(), key=lambda x: x[1], reverse=True)
        top_strength_key = sorted_metrics[0][0]
        improvement_key = sorted_metrics[-1][0]
        
        key_to_name = {
            "payment_behaviour": "Debt Mgmt",
            "savings_habit": "Savings",
            "financial_stability": "Stability",
            "investment_behaviour": "Investments",
            "upi_activity": "UPI Usage",
            "utility_bills": "Bill Payments"
        }
        
        return {
            "top_strength": key_to_name.get(top_strength_key, "General"),
            "improvement_opportunity": key_to_name.get(improvement_key, "None")
        }
