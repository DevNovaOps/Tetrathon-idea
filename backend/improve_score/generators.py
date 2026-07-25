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
                "description": "Enable auto-pay for electricity, internet, and water bills.",
                "reason": "Late bill payments severely damage your credit history and drop your score instantly.",
                "benefit": "Maintains a 100% clean payment history, signaling high reliability to lenders.",
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
                "description": "Cut non-essential dining and subscriptions by 10% this month.",
                "reason": f"Your current expense ratio ({int(expense_ratio * 100)}%) is too high, limiting wealth accumulation.",
                "benefit": "Improves your disposable income buffer and reduces financial stress.",
                "priority": TASK_PRIORITY_MEDIUM if expense_ratio < 0.80 else TASK_PRIORITY_HIGH,
                "expected_points": 15,
                "difficulty": TASK_DIFFICULTY_MEDIUM,
                "duration": "45 Days",
                "impact_type": "expenses"
            })
            
        # Rule 3: Savings Rate
        savings_ratio = self.raw.get('savings_ratio', 0)
        income = self.raw.get('income', 0)
        if savings_ratio < 2.0:
            target_monthly = int(income * 0.20) if income > 0 else 2000
            tasks.append({
                "title": f"Increase savings by ₹{target_monthly:,} monthly",
                "description": f"Automate a ₹{target_monthly:,} monthly transfer to your liquid savings account.",
                "reason": "Your current savings provide less than two months of runway.",
                "benefit": "Builds a stronger financial buffer to absorb unexpected shocks.",
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
                "description": "Deposit funds monthly into high-yield savings to expand liquidity.",
                "reason": "You currently lack a 6-month safety net.",
                "benefit": "Prevents the need for high-interest borrowing during emergencies.",
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
                "description": "Begin investing a small amount monthly in Index Funds.",
                "reason": "You currently have 0% of your income allocated to investments.",
                "benefit": "Kickstarts long-term compounding wealth generation.",
                "priority": TASK_PRIORITY_MEDIUM,
                "expected_points": 10,
                "difficulty": TASK_DIFFICULTY_EASY,
                "duration": "14 Days",
                "impact_type": "investment"
            })
        elif investment_ratio < 0.15:
            tasks.append({
                "title": "Maintain monthly investments",
                "description": "Keep recurring mutual fund SIPs active without skipping cycles.",
                "reason": "Consistent investing signals strong financial discipline.",
                "benefit": "Maximizes returns and steadily boosts your investment readiness score.",
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
                "description": "Target paying off high-interest personal loans aggressively.",
                "reason": "Multiple loans increase your debt-to-income ratio significantly.",
                "benefit": "Lowers your credit utilization and frees up monthly cash flow.",
                "priority": TASK_PRIORITY_CRITICAL,
                "expected_points": 30,
                "difficulty": TASK_DIFFICULTY_HARD,
                "duration": "6 Months",
                "impact_type": "debt"
            })

        # Ensure we always have at least 4 tasks
        if len(tasks) < 4:
            tasks.append({
                "title": "Review Credit Profile Regularly",
                "description": "Check your credit report monthly for inaccuracies.",
                "reason": "Errors in credit reports can drag down your score silently.",
                "benefit": "Ensures your profile accurately reflects your good habits.",
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
