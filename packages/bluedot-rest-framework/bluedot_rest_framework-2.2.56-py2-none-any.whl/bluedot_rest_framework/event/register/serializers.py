from bluedot_rest_framework.utils.serializers import CustomSerializer
from rest_framework.serializers import SerializerMethodField, CharField, IntegerField
from bluedot_rest_framework import import_string


Event = import_string('event.models')
EventRegisterConfig = import_string('event.register.config_models')
EventRegister = import_string('event.register.models')


class EventRegisterSerializer(CustomSerializer):
    event_data = SerializerMethodField()
    unionid = CharField(required=False)
    wechat_id = IntegerField(required=False)
    country = CharField(required=False)
    class Meta:
        model = EventRegister
        fields = '__all__'

    def get_event_data(self, queryset):

        event_id = queryset.event_id
        event_queryset = Event.objects.filter(pk=event_id).first()
        return {
            "title": event_queryset.title,
            "start_time": event_queryset.start_time,
            "end_time": event_queryset.end_time,
            "banner": event_queryset.banner
        }


class EventRegisterConfigSerializer(CustomSerializer):

    class Meta:
        model = EventRegisterConfig
        fields = '__all__'
