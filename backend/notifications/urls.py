from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_notifications, name='notifications-list'),
    path('unread/', views.unread_notifications, name='notifications-unread'),
    path('stats/', views.notification_stats, name='notifications-stats'),
    path('preferences/', views.preferences, name='notifications-preferences'),
    path('read-all/', views.mark_all_read, name='notifications-read-all'),
    path('history/', views.notification_history, name='notifications-history'),
    path('filter/', views.filter_notifications_view, name='notifications-filter'),
    path('search/', views.search_notifications_view, name='notifications-search'),
    path('<uuid:id>/read/', views.mark_read, name='notifications-mark-read'),
    path('<uuid:id>/', views.delete_notification, name='notifications-delete'),
]
