from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework import import_string
from .models import EventLivePPTCurrent


class EventLivePPTCurrentSerializer(CustomSerializer):

    class Meta:
        model = EventLivePPTCurrent
        fields = '__all__'
