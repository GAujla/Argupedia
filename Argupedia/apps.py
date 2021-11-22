from django.apps import AppConfig
from django.apps import AppConfig

class ArgupediaConfig(AppConfig):
    name = 'Argupedia'

    def ready(self):
        import Argupedia.signals



