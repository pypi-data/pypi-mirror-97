from bluedot_rest_framework.utils.serializers import CustomSerializer
from rest_framework.serializers import SerializerMethodField, CharField
from bluedot_rest_framework import import_string

User = import_string('user.models')
WechatUser = import_string('wechat.models')


class UserSerializer(CustomSerializer):
    country = CharField(required=False, read_only=True)
    wechat_profile = SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_wechat_profile(self, queryset):
        unionid = queryset.unionid
        wechat_queryset = WechatUser.objects.filter(unionid=unionid).first()
        return {
            'avatar_url': wechat_queryset.avatar_url,
            'nick_name': wechat_queryset.nick_name
        }
