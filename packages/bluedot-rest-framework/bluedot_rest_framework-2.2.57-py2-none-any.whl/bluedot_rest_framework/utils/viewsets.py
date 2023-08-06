from datetime import datetime
from rest_framework import status
from rest_framework.decorators import (action)
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .filterset import FilterBackend
from .func import get_tree
from .jwt_token import jwt_get_userinfo_handler


class CustomModelViewSet(ModelViewSet):
    model_class = None

    filterset_fields = {
        # '_type': {
        #     'field_type': 'int',
        #     'lookup_expr': ''
        # },
        # 'time_state': {
        #     'start_time': 'start_time',
        #     'end_time': 'end_time'
        # },
        # 'title': {
        #     'field_type': 'string',
        #     'lookup_expr': '__icontains'
        # },
        # 'extend__is_banner': {
        #     'field_type': 'boolean',
        #     'lookup_expr': ''
        # },
        # 'extend__is_index': {
        #     'field_type': 'boolean',
        #     'lookup_expr': ''
        # },
    }

    def get_queryset(self):
        queryset = self.model_class.objects.all()
        queryset = FilterBackend.get_filterset(
            self.request, queryset, self.filterset_fields)

        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            queryset = queryset.order_by(ordering)
        return queryset


def user_perform_create(token, serializer):
    wechat_id, unionid ,userid= jwt_get_userinfo_handler(token)
    serializer.save(unionid=unionid, wechat_id=wechat_id,userid=userid)


class TreeAPIView(ListAPIView):

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        parent = request.query_params.get('parent', 0)
        data = get_tree(serializer.data, parent)
        return Response(data)


class AllView:

    @action(detail=False, methods=['get'], url_path='all', url_name='all')
    def all(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
