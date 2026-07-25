from django.urls import path
from .views import InvestmentPlanView

urlpatterns = [
    path('', InvestmentPlanView.as_view(), name='investment-plan'),
]
