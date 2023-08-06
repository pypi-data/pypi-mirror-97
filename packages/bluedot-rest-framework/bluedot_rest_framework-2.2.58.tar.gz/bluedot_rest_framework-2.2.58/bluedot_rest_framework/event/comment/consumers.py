import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from bluedot_rest_framework import import_string
from django.db.models import F

EventComment = import_string('event.comment.models')
EventCommentSerializer = import_string('event.comment.serializers')

EventCommentLike = import_string('event.comment.like_models')
EventCommentLikeSerializer = import_string('event.comment.like_serializers')


class CommentConsumer(WebsocketConsumer):
    def connect(self):
        self.schedule_id = self.scope['url_route']['kwargs']['schedule_id']
        self.room_group_name = 'comment_%s' % self.schedule_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        state = text_data_json.get('state', 0)
        if state == 0:
            data = {
                'unionid': text_data_json.get('unionid', None),
                'nick_name': text_data_json.get('nick_name', None),
                'avatar_url': text_data_json.get('avatar_url', None),
                'schedule_id': self.schedule_id,
                'data': text_data_json.get('data', None),
            }
            EventComment.objects.create(**data)
        elif state == 1:  # 通过
            _id = text_data_json.get('id', None)
            event_queryset = EventComment.objects.get(pk=_id)
            event_queryset.state = 1
            event_queryset.save()
            data = EventCommentSerializer(event_queryset).data
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'event_comment_message',
                    **data
                }
            )
        elif state == 2:  # 拒绝
            _id = text_data_json.get('id', None)
            event_queryset = EventComment.objects.get(pk=_id)
            event_queryset.state = 2
            event_queryset.save()
        elif state in [3, 4]:  # 点赞
            data = {
                'unionid': text_data_json.get('unionid', None),
                'comment_id': text_data_json.get('comment_id', None),
            }
            event_comment_queryset = EventComment.objects.get(
                pk=data['comment_id'])
            if state == 3:
                EventCommentLike.objects.create(**data)
                event_comment_queryset.like_count = F('like_count') + 1
            else:
                queryset = EventCommentLike.objects.filter(**data)
                if queryset:
                    queryset.delete()
                    event_comment_queryset.like_count = F('like_count') - 1
            event_comment_queryset.save()
            queryset = EventComment.objects.get(pk=data['comment_id'])
            send_data = {
                'id': data['comment_id'],
                'like_count': queryset.like_count,
                'state': state
            }
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'event_comment_message',
                    **send_data
                }
            )
        elif state == 5:  # 撤回
            _id = text_data_json.get('id', None)
            EventComment_queryset = EventComment.objects.get(pk=_id)
            EventComment_queryset.state = 0
            EventComment_queryset.save()
            send_data = {
                'id': _id,
                'state': state
            }
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'event_comment_message',
                    **send_data
                }
            )

    def event_comment_message(self, data):
        self.send(text_data=json.dumps({
            **data
        }))
