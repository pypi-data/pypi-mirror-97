from django.db import models
from bluedot_rest_framework.question.abstract_models import AbstractQuestion, AbstractQuestionUser


class SurveyUser(AbstractQuestionUser):
    event_id = models.CharField(max_length=32, default='', verbose_name='活动id')
    first_name = models.CharField(max_length=100, verbose_name='名字')
    last_name = models.CharField(max_length=100, verbose_name='姓氏')
    email = models.CharField(max_length=100, verbose_name='邮箱')
    tel = models.CharField(max_length=100, verbose_name='电话')
    company = models.CharField(max_length=100, verbose_name='公司')
    job = models.CharField(max_length=100, verbose_name='职位')
    country = models.CharField(max_length=100, verbose_name='国家')

    class Meta:
        db_table = 'event_survey_user'
