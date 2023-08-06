from django.apps import AppConfig


class BluedotRestFrameworkConfig(AppConfig):
    name = 'bluedot_rest_framework'
    verbose_name = "Bluedot REST framework"

    # def ready(self):
    # Add System checks
    # from .checks import pagination_system_check  # NOQA
