from django.apps import AppConfig


class ApppapConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appPAP'
    
    def ready(self):
        import appPAP.signals 