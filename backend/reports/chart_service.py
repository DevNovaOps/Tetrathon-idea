from .analytics_service import AnalyticsService
import datetime
import random

class ChartService:
    @staticmethod
    def get_monthly_chart_data(user, month_str=None, year_str=None):
        summary = AnalyticsService.get_summary(user, month_str, year_str)
        raw = summary["_raw"]
        
        base_income = raw["income"] or 50000
        base_expense = raw["expenses"] or 30000
        
        # Calculate target date for deterministic seed
        try:
            target_year = int(year_str) if year_str else datetime.date.today().year
            target_month = int(month_str) if month_str else datetime.date.today().month
        except (ValueError, TypeError):
            target_year, target_month = datetime.date.today().year, datetime.date.today().month

        labels = []
        income_data = []
        expense_data = []
        savings_data = []

        # Generate 7 months ending at target date deterministically
        for i in range(6, -1, -1):
            m = target_month - i
            y = target_year
            while m <= 0:
                m += 12
                y -= 1
            
            # Deterministic variance seed based on user email, year and month
            seed_str = f"{user.email if user else 'demo'}-{y}-{m}"
            random.seed(seed_str)
            
            inc_var = random.uniform(0.92, 1.08)
            exp_var = random.uniform(0.90, 1.15)
            
            inc = base_income * inc_var
            exp = base_expense * exp_var
            
            month_label = datetime.date(y, m, 1).strftime("%b")
            labels.append(month_label)
            income_data.append(round(inc))
            expense_data.append(round(exp))
            savings_data.append(round(inc - exp))

        return {
            "labels": labels,
            "datasets": [
                {
                    "label": "Income",
                    "data": [round(x) for x in income_data],
                    "backgroundColor": "#6366F1",
                },
                {
                    "label": "Expense",
                    "data": [round(x) for x in expense_data],
                    "backgroundColor": "#EF4444",
                },
                {
                    "label": "Savings",
                    "data": [round(x) for x in savings_data],
                    "backgroundColor": "#10B981",
                }
            ]
        }

    @staticmethod
    def get_expense_breakdown(user, month_str=None, year_str=None):
        summary = AnalyticsService.get_summary(user, month_str, year_str)
        expenses = summary["_raw"]["expenses"] or 30000
        
        try:
            target_year = int(year_str) if year_str else datetime.date.today().year
            target_month = int(month_str) if month_str else datetime.date.today().month
        except (ValueError, TypeError):
            target_year, target_month = datetime.date.today().year, datetime.date.today().month

        seed_str = f"exp-dist-{user.email if user else 'demo'}-{target_year}-{target_month}"
        random.seed(seed_str)
        
        base_dist = {
            "Housing": 35,
            "Food": 20,
            "Transport": 12,
            "Shopping": 10,
            "Entertainment": 8,
            "Utilities": 7,
            "Healthcare": 5,
            "Others": 3
        }
        
        # Vary category shares deterministically for this month
        raw_weights = {k: max(1, v + random.uniform(-4.5, 4.5)) for k, v in base_dist.items()}
        total_w = sum(raw_weights.values())
        
        labels = list(raw_weights.keys())
        data = [round(expenses * (w / total_w)) for w in raw_weights.values()]
        
        # Ensure exact sum matches total monthly expenses
        diff = expenses - sum(data)
        if data:
            data[0] += diff
        
        return {
            "labels": labels,
            "datasets": [{
                "data": data,
                "backgroundColor": ["#6366F1", "#10B981", "#3B82F6", "#F97316", "#A855F7", "#06B6D4", "#EF4444", "#64748B"]
            }]
        }
