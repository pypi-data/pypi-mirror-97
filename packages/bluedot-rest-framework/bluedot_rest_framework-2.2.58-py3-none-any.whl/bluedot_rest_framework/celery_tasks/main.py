# celery入口
import os
from celery import Celery
from django.conf import settings

# 为celery使用django配置文件进行设置


celery_app = Celery('bluedot')
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
# 加载配置
celery_app.config_from_object('bluedot_rest_framework.celery_tasks.config')
# 注册任务
celery_app.autodiscover_tasks(["bluedot_rest_framework.celery_tasks.email"])
return celery_app

