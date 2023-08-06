from django.db import models

models = models


class AbstractRelationTime(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractRelationUser(models.Model):
    userid = models.IntegerField(null=True)
    wechat_id = models.IntegerField(null=True)
    unionid = models.CharField(max_length=100, null=True)

    class Meta:
        abstract = True
