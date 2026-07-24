"""URLs for the dashboard API."""
from django.urls import path

from .views import DashboardAPIView

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardAPIView.as_view(), name='dashboard-main'),
]
