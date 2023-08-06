from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Group

from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, TreeAPIView, AllView
from .serializers import AuthUserSerializer, AuthMenuSerializer, AuthGroupMenuSerializer
from .models import AuthGroupMenu, AuthMenu, AuthUser
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from bluedot_rest_framework.utils.func import get_tree, get_tree_menu


class AuthUserViewSet(CustomModelViewSet):
    model_class = AuthUser
    serializer_class = AuthUserSerializer

    def create(self, request, *args, **kwargs):
        return self.model_class.objects.create_user(**request.data)

    @action(detail=False, methods=['get'], url_path='current', url_name='current')
    def current(self, request, *args, **kwargs):
        user = AuthUserSerializer(request.user, context={
            'request': request}).data
        return Response(user)


class AuthGroupViewSet(CustomModelViewSet, AllView):
    model_class = AuthGroupMenu
    serializer_class = AuthGroupMenuSerializer

    permission_classes = [IsAdminUser]


class AuthMenuViewSet(CustomModelViewSet, TreeAPIView):
    model_class = AuthMenu
    serializer_class = AuthMenuSerializer
