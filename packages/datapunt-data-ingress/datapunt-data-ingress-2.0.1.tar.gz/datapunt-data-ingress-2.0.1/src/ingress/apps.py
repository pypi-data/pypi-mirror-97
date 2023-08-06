from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured

from ingress.settings import app_settings


class IngressConfig(AppConfig):
    name = "ingress"

    def ready(self):
        if not (app_settings.PERMISSION_CLASSES or app_settings.AUTHENTICATION_CLASSES):
            raise ImproperlyConfigured(
                "At lease one of INGRESS_PERMISSION_CLASSES and "
                "INGRESS_AUTHENTICATION_CLASSES settings must be set"
            )

        super().ready()
