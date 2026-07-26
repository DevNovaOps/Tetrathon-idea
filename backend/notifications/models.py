import uuid
from django.db import models
from django.conf import settings

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    category = models.CharField(max_length=50, default='General', db_index=True)
    priority = models.CharField(max_length=20, default='Medium')
    status = models.CharField(max_length=20, default='Unread', db_index=True)
    notification_type = models.CharField(max_length=50, default='Information', db_column='type')
    action_url = models.CharField(max_length=500, null=True, blank=True)
    action_label = models.CharField(max_length=100, null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    is_read = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.title} ({self.status})"


class NotificationPreference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_preference')
    bills = models.BooleanField(default=True)
    investments = models.BooleanField(default=True)
    credit_score = models.BooleanField(default=True)
    education = models.BooleanField(default=True)
    security = models.BooleanField(default=True)
    ai_insights = models.BooleanField(default=True)
    reports = models.BooleanField(default=True)
    goals = models.BooleanField(default=True)
    achievements = models.BooleanField(default=True)
    simulator = models.BooleanField(default=True)
    risk_profile = models.BooleanField(default=True)
    dashboard = models.BooleanField(default=True)
    profile = models.BooleanField(default=True)
    general = models.BooleanField(default=True)
    email_enabled = models.BooleanField(default=True)
    push_enabled = models.BooleanField(default=True)
    in_app_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Preferences for {self.user.email}"


class NotificationHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='history_records')
    delivered_at = models.DateTimeField(auto_now_add=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)
    dismissed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-delivered_at']

    def __str__(self):
        return f"History for {self.notification.id}"
