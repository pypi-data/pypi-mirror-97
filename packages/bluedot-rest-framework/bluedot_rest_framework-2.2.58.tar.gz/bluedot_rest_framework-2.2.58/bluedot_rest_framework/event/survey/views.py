import xlwt
from io import BytesIO
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from bluedot_rest_framework import import_string
from django.db.models import Q
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bluedot_rest_framework.event.survey.models import SurveyUser
from bluedot_rest_framework.event.survey.serializers import SurveyUserSerializer
from bluedot_rest_framework.utils.crypto import AESEncrypt
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, user_perform_create
from bluedot_rest_framework.utils.jwt_token import jwt_get_wechatid_handler, jwt_get_userid_handler


class EventSurveyUserView(CustomModelViewSet):
    model_class = SurveyUser
    serializer_class = SurveyUserSerializer
    filterset_fields = {
        'event_id': {
            'field_type': 'int',
            'lookup_expr': ''
        }
    }

    @action(detail=False, methods=['get'], url_path='data_down', url_name='data_down')
    def data_down(self, request, *args, **kwargs):
        ws = xlwt.Workbook(encoding="UTF-8")
        w = ws.add_sheet(u'Sheet1')
        # 表头
        colums_indexs = ['姓名', '公司名称', '职位描述', '联系电话', '电子邮箱', '国家',
                         '填写问卷时间', '问题']
        num = 0
        for index_name in colums_indexs:
            w.write(0, num, index_name)
            num += 1
        excel_row = 1
        queryset = self.model_class.objects.all()
        for item in queryset:
            username = AESEncrypt.decrypt(
                item.first_name) + AESEncrypt.decrypt(item.last_name)
            qa = item.qa
            w.write(excel_row, 0, username)
            w.write(excel_row, 1, AESEncrypt.decrypt(item.company))
            w.write(excel_row, 2, AESEncrypt.decrypt(item.job))
            w.write(excel_row, 3, AESEncrypt.decrypt(item.tel))
            w.write(excel_row, 4, AESEncrypt.decrypt(item.email))
            w.write(excel_row, 5, item.country)
            w.write(excel_row, 6, str(item.created)[0:19])
            for index, val in enumerate(qa):
                for option in val['option']:
                    if option['checked'] == 1:
                        qa_value = option['value']
                        w.write(excel_row, 7, str(index+1)+'、'+qa_value)
                        excel_row += 1
            excel_row += 1
        sio = BytesIO()
        ws.save(sio)
        sio.seek(0)
        response = HttpResponse(
            sio.getvalue(), content_type='application/octet-stream')
        return response
