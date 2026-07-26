import uuid
from django.db import models
from django.conf import settings

class UserPreference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_preferences')
    theme = models.CharField(max_length=20, default='dark')
    accent_color = models.CharField(max_length=20, default='purple')
    animations_enabled = models.BooleanField(default=True)
    density = models.CharField(max_length=20, default='comfortable')
    language = models.CharField(max_length=50, default='en-US')
    currency = models.CharField(max_length=10, default='INR')
    timezone = models.CharField(max_length=50, default='Asia/Kolkata')
    two_factor_ready = models.BooleanField(default=False)
    marketing_emails = models.BooleanField(default=False)
    weekly_reports_email = models.BooleanField(default=True)
    monthly_reports_email = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferences for {self.user.email}"
