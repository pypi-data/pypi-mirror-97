from datetime import datetime
from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework import import_string
from rest_framework.serializers import SerializerMethodField, CharField, IntegerField

EventQuestion = import_string('event.question.models')
EventQuestionUser = import_string('event.question.user_models')


class EventQuestionSerializer(CustomSerializer):
    time_state = SerializerMethodField()

    class Meta:
        model = EventQuestion
        fields = '__all__'

    def get_time_state(self, queryset):
        date_now = datetime.now()
        time_state = 1
        if queryset.start_time > date_now:
            time_state = 1
        elif queryset.start_time < date_now and queryset.end_time > date_now:
            time_state = 2
        elif queryset.end_time < date_now:
            time_state = 3
        return time_state


class EventQuestionUserSerializer(CustomSerializer):
    user_id = IntegerField(required=False)
    unionid = CharField(required=False)
    openid = CharField(required=False)
    wechat_id = IntegerField(required=False)

    class Meta:
        model = EventQuestionUser
        fields = '__all__'
