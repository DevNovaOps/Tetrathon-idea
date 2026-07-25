"""config URL Configuration."""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # API — Authentication
    path('api/auth/', include('accounts.urls')),

    # API — Onboarding
    path('api/onboarding/', include('onboarding.urls')),

    # API — Dashboard
    path('api/dashboard/', include('dashboard.urls')),

    # API — Credit Score
    path('api/credit-score/', include('credit_score.urls')),

    # API — Improve Score
    path('api/improve-score/', include('improve_score.urls')),

    # API - AI Assistant
    path('api/assistant/', include('ai_assistant.urls')),

    # django-allauth (Google OAuth callbacks)
    path('accounts/', include('allauth.urls')),

    # Root redirect to landing page
    path('', RedirectView.as_view(url='/01-landing-page/index.html', permanent=False)),
    
    # Serve static files at root
    re_path(r'^(?P<path>.*)$', serve, {'document_root': settings.STATICFILES_DIRS[0]}),
]
