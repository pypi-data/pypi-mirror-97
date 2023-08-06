from bluedot_rest_framework.utils.models import models, AbstractRelationUser, AbstractRelationTime


class AbstractEventRegister(AbstractRelationUser, AbstractRelationTime):

    event_id = models.CharField(max_length=32, verbose_name='活动id')
    event_type = models.IntegerField(default=1, verbose_name='活动类型')
    source = models.IntegerField(default=0, verbose_name='来源')
    state = models.IntegerField(default=0, verbose_name='活动状态')

    tel_region = models.CharField(
        max_length=32, null=True, default='', verbose_name='+86')
    industry = models.CharField(
        max_length=100, null=True, default='', verbose_name='行业')
    first_name = models.CharField(max_length=100, verbose_name='名字')
    last_name = models.CharField(max_length=100, verbose_name='姓氏')
    email = models.CharField(max_length=100, verbose_name='邮箱')
    tel = models.CharField(max_length=100, verbose_name='电话')
    company = models.CharField(max_length=100, verbose_name='公司')
    job = models.CharField(max_length=100, verbose_name='职位')
    country = models.CharField(max_length=100, verbose_name='国家')


    class Meta:
        abstract = True


class EventRegister(AbstractEventRegister):
    class Meta:
        db_table = 'event_register'


class EventRegisterConfig(AbstractRelationTime):
    event_id = models.CharField(max_length=32, verbose_name='活动id')
    over_time = models.DateTimeField(verbose_name='')

    field_list = models.JSONField(verbose_name='')

    class Meta:
        db_table = 'event_register_config'
