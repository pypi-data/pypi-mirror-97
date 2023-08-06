from rest_framework.serializers import SerializerMethodField
from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.serializers import CustomSerializer


EventSpeaker = import_string('event.speaker.models')
EventSpeakerSerializer = import_string('event.speaker.serializers')
EventSchedule = import_string('event.schedule.models')


class EventScheduleSerializer(CustomSerializer):

    speaker_user = SerializerMethodField()

    class Meta:
        model = EventSchedule
        fields = '__all__'

    def get_speaker_user(self, queryset):
        if queryset.speaker_ids:
            speaker_user_queryset = EventSpeaker.objects.filter(
                pk__in=queryset.speaker_ids)
            return EventSpeakerSerializer(speaker_user_queryset, many=True).data
        return []
