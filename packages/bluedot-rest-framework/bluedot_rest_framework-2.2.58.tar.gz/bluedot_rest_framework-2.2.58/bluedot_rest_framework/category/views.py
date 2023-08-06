from rest_framework.decorators import action
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, TreeAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bluedot_rest_framework import import_string

Category = import_string('category.models')
CategorySerializer = import_string('category.serializers')


class CategoryView(CustomModelViewSet, TreeAPIView):
    model_class = Category
    serializer_class = CategorySerializer
    pagination_class = None
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = {
        'category_type': {
            'field_type': 'int',
            'lookup_expr': ''
        },
        'title': {
            'field_type': 'string',
            'lookup_expr': '__icontains'
        }
    }

    @action(detail=False, methods=['post'], url_path='sort', url_name='sort')
    def sort(self, request, *args, **kwargs):
        before_sort = request.data.get('before_sort')
        before_id = request.data.get('before_id')
        after_sort = request.data.get('after_sort')
        after_id = request.data.get('after_id')
        self.model_class.objects.get(pk=before_id).update(sort=after_sort)
        self.model_class.objects.get(pk=after_id).update(sort=before_sort)
        return Response(status=200)
