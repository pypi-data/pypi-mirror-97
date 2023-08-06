from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

class TransactionalMailConfig(AppConfig):
    name = 'transactional_mail'

    def ready(self):
        # Automatically discover any emails in installed apps
        autodiscover_modules('emails')