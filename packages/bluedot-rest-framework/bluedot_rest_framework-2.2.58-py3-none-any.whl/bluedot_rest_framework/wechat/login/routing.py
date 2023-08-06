from django.conf.urls import url
from bluedot_rest_framework import import_string
from .consumers import WechatLoginConsumer


websocket_urlpatterns = [
    url(r'ws/wechat/login/(?P<scene_str>\w+)', WechatLoginConsumer),
]
