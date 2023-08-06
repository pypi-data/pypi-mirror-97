import random
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, AllView
from bluedot_rest_framework.wechat import App
from rest_framework import status
from rest_framework.response import Response
from .models import WeChatResponseMaterial, WeChatResponseEvent
from .serializers import WeChatResponseMaterialSerializer, WeChatResponseEventSerializer


class WeChatResponseMaterialView(CustomModelViewSet, AllView):
    model_class = WeChatResponseMaterial
    serializer_class = WeChatResponseMaterialSerializer

    filterset_fields = {
        'material_type': {
            'field_type': 'int',
            'lookup_expr': ''
        },
        'title': {
            'field_type': 'string',
            'lookup_expr': '__icontains'
        },
    }


class WeChatResponseEventView(CustomModelViewSet):
    model_class = WeChatResponseEvent
    serializer_class = WeChatResponseEventSerializer

    filterset_fields = {
        'event_type': {
            'field_type': 'int',
            'lookup_expr': ''
        },
        'title': {
            'field_type': 'string',
            'lookup_expr': '__icontains'
        },
    }

    def create(self, request, *args, **kwargs):
        if request.data['event_type'] == 2:
            event_key = str(random.uniform(1, 10))
            result = App(request.data['appid']).qrcode.create({
                'action_name': 'QR_LIMIT_STR_SCENE',
                'action_info': {
                    'scene': {'scene_str': event_key},
                }
            })
            request.data['qrcode_ticket'] = result['ticket']
            request.data['qrcode_url'] = result['url']
            request.data['event_key'] = event_key
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
