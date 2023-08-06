from django.db import models
from bluedot_rest_framework.question.abstract_models import AbstractQuestion, AbstractQuestionUser


class EventQuestion(AbstractQuestion):
    event_id = models.CharField(max_length=32, verbose_name='活动id')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')

    class Meta:
        db_table = 'event_question'


class EventQuestionUser(AbstractQuestionUser):
    event_id = models.CharField(max_length=32, verbose_name='活动id')

    class Meta:
        db_table = 'event_question_user'
