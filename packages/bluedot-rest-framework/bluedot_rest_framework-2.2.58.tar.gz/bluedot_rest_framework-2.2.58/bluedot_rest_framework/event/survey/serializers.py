from datetime import datetime
from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework import import_string
from rest_framework.serializers import SerializerMethodField, CharField, IntegerField
from bluedot_rest_framework.event.survey.models import SurveyUser


class SurveyUserSerializer(CustomSerializer):

    class Meta:
        model = SurveyUser
        fields = '__all__'
