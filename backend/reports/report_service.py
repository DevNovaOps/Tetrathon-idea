from .analytics_service import AnalyticsService
from .chart_service import ChartService
from .insight_service import InsightService
from .history_service import HistoryService
from .financial_health_engine import FinancialHealthEngine

class ReportService:
    @staticmethod
    def get_full_report(user, month=None, year=None):
        """
        Orchestrates the entire report payload for the frontend
        """
        summary = AnalyticsService.get_summary(user)
        
        return {
            "summary": {k: v for k, v in summary.items() if not k.startswith("_")},
            "performance": AnalyticsService.get_performance(user),
            "charts": {
                "monthly": ChartService.get_monthly_chart_data(user, month, year),
                "expenses": ChartService.get_expense_breakdown(user)
            },
            "insights": InsightService.get_insights(user),
            "health": FinancialHealthEngine.calculate_health(user),
            "available_months": HistoryService.get_available_months()
        }
