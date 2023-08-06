from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class AbstractEventSpeaker(AbstractRelationTime):
    event_id = models.IntegerField(verbose_name='活动id')
    name = models.CharField(max_length=255, verbose_name='嘉宾名称')
    job = models.CharField(max_length=255, verbose_name='职位')
    description = models.TextField(verbose_name='描述')
    img = models.CharField(max_length=255, verbose_name='图片')
    is_sign_page = models.BooleanField(default=False, verbose_name='')
    sort = models.IntegerField(default=1, verbose_name='排序')

    class Meta:
        abstract = True


class EventSpeaker(AbstractEventSpeaker):

    class Meta:
        db_table = 'event_speaker'
