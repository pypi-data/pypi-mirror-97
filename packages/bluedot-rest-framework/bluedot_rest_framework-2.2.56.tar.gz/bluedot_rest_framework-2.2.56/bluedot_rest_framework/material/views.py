from rest_framework.decorators import action
from rest_framework.response import Response
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, AllView
from bluedot_rest_framework import import_string
from rest_framework.permissions import IsAuthenticatedOrReadOnly

Material = import_string('material.models')
MaterialSerializer = import_string('material.serializers')


class MaterialView(CustomModelViewSet, AllView):
    model_class = Material
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filterset_fields = {
        'material_type': {
            'field_type': 'int',
            'lookup_expr': ''
        },
        'title': {
            'field_type': 'string',
            'lookup_expr': '__icontains'
        },
        'category_id': {
            'field_type': 'int',
            'lookup_expr': ''
        },
        'extend_category_id': {
            'field_type': 'int',
            'lookup_expr': '__in'
        },
        '_type': {
            'field_type': 'int',
            'lookup_expr': ''
        },
    }
