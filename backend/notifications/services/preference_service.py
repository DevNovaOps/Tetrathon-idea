from notifications.models import NotificationPreference

class PreferenceService:
    @staticmethod
    def get_preferences(user):
        if not user or not user.is_authenticated:
            return None
        pref, _ = NotificationPreference.objects.get_or_create(user=user)
        return pref

    @staticmethod
    def update_preferences(user, data):
        if not user or not user.is_authenticated:
            return {"error": "Authentication required"}
        pref, _ = NotificationPreference.objects.get_or_create(user=user)
        for field in [
            'bills', 'investments', 'credit_score', 'education', 'security',
            'ai_insights', 'reports', 'goals', 'achievements', 'simulator',
            'risk_profile', 'dashboard', 'profile', 'general',
            'email_enabled', 'push_enabled', 'in_app_enabled'
        ]:
            if field in data:
                setattr(pref, field, bool(data[field]))
        pref.save()
        return pref

    @staticmethod
    def is_category_enabled(user, category):
        if not user or not user.is_authenticated:
            return True
        pref, _ = NotificationPreference.objects.get_or_create(user=user)
        if not pref.in_app_enabled:
            return False
        cat_map = {
            'bills': pref.bills,
            'investments': pref.investments,
            'credit score': pref.credit_score,
            'credit_score': pref.credit_score,
            'education': pref.education,
            'learning': pref.education,
            'security': pref.security,
            'ai insights': pref.ai_insights,
            'ai_insights': pref.ai_insights,
            'reports': pref.reports,
            'goals': pref.goals,
            'achievements': pref.achievements,
            'simulator': pref.simulator,
            'risk profile': pref.risk_profile,
            'risk_profile': pref.risk_profile,
            'dashboard': pref.dashboard,
            'profile': pref.profile,
            'general': pref.general,
        }
        key = str(category).lower().strip()
        return cat_map.get(key, True)
