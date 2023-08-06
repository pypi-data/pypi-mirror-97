from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class AbstractUser(AbstractRelationTime):
    wechat_id = models.IntegerField(null=True)
    unionid = models.CharField(max_length=100, null=True)
    tel_region = models.CharField(max_length=32, null=True, verbose_name='+86')
    industry = models.CharField(max_length=100, null=True, verbose_name='行业')

    user_name = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True, verbose_name='邮箱')
    tel = models.CharField(max_length=100, null=True, verbose_name='电话')
    company = models.CharField(max_length=100, null=True, verbose_name='公司')
    job = models.CharField(max_length=100, null=True, verbose_name='职位')

    country = models.CharField(max_length=100, null=True, verbose_name='国家')
    source_type = models.CharField(
        max_length=100, null=True, verbose_name='来源')

    class Meta:
        abstract = True
