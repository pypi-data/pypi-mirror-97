from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class AbstractCategory(AbstractRelationTime):
    category_type = models.IntegerField(default=1, verbose_name='类型')
    title = models.CharField(max_length=100, null=True, verbose_name='标题')
    parent = models.IntegerField(default=0, verbose_name='父级ID')
    sort = models.IntegerField(default=1, verbose_name='排序')

    class Meta:
        abstract = True


class Category(AbstractCategory):
    class Meta:
        db_table = 'category'
