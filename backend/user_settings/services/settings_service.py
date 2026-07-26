from user_settings.models import UserPreference
from notifications.services.preference_service import PreferenceService

class SettingsService:
    @staticmethod
    def get_preferences(user):
        if not user or not user.is_authenticated:
            return None
        pref, _ = UserPreference.objects.get_or_create(user=user)
        return pref

    @staticmethod
    def update_preferences(user, data):
        if not user or not user.is_authenticated:
            return {"error": "Authentication required"}
        pref, _ = UserPreference.objects.get_or_create(user=user)
        
        fields = [
            'theme', 'accent_color', 'animations_enabled', 'density',
            'language', 'currency', 'timezone', 'two_factor_ready',
            'marketing_emails', 'weekly_reports_email', 'monthly_reports_email'
        ]
        for f in fields:
            if f in data and data[f] is not None:
                val = data[f]
                if f in ['animations_enabled', 'two_factor_ready', 'marketing_emails', 'weekly_reports_email', 'monthly_reports_email']:
                    val = bool(val) if val not in ['false', 'False', '0', 0, False] else False
                setattr(pref, f, val)
        pref.save()
        
        # Synchronize user timezone/currency if present
        if 'timezone' in data and data['timezone']:
            user.timezone = data['timezone']
        if 'currency' in data and data['currency']:
            user.preferred_currency = data['currency']
        user.save()

        # Record timeline event
        from user_profile.services.timeline_service import TimelineService
        TimelineService.record_event(
            user=user,
            event_type="settings_updated",
            title="System Settings Updated",
            description=f"Theme set to '{pref.theme}' with '{pref.currency}' currency.",
            category="Settings"
        )
        return pref

    @staticmethod
    def get_notification_preferences(user):
        return PreferenceService.get_preferences(user)

    @staticmethod
    def update_notification_preferences(user, data):
        return PreferenceService.update_preferences(user, data)
