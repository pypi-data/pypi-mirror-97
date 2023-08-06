from bluedot_rest_framework.utils.models import models
from bluedot_rest_framework.question.abstract_models import AbstractQuestion


class AbstractMaterial(AbstractQuestion):
    material_type = models.IntegerField(verbose_name='文章类型')
    category_id = models.JSONField(null=True,default=list,verbose_name='分类id')
    title = models.CharField(max_length=100, verbose_name='标题')
    banner = models.CharField(max_length=255, verbose_name='banner图片')
    state = models.IntegerField(default=1, verbose_name='状态')
    is_new = models.IntegerField(default=0, verbose_name='是否展示首页')
    average_grade = models.FloatField(default=0, verbose_name='平均分')
    data = models.TextField(null=True, verbose_name='富文本数据')
    tags_id = models.JSONField(null=True, default=list,verbose_name='标签id')
    extend = models.JSONField(null=True, verbose_name='行业作者内容')
    article = models.JSONField(null=True, verbose_name='')
    recommend = models.JSONField(null=True, verbose_name='关联数据')

    class Meta:
        abstract = True
