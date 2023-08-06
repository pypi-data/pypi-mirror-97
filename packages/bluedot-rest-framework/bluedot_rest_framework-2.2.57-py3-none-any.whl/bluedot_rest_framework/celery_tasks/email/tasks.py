from bluedot_rest_framework.celery_tasks.main import start
from django.core.mail import send_mail
from django.conf import settings
from email.utils import formataddr

celery_app=start()

@celery_app.task(name='send_verify_email', retry_backoff=3)
def send_verify_email(email, html_content):
    """
    发送验证邮箱邮件
    :param to_email: 收件人邮箱
    :param verify_url: 验证链接
    :return: None
    """

    from_email = formataddr(
        pair=(settings.EMAIL_FROM_NAME, settings.EMAIL_HOST_USER))
    send_mail(subject='【下载资料】',
              message='',
              html_message=html_content,
              from_email=from_email,
              recipient_list=[email])


@celery_app.task(name='send_verify_code', retry_backoff=3)
def send_verify_code(email, html_content):
    send_mail(subject, html_message,
              settings.EMAIL_HOST_USER, [to_email])