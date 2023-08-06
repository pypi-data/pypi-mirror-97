from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class AbstractEventDataDownload(AbstractRelationTime):
    event_id = models.IntegerField(verbose_name='活动id')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')

    data = models.JSONField()

    class Meta:
        abstract = True


class EventDataDownload(AbstractEventDataDownload):

    class Meta:
        db_table = 'event_data_download'
