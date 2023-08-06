from bluedot_rest_framework.utils.models import models, AbstractRelationTime, AbstractRelationUser


class AbstractDataDownload(AbstractRelationTime):
    data_download_type = models.IntegerField(default=1, verbose_name='下载类型')
    category_id = models.IntegerField(verbose_name='分类id')
    title = models.CharField(max_length=255, default='', verbose_name='标题')
    data = models.JSONField(verbose_name='下载数据内容')
    view_count = models.IntegerField(null=True, verbose_name='数量')

    class Meta:
        abstract = True


class DataDownload(AbstractDataDownload):
    class Meta:
        db_table = 'data_download'


class AbstractDataDownloadUser(AbstractRelationUser, AbstractRelationTime):
    data_download_id = models.IntegerField(verbose_name='下载id')

    class Meta:
        abstract = True


class DataDownloadUser(AbstractDataDownloadUser):
    class Meta:
        db_table = 'data_download_user'
