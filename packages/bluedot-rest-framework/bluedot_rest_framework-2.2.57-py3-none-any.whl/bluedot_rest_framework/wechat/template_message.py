import json
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from bluedot_rest_framework import import_string
from bluedot_rest_framework.wechat import OfficialAccount
from bluedot_rest_framework.wechat.models import WeChatUserOpenid
from bluedot_rest_framework.utils.json_date import DateEncoder
User = import_string('user.models')
UserSerializer = import_string('user.serializers')


@permission_classes([])
def event_register_template(wechat_id=None, event_id=None, keyword1=None, keyword3=None, keyword4=None,  remark=None):
    wechat_data = WeChatUserOpenid.objects.filter(wechat_id=wechat_id).first()
    if wechat_data:
        template_data = {
            'user_id': wechat_data.openid,
            'template_id': 'Ql-bSXKlgl-6bhPJz4ejF-G9EtELQWggHysa1r_jZlY',
            'data': {
                "first": {
                    "value": '您提交的报名申请已经通过。',
                    "color": "#173177"
                },
                "keyword1": {
                    "value": keyword1,
                    "color": "#173177"
                },
                "keyword2": {
                    "value": '审核通过',
                    "color": "#173177"
                },
                "keyword3": {
                    "value": keyword3,
                    "color": "#173177"
                },
                "keyword4": {
                    "value": keyword4,
                    "color": "#173177"
                },
                "remark": {
                    "value": remark,
                    "color": "#173177"
                }
            },
            'url': settings.BLUEDOT_REST_FRAMEWORK['wechat']['templates_url'],
            'mini_program': None
        }
        result = OfficialAccount.message.send_template(**template_data)
        return Response({'code': '1000', 'msg': 'success'})
    return Response({'code': '1001', 'msg': 'Server Error'})
