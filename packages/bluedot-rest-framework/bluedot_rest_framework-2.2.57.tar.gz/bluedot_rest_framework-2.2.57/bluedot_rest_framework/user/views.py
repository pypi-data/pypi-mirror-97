from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.conf import settings
from django.core.mail import send_mail
from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.crypto import AESEncrypt
from bluedot_rest_framework.utils.code import code
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, user_perform_create, AllView
from bluedot_rest_framework.utils.jwt_token import jwt_create_token_wechat, jwt_get_userinfo_handler


User = import_string('user.models')
UserSerializer = import_string('user.serializers')


class UserView(CustomModelViewSet):
    model_class = User
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        email = request.data["email"]
        wechat_id, unionid ,userid= jwt_get_userinfo_handler(request.auth)
        queryset = self.model_class.objects.filter(email=email).first()
        if queryset:
            data = request.data
            data['wechat_id'] = wechat_id
            data['unionid'] = unionid
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(
                queryset, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            serializer.save(unionid=unionid, wechat_id=wechat_id)
            user_data = serializer.data
            return Response(user_data, status=status.HTTP_201_CREATED)


