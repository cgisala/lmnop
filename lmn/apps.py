from django.apps import AppConfig


class LmnConfig(AppConfig):
    name = 'LMN'

    def ready(self):
        import lmn.signals