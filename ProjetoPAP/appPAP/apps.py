from django.apps import AppConfig


class ApppapConfig(AppConfig):
    name = 'appPAP'

    def ready(self):
        import appPAP.signals