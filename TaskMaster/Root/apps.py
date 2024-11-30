# Root/apps.py
from django.apps import AppConfig

class RootConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Root'

    def ready(self):
        import Root.signals  # Registra las señales para que se ejecuten después de las migraciones
