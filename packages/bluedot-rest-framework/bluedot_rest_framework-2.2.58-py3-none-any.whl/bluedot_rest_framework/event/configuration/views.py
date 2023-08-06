
from rest_framework import status
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, AllView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bluedot_rest_framework import import_string

EventConfiguration = import_string('event.configuration.models')
EventConfigurationSerializer = import_string('event.configuration.serializers')


class EventConfigurationView(CustomModelViewSet):
    model_class = EventConfiguration
    serializer_class = EventConfigurationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        event_id = request.query_params.get('event_id', None)
        queryset = self.model_class.objects.filter(event_id=event_id).first()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        queryset = self.model_class.objects.filter(
            event_id=request.data.get('event_id', None)).first()
        if queryset:
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(
                queryset, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
