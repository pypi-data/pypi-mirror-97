from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class WeChatUser(AbstractRelationTime):
    unionid = models.CharField(max_length=32,null=True)
    nick_name = models.CharField(max_length=100, verbose_name='昵称')
    gender = models.IntegerField(verbose_name='性别')
    language = models.CharField(max_length=32, verbose_name='语言')
    city = models.CharField(max_length=32, verbose_name='城市')
    province = models.CharField(max_length=32, verbose_name='省份')
    country = models.CharField(max_length=32, verbose_name='国家')
    avatar_url = models.TextField(verbose_name='头像')


    class Meta:
        db_table = 'wechat_user'


class WeChatUserOpenid(AbstractRelationTime):
    wechat = models.ForeignKey(
        WeChatUser, on_delete=models.CASCADE)
    appid = models.CharField(max_length=32)
    openid = models.CharField(max_length=32)
    subscribe = models.IntegerField(default=0, verbose_name='')

    class Meta:
        db_table = 'wechat_user_openid'
