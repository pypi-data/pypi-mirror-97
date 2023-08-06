from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework import import_string

Tags = import_string('material.tags.models')


class TagsSerializer(CustomSerializer):

    class Meta:
        model = Tags
        fields = '__all__'
