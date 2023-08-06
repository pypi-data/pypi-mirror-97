from datetime import datetime
from rest_framework.serializers import SerializerMethodField, CharField, IntegerField, DateTimeField, JSONField
from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework import import_string

Event = import_string('event.models')


class EventSerializer(CustomSerializer):
    time_state = SerializerMethodField()
    banner = CharField(required=False)
    description = CharField(required=False)
    end_time = DateTimeField(required=False)
    start_time = DateTimeField(required=False)
    title = CharField(required=False)
    module_list = JSONField(required=False)
    live_inav = JSONField(required=False)

    class Meta:
        model = Event
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
