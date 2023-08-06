from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework import import_string
from rest_framework.serializers import SerializerMethodField, CharField, JSONField, IntegerField, ReadOnlyField
Material = import_string('material.models')
Event = import_string('event.models')


class MaterialSerializer(CustomSerializer):
    recommend_relation_read = SerializerMethodField()
    category_id = JSONField(required=False)
    tags_id = JSONField(required=False)
    article = JSONField(required=False)

    class Meta:
        model = Material
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
                    instance = self.Meta.model.objects.get(
                        pk=item['material_id'])
                    data.append({'id': str(instance.id), '_type': instance.material_type,
                                 'title': instance.title, 'created': instance.created})

        except:
            pass
        return data
