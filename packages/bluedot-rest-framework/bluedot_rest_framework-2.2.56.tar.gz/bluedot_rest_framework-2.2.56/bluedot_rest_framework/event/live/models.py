from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class AbstractEventLivePPT(AbstractRelationTime):
    event_id = models.IntegerField(verbose_name='活动id')

    class Meta:
        abstract = True


class EventLivePPT(AbstractEventLivePPT):
    image_list = models.JSONField(null=True, verbose_name='PPT图片列表')

    class Meta:
        db_table = 'event_live_ppt'

class EventLivePPTCurrent(AbstractRelationTime):
    event_id = models.IntegerField(verbose_name='活动id')
    activeIndex = models.IntegerField(verbose_name='ppt页码')

    class Meta:
        db_table = 'event_live_ppt_current'