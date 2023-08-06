from bluedot_rest_framework.utils.models import models, AbstractRelationUser, AbstractRelationTime


class AbstractEventChat(AbstractRelationUser, AbstractRelationTime):
    event_id = models.IntegerField(verbose_name='活动id')

    nick_name = models.CharField(max_length=100, verbose_name='昵称')
    avatar_url = models.CharField(max_length=255, verbose_name='头像')

    state = models.IntegerField(default=0, verbose_name='状态')
    data = models.TextField(verbose_name='内容')
    like_count=models.IntegerField(default=0, verbose_name='点赞数')

    class Meta:
        abstract = True


class EventChat(AbstractEventChat):
    class Meta:
        db_table = 'event_chat'


class EventChatLike(AbstractRelationUser, AbstractRelationTime):
    event_chat_id = models.IntegerField(verbose_name='评论id')
    
    class Meta:
        db_table = 'event_chat_like'