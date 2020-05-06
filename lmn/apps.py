from django.apps import AppConfig


class LmnConfig(AppConfig):
    name = 'lmn'

    def ready(self):
        import lmn.signals