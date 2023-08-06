from rest_framework.serializers import SerializerMethodField, CharField, IntegerField
from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.serializers import CustomSerializer


Config = import_string('config.models')


class ConfigSerializer(CustomSerializer):

    class Meta:
        model = Config
        fields = '__all__'
