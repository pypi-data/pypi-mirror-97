from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework import import_string
from rest_framework.serializers import CharField, IntegerField
from rest_framework.serializers import SerializerMethodField

EventVote = import_string('event.vote.models')
EventVoteUser = import_string('event.vote.user_models')


class EventVoteSerializer(CustomSerializer):
    voting_count = SerializerMethodField()

    class Meta:
        model = EventVote
        fields = '__all__'

    def get_voting_count(self, queryset):
        count = 0
        user_queryset_count = EventVoteUser.objects.filter(
            schedule_id=queryset.schedule_id).count()
        count = user_queryset_count
        return count


class EventVoteUserSerializer(CustomSerializer):
    user_id = IntegerField(required=False)
    unionid = CharField(required=False)
    openid = CharField(required=False)
    wechat_id = IntegerField(required=False)

    class Meta:
        model = EventVoteUser
        fields = '__all__'
