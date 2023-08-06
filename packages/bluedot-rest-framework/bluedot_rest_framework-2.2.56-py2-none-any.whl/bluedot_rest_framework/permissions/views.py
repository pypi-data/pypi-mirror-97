from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import Permission, ContentType, Group
from api_auth.models import AuthUser


class CreateGroup(APIView):
    def get(request):
        name = request.query_params.get('name', None)
        Group.objects.create(name=name)
        return Response('操作分组')
