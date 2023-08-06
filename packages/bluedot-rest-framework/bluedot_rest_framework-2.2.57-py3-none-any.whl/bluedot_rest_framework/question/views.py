from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from bluedot_rest_framework import import_string
from bluedot_rest_framework.config.models import Config
from bluedot_rest_framework.config.serializers import ConfigSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, user_perform_create, AllView
from bluedot_rest_framework.utils.jwt_token import jwt_get_wechatid_handler, jwt_get_unionid_handler

Question = import_string('question.models')
QuestionSerializer = import_string('question.serializers')
QuestionUser = import_string('question.user_models')
QuestionUserSerializer = import_string('question.user_serializers')


class QuestionView(CustomModelViewSet, AllView):
    model_class = Question
    serializer_class = QuestionSerializer

    filterset_fields = {
        'title': {
            'field_type': 'string',
            'lookup_expr': '__icontains'
        },
    }

    def create(self, request, *args, **kwargs):
        qa_id = self.request.data.get('qa_id', None)
        queryset = self.model_class.objects.filter(pk=qa_id).first()
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

    @action(detail=False, methods=['get'], url_path='new', url_name='new')
    def new(self, request):
        unionid = jwt_get_unionid_handler(self.request.auth)
        queryset = QuestionUser.objects.filter(unionid=unionid)
        qa = QuestionUserSerializer(queryset, many=True).data
        queryset = self.model_class.objects.exclude(
            id__in=[i['qa_id'] for i in qa if i])
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class QuestionUserView(CustomModelViewSet):
    model_class = QuestionUser
    serializer_class = QuestionUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filterset_fields = {
        'unionid': {
            'field_type': 'string',
            'lookup_expr': ''
        },
    }

    @action(detail=False, methods=['get'], url_path='code', url_name='code')
    def code(self, request):
        unionid = jwt_get_unionid_handler(self.request.auth)
        qa_id = request.query_params.get('qa_id')
        questionUserQueryset = self.model_class.objects.filter(
            unionid=unionid, qa_id=qa_id).first()
        if questionUserQueryset:
            return Response({'code': 1})
        else:
            return Response({'code': 0})

    @action(detail=False, methods=['get'], url_path='current', url_name='current')
    def current(self, request):
        unionid = jwt_get_unionid_handler(self.request.auth)
        qa_id = request.query_params.get('qa_id')
        questionQueryset = Question.objects.get(pk=qa_id)
        questionUserQueryset = self.model_class.objects.filter(
            unionid=unionid, qa_id=qa_id).first()
        data = self.get_serializer(questionUserQueryset).data

        for index, qa_item in enumerate(data['qa']):
            if qa_item['qa_type'] in [1, 2]:
                for option_index, qa_option in enumerate(qa_item['option']):
                    rate_data = questionQueryset.qa[index]
                    if 'rate' not in rate_data:
                        if 'checked' in qa_option and qa_option['checked'] == 1:
                            qa_option['rate'] = 1
                        else:
                            qa_option['rate'] = 0
                    else:
                        qa_option['rate'] = rate_data['rate']
        return Response(data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_data = serializer.data
        qa = response_data['qa']
        Question_queryset = Question.objects.get(pk=response_data['qa_id'])
        for index, qa_item in enumerate(qa):
            if qa_item['qa_type'] in [1, 2]:
                option_sum = 0  # 选择总数
                option_list = list()  # 每个选项数
                for option_index, qa_option in enumerate(qa_item['option']):
                    count = 0
                    qa_data = self.model_class.objects.filter(
                        qa_id=response_data['qa_id'])
                    for item in qa_data:
                        qa_checked = item.qa[index]['option'][option_index]
                        if 'checked' in qa_checked and qa_checked['checked'] == 1:
                            count += 1
                    option_list.append(count)

                    option_sum += count
                for option_index, option_item in enumerate(option_list):
                    rate = round(float(option_item / option_sum), 2)
                    Question_queryset.qa[index]['option'][option_index]['rate'] = rate
                    Question_queryset.save()
                    response_data['qa'][index]['option'][option_index]['rate'] = rate

        headers = self.get_success_headers(response_data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return user_perform_create(self.request.auth, serializer)
