from django.utils import timezone
from datetime import timedelta
from notifications.models import NotificationHistory, Notification

class HistoryService:
    @staticmethod
    def record_delivery(notification):
        if not notification:
            return None
        return NotificationHistory.objects.create(notification=notification)

    @staticmethod
    def record_read(notification):
        if not notification:
            return None
        now = timezone.now()
        NotificationHistory.objects.filter(notification=notification, opened_at__isnull=True).update(opened_at=now)

    @staticmethod
    def get_user_history(user, filter_params=None):
        if not user or not user.is_authenticated:
            return NotificationHistory.objects.none()
        
        qs = NotificationHistory.objects.filter(notification__user=user).select_related('notification')
        if not filter_params:
            return qs

        now = timezone.now()
        date_filter = filter_params.get('date') or filter_params.get('timeframe')
        if date_filter == 'today':
            qs = qs.filter(delivered_at__date=now.date())
        elif date_filter == 'this_week' or date_filter == 'week':
            start_week = now - timedelta(days=now.weekday())
            qs = qs.filter(delivered_at__gte=start_week.replace(hour=0, minute=0, second=0, microsecond=0))
        elif date_filter == 'this_month' or date_filter == 'month':
            qs = qs.filter(delivered_at__year=now.year, delivered_at__month=now.month)
        elif date_filter == 'year':
            qs = qs.filter(delivered_at__year=now.year)

        category = filter_params.get('category')
        if category and category.lower() != 'all':
            qs = qs.filter(notification__category__iexact=category)

        status = filter_params.get('status')
        if status and status.lower() != 'all':
            qs = qs.filter(notification__status__iexact=status)

        priority = filter_params.get('priority')
        if priority and priority.lower() != 'all':
            qs = qs.filter(notification__priority__iexact=priority)

        return qs

    @staticmethod
    def export_history_data(user):
        if not user or not user.is_authenticated:
            return ""
        qs = NotificationHistory.objects.filter(notification__user=user).select_related('notification').order_by('-delivered_at')
        lines = ["ID,Title,Category,Priority,Status,Type,DeliveredAt,OpenedAt"]
        for h in qs:
            n = h.notification
            delivered = h.delivered_at.strftime("%Y-%m-%d %H:%M:%S") if h.delivered_at else ""
            opened = h.opened_at.strftime("%Y-%m-%d %H:%M:%S") if h.opened_at else ""
            title = n.title.replace(',', ' ')
            lines.append(f"{h.id},{title},{n.category},{n.priority},{n.status},{n.notification_type},{delivered},{opened}")
        return "\n".join(lines)
