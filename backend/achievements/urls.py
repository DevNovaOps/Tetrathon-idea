from django.urls import path
from . import views

urlpatterns = [
    path('', views.achievements_summary, name='achievements-summary'),
    path('statistics/', views.statistics, name='achievements-statistics'),
    path('progress/', views.progress, name='achievements-progress'),
    path('badges/', views.badges, name='achievements-badges'),
    path('history/', views.history, name='achievements-history'),
    path('explain/<uuid:id>/', views.explain_achievement, name='achievements-explain'),
]
