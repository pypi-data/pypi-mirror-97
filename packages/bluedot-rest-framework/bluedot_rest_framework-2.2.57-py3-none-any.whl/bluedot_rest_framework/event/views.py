
from datetime import datetime
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, AllView
from bluedot_rest_framework.utils.func import get_tree
from bluedot_rest_framework.utils.area import area
from bluedot_rest_framework.utils.get_duration import get_duration
from .live.views import LiveView
from .frontend_views import FrontendView

Event = import_string('event.models')
EventSerializer = import_string('event.serializers')
EventRegister = import_string('event.register.models')


class EventView(CustomModelViewSet, FrontendView, LiveView, AllView):
    model_class = Event
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filterset_fields = {
        'event_type': {
            'field_type': 'int',
            'lookup_expr': ''
        },
        'time_state': {
            'start_time': 'start_time',
            'end_time': 'end_time'
        },

        'title': {
            'field_type': 'string',
            'lookup_expr': '__icontains'
        },
        'extend_is_banner': {
            'field_type': 'bool',
            'lookup_expr': ''
        },
        'extend_is_index': {
            'field_type': 'bool',
            'lookup_expr': ''
        },
        'extend_category_id': {
            'field_type': 'int',
            'lookup_expr': ''
        },
    }

    def create(self, request, *args, **kwargs):
        start = request.data['start_time']
        end = request.data['end_time']
        duration = get_duration(start, end)
        request.data['duration'] = duration
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        if 'start_time' in request.data or 'end_time' in request.data:
            start = request.data['start_time']
            end = request.data['end_time']
            duration = get_duration(start, end)
            request.data['duration'] = duration
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='area', url_name='area')
    def area(self, request, *args, **kwargs):
        return Response(area)
