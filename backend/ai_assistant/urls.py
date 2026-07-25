from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.StartConversationAPIView.as_view(), name='ai_start'),
    path('message/', views.MessageAPIView.as_view(), name='ai_message'),
    path('history/', views.HistoryAPIView.as_view(), name='ai_history'),
    path('reset/', views.ResetAPIView.as_view(), name='ai_reset'),
]
