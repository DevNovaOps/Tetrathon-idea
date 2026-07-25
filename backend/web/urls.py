from django.views.generic import TemplateView
from django.urls import path

class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

class CreditScoreView(TemplateView):
    template_name = 'credit_score/credit-score.html'

class ImproveScoreView(TemplateView):
    template_name = 'improve_score/improve-score.html'

class AiAssistantView(TemplateView):
    template_name = 'ai_assistant/ai-assistant.html'

class RiskProfileView(TemplateView):
    template_name = 'risk_profile/risk-profile.html'

class InvestmentView(TemplateView):
    template_name = 'investment/investment.html'

class SimulatorView(TemplateView):
    template_name = 'growth_simulator/growth-simulator.html'

class ReportsView(TemplateView):
    template_name = 'reports/reports.html'

# Additional pages
class LandingView(TemplateView):
    template_name = 'landing/index.html'

class LoginView(TemplateView):
    template_name = 'auth/login.html'

class SignupView(TemplateView):
    template_name = 'auth/signup.html'

class ForgotPasswordView(TemplateView):
    template_name = 'auth/forgot-password.html'

class OnboardingView(TemplateView):
    template_name = 'onboarding/index.html'

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('onboarding/', OnboardingView.as_view(), name='onboarding'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('credit-score/', CreditScoreView.as_view(), name='credit-score'),
    path('improve-score/', ImproveScoreView.as_view(), name='improve-score'),
    path('ai-assistant/', AiAssistantView.as_view(), name='ai-assistant'),
    path('risk-profile/', RiskProfileView.as_view(), name='risk-profile'),
    path('investments/', InvestmentView.as_view(), name='investment'),
    path('simulator/', SimulatorView.as_view(), name='simulator'),
    path('reports/', ReportsView.as_view(), name='reports'),
]
