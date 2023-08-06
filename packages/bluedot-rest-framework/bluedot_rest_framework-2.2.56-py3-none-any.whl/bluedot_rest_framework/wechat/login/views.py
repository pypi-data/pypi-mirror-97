import json
from websocket import create_connection
from django.http import HttpResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

from bluedot_rest_framework.utils.oss import OSS
from .. import App
from ..handle import WeChatUserSet
from bluedot_rest_framework import import_string

from .models import WeChatLogin

User = import_string('user.models')


class WeChatLoginView(APIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        appid = request.query_params.get('appid', '')
        scene_str = request.query_params.get('code', '')
        result = App(appid).qrcode.create({
            'expire_seconds': 86400,
            'action_name': 'QR_STR_SCENE',
            'action_info': {
                'scene': {'scene_str': scene_str},
            }
        })
        WeChatLogin.objects.create(scene_str=scene_str)
        return Response(result)


class WeChatLoginWebSocketView(APIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        appid = request.query_params.get('appid', '')
        scene_str = request.query_params.get('scene_str', '')
        openid = request.query_params.get('openid', '')
        user_info = App(appid).user.get(openid)
        token = WeChatUserSet(appid=appid, user_info=user_info).get_token()
        ws = create_connection(
            f"wss://{settings.ALLOWED_HOSTS[0]}/ws/wechat/login/" + scene_str)
        ws.send(json.dumps({'token': token}))
        ws.close()
        return Response({'token': token})
