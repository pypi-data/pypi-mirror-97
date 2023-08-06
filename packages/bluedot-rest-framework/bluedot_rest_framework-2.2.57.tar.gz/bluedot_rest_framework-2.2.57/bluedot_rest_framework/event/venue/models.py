from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class EventVenue(AbstractRelationTime):
    event_id = models.IntegerField(verbose_name='活动id')
    image_list = models.JSONField(verbose_name='会场图片')

    class Meta:
        db_table = 'event_venue'
