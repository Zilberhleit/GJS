from django.apps import AppConfig
from django.db.models import signals

class JamsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jams'
    verbose_name = 'Геймджемы'

    # Для работы с сигналами
    def ready(self):
        import jams.signals