from bluedot_rest_framework.utils.models import models, AbstractRelationUser, AbstractRelationTime


class AbstractQuestion(AbstractRelationTime):
    title = models.CharField(max_length=100, null=True, verbose_name='标题')
    qa = models.JSONField(verbose_name='问题内容')

    class Meta:
        abstract = True


class AbstractQuestionUser(AbstractRelationUser, AbstractRelationTime):
    qa_id = models.IntegerField(null=True, verbose_name='问题id')
    title = models.CharField(max_length=100, null=True, verbose_name='标题')
    integral = models.IntegerField(default=0, verbose_name='积分')
    qa = models.JSONField(null=True, verbose_name='问题内容')

    class Meta:
        abstract = True
