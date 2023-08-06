from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from bluedot_rest_framework import import_string
from .response.views import WeChatResponseEventView, WeChatResponseMaterialView
from .login.views import WeChatLoginView, WeChatLoginWebSocketView
from .views import JSSdk, OAuth, Menu, Current, Auth, OAuthDev
from .template_message import event_register_template
# from .response.qrcode import WeChatQrcodeView
Response = import_string('wechat.response')
router = DefaultRouter(trailing_slash=False)

router.register(r'wechat/response/material', WeChatResponseMaterialView,
                basename='wechat-response-material')
router.register(r'wechat/response/event', WeChatResponseEventView,
                basename='wechat-response-event')
urlpatterns = router.urls

urlpatterns += [
    # url(r'^wechat/qrcode', WeChatQrcodeView.as_view()),
    url(r'^wechat/current', Current.as_view()),
    url(r'^wechat/response', Response.as_view()),
    url(r'^wechat/auth', Auth.as_view()),
    url(r'^wechat/oauth', OAuth.as_view()),
    url(r'^wechat/oauth-dev', OAuthDev.as_view()),
    url(r'^wechat/jssdk', JSSdk.as_view()),
    url(r'^wechat/menu', Menu.as_view()),
    url(r'^wechat/login-websocket', WeChatLoginWebSocketView.as_view()),
    url(r'^wechat/login', WeChatLoginView.as_view()),
]
