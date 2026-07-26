from rest_framework import serializers
from .models import UserPreference

class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = [
            'id', 'theme', 'accent_color', 'animations_enabled', 'density',
            'language', 'currency', 'timezone', 'two_factor_ready',
            'marketing_emails', 'weekly_reports_email', 'monthly_reports_email',
            'created_at', 'updated_at'
        ]
