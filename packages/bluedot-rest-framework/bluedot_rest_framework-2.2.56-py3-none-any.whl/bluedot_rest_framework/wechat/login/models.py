from django.db import models


class WeChatLogin(models.Model):
    openid = models.CharField(max_length=32)
    scene_str = models.CharField(max_length=32)
    ticket = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wechat_login'
