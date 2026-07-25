from django.urls import path
from . import views

urlpatterns = [
    path('', views.ImproveScoreAPIView.as_view(), name='improve_score_dashboard'),
    path('progress/', views.ImproveScoreProgressAPIView.as_view(), name='improve_score_progress'),
    path('task/<uuid:task_id>/complete/', views.CompleteTaskAPIView.as_view(), name='complete_task'),
    path('regenerate/', views.RegeneratePlanAPIView.as_view(), name='regenerate_plan'),
]
