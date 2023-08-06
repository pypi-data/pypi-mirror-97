from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class AbstractConfig(AbstractRelationTime):

    config_type = models.IntegerField(verbose_name='配置类型')
    title = models.CharField(max_length=255, verbose_name='配置标题')
    value = models.JSONField(verbose_name='内容')

    class Meta:
        abstract = True


class Config(AbstractConfig):

    class Meta:
        db_table = 'config'
