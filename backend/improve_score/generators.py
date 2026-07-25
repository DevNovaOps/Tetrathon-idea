from onboarding.models import UserProfile
from credit_score.metrics import FinancialMetricsCalculator
from .constants import *

class TaskGenerator:
    """Dynamic rule engine to generate personalized improvement tasks."""

    def __init__(self, profile: UserProfile):
        self.profile = profile
        self.metrics = FinancialMetricsCalculator(profile).calculate()
        self.raw = self.metrics.get('raw', {})

    def generate_tasks(self) -> list:
        tasks = []
        
        # Rule 1: Bill Payments
        if self.profile.bill_payment_habit in ['Frequently late', 'Occasionally late']:
            tasks.append({
                "title": "Avoid late utility bill payments",
                "description": "Enable auto-pay for electricity, internet, and water bills to maintain a 100% clean credit history.",
                "priority": TASK_PRIORITY_CRITICAL,
                "expected_points": 25,
                "difficulty": TASK_DIFFICULTY_EASY,
                "duration": "Immediate",
                "impact_type": "bills"
            })
            
        # Rule 2: Expense Ratio
        expense_ratio = self.raw.get('expense_ratio', 0)
        if expense_ratio > 0.60:
            tasks.append({
                "title": "Reduce discretionary spending",
                "description": "Cut non-essential dining and streaming subscriptions by 10% to improve disposable income buffer.",
                "priority": TASK_PRIORITY_MEDIUM if expense_ratio < 0.80 else TASK_PRIORITY_HIGH,
                "expected_points": 15,
                "difficulty": TASK_DIFFICULTY_MEDIUM,
                "duration": "45 Days",
                "impact_type": "expenses"
            })
            
        # Rule 3: Savings Rate
        savings_ratio = self.raw.get('savings_ratio', 0)
        income = self.raw.get('income', 0)
        # If savings < 2 months of income or monthly savings rate is low
        # Since we only have total savings, let's use savings_ratio (months of income saved)
        if savings_ratio < 2.0:
            target_monthly = int(income * 0.20) if income > 0 else 2000
            tasks.append({
                "title": f"Increase savings by ₹{target_monthly:,} monthly",
                "description": f"Automate ₹{target_monthly:,} monthly transfer to liquid savings to build a stronger financial buffer.",
                "priority": TASK_PRIORITY_HIGH,
                "expected_points": 20,
                "difficulty": TASK_DIFFICULTY_EASY,
                "duration": "30 Days",
                "impact_type": "savings"
            })
            
        # Rule 4: Emergency Fund
        ef_coverage = self.raw.get('emergency_fund_coverage', 0)
        if ef_coverage < 6:
            tasks.append({
                "title": "Build an emergency fund",
                "description": "Deposit funds monthly into high-yield savings to expand emergency liquidity coverage to 6 full months.",
                "priority": TASK_PRIORITY_HIGH,
                "expected_points": 12,
                "difficulty": TASK_DIFFICULTY_MEDIUM,
                "duration": "6 Months",
                "impact_type": "security"
            })
            
        # Rule 5: Investment
        investment_ratio = self.raw.get('investment_ratio', 0)
        if investment_ratio == 0:
            tasks.append({
                "title": "Start your first SIP",
                "description": "Begin investing a small amount monthly in Index Funds to kickstart wealth generation.",
                "priority": TASK_PRIORITY_MEDIUM,
                "expected_points": 10,
                "difficulty": TASK_DIFFICULTY_EASY,
                "duration": "14 Days",
                "impact_type": "investment"
            })
        elif investment_ratio < 0.15:
            tasks.append({
                "title": "Maintain monthly investments",
                "description": "Keep recurring mutual fund SIPs active without skipping cycles to demonstrate disciplined habits.",
                "priority": TASK_PRIORITY_LOW,
                "expected_points": 18,
                "difficulty": TASK_DIFFICULTY_MEDIUM,
                "duration": "90 Days",
                "impact_type": "investment"
            })
            
        # Rule 6: Debt / Credit Utilization
        loans = self.profile.existing_loans
        if loans in ['Personal Loan', 'Multiple Loans']:
            tasks.append({
                "title": "Reduce active loan burden",
                "description": "Target paying off high-interest personal loans to bring down overall credit utilization.",
                "priority": TASK_PRIORITY_CRITICAL,
                "expected_points": 30,
                "difficulty": TASK_DIFFICULTY_HARD,
                "duration": "6 Months",
                "impact_type": "debt"
            })

        # Ensure we always have at least 4 tasks for the roadmap
        if len(tasks) < 4:
            tasks.append({
                "title": "Review Credit Profile Regularly",
                "description": "Check your credit report monthly for inaccuracies.",
                "priority": TASK_PRIORITY_LOW,
                "expected_points": 5,
                "difficulty": TASK_DIFFICULTY_EASY,
                "duration": "Immediate",
                "impact_type": "review"
            })

        # Sorting logic: Highest impact, lowest effort, highest points
        priority_weights = {TASK_PRIORITY_CRITICAL: 4, TASK_PRIORITY_HIGH: 3, TASK_PRIORITY_MEDIUM: 2, TASK_PRIORITY_LOW: 1}
        difficulty_weights = {TASK_DIFFICULTY_EASY: 3, TASK_DIFFICULTY_MEDIUM: 2, TASK_DIFFICULTY_HARD: 1}
        
        for task in tasks:
            score = (priority_weights[task['priority']] * 10) + \
                    (difficulty_weights[task['difficulty']] * 5) + \
                    task['expected_points']
            task['sort_score'] = score
            
        sorted_tasks = sorted(tasks, key=lambda x: x['sort_score'], reverse=True)
        
        # Add order
        for idx, task in enumerate(sorted_tasks):
            task['order'] = idx + 1
            
        return sorted_tasks
