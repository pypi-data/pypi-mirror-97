# 定义任务
from . import constants
from . import SMS
from bluedot_rest_framework.celery_tasks.main import celery_app


# 使用装饰器装饰异步任务，保证celery识别任务
@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    text = f'您的验证码是{sms_code}。如非本人操作，请忽略本短信'
    result = SMS(tel=mobile, text=text).send()
    return result
