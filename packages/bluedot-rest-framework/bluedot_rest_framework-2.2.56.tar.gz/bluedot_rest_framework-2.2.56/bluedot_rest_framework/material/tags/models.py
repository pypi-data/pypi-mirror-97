from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class Tags(AbstractRelationTime):
    title = models.CharField(max_length=255, verbose_name='标题')

    class Meta:
        db_table = 'tags'
