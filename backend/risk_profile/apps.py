from django.apps import AppConfig


class RiskProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'risk_profile'

    def ready(self):
        import risk_profile.signals
