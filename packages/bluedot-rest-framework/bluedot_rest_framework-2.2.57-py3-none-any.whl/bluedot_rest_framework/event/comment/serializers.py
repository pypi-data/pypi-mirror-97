from bluedot_rest_framework.utils.serializers import CustomSerializer
from rest_framework.serializers import CharField, IntegerField
from bluedot_rest_framework import import_string

EventComment = import_string('event.comment.models')
EventCommentLike = import_string('event.comment.like_models')


class EventCommentSerializer(CustomSerializer):
    openid = CharField(required=False)
    unionid = CharField(required=False)
    wechat_id = CharField(required=False)

    class Meta:
        model = EventComment
        fields = '__all__'


class EventCommentLikeSerializer(CustomSerializer):
    class Meta:
        model = EventCommentLike
        fields = '__all__'
