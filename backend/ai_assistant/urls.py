from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.StartConversationAPIView.as_view(), name='assistant_start'),
    path('message/', views.SendMessageAPIView.as_view(), name='assistant_message'),
    path('history/', views.ConversationHistoryAPIView.as_view(), name='assistant_history'),
    path('reset/', views.ResetConversationAPIView.as_view(), name='assistant_reset'),
]
