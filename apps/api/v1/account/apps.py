from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.api.v1.account'

    def ready(self):
        import apps.api.v1.account.services