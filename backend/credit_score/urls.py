"""
URLs for the Credit Score app.
"""
from django.urls import path
from .views import CreditScoreAPIView

app_name = 'credit_score'

urlpatterns = [
    path('', CreditScoreAPIView.as_view(), name='credit-score-main'),
]
