from rest_framework.response import Response
from rest_framework.decorators import action
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, AllView
from bluedot_rest_framework import import_string

Tags = import_string('material.tags.models')
TagsSerializer = import_string('material.tags.serializers')


class TagsView(CustomModelViewSet, AllView):
    model_class = Tags
    serializer_class = TagsSerializer

    filterset_fields = {
        'title': {
            'field_type': 'string',
            'lookup_expr': '__icontains'
        },
    }

    @action(detail=False, methods=['get'], url_path='title-unique', url_name='title-unique')
    def title_unique(self, request, *args, **kwargs):
        title = request.query_params.get('title', None)
        queryset = self.model_class.objects.filter(title=title)
        code = 0
        if queryset:
            code = 1

        return Response({'code': code})
