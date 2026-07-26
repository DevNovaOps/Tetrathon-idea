from django.db import models
from django.utils import timezone
from datetime import timedelta
from notifications.models import Notification

class FilterService:
    @staticmethod
    def filter_notifications(user, filter_param='all', search_query=None, limit=50):
        if not user or not user.is_authenticated:
            return Notification.objects.none()

        qs = Notification.objects.filter(user=user)

        if search_query:
            q = search_query.strip()
            qs = qs.filter(
                models.Q(title__icontains=q) |
                models.Q(message__icontains=q) |
                models.Q(category__icontains=q) |
                models.Q(priority__icontains=q) |
                models.Q(notification_type__icontains=q)
            )

        f = str(filter_param).lower().strip() if filter_param else 'all'
        if f == 'all':
            pass
        elif f == 'unread':
            qs = qs.filter(is_read=False)
        elif f == 'read':
            qs = qs.filter(is_read=True)
        elif f == 'ai insights' or f == 'ai_insights' or f == 'ai recommendations':
            qs = qs.filter(
                models.Q(category__iexact='AI Insights') | models.Q(notification_type__iexact='AI Recommendation')
            )
        else:
            # Match category or type
            qs = qs.filter(
                models.Q(category__iexact=filter_param) | models.Q(notification_type__iexact=filter_param)
            )

        return qs[:limit]
