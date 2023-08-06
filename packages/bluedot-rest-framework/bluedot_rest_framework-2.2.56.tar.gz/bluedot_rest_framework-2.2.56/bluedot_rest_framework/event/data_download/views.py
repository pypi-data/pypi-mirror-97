import requests
from rest_framework import status
from email.utils import formataddr
from django.conf import settings
from rest_framework.response import Response
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
from rest_framework.decorators import action
from bluedot_rest_framework import import_string
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet
from bluedot_rest_framework.utils.crypto import AESEncrypt
from bluedot_rest_framework.utils.jwt_token import jwt_get_wechatid_handler, jwt_get_userid_handler
from bluedot_rest_framework.event.frontend_views import FrontendView


EventRegister = import_string('event.register.models')
EventDataDownload = import_string('event.data_download.models')
EventDataDownloadSerializer = import_string('event.data_download.serializers')


class EventDataDownloadView(CustomModelViewSet, FrontendView):
    model_class = EventDataDownload
    serializer_class = EventDataDownloadSerializer
    pagination_class = None
    permission_classes = [IsAuthenticatedOrReadOnly]

