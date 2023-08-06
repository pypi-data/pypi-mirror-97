from django.db import models
from .abstract_models import AbstractQuestion, AbstractQuestionUser
from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class Question(AbstractQuestion):
    recommend = models.JSONField(null=True,  verbose_name='关联内容')
    relation = models.JSONField(null=True, verbose_name='推荐位')

    integral = models.IntegerField(default=0, verbose_name='积分')

    class Meta:
        db_table = 'question'


class QuestionUser(AbstractQuestionUser):

    class Meta:
        db_table = 'question_user'
