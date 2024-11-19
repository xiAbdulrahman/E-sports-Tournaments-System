from django.apps import AppConfig


class MainpageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MainPage'

    def ready(self):
        import MainPage.signals  # noqa