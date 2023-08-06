from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.func import orm_bulk_update
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet

EventSchedule = import_string('event.schedule.models')
EventScheduleSerializer = import_string('event.schedule.serializers')


class EventScheduleView(CustomModelViewSet):
    model_class = EventSchedule
    serializer_class = EventScheduleSerializer
    pagination_class = None
    filterset_fields = {
        'topic_title': {
            'field_type': 'string',
            'lookup_expr': '__icontains'
        },
        'event_id': {
            'field_type': 'int',
            'lookup_expr': ''
        },
    }
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        data = request.data
        ids = list()
        for index, item in enumerate(data['schedule_list']):
            item['sort'] = index
            if 'id' in item:
                ids.append(item['id'])
                schedule_data = {
                    "project_title": item.get('project_title', None),
                    "topic_title": item.get('topic_title', None),
                    "speaker_ids": item.get('speaker_ids', None),
                    "start_time:": item['start_time'],
                    "end_time": item['end_time'],
                    "sort": item['sort']}
                schedule_queryset = self.model_class.objects.get(pk=item['id'])
                orm_bulk_update(schedule_queryset, schedule_data)
            else:
                queryset = self.model_class.objects.create(
                    project_title=item.get('project_title', None), topic_title=item.get('topic_title', None), speaker_ids=item.get('speaker_ids', None), start_time=item['start_time'], end_time=item['end_time'], sort=item['sort'], event_id=data['event_id'])
                ids.append(str(queryset.pk))
        schedule_model = self.model_class.objects.exclude(id__in=ids)
        schedule_model.filter(event_id=data['event_id']).delete()
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
        self.model_class.objects.get(pk=before_id).update(sort=after_sort)
        self.model_class.objects.get(pk=after_id).update(sort=before_sort)
        return Response(status=200)
