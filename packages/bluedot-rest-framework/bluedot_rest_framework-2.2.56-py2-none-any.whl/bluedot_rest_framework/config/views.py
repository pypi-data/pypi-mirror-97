from rest_framework.permissions import IsAuthenticatedOrReadOnly

from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet


Config = import_string('config.models')
ConfigSerializer = import_string('config.serializers')


class ConfigView(CustomModelViewSet):
    model_class = Config
    serializer_class = ConfigSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    ppagination_class = None
    filterset_fields = {
        'config_type': {
            'field_type': 'int',
            'lookup_expr': ''
        }
    }
