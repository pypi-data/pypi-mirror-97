from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework import import_string


EventSpeaker = import_string('event.speaker.models')


class EventSpeakerSerializer(CustomSerializer):

    class Meta:
        model = EventSpeaker
        fields = '__all__'
