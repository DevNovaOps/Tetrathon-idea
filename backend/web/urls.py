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

# Sidebar pages
class EducationView(TemplateView):
    template_name = 'education/education.html'

class AchievementsView(TemplateView):
    template_name = 'achievements/achievements.html'

class NotificationsView(TemplateView):
    template_name = 'notifications/notifications.html'

class ProfileView(TemplateView):
    template_name = 'profile/profile.html'

class SettingsView(TemplateView):
    template_name = 'settings/settings.html'

# Footer Subpages
class CareersView(TemplateView):
    template_name = 'pages/careers.html'

class PressView(TemplateView):
    template_name = 'pages/press.html'

class ContactView(TemplateView):
    template_name = 'pages/contact.html'

class BlogView(TemplateView):
    template_name = 'pages/blog.html'

class DocsView(TemplateView):
    template_name = 'pages/docs.html'

class HelpView(TemplateView):
    template_name = 'pages/help.html'

class CommunityView(TemplateView):
    template_name = 'pages/community.html'

class StatusView(TemplateView):
    template_name = 'pages/status.html'

class SecurityView(TemplateView):
    template_name = 'pages/security.html'

class PrivacyView(TemplateView):
    template_name = 'pages/privacy.html'

class TermsView(TemplateView):
    template_name = 'pages/terms.html'

class CookiesView(TemplateView):
    template_name = 'pages/cookies.html'

class ComplianceView(TemplateView):
    template_name = 'pages/compliance.html'

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
    path('learn/', EducationView.as_view(), name='learn'),
    path('achievements/', AchievementsView.as_view(), name='achievements'),
    path('notifications/', NotificationsView.as_view(), name='notifications'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('settings/', SettingsView.as_view(), name='settings'),

    # Footer Subpage URLs
    path('careers/', CareersView.as_view(), name='careers'),
    path('press/', PressView.as_view(), name='press'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('docs/', DocsView.as_view(), name='docs'),
    path('help/', HelpView.as_view(), name='help'),
    path('community/', CommunityView.as_view(), name='community'),
    path('status/', StatusView.as_view(), name='status'),
    path('security/', SecurityView.as_view(), name='security'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),
    path('terms/', TermsView.as_view(), name='terms'),
    path('cookies/', CookiesView.as_view(), name='cookies'),
    path('compliance/', ComplianceView.as_view(), name='compliance'),
]


