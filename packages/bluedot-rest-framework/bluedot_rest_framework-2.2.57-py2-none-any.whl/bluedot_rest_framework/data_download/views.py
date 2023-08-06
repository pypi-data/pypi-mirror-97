from rest_framework.response import Response
from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, AllView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

DataDownload = import_string('data_download.models')
DataDownloadSerializer = import_string('data_download.serializers')
DataDownloadUser = import_string('data_download.user_models')
DataDownloadUserSerializer = import_string('data_download.user_serializers')


class DataDownloadView(CustomModelViewSet, AllView):
    model_class = DataDownload
    serializer_class = DataDownloadSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filterset_fields = {
        'data_download_type': {
            'field_type': 'int',
            'lookup_expr': ''
        },
        'category_id': {
            'field_type': 'int',
            'lookup_expr': ''
        },
    }


class DataDownloadUserView(CustomModelViewSet, AllView):
    model_class = DataDownloadUser
    serializer_class = DataDownloadUserSerializer
