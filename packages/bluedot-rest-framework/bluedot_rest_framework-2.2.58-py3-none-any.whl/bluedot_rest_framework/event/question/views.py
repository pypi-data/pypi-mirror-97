from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.crypto import AESEncrypt
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, user_perform_create
from bluedot_rest_framework.utils.jwt_token import jwt_get_wechatid_handler, jwt_get_userid_handler
from bluedot_rest_framework.event.survey.models import SurveyUser
from bluedot_rest_framework.event.survey.serializers import SurveyUserSerializer

EventQuestion = import_string('event.question.models')
EventQuestionUser = import_string('event.question.user_models')
EventQuestionSerializer = import_string('event.question.serializers')
EventQuestionUserSerializer = import_string('event.question.user_serializers')
EventRegister = import_string('event.register.models')


class EventQuestionView(CustomModelViewSet):
    model_class = EventQuestion
    serializer_class = EventQuestionSerializer
    pagination_class = None
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        event_id = self.request.data.get('event_id', None)
        queryset = self.model_class.objects.filter(event_id=event_id).first()
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

    def list(self, request, *args, **kwargs):
        event_id = request.query_params.get('event_id', None)
        queryset = self.model_class.objects.filter(event_id=event_id).first()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class EventQuestionUserView(CustomModelViewSet):
    model_class = EventQuestionUser
    serializer_class = EventQuestionUserSerializer
    filterset_fields = {
        'event_id': {
            'field_type': 'int',
            'lookup_expr': ''
        }
    }

    def list(self, request, *args, **kwargs):
        event_id = request.query_params.get('event_id', None)
        wechat_id = jwt_get_wechatid_handler(request.auth)
        if wechat_id == 0:
            userid = jwt_get_userid_handler(request.auth)
        data = EventQuestionUser.objects.filter(
            Q(event_id=event_id, wechat_id=wechat_id) | Q(event_id=event_id, userid=userid)).first()
        if data:
            serializer = self.get_serializer(data)
            return Response({'code': '1', 'data': serializer.data})
        else:
            return Response({'code': '0'})

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        wechat_id = jwt_get_wechatid_handler(request.auth)
        register_queryset = EventRegister.objects.filter(
            wechat_id=wechat_id).first()
        data['wechat_id'] = wechat_id
        data['first_name'] = register_queryset.first_name
        data['last_name'] = register_queryset.last_name
        data['tel'] = register_queryset.tel
        data['email'] = register_queryset.email
        data['company'] = register_queryset.company
        data['job'] = register_queryset.job
        data['country'] = register_queryset.country
        SurveyUser.objects.create(**data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return user_perform_create(self.request.auth, serializer)
