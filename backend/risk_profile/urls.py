from django.urls import path
from .views import RiskProfileView

urlpatterns = [
    path('', RiskProfileView.as_view(), name='risk_profile_api'),
]
