import re
from django.utils import timezone
from notifications.models import Notification
from notifications.services.delivery_service import DeliveryService
from notifications.services.history_service import HistoryService

class NotificationService:
    @staticmethod
    def create_notification(user, title, message, category='General', priority='Medium', notification_type='Information', action_url=None, action_label=None, metadata=None):
        if not user or not user.is_authenticated:
            return None
        if metadata is None:
            metadata = {}

        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        # Smart Merge Rule for duplicate events today (e.g. Income Added, Expense Added)
        merge_keywords = ['Income Added', 'Expense Added', 'Transaction Added', 'New Course']
        for kw in merge_keywords:
            if kw.lower() in title.lower():
                existing = Notification.objects.filter(
                    user=user,
                    category=category,
                    is_read=False,
                    created_at__gte=today_start,
                    title__icontains=kw.split()[0]
                ).first()
                if existing:
                    count = existing.metadata.get('merge_count', 1) + 1
                    existing.metadata['merge_count'] = count
                    item_type = kw.split()[0].lower()
                    existing.title = f"{count} new {item_type} transactions added today."
                    existing.message = f"You have added {count} {item_type} entries today. View your dashboard for updated summaries."
                    existing.created_at = now
                    existing.save()
                    return existing

        notif = Notification.objects.create(
            user=user,
            title=title,
            message=message,
            category=category,
            priority=priority,
            status='Unread',
            notification_type=notification_type,
            action_url=action_url,
            action_label=action_label,
            metadata=metadata
        )
        DeliveryService.deliver(notif)
        return notif

    @staticmethod
    def mark_as_read(user, notification_id):
        if not user or not user.is_authenticated:
            return None
        try:
            notif = Notification.objects.get(id=notification_id, user=user)
            if not notif.is_read:
                notif.is_read = True
                notif.status = 'Read'
                notif.read_at = timezone.now()
                notif.save()
                HistoryService.record_read(notif)
            return notif
        except Notification.DoesNotExist:
            return None

    @staticmethod
    def mark_all_as_read(user):
        if not user or not user.is_authenticated:
            return 0
        now = timezone.now()
        unread = Notification.objects.filter(user=user, is_read=False)
        count = unread.count()
        for n in unread:
            HistoryService.record_read(n)
        unread.update(is_read=True, status='Read', read_at=now)
        return count

    @staticmethod
    def delete_notification(user, notification_id):
        if not user or not user.is_authenticated:
            return False
        try:
            notif = Notification.objects.get(id=notification_id, user=user)
            notif.delete()
            return True
        except Notification.DoesNotExist:
            return False

    @staticmethod
    def get_unread(user):
        if not user or not user.is_authenticated:
            return Notification.objects.none()
        return Notification.objects.filter(user=user, is_read=False)

    @staticmethod
    def seed_default_notifications(user):
        if not user or not user.is_authenticated:
            return
        if Notification.objects.filter(user=user).exists():
            return

        defaults = [
            {
                "title": "Electricity Bill Paid Successfully",
                "message": "Your electricity bill of ₹1,250 has been paid on time.",
                "category": "Bills",
                "priority": "Medium",
                "type": "Success",
                "is_read": False
            },
            {
                "title": "Salary Credited — ₹50,000 Added",
                "message": "Your monthly salary has been deposited to your primary account.",
                "category": "Dashboard",
                "priority": "High",
                "type": "Success",
                "is_read": False
            },
            {
                "title": "Credit Score Updated — 730",
                "message": "Your credit score increased by +18 points this month. Great job!",
                "category": "Credit Score",
                "priority": "High",
                "type": "Achievement",
                "is_read": False
            },
            {
                "title": "AI Recommendation",
                "message": "Increase your monthly SIP by ₹500 to improve 5-year returns by 28%.",
                "category": "AI Insights",
                "priority": "Critical",
                "type": "AI Recommendation",
                "is_read": False
            },
            {
                "title": "Investment Reminder",
                "message": "Your monthly SIP of ₹2,000 is due tomorrow. Ensure sufficient balance.",
                "category": "Investments",
                "priority": "Medium",
                "type": "Reminder",
                "is_read": False
            },
            {
                "title": "Emergency Fund Reminder",
                "message": "Maintain at least 6 months of expenses in your emergency fund.",
                "category": "Security",
                "priority": "Low",
                "type": "Information",
                "is_read": True
            },
            {
                "title": "Weekly Financial Summary",
                "message": "Your savings improved by 8% this week. Keep up the momentum!",
                "category": "Reports",
                "priority": "Medium",
                "type": "Information",
                "is_read": True
            },
            {
                "title": "Portfolio Milestone Reached",
                "message": "Your investment portfolio crossed ₹1,00,000 for the first time!",
                "category": "Achievements",
                "priority": "High",
                "type": "Achievement",
                "is_read": True
            },
            {
                "title": "Financial Report Generated",
                "message": "Your latest monthly financial report is ready to download.",
                "category": "Reports",
                "priority": "Low",
                "type": "Information",
                "is_read": True
            },
            {
                "title": "New Educational Article",
                "message": "\"How to Build an Emergency Fund in 6 Months\" is now available in Learn.",
                "category": "Education",
                "priority": "Low",
                "type": "Education",
                "is_read": True
            },
            {
                "title": "Risk Assessment Completed",
                "message": "Your risk profile has been analyzed. View your results in Risk Profile.",
                "category": "Risk Profile",
                "priority": "Medium",
                "type": "Information",
                "is_read": True
            }
        ]

        from datetime import timedelta
        now = timezone.now()
        for idx, d in enumerate(defaults):
            # stagger created_at so they sort nicely into today, this week, older
            created = now - timedelta(hours=idx*5 if idx < 3 else (days:=idx))
            notif = Notification.objects.create(
                user=user,
                title=d["title"],
                message=d["message"],
                category=d["category"],
                priority=d["priority"],
                status="Read" if d["is_read"] else "Unread",
                notification_type=d["type"],
                is_read=d["is_read"],
                created_at=created
            )
            # update created_at manually since auto_now_add sets to now on create
            Notification.objects.filter(id=notif.id).update(created_at=created)
            DeliveryService.deliver(notif)
