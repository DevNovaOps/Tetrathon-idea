from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .report_service import ReportService
from .analytics_service import AnalyticsService
from .chart_service import ChartService
from .insight_service import InsightService
from .history_service import HistoryService
from .export_service import ExportService
from config.disclaimers import EDUCATIONAL_DISCLAIMER

class FullReportView(APIView):
    # Temporarily remove permission for testing/demo without login
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        # We use a dummy user for demo if request.user is anonymous
        user = request.user if request.user.is_authenticated else None
        month = request.query_params.get("month")
        year = request.query_params.get("year")
        
        data = ReportService.get_full_report(user, month, year)
        data['educational_disclaimer'] = EDUCATIONAL_DISCLAIMER
        return Response(data)

class MonthlyChartView(APIView):
    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        month = request.query_params.get("month")
        year = request.query_params.get("year")
        return Response(ChartService.get_monthly_chart_data(user, month, year))

class ExpensesChartView(APIView):
    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        month = request.query_params.get("month")
        year = request.query_params.get("year")
        return Response(ChartService.get_expense_breakdown(user, month, year))

class PerformanceView(APIView):
    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        month = request.query_params.get("month")
        year = request.query_params.get("year")
        return Response(AnalyticsService.get_performance(user, month, year))

class InsightsView(APIView):
    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        month = request.query_params.get("month")
        year = request.query_params.get("year")
        return Response(InsightService.get_insights(user, month, year))

class HistoryView(APIView):
    def get(self, request):
        return Response(HistoryService.get_available_months())

class ExportView(APIView):
    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        report_type = request.query_params.get("type", "monthly")
        month = request.query_params.get("month")
        year = request.query_params.get("year")
        return ExportService.generate_pdf(report_type, user, month, year)
