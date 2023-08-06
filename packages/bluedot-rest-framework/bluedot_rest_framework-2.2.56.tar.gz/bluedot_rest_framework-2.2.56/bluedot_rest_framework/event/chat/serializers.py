from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework import import_string

EventChat = import_string('event.chat.models')


class EventChatSerializer(CustomSerializer):

    class Meta:
        model = EventChat
        fields = '__all__'
