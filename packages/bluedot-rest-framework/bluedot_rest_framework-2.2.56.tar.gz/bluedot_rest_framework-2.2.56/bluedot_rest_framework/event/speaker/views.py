from rest_framework.decorators import action
from rest_framework.response import Response
from bluedot_rest_framework import import_string
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet
from bluedot_rest_framework.utils.func import orm_bulk_update

EventSpeaker = import_string('event.speaker.models')
EventSpeakerSerializer = import_string('event.speaker.serializers')


class EventSpeakerView(CustomModelViewSet):
    model_class = EventSpeaker
    serializer_class = EventSpeakerSerializer
    pagination_class = None
    permission_classes = [IsAuthenticatedOrReadOnly]

    filterset_fields = {
        'event_id': {
            'field_type': 'int',
            'lookup_expr': ''
        },

    }

    def create(self, request, *args, **kwargs):
        data = request.data
        ids = list()
        for index, item in enumerate(data['speaker_list']):
            item['sort'] = index
            if 'id' in item:
                ids.append(item['id'])
                speaker_data = {
                    "description": item.get('description', ''),
                    "img": item.get('img', ''),
                    "job": item.get('job', ''),
                    "name": item.get('name', ''),
                    "sort": item['sort'],
                    "is_sign_page": item.get('is_sign_page', False)
                }
                speaker_queryset = self.model_class.objects.get(pk=item['id'])
                orm_bulk_update(speaker_queryset, speaker_data)
            else:
                queryset = self.model_class.objects.create(
                    description=item.get('description', ''), img=item.get('img', ''), job=item.get('job', ''), name=item.get('name', ''), sort=item['sort'], is_sign_page=item.get('is_sign_page', False), event_id=data['event_id'])
                ids.append(str(queryset.pk))
        speaker_model = self.model_class.objects.exclude(id__in=ids)
        speaker_model.filter(event_id=data['event_id']).delete()
        queryset = self.model_class.objects.filter(
            event_id=data['event_id']).order_by('sort')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='sort', url_name='sort')
    def sort(self, request, *args, **kwargs):
        before_sort = request.data.get('before_sort')
        before_id = request.data.get('before_id')
        after_sort = request.data.get('after_sort')
        after_id = request.data.get('after_id')
        before_queryset = self.model_class.objects.get(pk=before_id)
        before_queryset.sort = after_sort
        before_queryset.save()
        after_queryset = self.model_class.objects.get(pk=after_id)
        after_queryset.sort = before_sort
        after_queryset.save
        return Response(status=200)
