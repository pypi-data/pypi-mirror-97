from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import Permission, ContentType, Group
from rest_framework import permissions
from bluedot_rest_framework.api_auth.models import AuthUser


class CreateGroup(APIView):
    def get(self, request, *args, **kwargs):
        name = request.query_params.get('name', None)
        Group.objects.create(name=name)
        return Response('success')


class AddUser(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id', None)
        group = Group.objects.filter(name='总管理员').first()
        user = AuthUser.objects.filter(pk=user_id).first()
        user.groups.add(group)
        user.save()
        return Response('success')


class GroupPermission(APIView):
    def get(self, request, *args, **kwargs):
        name = request.query_params.get('name', None)
        group = Group.objects.filter(name=name).first()
        content_type = ContentType.objects.filter(pk=6).first()
        permissions = Permission.objects.filter(content_type=content_type)
        group.permissions.set(permissions)
        # permissions = Permission.objects.all()
        # for permission in permissions:
        #     group.permissions.set(permissions)
        return Response('success')
