from django.urls import path
from . import views

urlpatterns = [
    path('', views.memory_list_view, name='ai-memory-list'),
    path('context/', views.memory_context_view, name='ai-memory-context'),
    path('trends/', views.improvement_trends_view, name='ai-memory-trends'),
]
