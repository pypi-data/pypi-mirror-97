from django.apps import AppConfig
from django.conf import settings
from django.core.checks import Tags, Warning, register


class WeChatConfig(AppConfig):
    name = 'bluedot_rest_framework.wechat'

    def ready(self):
        pass
