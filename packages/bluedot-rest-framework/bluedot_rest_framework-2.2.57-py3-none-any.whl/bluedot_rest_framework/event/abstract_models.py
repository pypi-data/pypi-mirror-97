from django.db import models


class AbstractEventExtend(models.Model):
    extend_category_id = models.IntegerField(null=True, verbose_name='分类id')
    extend_video_url = models.TextField(null=True, verbose_name='视频地址')
    extend_is_banner = models.BooleanField(default=False, verbose_name='是否显示banner')
    extend_is_index = models.BooleanField(default=False, verbose_name='是否显示首页')

    class Meta:
        abstract = True


class AbstractEventLive(models.Model):
    """
    0:直播
    1:拟直播
    2:多人直播
    """
    live_type = models.IntegerField(default=1)
    live_room_id = models.CharField(
        max_length=16, verbose_name='直播房间id', null=True)
    live_create_room_time = models.DateTimeField(
        verbose_name='创建房间时间', null=True)
    live_stream_number = models.CharField(
        max_length=16, verbose_name='串流码', null=True)
    live_push_address = models.CharField(
        max_length=128, verbose_name='推流地址', null=True)
    live_vod_id = models.CharField(
        max_length=256, verbose_name='回放id', null=True)
    live_task_id = models.CharField(
        max_length=256, verbose_name='任务id', null=True)
    live_playback = models.IntegerField(default=0, verbose_name='直播回放')

    """
    id:互动房间ID
    layout: CANVAS_LAYOUT_PATTERN_TILED_5_1L4R(主次平铺，一列4个位于右边)
    
    """
    live_inav = models.JSONField(verbose_name='互动房间配置',null=True)

    class Meta:
        abstract = True


class AbstractEventAddress(models.Model):
    address_country = models.CharField(max_length=32, null=True, verbose_name='国家')
    address_province = models.CharField(max_length=32, null=True, verbose_name='省份')
    address_city = models.CharField(max_length=32, null=True, verbose_name='城市')
    address_info = models.CharField(max_length=255, null=True, verbose_name='详细信息')
    address_detail_info = models.CharField(max_length=255, null=True, verbose_name='缩略信息')

    class Meta:
        abstract = True
