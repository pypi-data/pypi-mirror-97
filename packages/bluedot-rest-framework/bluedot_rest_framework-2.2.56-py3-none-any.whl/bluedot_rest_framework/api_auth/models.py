from django.db import models
from django.contrib.auth.models import AbstractUser


class AuthUser(AbstractUser):
    _type = models.IntegerField(default=0, verbose_name='类型')
    avatar_url = models.TextField(null=True, verbose_name='头像')
    group_ids = models.JSONField(null=True, verbose_name='分组id')

    class Meta:
        db_table = 'auth_user'
        swappable = 'AUTH_USER_MODEL'


class AuthMenu(models.Model):
    path = models.CharField(max_length=150, verbose_name='路径')
    name = models.CharField(max_length=150, verbose_name='名称')
    icon = models.CharField(max_length=150, verbose_name='图标')
    parent = models.IntegerField(default=0, verbose_name='父级路径')
    is_menu = models.IntegerField(default=0, verbose_name='')
    sort = models.IntegerField(default=0, verbose_name='排序')

    class Meta:
        db_table = 'auth_menu'


class AuthGroupMenu(models.Model):
    name = models.CharField(max_length=150, verbose_name='名称')
    menu_ids = models.JSONField(verbose_name='菜单id')

    class Meta:
        db_table = 'auth_group_menu'
