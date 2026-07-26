from django.apps import AppConfig

class DigitalSignalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'digital_signals'
    verbose_name = 'Digital Signals'

    def ready(self):
        import digital_signals.signals  # noqa
