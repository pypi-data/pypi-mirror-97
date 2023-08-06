from rest_framework import serializers


class CustomSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(CustomSerializer, self).__init__(*args, **kwargs)

        exclude_fields = kwargs.pop('exclude_fields', None)

        # include_fields = kwargs.pop('include_fields', None)
        if exclude_fields is None:
            if 'request' in self.context:
                exclude_fields = self.context['request'].query_params.get(
                    'exclude_fields', None)

        if exclude_fields:

            exclude_fields = exclude_fields.split(',')
            # Drop fields specified in the `fields` argument.
            banished = set(exclude_fields)
            for field_name in banished:

                self.fields.pop(field_name)
