from rest_framework.decorators import action
from rest_framework.response import Response
from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, user_perform_create, AllView
from bluedot_rest_framework.utils.jwt_token import jwt_get_unionid_handler

EventComment = import_string('event.comment.models')
EventCommentSerializer = import_string('event.comment.serializers')
EventCommentLike = import_string('event.comment.like_models')
EventCommentLikeSerializer = import_string('event.comment.like_serializers')


class EventCommentView(CustomModelViewSet):
    model_class = EventComment
    serializer_class = EventCommentSerializer

    filterset_fields = {
        'state': {
            'field_type': 'int',
            'lookup_expr': ''
        },
        'schedule_id': {
            'field_type': 'int',
            'lookup_expr': ''
        },
        'event_id': {
            'field_type': 'int',
            'lookup_expr': ''
        },
    }

    def perform_create(self, serializer):
        return user_perform_create(self.request.auth, serializer)

    @action(detail=False, methods=['get'], url_path='show', url_name='show')
    def show(self, request, *args, **kwargs):
        unionid = jwt_get_unionid_handler(request.auth)
        queryset = self.filter_queryset(self.get_queryset())
        data = self.get_serializer(queryset, many=True).data
        for item in data:
            item['is_like'] = 0
            if EventCommentLike.objects.filter(unionid=unionid, comment_id=item['id']):
                item['is_like'] = 1
        return Response(data)


class EventCommentLikeView(CustomModelViewSet):
    model_class = EventCommentLike
    serializer_class = EventCommentLikeSerializer
