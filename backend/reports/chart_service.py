from .analytics_service import AnalyticsService

class ChartService:
    @staticmethod
    def get_monthly_chart_data(user, month=None, year=None):
        # We simulate 7 months of data ending at the requested month/year
        # based on their current income/expense to provide a realistic looking chart
        summary = AnalyticsService.get_summary(user)
        raw = summary["_raw"]
        
        base_income = raw["income"] or 50000
        base_expense = raw["expenses"] or 30000
        
        # Simulated variances for the last 7 months
        income_data = [base_income * var for var in [0.95, 1.0, 0.98, 1.02, 1.0, 1.05, 1.0]]
        expense_data = [base_expense * var for var in [1.02, 1.0, 0.95, 0.98, 1.05, 0.98, 1.0]]
        savings_data = [i - e for i, e in zip(income_data, expense_data)]
        
        return {
            "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
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
    def get_expense_breakdown(user):
        summary = AnalyticsService.get_summary(user)
        expenses = summary["_raw"]["expenses"] or 30000
        
        # Simulated distribution of expenses
        distribution = {
            "Housing": 0.35,
            "Food": 0.20,
            "Transport": 0.12,
            "Shopping": 0.10,
            "Entertainment": 0.08,
            "Utilities": 0.07,
            "Healthcare": 0.05,
            "Others": 0.03
        }
        
        labels = list(distribution.keys())
        data = [round(expenses * dist) for dist in distribution.values()]
        
        return {
            "labels": labels,
            "datasets": [{
                "data": data,
                "backgroundColor": ["#6366F1", "#10B981", "#3B82F6", "#F97316", "#A855F7", "#06B6D4", "#EF4444", "#64748B"]
            }]
        }
