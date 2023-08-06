from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, user_perform_create, AllView
from bluedot_rest_framework.utils.jwt_token import jwt_get_wechatid_handler,jwt_get_userid_handler

EventVote = import_string('event.vote.models')
EventVoteSerializer = import_string('event.vote.serializers')
EventVoteUser = import_string('event.vote.user_models')
EventVoteUserSerializer = import_string('event.vote.user_serializers')


class EventVoteView(CustomModelViewSet, AllView):
    model_class = EventVote
    serializer_class = EventVoteSerializer

    filterset_fields = {
        'event_id': {
            'field_type': 'int',
            'lookup_expr': ''
        },
        'schedule_id': {
            'field_type': 'int',
            'lookup_expr': ''
        },
    }

    def create(self, request, *args, **kwargs):
        schedule_id = self.request.data.get('schedule_id', None)
        queryset = self.model_class.objects.filter(schedule_id=schedule_id).first()
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




class EventVoteUserView(CustomModelViewSet):
    model_class = EventVoteUser
    serializer_class = EventVoteUserSerializer

    filterset_fields = {
        'event_id': {
            'field_type': 'int',
            'lookup_expr': ''
        },
        'schedule_id': {
            'field_type': 'int',
            'lookup_expr': ''
        },
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_data = serializer.data
        qa = response_data['qa']
        EventVote_queryset = EventVote.objects.get(pk=response_data['qa_id'])
        for index, qa_item in enumerate(qa):
            if qa_item['qa_type'] in [1, 2]:
                option_sum = 0  # 选择总数
                option_list = list()  # 每个选项数
                for option_index, qa_option in enumerate(qa_item['option']):
                    count = 0
                    qa_data = self.model_class.objects.filter(
                        qa_id=response_data['qa_id'])
                    for item in qa_data:
                        if item.qa[index]['option'][option_index]['checked'] == 1:
                            count += 1
                    option_list.append(count)

                    option_sum += count
                for option_index, option_item in enumerate(option_list):
                    rate = round(float(option_item / option_sum), 2)
                    EventVote_queryset.qa[index]['option'][option_index]['rate'] = rate
                    EventVote_queryset.save()
                    response_data['qa'][index]['option'][option_index]['rate'] = rate

        headers = self.get_success_headers(response_data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        schedule_id = request.query_params.get('schedule_id', None)
        wechat_id = jwt_get_wechatid_handler(request.auth)
        if wechat_id == 0:
            userid = jwt_get_userid_handler(request.auth)
            data = self.model_class.objects.filter(
                schedule_id=schedule_id, userid=userid).first()
        else:
            data = self.model_class.objects.filter(
                schedule_id=schedule_id, wechat_id=wechat_id).first()
        if data:
            serializer = self.get_serializer(data)
            return Response({'code': '1', 'data': serializer.data})
        else:
            return Response({'code': '0'})

    def perform_create(self, serializer):
        return user_perform_create(self.request.auth, serializer)
