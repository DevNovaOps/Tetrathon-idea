from django.urls import path
from . import views

urlpatterns = [
    path('', views.FullReportView.as_view(), name='api-reports-full'),
    path('monthly/', views.MonthlyChartView.as_view(), name='api-reports-monthly'),
    path('expenses/', views.ExpensesChartView.as_view(), name='api-reports-expenses'),
    path('performance/', views.PerformanceView.as_view(), name='api-reports-performance'),
    path('insights/', views.InsightsView.as_view(), name='api-reports-insights'),
    path('history/', views.HistoryView.as_view(), name='api-reports-history'),
    path('export/', views.ExportView.as_view(), name='api-reports-export'),
]
