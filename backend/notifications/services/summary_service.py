from django.db import models
from django.utils import timezone
from datetime import timedelta
from notifications.models import Notification

class SummaryService:
    @staticmethod
    def get_statistics(user):
        if not user or not user.is_authenticated:
            return {
                "unread": 0,
                "today_alerts": 0,
                "this_week": 0,
                "ai_recommendations": 0,
                "security_alerts": 0
            }
        
        qs = Notification.objects.filter(user=user)
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=now.weekday())

        unread_count = qs.filter(is_read=False).count()
        today_count = qs.filter(created_at__gte=today_start).count()
        week_count = qs.filter(created_at__gte=week_start).count()
        ai_count = qs.filter(
            models.Q(category__iexact='AI Insights') | models.Q(notification_type__iexact='AI Recommendation')
        ).count()
        security_count = qs.filter(
            models.Q(category__iexact='Security') | models.Q(notification_type__iexact='Security')
        ).count()

        return {
            "unread": unread_count,
            "today_alerts": today_count,
            "this_week": week_count,
            "ai_recommendations": ai_count,
            "security_alerts": security_count
        }
