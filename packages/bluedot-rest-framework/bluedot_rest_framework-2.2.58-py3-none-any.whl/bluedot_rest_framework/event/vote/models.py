from bluedot_rest_framework.question.abstract_models import AbstractQuestionUser
from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class EventVote(models.Model):
    event_id = models.IntegerField(verbose_name='活动id')
    schedule_id = models.IntegerField(verbose_name='日程id')
    state = models.IntegerField(default=0, verbose_name='状态')
    qa = models.JSONField(verbose_name='问题内容')

    class Meta:
        db_table = 'event_vote'


class EventVoteUser(AbstractQuestionUser):
    schedule_id = models.IntegerField(default=0, verbose_name='日程id')

    class Meta:
        db_table = 'event_vote_user'
