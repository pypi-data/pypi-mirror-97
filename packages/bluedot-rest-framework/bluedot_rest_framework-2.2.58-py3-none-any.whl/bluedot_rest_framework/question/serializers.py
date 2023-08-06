from bluedot_rest_framework.utils.serializers import CustomSerializer
from rest_framework.serializers import CharField, JSONField, IntegerField
from .models import Question, QuestionUser
from bluedot_rest_framework import import_string
from rest_framework.serializers import SerializerMethodField

Material = import_string('material.models')
Event = import_string('event.models')


class QuestionSerializer(CustomSerializer):
    recommend_relation_read = SerializerMethodField()
    recommend = JSONField(required=False)
    description = CharField(required=False)
    qa_id = IntegerField(required=False)
    qa = JSONField(required=False)

    class Meta:
        model = Question
        fields = '__all__'

    def get_recommend_relation_read(self, queryset):
        data = []
        try:
            relation_read = queryset.recommend['relation_read']
            for item in relation_read:
                if item['_type'] == 5:
                    instance = Event.objects.get(pk=item['material_id'])
                    data.append({'id': str(instance.id), '_type': 5,
                                 'title': instance.title, 'created': instance.created})
                else:
                    instance = Material.objects.get(
                        pk=item['material_id'])
                    data.append({'id': str(instance.id), '_type': instance.material_type,
                                 'title': instance.title, 'created': instance.created})
        except:
            pass
        return data


class QuestionUserSerializer(CustomSerializer):
    relation = SerializerMethodField()

    class Meta:
        model = QuestionUser
        fields = '__all__'

    def get_relation(self, queryset):
        question_queryset = Question.objects.filter(
            recommend__has_key='relation_read')
        if question_queryset:
            return QuestionSerializer(question_queryset, many=True).data[0]
        else:
            return []
