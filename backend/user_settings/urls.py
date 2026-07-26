from django.urls import path
from . import views

urlpatterns = [
    path('', views.settings_overview, name='settings-overview'),
    path('update/', views.update_settings_view, name='settings-update'),
    path('notifications/', views.settings_notifications_view, name='settings-notifications'),
    path('privacy/action/', views.privacy_action_view, name='settings-privacy-action'),
]
