from rest_framework import serializers
from .models import Notification, NotificationPreference, NotificationHistory

class NotificationSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='notification_type', read_only=True)
    created_at_formatted = serializers.SerializerMethodField()
    time_ago = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'message', 'category', 'priority', 'status',
            'type', 'action_url', 'action_label', 'metadata', 'is_read',
            'created_at', 'created_at_formatted', 'time_ago', 'read_at'
        ]

    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime("%b %d, %Y, %I:%M %p")

    def get_time_ago(self, obj):
        from django.utils import timezone
        now = timezone.now()
        diff = now - obj.created_at
        seconds = diff.total_seconds()
        if seconds < 60:
            return "Just now"
        elif seconds < 3600:
            mins = int(seconds // 60)
            return f"{mins}m ago"
        elif seconds < 86400:
            hours = int(seconds // 3600)
            return f"{hours}h ago"
        else:
            days = int(seconds // 86400)
            return f"{days}d ago"


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = [
            'bills', 'investments', 'credit_score', 'education', 'security',
            'ai_insights', 'reports', 'goals', 'achievements', 'simulator',
            'risk_profile', 'dashboard', 'profile', 'general',
            'email_enabled', 'push_enabled', 'in_app_enabled'
        ]


class NotificationHistorySerializer(serializers.ModelSerializer):
    notification_title = serializers.CharField(source='notification.title', read_only=True)
    notification_category = serializers.CharField(source='notification.category', read_only=True)
    notification_priority = serializers.CharField(source='notification.priority', read_only=True)
    notification_status = serializers.CharField(source='notification.status', read_only=True)

    class Meta:
        model = NotificationHistory
        fields = [
            'id', 'notification', 'notification_title', 'notification_category',
            'notification_priority', 'notification_status', 'delivered_at',
            'opened_at', 'clicked_at', 'dismissed_at'
        ]
