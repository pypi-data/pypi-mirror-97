from django.apps import AppConfig


class DjangofileConfig(AppConfig):
    name = 'djangofile'

    def ready(self):
        import djangofile.signals
